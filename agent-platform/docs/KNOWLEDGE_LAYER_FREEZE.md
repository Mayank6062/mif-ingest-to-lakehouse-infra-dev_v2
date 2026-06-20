# Knowledge Layer Verification & Freeze (STEP-8)

Authority: architecture-only freeze. No code. No redesign. This document verifies and freezes the Knowledge Layer, Repository Knowledge Model, RepositoryKnowledgeProvider (RKP), KnowledgeBaseService (KBS), knowledge loader, derived-value mapping, provenance, validation ownership, and architecture drift analysis.

Final verdict: PASS with small documentation gaps (see Missing Gaps).

---

SOURCES INSPECTED
- `saptcc/locals.tf`, `saptcc/glue.tf`
- `saptce/locals.tf`, `saptce/glue.tf`
- `confluent_minerva_dev/topics_saptcc.tf`, `topics_saptce.tf`
- `knowledge_base/mif-glue-job-creation-terraform-script-process.md`
- `project_information/mif-glue-job-creation-terraform-script-process.md`
- `agent-platform/docs/ARCHITECTURE.md`
- `agent-platform/docs/FRONTEND_COMPONENT_CONTRACTS.md`
- Other freeze docs previously created (DTO_FREEZE, FRONTEND_FREEZE)

These confirm repo patterns: `locals.tf` contains `glue_jobs` map entries; `glue.tf` consumes module `glue_jobs` entries; `topics_*.tf` declare topic modules. Knowledge base docs describe template and job creation rules.

---

SECTION 1 — REPOSITORY FACTS MODEL

Goal: canonical list of repository facts and mapping to source files.

Canonical Fact types and mapping:

- `EnvironmentFact`
  - Source files: any `locals.tf` using `local.env`, top-level `confluent_minerva_dev/topics_*.tf` (environment set via locals)
  - Ownership: repository (git) for raw facts; RKP reads and normalizes
  - Purpose: environment-scoped endpoints and account ids
  - Consumers: KBS, Derivers, Validation
  - Source-of-truth: repository

- `SourceSystemFact`
  - Source files: folder names (`saptcc/`, `saptce/`), `module` `source_system` attributes in `topics_*.tf`
  - Ownership: repository
  - Purpose: identity for job/topic grouping and template selection
  - Consumers: RKP, KBS, UI navigator
  - Source-of-truth: repository

- `SchemaGrainFact`
  - Source files: `for_each` keys in `topics_*.tf` and `locals.tf` glue_jobs map keys (e.g., `multi-1`)
  - Purpose: per-stream grain (multi-1, acdoca)
  - Consumers: KBS, derivers
  - Source-of-truth: repository

- `TopicFact`
  - Source files: `confluent_minerva_dev/topics_*.tf`, module inputs (topic name pattern), `glue_job_arguments` `--source_kafka_topic` occurrences in `locals.tf`
  - Purpose: topic name(s), partitions, schema info
  - Consumers: KBS, validation, draft creation
  - Source-of-truth: repository

- `GlueJobFact`
  - Source files: `locals.tf` `glue_jobs` map, `glue.tf` module instantiation
  - Purpose: job_key, job_type, glue_version, worker_type, number_of_workers, glue_job_arguments
  - Consumers: KBS, derivers, DraftWorkspace when creating job entries
  - Source-of-truth: repository

- `LocalsFact`
  - Source files: `locals.tf` (bootstrap endpoints, account ids, groupings)
  - Purpose: environment constants used in derivation and templating
  - Consumers: Derivers, KBS
  - Source-of-truth: repository

- `TerraformPatternFact` (RepositoryPatternFact)
  - Source files: `glue.tf` module source references, `modules/minerva_cc_topic` pattern usage
  - Purpose: canonical repo patterns to scaffold new source-system folders and job entries
  - Consumers: RKP, KBS (for template hints)
  - Source-of-truth: repository

- `StorageFact`
  - Source files: `locals.tf` glue_job_arguments (`--sink_iceberg_warehouse`, `--sink_iceberg_checkpoint_dir`)
  - Purpose: S3 prefixes, DB names
  - Consumers: KBS, derivers
  - Source-of-truth: repository

- `ValidationArtifactFact`
  - Source files: `knowledge_base/*.md` and later `validation_rules.json` (if present)
  - Purpose: guidance for validation rule creation and mapping
  - Consumers: KBS, validation service
  - Source-of-truth: knowledge base / repo

- `TemplateFact`
  - Source files: referenced module source in `glue.tf` and potentially `terraform_templates.json` (recommended)
  - Purpose: candidate Terraform templates for new source systems or job entries
  - Consumers: KBS for template hints
  - Source-of-truth: repository (module sources) and knowledge base

- `RepositoryPatternFact`
  - Source files: repo-level conventions captured in `knowledge_base` docs and `glue.tf` module patterns
  - Purpose: to steer code generation or scaffold recommendations
  - Consumers: KBS, RKP
  - Source-of-truth: repository + knowledge_base

Final Repository Knowledge Model: these fact types are sufficient to represent the current repository artifacts for Phase-1 Glue/Kafka patterns. Field-level specs (FileImpact, RepositoryTreeDTO) are conceptually present but missing explicit field-level freezes — see Missing Gaps.

PASS for Repository Fact model (conceptual) but small documentation gaps for explicit DTO field-level definitions. See Missing Gaps.

---

SECTION 2 — REPOSITORYKNOWLEDGEPROVIDER (RKP) FREEZE

RKP responsibilities (frozen):
- Read repository (files and folders) at a configured repo root and branch (source-of-truth: git).
- Parse Terraform `locals.tf`, `glue.tf`, `topics_*.tf` files and other structured repo artifacts.
- Discover repository patterns (module usage, glue_jobs map patterns, topic module patterns).
- Normalize artifacts into Repository Facts (EnvironmentFact, SourceSystemFact, SchemaGrainFact, TopicFact, GlueJobFact, LocalsFact, TemplateFact, StorageFact, ValidationArtifactFact).
- Attach minimal provenance metadata (file path, repository_ref, commit_ref placeholder, parse timestamp) to each fact.
- Provide cached access (in-memory cache with TTL or persisted cache) and query APIs for KBS (e.g., get_source_system(name), list_glue_jobs(source_system)).

RKP MUST NOT (frozen constraints):
- Apply business rules (e.g., existing-vs-new decisions)
- Perform derivation (no DerivedValue creation)
- Perform validation beyond syntactic parsing
- Select templates
- Mutate drafts
- Mutate DB state
- Mutate LangGraph state
- Create PRs
- Execute workflow logic

Verification: repository files confirm RKP inputs (TF files, modules). No frozen artifact contradicts RKP responsibilities. The architecture docs and earlier freezes explicitly separate repository scanning and knowledge derivation responsibilities.

RKP PASS.

---

SECTION 3 — KNOWLEDGEBASESERVICE (KBS) FREEZE

KBS receives as inputs:
- Repository Facts (from RKP)
- Knowledge rules (from knowledge loader / kb rules registry)
- Templates (template hints)
- Validation rules registry
- Derivation context (env, selected source system, schema grain, operation_context)

KBS produces:
- DerivedValues (DerivedValuesDTO)
- ValidationRules mapped to entities
- TemplateHints (suggested template ids)
- Provenance metadata attached to derived values

KBS responsibilities (frozen):
- Coordinate derivers (invoke per-domain derivers for topic, job, storage, secrets)
- Apply KB rules and heuristics (define which rule contributed which derived value)
- Apply template hints (not to create files, only selection suggestion)
- Apply validation rules (trigger validation for candidate derived values)
- Apply fallback and bootstrap logic for missing repository facts

KBS MUST NOT:
- Read raw TF directly (it receives normalized facts from RKP only)
- Mutate DB or LangGraph state directly (persistence via services/repositories)
- Create drafts or PRs directly (KBS can suggest a draft but creation done by DraftWorkspace service / nodes)
- Perform repository scanning (RKP owns scanning)

Verification: this matches the frozen architecture flow (Repository -> RKP -> KBS -> Derivers -> Draft). No contradictions found.

KBS PASS.

---

SECTION 4 — KNOWLEDGE LOADER

Concepts evaluated: `knowledge/` folder, `source_systems.json`, `validation_rules.json`, `terraform_templates.json`, `repo_patterns.json`.

Current repo: there is a `knowledge_base/*.md` guidance file but no JSON registries detected. Recommendation and freeze:

- Ownership: `knowledge` artifacts are project-maintained (Knowledge Team). They are authoritative for KB rules and templates; canonical location: `knowledge/` or `knowledge_base/` in repo root.
- Loading order (frozen):
  1. repo_patterns.json (patterns)
  2. terraform_templates.json (templates)
  3. source_systems.json (source system canonical list)
  4. validation_rules.json (validation rules catalog)
  5. knowledge rules (rule wiring, mapping)

- Caching strategy: load at KBS startup and refresh on commit notification / periodic TTL; RKP cache invalidation triggers reload of dependent artifacts.
- Normalization: loader normalizes keys (lowercase ids), validates schema, and produces versioned registry entries (semantic version or incrementing registry version).
- Consumer services: KBS, validation service, UI for hints
- Source-of-truth hierarchy: knowledge files in repo > KB admin UI (future) > ephemeral in-memory cache

Current drift: registry JSON files are not present; knowledge exists as MD only. This is not an architecture failure but a missing freeze: a versioned machine-readable registry is recommended.

Knowledge Loader PASS (conceptual) with Missing Gap: supply machine-readable registries (`validation_rules.json`, `terraform_templates.json`, `repo_patterns.json`).

---

SECTION 5 — EXISTING VS NEW SOURCE SYSTEM STRATEGY

Frozen behavior from Business Rules / knowledge docs:
- Existing Source System: modify `locals.tf` only (add glue_job entry)
- Existing Source System: do NOT modify `glue.tf` module template; glue.tf pattern remains
- New Source System: create new folder, add `locals.tf` and `glue.tf` matching repo patterns
- After PR merge for New Source System: repository becomes source-of-truth (new folder persisted)

Verification vs architecture:
- Matches `knowledge_base` docs and `project_information` process notes.
- Nodes responsible: Decision logic belongs to KnowledgeDerivationNode/KBS, but RKP only reports repository facts.
- Enforcement: DraftWorkspaceService and PRCreationNode ensure repository mutation is gated by PR.

PASS.

---

SECTION 6 — DERIVED VALUE MAPPING

Inputs (frozen): env, source_system, schema_grain, operation_context, repository_facts, knowledge_rules, validation_rules
Outputs (frozen): topic_name, job_name, secret_name, checkpoint_path, worker_type, worker_count, iam_role, glue_version, lh_database, s3_path, template_selection, validation_rules (applied)

Notes from repo:
- `glue_jobs` entries in `locals.tf` show canonical mapping fields (glue_version, worker_type, number_of_workers, glue_job_arguments with sink/checkpoint paths). These align with derived-value outputs.
- Topic patterns exist in `topics_*.tf` with schema_grain mapping.

Editability rule (frozen): Derived values are Knowledge Driven but editable in Review Workspace until Draft.status == PR_CREATING. This matches prior DTO freeze.

Mapping freeze (sample):
- `topic_name` := `${env}.${source_system}.${schema_grain}.raw` (pattern from knowledge docs)
- `job_name` := `kafka-to-iceberg-batch-${source_system}-${schema_grain}` or glue_jobs key
- `secret_name` := pattern `minerva-${env}-corp-mif-${source_system}-gluejob-sa-cc-api-creds` when present
- `checkpoint_path` := `--sink_iceberg_checkpoint_dir` from locals
- `worker_type`, `worker_count`, `glue_version` := from glue_jobs entry
- `lh_database` := `--sink_iceberg_database` or mapping rule
- `s3_path` := `--sink_iceberg_warehouse`
- `template_selection` := inferred from module source reference and repo patterns

PASS: Derived mapping aligns; editable-until-PR_CREATING rule preserved.

---

SECTION 7 — PROVENANCE MODEL

Minimum provenance fields (frozen):
- `derived_from` (fact id or source descriptor)
- `repository_ref` (path, e.g., `saptcc/locals.tf:glue_jobs.k`) 
- `commit_ref` (git commit SHA or branch@sha placeholder)
- `kb_rule_id` (knowledge rule id that generated value)
- `template_id` (if template suggested)
- `source_type` (TF, KB, MANUAL)
- `derived_at` (ISO8601)
- `derived_by` (system node id or user id)
- `confidence` (float 0..1)

Storage location: persisted in provenance table linked to draft_changes and derived_values; also included inline in Draft change entries.

Ownership: KBS produces provenance entries; persistence handled by backend repository layer; Audit service indexes for query.

Lifecycle: created at derivation time; immutable append to provenance trail; used in review and audit.

Consumers: UI (DerivedValuesPanel), Audit, Validation, PR creation process.

PASS.

---

SECTION 8 — VALIDATION RULE OWNERSHIP

Frozen assignment:
- Validation rule ownership: Knowledge Layer (KBS) + validation service (coordinated by KBS). Rules are authored/registered in knowledge loader and executed by validation service.
- NOT owned by LangGraph nodes; nodes invoke validation via KBS or validation service.
- NOT owned by UI or DraftWorkspace; UI displays ValidationDTOs only.

Rule loading: from `validation_rules.json` (recommended) or knowledge_base registry loaded by KBS at startup; versioned entries required.

Rule execution: validation service executes rules on Draft or Snapshot inputs; results persisted in `validation_runs` and `validation_results` tables.

Rule versioning: each rule has `rule_id` and `version` metadata; rule ids use prefix schema: `TR-###`, `JR-###`, `KV-###`, `TV-###` as previously frozen.

PASS.

---

SECTION 9 — ARCHITECTURE DRIFT ANALYSIS

Checked all frozen artifacts and repository files.

Findings:
- No major drift: repository facts, RKP, KBS, validation ownership, derived value editability, provenance requirements, existing-vs-new source strategy all align with previously frozen steps.
- Hidden coupling:
  - Templates: module source references in `glue.tf` imply coupling to external module implementations (module source git URL). KBS should treat template selection as hint; RKP must not select templates. This is already defined but calls out the risk.
  - `glue_job_arguments` includes secret names that follow repository conventions; hardcoded secret patterns risk environment-specific leakage. Recommend rules to avoid embedding secrets in TF files.
- Missing freezes / gaps:
  - No machine-readable registry files (`validation_rules.json`, `terraform_templates.json`, `repo_patterns.json`) — knowledge exists as MD but not as canonical JSON registries.
  - `FileImpact` and `RepositoryTreeDTO` field-level definitions not yet frozen — these are used by UI and provenance; recommend explicit field-level freeze.
  - No explicit schema for Template IDs and template registry entries.

Severity: Low — these are documentation gaps, not architecture-breaking.

PASS with recommended minor documentation additions.

---

SECTION 10 — FINAL MATRICES (CONDENSED)

Knowledge Layer Freeze Matrix (roles & responsibilities):
- RKP: repository scanning, parsing, normalization, provenance attach (parse-level), caching, query API. (Must NOT derive/validate/mutate)
- KBS: coordinate derivers, apply KB rules, generate DerivedValues and provenance, advise templates, coordinate validation runs. (Must NOT scan repo or create PRs)
- Validation Service: execute validation rules provided by KBS; persist results
- DraftWorkspaceService: accept edits, persist draft changes, create snapshots
- PRCreationNode: handle PR creation and lock behavior

Repository Fact Matrix: see SECTION 1 mapping (EnvironmentFact, SourceSystemFact, SchemaGrainFact, TopicFact, GlueJobFact, LocalsFact, TerraformPatternFact, StorageFact, ValidationArtifactFact, TemplateFact)

RKP Responsibility Matrix: see SECTION 2 list

KBS Responsibility Matrix: see SECTION 3 list

Derived Value Matrix: mapping inputs -> outputs listed in SECTION 6

Provenance Matrix: fields and storage in SECTION 7

Validation Ownership Matrix: KBS + validation service, rule ids as `TR-###`, `JR-###`, `KV-###`, `TV-###`

Architecture Drift Report: PASS with minor documentation gaps (registry files, DTO field-level specifications, template registry)

Missing Gaps (actionable):
1. Add machine-readable registries: `validation_rules.json`, `terraform_templates.json`, `repo_patterns.json` under `knowledge/`.
2. Freeze DTO field-level spec for `FileImpact`, `RepositoryTreeDTO`, and `TemplateID` entries.
3. Define template registry schema and versioning policy.
4. Add guidance to avoid hardcoding secrets in TF; ensure secret names follow vault patterns.

---

FINAL DECISION: STEP-8 Knowledge Layer Verification & Freeze — PASS

Rationale: All core Knowledge Layer responsibilities, flows, and ownerships align with previously frozen architecture. No workflow or authority changes introduced. Missing items are documentation/registry gaps that should be added but do not constitute architecture drift.

Artifacts produced: `agent-platform/docs/KNOWLEDGE_LAYER_FREEZE.md` (this file).

Next recommended step: create the machine-readable registries and explicit DTO field-level freezes (documentation-only).
