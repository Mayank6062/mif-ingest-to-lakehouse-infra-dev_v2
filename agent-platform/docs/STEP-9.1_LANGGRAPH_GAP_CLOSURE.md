STEP-9.1 — LANGGRAPH GAP CLOSURE & DTO / REGISTRY FREEZE

Authority: architecture-only verification and freeze. No code, no implementation, no redesign.

Decision: Complete closure of LangGraph state gaps — DTOs, registries, provenance, versioning, and production-scale state ownership.

Final outcome: PASS — All gaps closed by freezing DTO schemas, registry schemas, ownership, and provenance model. The artifacts below are architecture-only freeze specifications. Implementation must follow exactly.

---

SECTION 1 — KNOWLEDGESTATE FINAL DECISION

Decision summary: KnowledgeState SHALL NOT contain the full registries or repository facts. LangGraph may store only lightweight references (ids, version tags, minimal descriptors). Full registry and fact storage belongs to KBS / repository.

For each candidate item:

- repository_facts
  - Store In LangGraph State? NO
  - Reason: repository facts are large, authoritative in RKP/KBS, and frequently updated — duplication causes drift and bloat.
  - Risk: duplication leads to stale decisions and memory explosion.
  - Correct Owner: Repository Knowledge Provider (RKP) → KBS normalizer.
  - Correct Storage Location: Source Git repository (for raw files) and KBS normalized store / cache (Postgres or object store) with KBS version id.
  - Required For Production? NO

- validation_rules
  - Store In LangGraph State? NO (only reference)
  - Reason: validation rules evolve and are authoritative in KBS registries; LangGraph must reference rule_set_version and rule ids.
  - Risk: inconsistent rule execution if duplicated.
  - Correct Owner: Knowledge Team / KBS Validation Service.
  - Correct Storage Location: `knowledge/validation_rules.json` in repo and KBS-backed registry table (Postgres) with `registry_version` metadata.
  - Required For Production? NO (references required)

- templates
  - Store In LangGraph State? NO (only reference to template_id + template_version)
  - Reason: templates include structural artifacts and may be used across pipelines — KBS or repo is source-of-truth.
  - Risk: template drift and compatibility issues.
  - Correct Owner: Template Team / KBS Template Registry.
  - Correct Storage Location: `knowledge/terraform_templates.json` (repo) + artifact source (git submodule or ACR/Git URL) with version metadata.
  - Required For Production? NO (references required)

- source_system_registry
  - Store In LangGraph State? NO (only store `source_system_id` and `source_registry_version`)
  - Reason: registry contains canonical metadata about external systems; LangGraph only needs identity and version.
  - Risk: stale metadata in LangGraph causes incorrect derivations.
  - Correct Owner: Integration/Onboarding team (KBS owner)
  - Correct Storage Location: `knowledge/source_systems.json` in repo + KBS table.
  - Required For Production? NO (references required)

- repo_patterns
  - Store In LangGraph State? NO
  - Reason: repository pattern data drives normalization and derivation; KBS must own patterns.
  - Risk: duplication/staleness.
  - Correct Owner: Knowledge Team (KBS)
  - Correct Storage Location: `knowledge/repo_patterns.json` + KBS table.
  - Required For Production? NO

Final frozen KnowledgeState model (concise):
- Fields LangGraph MAY store (all small, id/enum/string only):
  - `kb_version` (string) — authoritative KBS registry version id
  - `rule_set_version` (string)
  - `template_registry_version` (string)
  - `source_registry_version` (string)
  - `source_system_id` (string)
  - `repository_id` (string)
  - `small_hints` (optional short strings, <= 256 chars) — e.g., `preferred_template_id`
- LangGraph MUST NOT store: full `repository_facts`, `validation_rules`, `terraform_templates`, `repo_patterns`, or template/content payloads.

PASS: KnowledgeState frozen (reference-only model).

---

SECTION 2 — REPOSITORYTREETDTO FREEZE

Purpose: lightweight, navigable representation of repository tree for navigator, recovery, diff preview, and minimal UI rendering.

Owner: Repository Knowledge Provider (RKP) for production data; DTO owner: API/schema team (backend). LangGraph and UI consume.

Producer: RKP (normalized), or DraftSnapshot service for draft-specific trees.

Consumers: UI Navigator, Recovery flows, LangGraph nodes (as transient input), Review UI, Diff engine (shallow).

Recovery usage: Used by NavigatorRecovery flows to reconstruct cursor and limited tree context. Must not be used for full repo indexing.

Field definitions (exact frozen schema):
- `version` (string) — DTO schema version (e.g., "1.0.0"); REQUIRED
- `repository_id` (string); REQUIRED
- `root` (string) — repository root path; REQUIRED
- `cursor` (object|null) — optional navigation cursor:
  - `path` (string)
  - `offset` (integer)
  - `timestamp` (ISO8601 string)
- `nodes` (array of Node objects) — REQUIRED (may be paged)
  - Node object:
    - `path` (string) — REQUIRED
    - `name` (string) — REQUIRED
    - `type` ("file" | "dir") — REQUIRED
    - `has_children` (boolean) — REQUIRED for dirs
    - `size_bytes` (integer|null) — OPTIONAL
    - `last_modified` (ISO8601|null) — OPTIONAL
    - `sha256` (string|null) — OPTIONAL — short file fingerprint if small
    - `metadata` (object|null) — OPTIONAL small key-values (max 5 entries)

Required fields: `version`, `repository_id`, `root`, `nodes[].path`, `nodes[].type`, `nodes[].name`.
Optional fields: `nodes[].size_bytes`, `nodes[].last_modified`, `nodes[].sha256`, `cursor`.

Pagination: `nodes` MUST be pageable; DTO may contain `next_cursor` (string|null) if more nodes available.

Versioning strategy: Use `version` string and semantic versioning for schema changes. DTO schema v1.0.0 frozen.

PASS: RepositoryTreeDTO frozen (v1.0.0).

---

SECTION 3 — FILEIMPACTDTO FREEZE

Purpose: represent the impact of a change on a file for review, auditing, and downstream diff/merge flows.

Owner: DraftWorkspaceService (authoritative for change ownership). DTO owner: API/schema team.

Producers: Draft change generator, DerivedValue application, Diff engine.

Consumers: Review UI, Audit, Diff engine, Validation service.

Lifecycle: Created at change generation, persisted in `draft_files` or `draft_changes` table as metadata; LangGraph may carry references (file_impact_id).

Exact frozen schema:
- `version` (string) — DTO schema version; REQUIRED
- `file_impact_id` (string, uuid) — REQUIRED
- `draft_id` (string, uuid) — REQUIRED
- `file_path` (string) — REQUIRED
- `impact_type` ("ADDED" | "MODIFIED" | "DELETED" | "RENAMED") — REQUIRED
- `lines_added` (integer|null) — OPTIONAL (for text files)
- `lines_removed` (integer|null) — OPTIONAL
- `hunks` (array|null) — OPTIONAL — shallow hunks with start/end lines (max 10 entries)
  - hunk: { `start_line`: integer, `end_line`: integer }
- `provenance_refs` (array of provenance_id strings) — REQUIRED (may be empty array)
- `affected_rules` (array of { `rule_id`: string, `severity`: "CRITICAL"|"HIGH"|"MEDIUM"|"LOW" }) — OPTIONAL
- `estimated_risk` ("LOW"|"MEDIUM"|"HIGH") — OPTIONAL
- `size_bytes` (integer|null) — OPTIONAL
- `sha256` (string|null) — OPTIONAL
- `created_at` (ISO8601) — REQUIRED
- `created_by` (string user_id) — REQUIRED

Ownership: authoritative metadata persisted by DraftWorkspaceService in `draft_files` table; provenance_refs link to provenance table entries created by KBS.

Support for Review Workspace: `FileImpactDTO` is queryable by `draft_id` and `file_path`.

PASS: FileImpactDTO frozen (v1.0.0).

---

SECTION 4 — REVIEWAPPROVALDTO FREEZE

Purpose: capture discrete approval actions within a review; used for audit and PR gating.

Owner: Review service (authoritative).

Producer: Review UI / Review API.

Consumers: PRCreationNode, Audit, UI.

Exact frozen schema:
- `version` (string) — DTO schema version; REQUIRED
- `approval_id` (string, uuid) — REQUIRED
- `review_id` (string, uuid) — REQUIRED
- `approver_id` (string user_id) — REQUIRED
- `decision` ("APPROVE" | "REQUEST_CHANGES" | "COMMENT") — REQUIRED
- `note` (string|null) — OPTIONAL (max 4096 chars)
- `created_at` (ISO8601) — REQUIRED
- `linked_pr_id` (string|null) — OPTIONAL
- `audit_reference` (string|null) — OPTIONAL — pointer to audit events table

Audit linkage: `approval_id` and `audit_reference` must be present in audit events with immutable timestamps.

PR approval linkage: PRCreationNode must consult `review_id` approvals; `linked_pr_id` is set when PR created.

PASS: ReviewApprovalDTO frozen (v1.0.0).

---

SECTION 5 — NAVIGATORRECOVERYDTO FREEZE

Purpose: enable browser/session navigator restoration and step recovery for user sessions.

Owner: Navigator service / Session service.

Producer: UI save points, LangGraph orchestrator during recovery.

Consumers: UI, Recovery flows.

Exact frozen schema:
- `version` (string) — DTO schema version; REQUIRED
- `navigator_id` (string, uuid) — REQUIRED
- `session_id` (string) — REQUIRED
- `repository_id` (string) — REQUIRED
- `last_cursor` (object) — REQUIRED
  - `path` (string)
  - `line` (integer|null)
  - `offset` (integer|null)
  - `timestamp` (ISO8601)
- `current_step` (string|null) — optional readable step id for LangGraph resume
- `restored_at` (ISO8601|null)
- `restored_by` (string|null)
- `ttl_seconds` (integer) — OPTIONAL — how long this recovery point valid for (default 30 days)

Browser refresh recovery: UI should call recovery endpoint returning NavigatorRecoveryDTO; LangGraph uses `current_step`, `session_id`, and `last_cursor` for resume orchestration.

PASS: NavigatorRecoveryDTO frozen (v1.0.0).

---

SECTION 6 — TEMPLATEREGISTRYDTO FREEZE

Purpose: describe templates used for generation (Terraform, jobs, scaffolds) and compatibility metadata.

Owner: KBS Template Registry (authoritative).

Producer: Template authors / Template registry upstream (git tags or artifact store).

Consumers: KBS, Draft suggestion engine, UI hints.

Exact frozen schema:
- `version` (string) — DTO schema version; REQUIRED
- `template_id` (string) — REQUIRED
- `name` (string) — REQUIRED
- `description` (string|null) — OPTIONAL
- `source` (object) — REQUIRED
  - `type` ("git" | "artifact" | "registry") — REQUIRED
  - `uri` (string) — REQUIRED (git URL or artifact identifier)
  - `ref` (string|null) — OPTIONAL — git ref, tag, or artifact version
- `template_version` (string) — REQUIRED (semver or integer)
- `compatibility` (object|null) — OPTIONAL
  - `required_tool_version` (string|null)
  - `incompatible_with` (array of strings)
- `fields_required` (array of { `name`: string, `type`: string, `required`: boolean }) — OPTIONAL
- `published_at` (ISO8601) — REQUIRED
- `published_by` (string user_id) — REQUIRED
- `registry_version` (string) — REQUIRED — pointer to registry snapshot id

Template lifecycle: create → publish → deprecate → retire. Maintain immutable historical versions.

PASS: TemplateRegistryDTO frozen (v1.0.0).

---

SECTION 7 — KNOWLEDGE REGISTRY FREEZE

Frozen registry files (structure only) and ownership:

1) `validation_rules.json` (Registry schema v1.0.0)
- Purpose: canonical set of validation rules.
- Owner: Knowledge Team / KBS Validation Service.
- Versioning: file-level `registry_version` and per-entry `version` (integer) and `last_modified` timestamp.
- Consumers: Validation service, UI, Draft suggestion engines.
- Load Strategy: KBS loads on startup and supports hot-reload via a KBS watcher that listens to repository webhooks or file changes.
- Cache Strategy: KBS caches in Postgres `validation_rules` table (normalized) with `registry_version`; in-memory cache (LRU) for hot lookups.
- Invalidation Strategy: KBS increments `registry_version` and emits event `validation_rules.updated` for subscribers; LangGraph receives `registry_version` only.
- Source Of Truth: `knowledge/validation_rules.json` in git repo; canonical updates via PRs.
- PASS

Entry example fields (frozen):
- `rule_id` (string, e.g., "TR-001")
- `version` (integer)
- `title` (string)
- `description` (string)
- `severity` ("CRITICAL"|"HIGH"|"MEDIUM"|"LOW")
- `matcher` (object) — static matcher metadata or pointer to evaluation script id
- `created_at` (ISO8601)
- `created_by` (string)

2) `terraform_templates.json`
- Purpose: registry of Terraform template descriptors.
- Owner: Template Registry (KBS)
- Versioning: `registry_version` and per-template `template_version` (semver)
- Consumers: Template suggestion engine, KBS renderers.
- Load Strategy: KBS loads and normalizes; templates are referenced by `template_id` and `template_version`.
- Cache Strategy: metadata in Postgres; actual template content in artifact store (git/registry).
- Invalidation Strategy: increment `registry_version` and publish event; KBS to invalidate derived values if template changes break compatibility.
- Source Of Truth: `knowledge/terraform_templates.json` in repo + template artifact URIs.
- PASS

Entry example fields:
- `template_id`, `name`, `template_version`, `source.uri`, `published_at`, `registry_version`.

3) `repo_patterns.json`
- Purpose: patterns to detect repo layout, module naming, and canonical fact extraction rules.
- Owner: Knowledge Team (KBS)
- Versioning: `registry_version`, per-pattern `version` integer
- Consumers: RKP normalizer, KBS derivation rules
- Load/Cache/Invalidation: same as above
- Source Of Truth: `knowledge/repo_patterns.json`
- PASS

4) `source_systems.json`
- Purpose: canonical metadata for source systems (names, ids, schemas, endpoints)
- Owner: Integration/Onboarding team (KBS)
- Versioning: `registry_version`
- Consumers: KBS, ingestion pipelines, UI hints
- Load/Cache/Invalidation: KBS-backed tables
- Source Of Truth: `knowledge/source_systems.json`
- PASS

All registries MUST include top-level keys:
- `registry_version` (string)
- `created_at` (ISO8601)
- `created_by` (string)
- `entries` (array)

All registry changes must be submitted via PR to the `knowledge/` folder; KBS watches and increments versions on merge.

---

SECTION 8 — REGISTRY VERSIONING MODEL

Frozen model:
- `registry_version` (string) — globally unique id for registry snapshot (format: ISO8601 + short hash, e.g., 2026-06-20-<sha6>)
- `rule_set_version` (string) — pointer to validation_rules.json `registry_version`
- `template_version` (semver string) — per-template immutable version
- `repo_pattern_version` (string) — pointer to `repo_patterns.json` registry_version
- `source_registry_version` (string) — pointer to `source_systems.json` registry_version

Where stored: registry metadata stored in Git (`knowledge/`) and normalized into KBS Postgres tables. KBS records mapping from `registry_version` → normalized rowset.

Who owns updates: Knowledge Team (maintains `knowledge/` PR process). Merges increment `registry_version` via CI (automation increments and tags commit message). KBS admin tooling may create emergency hotfix versions with an audit entry.

How provenance references versions: Provenance entries include `registry_version` fields referencing the exact registry snapshot id used to derive that value.

PASS: Registry versioning model frozen.

---

SECTION 9 — PROVENANCE MODEL COMPLETION

Final frozen provenance schema (exact):
- `provenance_id` (string, uuid) — PRIMARY KEY
- `derived_from` (array of provenance_id|string) — list of upstream provenance ids (may be empty)
- `derived_at` (ISO8601) — REQUIRED
- `derived_by` (string service_id or user_id) — REQUIRED
- `rule_id` (string|null) — the rule that produced the derivation (e.g., "TR-001") — OPTIONAL
- `template_id` (string|null) — OPTIONAL
- `registry_version` (string|null) — pointer to the registry snapshot used — OPTIONAL but REQUIRED if rule/template referenced
- `repository_reference` (object|null) — minimal repository pointer
  - `repository_id` (string)
  - `commit_sha` (string|null)
  - `path` (string|null)
- `knowledge_context_id` (string|null) — KBS internal context id (e.g., derivation batch id)
- `audit_reference` (string|null) — pointer to audit event id for immutability trace
- `payload_summary` (string|null) — short text summary (<=1024 chars) of what was derived
- `created_at` (ISO8601) — REQUIRED
- `created_by` (string service_id) — REQUIRED

Owner: KBS (authoritative) — provenance entries created at derivation time and persisted in `provenance` table in Postgres.

Storage: Postgres `provenance` table; optionally mirrored to an append-only audit store (object store) for long-term immutable retention.

Consumers: UI, Validation, Audit, Draft change traces, PR review.

PASS: Provenance model frozen.

---

SECTION 10 — STATE REFERENCE MODEL (AUTHORITATIVE OWNERSHIP MATRIX)

What LangGraph stores:
- Small pointers and ids only: `session_id`, `draft_id`, `snapshot_id`, `run_id`, `pr_id`, `kb_version`, `registry_version`, `provenance_id[]`, `current_node`, `last_completed_node`, `current_step`.
- Small ephemeral execution context: `env`, `source_system_id`, `schema_grain` (strings/enums)

What Database (Postgres) stores:
- Authoritative persistent records: `sessions`, `drafts`, `draft_files`, `draft_changes`, `snapshots`, `validation_runs`, `validation_results`, `reviews`, `review_comments`, `review_approvals`, `pr_metadata`, `provenance`, `derived_values`, normalized registries (validation_rules, templates metadata, repo_patterns, source_systems)

What KBS stores:
- Normalized knowledge registries, derived values, rule execution metadata, and provenance creation. KBS is owner of registries and derived-values store.

What Repository stores:
- Template source code, raw terraform templates, raw repo contents, canonical registry JSON in `knowledge/` folder.

What Redis stores:
- Short-lived node checkpoints, orchestrator lock tokens, navigator cursors (if low-latency desired), ephemeral caches for derived_value lookups. Redis must not be treated as authoritative for persistent state.

What Audit stores:
- Append-only audit events, links to provenance entries, immutable snapshots of important transitions (PR creation, registry updates). Long-term retention in object store or dedicated audit DB.

Authority matrix (summary):
- Sessions: DB owner `sessions` table
- Drafts & Files: DB owner `drafts`/`draft_files`
- Derived values: KBS (normalized into `derived_values` table)
- Registries: KBS owner; repo is source-of-truth for canonical JSON
- LangGraph: orchestration pointers only

PASS: State reference model frozen.

---

SECTION 11 — PRODUCTION SCALE REVIEW

Scale requirements and frozen mitigations:
- 10,000+ users / concurrent sessions
  - LangGraph must rely on stateless node design; persist minimal pointers and use horizontally scaled orchestrators behind a queue (e.g., Kafka). Session hotspots sharded by `session_id`.
- Session recovery / Draft recovery / Snapshot recovery
  - Snapshots must be immutable, chunked, and paged. Store snapshot metadata in Postgres and heavy payloads in object storage (S3/Blob) with snapshot_id pointer; snapshot restore must stream rather than in-memory load.
- Registry updates / Knowledge versioning
  - KBS must support hot-reload and event-driven invalidation; registry_version used to gate derivations. Registries must be small JSON metadata only; templates/artifacts stored externally.
- Template versioning
  - Template compatibility checks must be part of KBS; incompatible template changes increment `registry_version` and trigger derivation re-validation.
- Audit & Provenance traceability
  - Provenance entries must be created synchronously or in a guaranteed-delivery pipeline; they are immutable and retained per retention policy (e.g., 365 days + archival).

Operational requirements (frozen):
- Rate limits for derivation & validation runs per repository to avoid storms (configurable in KBS).
- LangGraph node checkpoints limited to <= 10 KB per node to avoid state bloat in Redis.
- Snapshot size threshold: if > 10 MB, store chunked in object store and reference from DB.
- Registry version retention: retain last N registry snapshots (configurable, default 32) and archive older snapshots.

PASS: Production-scale constraints and mitigations frozen.

---

SECTION 12 — ARCHITECTURE DRIFT ANALYSIS

Compare against prior freezes (Step-5, Step-5.1, Step-8, Step-9):
- Drift: None in ownership or primary models. Prior recommendations to keep registries in `knowledge/` and KBS accepted and now frozen.
- Ownership conflicts: None; RKP/KBS/Draft/PR responsibilities clarified and aligned.
- Duplicate source-of-truth: Resolved — registries & repo facts remain KBS/repo only; LangGraph references only.
- State bloat: Mitigations applied (pointer-only LangGraph, snapshot chunking, Redis size limits).
- Recovery risks: Addressed by snapshot streaming, TTLs, and navigator cursor limits.

PASS: No unresolved drift.

---

SECTION 13 — FINAL GAP CLOSURE DECISION

STEP-9.1 LANGGRAPH GAP CLOSURE: PASS

Everything below is now frozen (architecture-only):
- KnowledgeState reference-only model
- DTOs: `RepositoryTreeDTO`, `FileImpactDTO`, `ReviewApprovalDTO`, `NavigatorRecoveryDTO`, `TemplateRegistryDTO` (v1.0.0 each)
- Registries: `validation_rules.json`, `terraform_templates.json`, `repo_patterns.json`, `source_systems.json` with `registry_version` meta
- Registry versioning model and update process
- Provenance schema and storage
- State reference ownership matrix and production-scale requirements

Remaining open items (none technical; operational):
- Create the actual machine-readable `knowledge/` JSON files and insert initial registry entries (documentation skeletons recommended). This is a documentation/registry-author task and not an architecture change.

If reviewers accept this freeze, implementations must adhere to the models above. Any schema change requires a formal new freeze (bump DTO `version` and document delta).

Artifacts created/updated: `agent-platform/docs/STEP-9.1_LANGGRAPH_GAP_CLOSURE.md` (this file).

---

If you want, I can next: (a) create machine-readable registry skeletons under `knowledge/` (documentation-only), or (b) export these DTO specs into `agent-platform/docs/DTO_FREEZE.md`. Which would you prefer next?