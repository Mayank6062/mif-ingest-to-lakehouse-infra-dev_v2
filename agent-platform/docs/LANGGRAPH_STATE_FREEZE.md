# LangGraph State Model Verification & Freeze (STEP-9)

Authority: architecture-only verification and freeze. No code, no implementation, no redesign. Verifies LangGraph state model against all prior frozen artifacts.

Final verdict: PASS with minor documentation gaps (DTO field-level freezes and registries). See 'Missing Gaps'.

---

SECTION 1 — CURRENT STATE INVENTORY

State objects required (inventory):

1. SessionState
- Purpose: track user sessions, last activity, active draft pointer and session-level metadata for UI and recovery.
- Owner: SessionNode / Session service (backend). LangGraph holds transient session pointers for orchestration.
- Lifecycle: created at session start, updated on activity, ended/archived on explicit close/timeout.
- Persistence: Postgres `sessions` table (primary). LangGraph holds ephemeral state with session_id and pointers.
- Consumers: UI, DraftNode, Recovery flows, LangGraph nodes.
- Producers: SessionNode, API endpoints, LangGraph orchestration.
- PASS

2. DraftState
- Purpose: represent active draft identity, status (DRAFT_EDITING, REVIEW_READY, PR_CREATING, PR_CREATED), lock info, latest snapshot reference, change stack head reference.
- Owner: DraftWorkspaceNode / DraftWorkspaceService (backend authoritative).
- Lifecycle: created when draft starts, mutated by draft changes, locked during PR_CREATING, closed/archived after PR_CREATED.
- Persistence: Postgres (`drafts`, `draft_changes`, `draft_files`, `snapshots`). LangGraph holds current draft_id and minimal draft_status for routing.
- Consumers: ReviewNode, PRCreationNode, ValidationNode, UI.
- Producers: DraftWorkspaceNode, KBS (suggested values), user actions via API.
- PASS

3. NodeState
- Purpose: node-specific transient state (inputs, outputs, progress markers) used during LangGraph execution for routing and retries.
- Owner: individual LangGraph nodes (one-node-one-responsibility).
- Lifecycle: ephemeral per execution run; may be checkpointed for long-running flows.
- Persistence: short-lived in Redis or in-memory; durable checkpoints must be persisted to DB/audit if required (node execution entries), not full state.
- Consumers: next nodes in graph, orchestrator.
- Producers: nodes themselves.
- PASS

4. ValidationState
- Purpose: track validation runs, aggregated results, last-run summary, per-rule outcomes.
- Owner: Validation service (invoked by KBS) with LangGraph nodes holding pointers to last run ids.
- Lifecycle: run per-request or per-change; results persisted as `validation_runs` and `validation_results`.
- Persistence: Postgres validation tables; LangGraph stores run_id and high-level outcome for orchestration.
- Consumers: UI, ReviewNode, PRCreationNode
- Producers: Validation service, invoked by KBS or validation nodes
- PASS

5. ReviewState
- Purpose: review workspace state (review_id, comments, approvals, status)
- Owner: ReviewWorkspaceNode / Review service
- Lifecycle: created when review begins, updated as comments/approvals occur, authoritative before PR creation
- Persistence: Postgres (`reviews`, `review_comments`, `review_approvals`); LangGraph stores review_id pointer
- Consumers: PRCreationNode, UI
- Producers: ReviewNode, users
- PASS

6. PRState
- Purpose: PR lifecycle tracking (pr_id, status, commit refs, duplicate protection flag, lock info)
- Owner: PRCreationNode / PR service
- Lifecycle: created on PR creation, updated on merge/close/failure, archived
- Persistence: Postgres `pr_metadata`; LangGraph holds PR flow state during creation
- Consumers: UI, Audit, downstream CI
- Producers: PRCreationNode, external VCS callbacks
- PASS

7. NavigatorState
- Purpose: minimally track navigator cursor, last visited path, and UI position for recovery
- Owner: NavigatorNode / UI
- Lifecycle: ephemeral; persisted when user requests navigator recovery
- Persistence: small cursor persisted in DB if required (navigator_recovery table) or in Redis; do NOT persist full repo tree
- Consumers: UI, recovery flows
- Producers: NavigatorNode, UI actions
- PASS

8. UIState
- Purpose: purely presentation state (modals, input buffers, optimistic UI flags)
- Owner: frontend UI (Redux `ui` slice)
- Lifecycle: client-managed; not authoritative
- Persistence: local browser storage or ephemeral in frontend; NOT in LangGraph
- Consumers: frontend only
- Producers: UI interactions
- PASS

9. ProvenanceState
- Purpose: store references to provenance entries created during derivation (provenance id list, pointers)
- Owner: KBS creates provenance entries; LangGraph nodes reference provenance ids when orchestrating
- Lifecycle: append-only; provenance entries persisted at derivation time
- Persistence: Postgres `provenance` table; LangGraph holds provenance references only
- Consumers: UI, Audit, Validation, PR flow
- Producers: KBS
- PASS

10. KnowledgeState (decision)
- Assessment: Repository facts and KB registries must NOT be duplicated into LangGraph. KnowledgeState should be limited to small operational pointers (e.g., KB version used, rule-set version) but NOT full registries.
- Owner: KBS; LangGraph may store `kb_version` pointer.
- Persistence: registry storage in repo / KBS-backed store; LangGraph stores version references only.
- PASS (KnowledgeState minimal pointer only)

11. SnapshotState
- Purpose: reference to latest snapshot id for draft and restoration pointers
- Owner: Snapshot service / DraftWorkspaceService
- Lifecycle: snapshot created on mutation; restore creates a new snapshot
- Persistence: Postgres `snapshots`; LangGraph holds snapshot_id reference when restore flow running
- Consumers: Restore flows, UI
- Producers: Draft service
- PASS


SECTION 2 — WHAT MUST EXIST IN STATE

Field-level required items (with owner/persistence/reason):

- `session_id`: Owner=Session service; Persistence=Postgres sessions; Reason=identify session for orchestration; PASS
- `user_id`: Owner=Auth service; Persistence=Postgres users; Reason=authorization/context; PASS
- `current_node`: Owner=LangGraph orchestrator; Persistence=transient in Redis; Reason=resume/monitor execution; PASS
- `last_completed_node`: Owner=LangGraph orchestrator; Persistence=transient checkpoint; Reason=resume/retry; PASS
- `active_draft_id`: Owner=Draft service; Persistence=Postgres drafts; Reason=single-draft-authority; PASS
- `env`: Owner=operation context; Persistence=transient (passed in), authoritative in repository facts; Reason=contextual derivation; PASS
- `source_system`: Owner=operation context; Persistence=transient in LangGraph, authoritative in RKP facts; PASS
- `schema_grain`: Owner=operation context; Persistence=transient; PASS
- `derived_values` (references): Owner=KBS; Persistence=Postgres derived_values; LangGraph stores derived_value_ids or snapshot references, NOT full payloads unless small and necessary for execution caching; Reason=avoid duplication; PASS
- `validation_results` (summary/ref): Owner=Validation service; Persistence=validation tables; LangGraph stores run_id and high-level outcome only; PASS
- `review_status`: Owner=Review service; Persistence=reviews table; LangGraph stores pointer; PASS
- `draft_status`: Owner=Draft service (DB); LangGraph stores status for routing; PASS
- `pr_status`: Owner=PR service; Persistence=pr_metadata; LangGraph stores pointer; PASS
- `navigator_position`: Owner=Navigator service/UI; Persistence=optional small cursor table or Redis; Reason=recovery UX; PASS
- `ui_action`: Owner=LangGraph orchestrator (payload ephemeral); Persistence=not stored long-term; PASS
- `current_step`: Owner=LangGraph orchestrator; Persistence=transient; PASS
- `provenance_references`: Owner=KBS; Persistence=provenance table; LangGraph stores ids only; PASS
- `snapshot_reference`: Owner=Snapshot service; Persistence=snapshots table; LangGraph stores snapshot_id when needed; PASS

Overall: everything authoritative is persisted in backend services (Postgres), LangGraph stores small pointers (ids, run_ids, version tags). PASS.

SECTION 3 — WHAT MUST NEVER EXIST IN STATE

Prohibited items (and rationale):

- GitHub OAuth Tokens
  - Reason: credentials; security breach risk
  - Correct storage: secure backend secrets store (vault) and short-lived session cookies
  - Risk: token leakage/exfiltration
  - PASS (must not store)

- Raw Secrets (raw secret values)
  - Reason: sensitive data exposure
  - Correct storage: secrets manager, do not include in LangGraph state
  - Risk: exposure via debug logs or backups
  - PASS

- Terraform Files / Generated Terraform / PR diffs / File contents
  - Reason: large binary/text artifacts; source-of-truth is repo
  - Correct storage: repository (git), drafts metadata refer to file diffs by id; full file content may be stored in draft_files table but not in LangGraph state
  - Risk: bloat, performance, leak
  - PASS

- Large Repository Trees / Full Repository Facts Cache
  - Reason: size and staleness
  - Correct storage: RKP cache (service) and query APIs; LangGraph should store needed references only
  - Risk: memory exhaustion, inconsistent copies
  - PASS

- Complete Audit Logs / Full Snapshots
  - Reason: size and immutability; audits persist in audit store
  - Correct storage: audit DB tables, snapshot store; LangGraph references ids only
  - Risk: duplication and retention complexity
  - PASS

- Knowledge Registries (validation_rules.json, terraform_templates.json, repo_patterns.json)
  - Reason: canonical registries live in KBS/knowledge loader; LangGraph may reference registry version id only
  - Correct storage: knowledge repo or KB service
  - Risk: drift and duplication
  - PASS

SECTION 4 — KNOWLEDGE LAYER STATE BOUNDARY

Verification:
- Repository Facts MUST NOT be stored in LangGraph state. Only RKP provides normalized facts to KBS; LangGraph may store pointers (e.g., source_system name, fact ids) but not full fact caches.
- KnowledgeState: LangGraph should store only small `kb_version` or `rule_set_id` metadata when needed. Full registry data belongs to KBS and knowledge loader.
- Derived Values: ownership resides with KBS; LangGraph may hold derived_value_ids or small ephemeral copies for current execution but must not be the authoritative store.
- Provenance: persisted in provenance table; LangGraph stores provenance id references only.

PASS: boundaries validated.

SECTION 5 — SNAPSHOT STATE MODEL

Rules validated:
- Snapshots are immutable and stored in `snapshots` table; each snapshot has a `snapshot_id` and metadata.
- Restore flow creates a new snapshot and updates draft latest_snapshot pointer.
- Undo model: represented by change stack (LIFO) and optional snapshot rollback creating a new snapshot on restore.
- LangGraph state: store snapshot_id references during restore flows; do NOT store full snapshot content in LangGraph.

Persistence: Postgres `snapshots` and `draft_changes`; LangGraph stores pointer and in-flight operation state.

PASS.

SECTION 6 — VALIDATION STATE MODEL

Verified items:
- ValidationStatus and ValidationResults persisted in `validation_runs` and `validation_results`.
- ValidationHistory: stored per-draft per-snapshot run entries.
- Rule IDs and severity: `TR-###`, `JR-###`, `KV-###`, `TV-###` enforced by registry.
- Ownership: KBS/Validation service owns rules and execution; LangGraph coordinates by referencing run_id.

LangGraph stores only run_id and a high-level outcome enum (PASS/WARN/FAIL) for routing.

PASS.

SECTION 7 — REVIEW STATE MODEL

Verified items:
- ReviewWorkspace authoritative until PR creation; ReviewState persisted in `reviews`, `review_comments`, `review_approvals`.
- LangGraph stores review_id to route to PRCreationNode.
- Review approvals, comments, and metadata persist in DB; LangGraph should not copy comment content as durable state (only pointers).

PASS.

SECTION 8 — PR STATE MODEL

Verified rules:
- One Draft → One Commit → One PR enforced by PRCreationNode; PR lock state held in DB and signaled to LangGraph during PR flow.
- PR metadata and status persisted in `pr_metadata` table; LangGraph stores pr_id during creation run.
- Duplicate PR protection: PRCreationNode checks existing PR metadata and returns DuplicatePRDTO; LangGraph uses that response to update flow.
- PR rollback: PR failures cause Draft.status revert via DraftWorkspaceService; LangGraph coordinates rollback but does not own persistence.

PASS.

SECTION 9 — NAVIGATOR & SESSION RECOVERY

Verified items:
- NavigatorRecoveryDTO and minimal cursor persisted in small table or Redis; LangGraph stores recovery pointers only.
- RepositoryTreeDTO belongs to RKP; LangGraph must not store full tree.
- Session/Draft/Navigator Recovery flows: LangGraph orchestrates calls to services (Draft restore, Snapshot restore) and stores in-flight pointers (snapshot_id, draft_id, session_id, current_step).

PASS.

SECTION 10 — DTO GAP VALIDATION

DTOs checked for presence in DTO freeze and frontend contracts. Missing or partially defined DTOs:

1. `RepositoryTreeDTO` — missing exact field-level freeze. Required fields recommended: `root`, `nodes[]` { `path`, `type` (file|dir), `has_children`, `size` (optional), `last_modified` (optional) }, `cursor` (optional).
2. `FileImpactDTO` (FileImpact) — missing exact fields. Recommended: `file_path`, `impact_type` (ADDED|MODIFIED|DELETED), `lines_changed`, `provenance_refs[]`, `affected_rules[]`.
3. `ReviewApprovalDTO` — partial; recommended fields: `approval_id`, `review_id`, `approver_id`, `approved_at`, `note`.
4. `NavigatorRecoveryDTO` — partial; recommended fields: `navigator_id`, `last_cursor`, `restored_at`, `restored_by`.
5. `TemplateRegistryDTO` — not defined; recommended fields: `template_id`, `name`, `source`, `version`, `description`, `fields_required`.

PASS/FAIL: PARTIAL — DTO level gaps documented and must be frozen separately.

SECTION 11 — KNOWLEDGE REGISTRY VALIDATION

Registries (recommended) and validation:
- Files: `validation_rules.json`, `terraform_templates.json`, `repo_patterns.json`, `source_systems.json`.
- Ownership: Knowledge Team (KBS owner); machine-readable registries stored under `knowledge/` in repo with version metadata.
- Versioning: include `registry_version` and per-entry `version` (semver or integer incremental).
- Loading: KBS loads at startup and subscribes to RKP change notifications for invalidation; supports hot-reload.
- Storage location: `knowledge/` in repo + KBS cache; LangGraph must reference only registry version id.
- Consumers: KBS, validation service, UI hints.
- Registry data belongs to KBS, not LangGraph state.

PASS with Missing Gap: registries absent; recommend creation.

SECTION 12 — STATE MUTATION OWNERSHIP

Ownership summary (create/update/delete/read):

- SessionState
  - Create: Session service
  - Update: Session service (activity), LangGraph triggers via API
  - Delete: Session service (archive)
  - Read: UI, LangGraph

- DraftState
  - Create: DraftWorkspaceService (user action/PR suggestions)
  - Update: DraftWorkspaceService (edits), KBS suggestions via Draft APIs
  - Delete: DraftWorkspaceService (archive)
  - Read: UI, LangGraph

- DerivedValues (persisted)
  - Create: KBS via Draft change APIs (suggestion), DraftWorkspaceService creates change entries on confirm
  - Update: DraftWorkspaceService (edits via DerivedValueEditDTO)
  - Delete: DraftWorkspaceService per change stack semantics
  - Read: UI, LangGraph

- ValidationState
  - Create: Validation service on run
  - Update: Validation service on re-run
  - Read: UI, LangGraph

- ReviewState
  - Create: Review service
  - Update: Review service (comments/approvals)
  - Read: UI, LangGraph

- PRState
  - Create: PRCreationNode via PR service
  - Update: PR service (merge/close)
  - Read: UI, LangGraph

One-node-one-responsibility: preserved — LangGraph nodes orchestrate but do not own persisted state. PASS.

SECTION 13 — ARCHITECTURE DRIFT ANALYSIS

Compared against all frozen artifacts. Findings:
- No drift in state ownership, snapshot model, derived-value editability, or PR lock semantics.
- Hidden coupling risk: templates referenced by modules create external coupling; KBS must treat templates as hints.
- DTO gaps noted (RepositoryTreeDTO, FileImpact, TemplateRegistryDTO). These are documentation gaps, not ownership violations.

PASS with gaps documented.

SECTION 14 — FINAL STATE MODEL (FROZEN HIERARCHY)

LangGraph minimal in-memory state (pointers only) with persistence in backend services.

SessionState (Postgres sessions) — owner: Session service
├─ DraftState (Postgres drafts, draft_changes) — owner: DraftWorkspaceService
│  ├─ SnapshotState (Postgres snapshots) — owner: Snapshot service
│  ├─ ValidationState (validation_runs/results) — owner: Validation service
│  └─ ReviewState (reviews/comments/approvals) — owner: Review service
├─ PRState (pr_metadata) — owner: PR service
├─ NavigatorState (cursor table/Redis) — owner: Navigator service
├─ ProvenanceState (provenance table) — owner: KBS
└─ NodeState (transient/in-memory/Redis checkpoints) — owner: individual nodes

Recovery strategy: LangGraph stores ids (session_id, draft_id, snapshot_id, run_id) to resume flows; persistent recovery artifacts live in DB and RKP caches.

SECTION 15 — FINAL DECISION

STEP-9 LANGGRAPH STATE MODEL: PASS (with minor DTO/registy documentation gaps to be frozen separately).

If any section is considered FAIL by reviewers, provide the exact missing field(s) or ownership change and I will produce a focused freeze doc for that item only (documentation-only).

---

Missing Gaps (actionable, documentation-only):
- Freeze DTO field-level specs for: `RepositoryTreeDTO`, `FileImpactDTO`, `TemplateRegistryDTO`, `NavigatorRecoveryDTO`, `ReviewApprovalDTO`.
- Add machine-readable registries: `validation_rules.json`, `terraform_templates.json`, `repo_patterns.json`, `source_systems.json` under `knowledge/`.

Artifacts created: `agent-platform/docs/LANGGRAPH_STATE_FREEZE.md` (this file).
