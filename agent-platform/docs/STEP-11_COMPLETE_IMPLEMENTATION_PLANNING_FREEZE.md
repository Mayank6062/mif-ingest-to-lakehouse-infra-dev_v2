STEP-11 — COMPLETE IMPLEMENTATION PLANNING FREEZE

Authority: Architecture-only planning and sequencing. No code, no implementation, no project generation.

Role: Principal Architect, LangGraph Architect, Database Architect, Platform Architect, Architecture Auditor.

Scope: Determine what must be built first, dependencies, parallelizable work, verification gates, and final roadmap.

All previous freezes (Steps 1–10) are locked and authoritative. Implementation must follow exactly.

Final verdict: PASS — Implementation planning frozen. No architecture conflicts detected. Roadmap sequenced for production-grade system at scale.

---

SECTION 1 — IMPLEMENTATION PHASE INVENTORY

Frozen implementation phases (top-level):

**Phase-1: Backend Foundation**
- Purpose: establish core application infrastructure
- Components: GitHub OAuth, Session persistence, Draft workspace, Snapshots, Knowledge layer bootstrap
- Duration estimate: week 1–2
- Entry criteria: project skeleton, frozen architecture
- Exit criteria: OAuth working, session data persists, draft model functional

**Phase-2: Database Layer**
- Purpose: implement all data persistence tables and repositories
- Components: User/session/draft/review/PR/audit tables, indexes, partitioning strategy
- Duration estimate: week 2–3
- Entry criteria: Phase-1 foundation stable
- Exit criteria: all tables created, migrations working, queries optimized

**Phase-3: Knowledge Layer**
- Purpose: implement repository knowledge extraction and normalization
- Components: RKP, KBS, validation engine, derivation engine, provenance engine
- Duration estimate: week 3–5
- Entry criteria: Phase-1, Phase-2 complete; frozen knowledge registries available
- Exit criteria: RKP scans repo, KBS derives values, validation rules enforced, provenance created

**Phase-4: LangGraph Foundation**
- Purpose: implement orchestration nodes and state management
- Components: all 18 LangGraph nodes, node-to-node communication, state transitions
- Duration estimate: week 4–6 (parallel with Phase-3)
- Entry criteria: Phase-1 foundation; frozen node definitions
- Exit criteria: nodes execute, state transitions validated, orchestration flows work

**Phase-5: API Layer**
- Purpose: implement FastAPI endpoints and contracts
- Components: Auth APIs, Session APIs, Draft APIs, Review APIs, Validation APIs, PR APIs, Audit APIs
- Duration estimate: week 5–7
- Entry criteria: Phase-1, Phase-2, Phase-3, Phase-4 complete
- Exit criteria: all frozen DTOs exposed, contracts match STEP-6.1

**Phase-6: Frontend Foundation**
- Purpose: implement React UI and Redux store
- Components: Pages, components, hooks, Redux slices, SSE integration, session sidebar, navigator
- Duration estimate: week 6–8 (parallel with Phase-5)
- Entry criteria: Phase-1; frozen component contracts (STEP-7.1)
- Exit criteria: UI renders, Redux synced with backend, authentication flow works

**Phase-7: Integration & End-to-End**
- Purpose: connect all layers; validate workflows
- Components: OAuth integration, session-to-draft flow, review workflow, PR creation workflow, recovery flows
- Duration estimate: week 8–9
- Entry criteria: Phases 1–6 complete
- Exit criteria: one complete user session from OAuth through PR creation works

**Phase-8: Validation & Testing**
- Purpose: implement comprehensive test suites
- Components: unit tests, integration tests, workflow tests, snapshot tests, recovery tests, UI tests, e2e tests
- Duration estimate: week 9–10 (parallel with Phase-7)
- Entry criteria: most implementation complete
- Exit criteria: >80% test coverage, critical paths validated

**Phase-9: Production Readiness & Performance**
- Purpose: production hardening, scaling, monitoring
- Components: load testing, recovery testing, security audit, observability (logging, tracing, metrics), CI/CD pipeline, documentation
- Duration estimate: week 10–11
- Entry criteria: Phase-8 testing passes
- Exit criteria: production deployment checklist complete

**Phase-10: Deployment & Rollout**
- Purpose: deploy to production with monitoring
- Components: staging validation, blue-green deployment, canary rollout, runbooks, incident response
- Duration estimate: week 11–12
- Entry criteria: Phase-9 readiness gates pass
- Exit criteria: system live, monitoring alerting, rollback procedures validated

PASS: 10 phases frozen.

---

SECTION 2 — DEPENDENCY GRAPH

Frozen critical path:

```
Phase-1: OAuth & Session Foundation
    ↓
Phase-2: Database Layer (can start week 2, parallel with Phase-1 final)
    ↓
Phase-3: Knowledge Layer ← requires Phases 1, 2
    ↓
Phase-4: LangGraph ← requires Phases 1, 3 (can parallel Phase-3 after week 2)
    ↓
Phase-5: API Layer ← requires Phases 1, 2, 3, 4 (hard dependency)
    ↓
Phase-6: Frontend ← requires Phase-1 (OAuth), Phase-5 (API contracts)
    ↓
Phase-7: Integration ← requires Phases 5, 6
    ↓
Phase-8: Testing ← requires Phase-7
    ↓
Phase-9: Production Readiness ← requires Phases 7, 8
    ↓
Phase-10: Deployment
```

Parallel opportunities:
- Phase-2 (DB) can start end of Phase-1 (not blocked by Phase-1)
- Phase-3 (Knowledge) and Phase-4 (LangGraph) can run parallel after Phase-2 complete (knowledge layer informs some LangGraph decisions but not blocking)
- Phase-6 (Frontend) can start as Phase-5 begins (API stubs/mocks sufficient for early UI work)
- Phase-8 (Testing) can run parallel with Phase-7 (integration tests for completed components)

Hard dependencies:
- Database must be ready before API layer
- Knowledge layer must validate before LangGraph nodes consume derived values
- OAuth must work before session persistence
- API contracts must be frozen before frontend hits endpoints

PASS: dependency graph frozen.

---

SECTION 3 — BUILD ORDER FREEZE

Exact build sequence per component:

**1. GitHub OAuth**
- Build Order: 1st (day 1)
- Why: unblocks session creation, user identity, all downstream flows
- Dependency: none (external service)
- Verification: callback handler works, session created on OAuth success
- Owners: backend auth team
- Pass/Fail: OAuth callback redirects to dashboard, session_id created

**2. Session Persistence**
- Build Order: 2nd (day 1–2)
- Why: unblocks draft creation, UI state retention
- Dependency: GitHub OAuth (1)
- Verification: sessions table, session retrieval, session timeout
- Pass/Fail: create session, retrieve by session_id, timeout works

**3. Draft Workspace Foundation**
- Build Order: 3rd (day 2–3)
- Why: unblocks snapshot, change stack, derived values
- Dependency: Session (2)
- Verification: drafts table, draft states, draft lifecycle
- Pass/Fail: create draft, transition states, update latest_snapshot_id

**4. Snapshots**
- Build Order: 4th (day 3–4)
- Why: unblocks undo/restore, recovery
- Dependency: Draft Workspace (3)
- Verification: snapshots table, immutability, lineage, restore logic
- Pass/Fail: create snapshot, restore from snapshot, lineage intact

**5. Database Layer (all tables)**
- Build Order: 5th (day 4–5)
- Why: foundational; all services depend on persistence
- Dependency: Phases 1–4 schema decisions locked
- Verification: all tables created, indexes, FK constraints, migration tool
- Pass/Fail: all DDL scripts pass, test data loads

**6. Repositories (Data Access Layer)**
- Build Order: 6th (day 5–6)
- Why: abstracts DB access; used by all services
- Dependency: Database (5)
- Verification: CRUD operations, queries, transaction support
- Pass/Fail: test repository methods (create, read, update, delete, query)

**7. RepositoryKnowledgeProvider (RKP)**
- Build Order: 7th (day 6–8)
- Why: ONLY component reading repository; unblocks KBS
- Dependency: Repositories (6), frozen knowledge registries exist
- Verification: scans repo, parses Terraform, normalizes facts, emits events
- Pass/Fail: RKP produces SourceSystemFact, TopicFact, GlueJobFact, fingerprints repository

**8. KnowledgeBaseService (KBS)**
- Build Order: 8th (day 8–10)
- Why: derives values, validates, creates provenance; core pipeline
- Dependency: RKP (7), Repositories (6), knowledge registries in repo (knowledge/)
- Verification: load registries, derive values, create provenance, validate deterministically
- Pass/Fail: KBS derives topic_name, job_name, validation passes

**9. Validation Service**
- Build Order: 9th (day 10–11)
- Why: validates derived values per rules; gating function
- Dependency: KBS (8), validation_rules registry
- Verification: run validation, store results, rule matching
- Pass/Fail: validation rules TR-/JR-/KV-/TV- execute, results persist

**10. Audit Service**
- Build Order: 10th (day 10–11, parallel with Validation)
- Why: append-only audit trail; compliance requirement
- Dependency: Repositories (6)
- Verification: audit log persistence, immutability, queries
- Pass/Fail: actions logged, audit records immutable, queries work

**11. LangGraph Nodes (complete set)**
- Build Order: 11th (day 11–14)
- Why: orchestration engine; integrates all components
- Dependency: Sessions (2), Draft Workspace (3), KBS (8), Validation Service (9)
- Verification: node communication, state transitions, error handling
- Pass/Fail: all 18 nodes execute, state transitions correct

**12. API Layer**
- Build Order: 12th (day 14–16)
- Why: client-facing contracts; frontend integration
- Dependency: All services (1–11) and frozen DTOs (STEP-6.1)
- Verification: endpoint contracts, DTO serialization, error codes
- Pass/Fail: API matches frozen contracts, endpoints respond with correct DTOs

**13. Frontend Layer**
- Build Order: 13th (day 15–18, parallel with API)
- Why: user-facing UI; integrates with API and Redux
- Dependency: API (12), frozen component contracts (STEP-7.1)
- Verification: pages render, Redux synced, authentication flow
- Pass/Fail: UI pages load, session state persisted, OAuth flow works

**14. Review Workspace Integration**
- Build Order: 14th (day 18–19)
- Why: review workflow; gating for PR creation
- Dependency: Frontend (13), LangGraph (11), validation results (9)
- Verification: review comments persist, approvals gated, PR link
- Pass/Fail: review created, comments added, approvals trigger PR creation

**15. PR Creation Flow**
- Build Order: 15th (day 19–20)
- Why: github integration; final workflow
- Dependency: Review Workspace (14), LangGraph (11)
- Verification: duplicate PR protection, commit creation, PR open
- Pass/Fail: one draft → one commit → one PR enforced, GitHub PR created

**16. Session Recovery**
- Build Order: 16th (day 20–21)
- Why: production resilience; session restoration after failures
- Dependency: Snapshots (4), Draft Workspace (3), LangGraph (11)
- Verification: session recovery, draft recovery, snapshot restore
- Pass/Fail: failed session can restore, draft state recovered

PASS: build order frozen for all 16 components.

---

SECTION 4 — PHASE-1 IMPLEMENTATION SCOPE

**Frozen Phase-1 Scope (MVP + Foundation)**

What Phase-1 must include (no exceptions):
- GitHub OAuth (full flow)
- Session persistence (Postgres sessions table)
- User identity stored
- Session timeout policy
- Draft workspace creation (create draft, read draft, list drafts)
- Snapshots (create, restore, lineage)
- Knowledge layer bootstrap (RKP scans repo, KBS produces initial derived values)
- Terraform validation (basic rules from registry)
- Review workspace structure (reviews table, approvals table)
- PR metadata table (for one-draft-one-PR enforcement)
- Audit logging (basic structure)
- Session recovery UI hooks (placeholder, full impl in Phase-8)

What Phase-1 must NOT include:
- Performance optimization (Phase-9)
- Load testing (Phase-9)
- Complex recovery scenarios (Phase-8+)
- Advanced monitoring (Phase-9)
- Canary deployment (Phase-10)
- Full knowledge derivation (Phase-3)
- All LangGraph nodes (Phase-4)
- Complete frontend (Phase-6)

Phase-1 exit criteria:
- OAuth functional (user logs in, session created)
- Draft CRUD works (create, read, update, delete)
- Snapshots functional (create, restore, list)
- RKP successfully scans one sample repository
- KBS derives at least one value (topic_name or job_name)
- Terraform validation runs without error
- Review workspace UI renders (basic)
- One test session from OAuth → Draft creation → Snapshot restore → Review ready

Duration: 2 weeks (intensive)
Team size: 6–8 engineers

PASS: Phase-1 scope frozen.

---

SECTION 5 — KNOWLEDGE LAYER BUILD PLAN

Frozen Knowledge Layer build sequence:

```
Week 1–2:
↓
Knowledge Loaders (load knowledge/validation_rules.json, terraform_templates.json, repo_patterns.json, source_systems.json)
↓
RepositoryKnowledgeProvider (RKP) scans Terraform files, normalizes facts
↓

Week 3:
↓
KnowledgeBaseService (KBS) consumes RKP facts + registries
↓
Derivation Engine produces derived_values + provenance
↓
Validation Engine evaluates validation_rules against derived values
↓

Week 4:
↓
Provenance Engine links derivations to rules/templates/registries
↓
Draft Integration (derived_values loaded into draft context)
↓
Review Integration (validation results available in Review workspace)
```

Build order within Knowledge Layer:
1. Knowledge Loaders: parse JSON registries, normalize into Postgres tables (day 1)
2. RKP Core: file scanning, Terraform parsing, fact extraction (days 1–3)
3. RKP Emission: event emission on repo changes, webhook support (days 3–4)
4. KBS Derivation: rule evaluation, derived_value generation (days 4–6)
5. Validation Engine: rule matching, result storage (days 6–7)
6. Provenance Engine: link derivations to sources, audit trail (days 7–8)
7. Draft Integration: derived_values available in draft context (days 8–9)

Verification gates per step:
- Knowledge Loaders PASS: all registries loaded, queries work
- RKP PASS: produces SourceSystemFact, TopicFact, GlueJobFact with correct fields
- KBS Derivation PASS: derives topic_name, job_name correctly
- Validation PASS: rules execute, results stored per rule_id
- Provenance PASS: every derived_value links to rule_id + registry_version
- Integration PASS: Draft reads derived_values, Review shows validation results

PASS: Knowledge Layer build plan frozen.

---

SECTION 6 — LANGGRAPH BUILD PLAN

Frozen LangGraph node build sequence (18 nodes total):

**Phase-4a: Foundation Nodes (days 1–3)**
1. GitHubOAuthNode — OAuth callback, session creation. Inputs: github_code. Outputs: session_id, user_id.
2. SessionNode — load session context. Inputs: session_id. Outputs: session state, draft_id pointer. Verification: session exists, user identity valid.

**Phase-4b: Context Nodes (days 3–5)**
3. EnvironmentNode — infer deployment environment. Inputs: session context. Outputs: env enum (DEV/STAGING/PROD). Verification: env correctly set.
4. OperationNode — determine operation type. Inputs: session context, user request. Outputs: operation enum (CREATE/UPDATE/VALIDATE/REVIEW/PR). Verification: operation inferred.
5. SourceTypeNode — determine source type. Inputs: user input. Outputs: source_type enum (EXISTING/NEW). Verification: type detected.

**Phase-4c: Knowledge Context Nodes (days 5–7)**
6. KafkaNode — resolve Kafka topic context. Inputs: env, source_system. Outputs: kafka_context. Dependency: KBS. Verification: topic resolved.
7. SourceSystemNode — load source system facts. Inputs: source_type. Outputs: source_system_id, source_system_facts. Dependency: RKP. Verification: facts loaded.
8. SchemaGrainNode — load schema grain. Inputs: source_system_facts. Outputs: schema_grain. Verification: grain extracted.

**Phase-4d: Derivation Nodes (days 7–9)**
9. TopicGenerationNode — derive topic_name. Inputs: schema_grain, source_system. Outputs: derived topic_name. Dependency: KBS. Verification: name matches rules.
10. TopicValidationNode — validate derived topic. Inputs: derived topic_name. Outputs: validation result. Dependency: Validation Service. Verification: result stored.

**Phase-4e: Knowledge Derivation (days 9–11)**
11. KnowledgeDerivationNode — run full KBS derivation. Inputs: env, source_system, schema_grain. Outputs: derived_values[], provenance_id[]. Dependency: KBS. Verification: all fields derived, provenance created.

**Phase-4f: Draft Workflow (days 11–13)**
12. DraftWorkspaceNode — create/update draft. Inputs: derived_values. Outputs: draft_id, snapshot_id. Dependency: KBS, Draft persistence. Verification: draft persisted.
13. ReviewWorkspaceNode — transition to review. Inputs: draft_id, validation results. Outputs: review_id. Dependency: Review Service. Verification: review created.

**Phase-4g: Validation & Confirmation (days 13–15)**
14. TerraformValidationNode — validate Terraform compatibility. Inputs: derived_values, terraform_registry. Outputs: terraform validation result. Dependency: Validation Service. Verification: terraform rules checked.
15. FinalConfirmationNode — user final approval. Inputs: review_id, all derived_values. Outputs: approval or rejection. Dependency: Review Workspace. Verification: user decision captured.

**Phase-4h: Terminal Nodes (days 15–17)**
16. PRCreationNode — create GitHub PR. Inputs: approved derived_values, draft_id. Outputs: pr_id, pr_url. Dependency: PR Service, GitHub API. Verification: PR created, one-draft-one-PR enforced.
17. SessionPersistNode — persist session state. Inputs: final state. Outputs: session saved. Dependency: Session persistence. Verification: recovery possible.
18. OutOfScopeQuestionNode — handle out-of-scope queries. Inputs: user request (unmatched). Outputs: message + clarification. Dependency: none. Verification: user receives clarification.

Build verification:
- Each node passes unit tests (inputs/outputs correct)
- Node communication verified (state transitions)
- Error handling tested (timeout, null, invalid state)
- Integration tested with adjacent nodes

PASS: LangGraph build plan frozen (18 nodes, sequential + some parallel).

---

SECTION 7 — DATABASE BUILD PLAN

Frozen table creation order (dependency-based):

**Week 1: Core Identity Tables**
1. users (user_id PK, email, roles, created_at, deleted_at)
2. sessions (session_id PK, user_id FK, created_at, expires_at, deleted_at)

**Week 1–2: Audit & Core Logging**
3. audit_events (event_id, user_id, entity_id, action, created_at, immutable archive pointer)
4. node_execution_logs (execution_id, session_id, node_id, inputs, outputs, created_at)

**Week 2: Draft Workspace**
5. drafts (draft_id PK, session_id FK, status enum, active_draft_id, latest_snapshot_id, lock_info, created_at)
6. draft_changes (change_id PK, draft_id FK, change_sequence, change_data, created_at, reverted_flag)
7. draft_files / file_impacts (file_impact_id PK, draft_id FK, file_path, impact_type, provenance_refs[])

**Week 2–3: Snapshots & Persistence**
8. snapshots (snapshot_id PK, draft_id FK, parent_snapshot_id, payload metadata, created_at, archived_flag)
9. derived_values (derived_value_id PK, draft_id FK, key, value, editable, source, repository_version, registry_version, provenance_id FK, created_at)

**Week 3: Validation & Provenance**
10. validation_runs (run_id PK, draft_id FK, snapshot_id FK, run_type, outcome, started_at, finished_at)
11. validation_results (result_id PK, run_id FK, rule_id, severity, message, file_path, created_at)
12. provenance (provenance_id PK, derived_from[], rule_id, template_id, repository_version, registry_version, knowledge_context_id, created_at)

**Week 3–4: Review & Approvals**
13. reviews (review_id PK, draft_id FK, status, created_at, created_by)
14. review_comments (comment_id PK, review_id FK, commenter_id, comment_text, created_at)
15. review_approvals (approval_id PK, review_id FK, approver_id, decision enum, note, created_at)

**Week 4: PR & Metadata**
16. pr_metadata (pr_id PK, draft_id FK UNIQUE (soft), commit_sha, pr_url, status, lock_info, created_at)

**Week 4: Knowledge & Registry**
17. repository_versions (repository_version_id PK, commit_sha UNIQUE, repository_id, scanned_at, fingerprint)
18. repository_facts (fact_id PK, repository_version_id FK, fact_type, fact_data, created_at) — denormalized per fact type or single table with type discriminator
19. knowledge_registry_versions (registry_version_id PK, registry_name, created_at, pointer to commit)

Migration order: 1→2→3→4→5→6→7→8→9→10→11→12→13→14→15→16→17→18→19

Indexing strategy:
- Primary keys (implicit)
- Foreign keys for FK constraints
- Composite indexes for common queries (e.g., (draft_id, created_at) for draft history)
- Partial indexes for soft-deleted records

Partitioning strategy (production):
- partition validation_results by month (time-series data)
- partition node_execution_logs by session_id (operational queries)
- shard audit_events if > 100M rows (by created_at range)

PASS: Database build plan frozen.

---

SECTION 8 — API BUILD PLAN

Frozen API layer build sequence (by HTTP path grouping):

**Week 1–2: Auth APIs**
- POST /auth/oauth/callback (GitHub OAuth)
- POST /auth/logout
- GET /auth/status (verify session)
Verification: OAuth flow end-to-end; session persisted

**Week 2–3: Session APIs**
- GET /sessions/{session_id}
- POST /sessions/{session_id}/refresh
- DELETE /sessions/{session_id} (logout)
Verification: session CRUD; timeout enforced

**Week 3–4: Draft APIs**
- POST /drafts (create new draft)
- GET /drafts/{draft_id}
- GET /drafts (list user drafts)
- PUT /drafts/{draft_id} (update status)
- POST /drafts/{draft_id}/snapshots (create snapshot)
- GET /drafts/{draft_id}/snapshots/{snapshot_id} (restore)
- GET /drafts/{draft_id}/changes (change history)
Verification: Draft CRUD; snapshot restore; change list

**Week 4–5: Validation APIs**
- POST /drafts/{draft_id}/validate (trigger validation run)
- GET /drafts/{draft_id}/validation-runs/{run_id}
- GET /drafts/{draft_id}/validation-results
Verification: Validation runs work; results persisted

**Week 5: Review APIs**
- POST /drafts/{draft_id}/reviews (create review)
- GET /reviews/{review_id}
- POST /reviews/{review_id}/comments (add comment)
- POST /reviews/{review_id}/approvals (submit approval)
- GET /reviews/{review_id}/approvals (list approvals)
Verification: Review workflow; approvals link to PR

**Week 5–6: PR APIs**
- POST /drafts/{draft_id}/pr (create PR)
- GET /pr/{pr_id}
- GET /drafts/{draft_id}/pr (get linked PR)
Verification: One-draft-one-PR enforced; GitHub PR created

**Week 6: Knowledge & Navigator APIs**
- GET /repository/facts (all repository facts)
- GET /repository/derived-values (current derived values for session)
- POST /navigator/cursor (save navigator position)
- GET /navigator/recovery (restore navigator state)
Verification: Facts queryable; derivation available; navigator restore works

**Week 6: Audit APIs**
- GET /audit/events (list audit events)
- GET /audit/trail/{entity_id} (trail for entity)
Verification: Audit queryable; immutable

Verification gate per group:
- Each endpoint returns correct DTO (STEP-6.1)
- Error codes match contract
- Authentication required for protected endpoints
- Rate limiting applied

PASS: API build plan frozen.

---

SECTION 9 — FRONTEND BUILD PLAN

Frozen frontend layer build sequence:

**Week 1–2: Foundation & Authentication**
- Authentication page (OAuth redirect)
- Session storage (Redux slice: session state)
- Protected routes (React Router guards)
- HTTP client (Axios with auth headers)
Verification: OAuth flow → dashboard redirect

**Week 2–3: Draft Workspace**
- Draft list page
- Draft creation modal
- Draft viewer page (show derived values)
- Snapshot restore UI
- Change history timeline
- Redux drafts slice
Verification: Create draft, view draft, restore snapshot

**Week 3–4: Navigator**
- Navigator sidebar (file tree)
- Tree navigation component
- Cursor persistence
- Recovery UI (restore from cursor)
Verification: Navigate tree, cursor saved, recovery works

**Week 4–5: Validation Results**
- Validation run trigger button
- Validation results page (rule list, PASS/WARN/FAIL)
- Rule details view
- Error message rendering
Verification: Validation runs trigger, results display

**Week 5–6: Review Workspace**
- Review creation page
- Comment thread component
- Approval voting UI
- Review status display
- Redux review slice
Verification: Create review, add comments, vote approvals

**Week 6–7: Diff View**
- File impact diff view
- Side-by-side diff rendering
- File change summary
- Line-number anchors
Verification: Diff renders correctly; impacts visible

**Week 7–8: Session Sidebar**
- Session info card
- Current step display
- LangGraph state indicators
- Recovery status
- Session timeout warning
Verification: Session state displayed; timeout warning works

**Week 8: Audit & Advanced UI**
- Audit log viewer
- Provenance trace UI
- Advanced filters
- Export audit data
Verification: Audit queryable from UI

Build verification per phase:
- Components match frozen contracts (STEP-7.1)
- Redux dispatches correct actions
- API calls return expected DTOs
- UI renders without errors
- Authentication flow works end-to-end

PASS: Frontend build plan frozen.

---

SECTION 10 — INTEGRATION PLAN

Frozen integration sequence:

**Week 8–9: Layer Integration**

Stage 1: Backend layers (days 1–2)
- Database (all tables) + Repositories (CRUD)
- Repositories + Services (RKP, KBS, Validation, Audit)
- Services + LangGraph (nodes call services)

Verification: each layer can communicate; no import errors; mocks work

Stage 2: LangGraph + API (days 2–3)
- LangGraph nodes output → API serialization (DTOs)
- API endpoints wrap LangGraph node calls
- SSE for real-time updates (node progress)

Verification: API returns correct DTOs from LangGraph results

Stage 3: Frontend + API (days 3–4)
- Frontend HTTP client hits all API endpoints
- Redux stores update from API responses
- SSE subscribes to node progress events

Verification: UI displays API data correctly

Stage 4: End-to-End Workflows (days 4–5)
- OAuth → Session → Draft → Validation → Review → PR (full loop)
- Snapshot restore during draft edit
- Session recovery after server restart
- Concurrent draft edits

Verification: complete user session works; conflicts resolved

Stage 5: Error Handling & Recovery (days 5–6)
- API error responses → frontend error display
- LangGraph node failures → retry logic
- Database connection failures → circuit breaker
- Session timeout → recovery prompt

Verification: system recovers gracefully; user informed

Integration gates:
- Each stage PASS before proceeding to next
- No architecture violations detected
- Performance baseline met (< 500ms API response)
- Concurrent users (10) don't deadlock

PASS: Integration plan frozen.

---

SECTION 11 — TESTING PLAN FREEZE

Frozen testing strategy and order:

**Phase-8a: Unit Tests (weeks 1–2 parallel with implementation)**
- Repository layer: CRUD operations, queries
- Service layer: derivation logic, validation rules, provenance creation
- LangGraph nodes: inputs/outputs, state transitions
- Utility functions: parsing, serialization

Coverage target: >80%
Tools: pytest (backend), Jest (frontend)

**Phase-8b: Integration Tests (weeks 2–3)**
- RKP + KBS: repository scan → fact extraction → derivation
- KBS + Validation: derivation → validation run → result persistence
- Services + API: service methods → API endpoint → DTO response
- Redux + API: state updates from API calls

Coverage target: >60%
Tools: pytest + test fixtures

**Phase-8c: Workflow Tests (weeks 3–4)**
- OAuth → Session → Draft creation (user flow)
- Draft → Snapshot restore → Review (undo flow)
- Review → PR creation (approval flow)
- Concurrent draft edits (conflict detection)

Coverage target: critical paths 100%
Tools: pytest + in-memory DB

**Phase-8d: Snapshot & Recovery Tests (week 4)**
- Snapshot creation immutability
- Snapshot restore lineage correctness
- Session recovery after crash simulation
- Draft recovery after network failure

Coverage target: >90%
Tools: pytest + chaos engineering harness

**Phase-8e: Validation Tests (week 4)**
- Validation rule execution determinism
- Validation result storage and history
- Rule ID registry parsing
- Validation failure recovery

Coverage target: >95%
Tools: pytest + rule engine test fixtures

**Phase-8f: PR Flow Tests (week 5)**
- One-draft-one-PR enforcement (duplicate detection)
- PR creation with GitHub API
- PR status updates (merge/close)
- PR rollback behavior

Coverage target: >90%
Tools: pytest + mock GitHub API

**Phase-8g: UI Component Tests (weeks 5–6)**
- Component rendering (React Testing Library)
- Redux dispatch verification
- Event handler execution
- Error state rendering

Coverage target: >70%
Tools: Jest + React Testing Library

**Phase-8h: E2E Tests (weeks 6–7)**
- Full user journey: OAuth → PR creation (Playwright)
- Session recovery (browser refresh)
- Concurrent user scenarios
- Error recovery paths

Coverage target: critical paths 100%
Tools: Playwright (Python or JS)

**Phase-9: Performance & Load Tests (week 7–8)**
- API response time baseline (< 500ms)
- Concurrent session load (100 users)
- Database query performance (< 100ms for common queries)
- Memory usage under load

Tools: locust, k6, or similar

**Verification gates per test type:**
- Unit: all tests pass; coverage >80%
- Integration: all workflows execute; no race conditions
- Workflow: critical paths (OAuth→PR, Undo, Recovery) PASS
- Snapshot: restore bit-perfect; lineage correct
- Validation: rules deterministic; history queryable
- PR: one-draft-one-PR enforced; GitHub integration works
- UI: components render; Redux syncs
- E2E: user journey end-to-end; browser recovery works
- Performance: response times meet SLA; concurrency handles 100+ users

PASS: Testing plan frozen.

---

SECTION 12 — VERIFICATION GATES

Frozen mandatory verification gates (sequential):

```
PHASE-1-READY ← OAuth works, Sessions persist, Drafts CRUD
    ↓
DATABASE-READY ← All tables created, queries work, indexes active
    ↓
KNOWLEDGE-READY ← RKP scans repo, KBS derives values, Validation runs
    ↓
LANGGRAPH-READY ← All 18 nodes execute, state transitions correct
    ↓
API-READY ← All endpoints return correct DTOs, error codes match
    ↓
FRONTEND-READY ← UI renders, Redux syncs, authentication flow works
    ↓
INTEGRATION-READY ← OAuth→Draft→Validation→Review→PR (one full flow)
    ↓
TEST-READY ← Unit >80%, Integration >60%, E2E critical paths 100%
    ↓
PRODUCTION-READY ← Load tests pass, observability enabled, runbooks written
    ↓
DEPLOYED ← Blue-green deployment validated, rollback tested
```

Gate 1: PHASE-1-READY
- Artifacts: OAuth working (callback handler), session_id persisted, draft CRUD functional
- Tests: OAuth test, session persistence test, draft CRUD test
- Pass condition: OAuth flow completes, session recoverable, draft states transition correctly
- Fail action: fix OAuth or session persistence before proceeding
- Duration: end of week 2

Gate 2: DATABASE-READY
- Artifacts: all 19 tables + migrations
- Tests: table creation scripts, sample data loads, queries execute
- Pass condition: all DDL passes, indexes created, FK constraints enforced
- Fail action: fix schema conflicts before proceeding
- Duration: end of week 3

Gate 3: KNOWLEDGE-READY
- Artifacts: RKP scans repository, KBS derives values, validation runs
- Tests: RKP produces facts (>5 facts per type), KBS produces derived_values (>3 per operation), validation results > 0
- Pass condition: RKP fingerprints repo, KBS derives deterministically, provenance created
- Fail action: debug RKP/KBS derivation before proceeding
- Duration: end of week 4

Gate 4: LANGGRAPH-READY
- Artifacts: all 18 nodes implemented, state transitions tested
- Tests: unit tests for each node, integration tests for adjacent nodes
- Pass condition: nodes execute without error, state transfers correctly, no deadlocks
- Fail action: fix node communication before proceeding
- Duration: end of week 5

Gate 5: API-READY
- Artifacts: all API endpoints per SECTION 8
- Tests: each endpoint returns correct DTO, error codes match contract
- Pass condition: API conformance tests pass >95%
- Fail action: fix API contract violations before proceeding
- Duration: end of week 6

Gate 6: FRONTEND-READY
- Artifacts: all frontend components per SECTION 9
- Tests: component rendering, Redux dispatch, event handling, SSE connection
- Pass condition: critical components render, Redux updates, SSE connects
- Fail action: fix UI issues before proceeding
- Duration: end of week 7

Gate 7: INTEGRATION-READY
- Artifacts: one complete user flow OAuth → PR creation works end-to-end
- Tests: E2E test covers full flow, error recovery paths tested, concurrent access safe
- Pass condition: one user can complete workflow; 10 concurrent users don't conflict
- Fail action: debug integration issues before proceeding
- Duration: end of week 8

Gate 8: TEST-READY
- Artifacts: comprehensive test suite (unit, integration, E2E, performance)
- Tests: coverage >80% (unit), >60% (integration), critical paths 100% (E2E), load test baseline
- Pass condition: all test categories pass, coverage requirements met
- Fail action: improve tests before proceeding to production
- Duration: end of week 9

Gate 9: PRODUCTION-READY
- Artifacts: observability (logging, tracing, metrics), runbooks, incident response procedures
- Tests: load testing validates 1000+ concurrent users, recovery procedures tested, security audit passed
- Pass condition: system stable under load, recovery procedures verified, monitoring alerting active
- Fail action: address production readiness gaps before deploying
- Duration: end of week 10

Gate 10: DEPLOYED
- Artifacts: production deployment, monitoring active, runbooks validated
- Tests: canary rollout succeeds, metrics baseline established, rollback procedure tested
- Pass condition: system live, alerts firing correctly, rollback plan verified
- Fail action: execute rollback procedure; fix issues; re-deploy
- Duration: week 11

PASS: 10 verification gates frozen with pass/fail criteria.

---

SECTION 13 — ARCHITECTURE DRIFT ANALYSIS

Comparing implementation plan (STEP-11) against all prior freezes (STEP-1 through STEP-10):

**Ownership compliance:**
- RKP only reads repository: ✓ enforced in Phase-3 (RKP build isolated)
- KBS owns derivation: ✓ enforced in Phase-3 (KBS depends on RKP, not repositories)
- LangGraph uses pointers only: ✓ enforced in Phase-4 (nodes pass IDs, not payloads)
- Services own persistence: ✓ enforced in Phase-2 (DB layer, then services)

**Source-of-truth compliance:**
- Repository facts from RKP only: ✓
- Registries from knowledge/ only: ✓
- Derived values from KBS only: ✓
- LangGraph stores IDs not copies: ✓

**State duplication checks:**
- Repository artifacts not duplicated in LangGraph: ✓
- Derived values not cached in nodes: ✓
- Validation results not duplicated: ✓

**Dependency compliance:**
- Database before services: ✓ Phase-2 before Phase-3/4
- RKP before KBS: ✓ Phase-3 RKP first
- Knowledge layer before LangGraph: ✓ Phase-3 before Phase-4
- API before Frontend: ✓ Phase-5 before Phase-6

**PR workflow compliance:**
- One Draft → One Commit → One PR enforced: ✓ Phase-1 draft model, Phase-15 PR node
- Review before PR: ✓ Phase-14 review, Phase-15 PR
- No direct repository writes from nodes: ✓ all nodes call services

**Recovery compliance:**
- Session recovery: ✓ Phase-16 (snapshots + draft restore)
- Snapshot recovery: ✓ Phase-4 (snapshots) + Phase-16 (restore logic)
- Audit trail: ✓ Phase-2 audit tables, Phase-10 audit service

**No architecture drift detected.**

PASS: Implementation plan aligns with all frozen architectures.

---

SECTION 14 — WHAT MUST NOT BE IMPLEMENTED FIRST

**Dangerous shortcuts and wrong build orders (EXPLICITLY FORBIDDEN):**

**MUST NOT:**

1. Build LangGraph nodes before database layer
   - Risk: nodes have nowhere to persist; state lost
   - Correct order: Phase-2 DB, then Phase-4 nodes

2. Build API before services are tested
   - Risk: API exposes incomplete/untested business logic
   - Correct order: Phase-3 services tested, Phase-5 API

3. Allow direct repository access from LangGraph nodes
   - Risk: violates RKP-only-reads rule; architecture drift
   - Enforcement: RKP interface only; nodes forbidden from importing repo modules

4. Store full repository facts in LangGraph state
   - Risk: memory bloat, stale copies
   - Enforcement: pointer-only; provenance links only

5. Bypass Draft locking for PR creation
   - Risk: violates one-draft-one-PR; duplicate PRs
   - Enforcement: database unique constraint + application lock check

6. Create PR without Review workspace approval
   - Risk: unvetted changes; compliance violation
   - Enforcement: PRCreationNode checks review status before creating PR

7. Skip validation before PR creation
   - Risk: invalid infrastructure pushed to production
   - Enforcement: validation results must be PASS or explicitly approved WARN

8. Store secrets in LangGraph state
   - Risk: credential leak; security breach
   - Enforcement: secrets manager only; never in state

9. Implement frontend before API contracts finalized
   - Risk: frontend-API mismatch; rework
   - Correct order: Phase-5 API frozen (STEP-6.1 DTOs), then Phase-6 frontend

10. Cache derived values indefinitely
    - Risk: stale values; incorrect derivations
    - Enforcement: cache TTL + invalidation on registry_version change

11. Implement recovery without snapshots
    - Risk: cannot restore draft; data loss
    - Enforcement: snapshots phase-4 must exist before recovery phase-16

12. Parallelize Phase-3 (Knowledge) and Phase-4 (LangGraph) without dependency waits
    - Risk: nodes call KBS before KBS ready; race condition
    - Enforcement: Phase-3 knowledge-ready gate must pass before Phase-4 uses KBS

13. Persist LangGraph state in database as authoritative
    - Risk: state duplication; ownership violation
    - Enforcement: LangGraph transient; DB owns persistent state

14. Allow concurrent draft edits without optimistic locking
    - Risk: lost updates; data corruption
    - Enforcement: optimistic locking (version field) on derived_values

15. Build audit system separate from services
    - Risk: audit trail incomplete; compliance gap
    - Enforcement: audit service integrated at Phase-10, called by services

**What MUST be frozen before build starts:**
- All DTOs (STEP-6.1)
- All database tables (STEP-10)
- All API contracts (STEP-6)
- All LangGraph nodes (STEP-5)
- All component contracts (STEP-7.1)

**No design-during-implementation allowed.** Implementation follows frozen architecture exactly.

PASS: forbidden patterns listed and enforced.

---

SECTION 15 — FINAL IMPLEMENTATION ROADMAP

**Frozen 10-Phase Implementation Roadmap for Production MIF Infrastructure Copilot**

**Phase-1: Backend Foundation (Week 1–2)**
- Entry criteria: Project skeleton complete, architecture frozen (Steps 1–10)
- Build: OAuth, Session persistence, Draft workspace, Snapshots
- Exit criteria: OAuth functional; session persists; draft CRUD works
- Gate: PHASE-1-READY
- Team: 6 engineers (backend)
- Deliverable: OAuth working demo

**Phase-2: Database Layer (Week 2–3, parallel start week 2)**
- Entry criteria: Phase-1 halfway complete
- Build: 19 tables, migrations, indexes, repositories
- Exit criteria: All DDL passes; queries optimized
- Gate: DATABASE-READY
- Team: 2 engineers (DBA + backend)
- Deliverable: Database schema + migration scripts

**Phase-3: Knowledge Layer (Week 3–5)**
- Entry criteria: Phase-2 DATABASE-READY
- Build: RKP, KBS, Validation Engine, Provenance Engine, Draft integration
- Exit criteria: RKP scans repo, KBS derives values, validation runs, provenance created
- Gate: KNOWLEDGE-READY
- Team: 3 engineers (knowledge team)
- Deliverable: Knowledge derivation pipeline end-to-end

**Phase-4: LangGraph Foundation (Week 4–6, parallel with Phase-3 after week 2)**
- Entry criteria: Phase-1 complete, Phase-3 KNOWLEDGE-READY
- Build: All 18 LangGraph nodes, state transitions, error handling
- Exit criteria: Nodes execute, state transitions correct, no deadlocks
- Gate: LANGGRAPH-READY
- Team: 3 engineers (orchestration)
- Deliverable: LangGraph DAG executable

**Phase-5: API Layer (Week 5–7)**
- Entry criteria: Phases 1, 2, 3, 4 complete
- Build: All FastAPI endpoints, DTO serialization, error handling, rate limiting
- Exit criteria: All endpoints return correct DTOs
- Gate: API-READY
- Team: 3 engineers (backend)
- Deliverable: OpenAPI spec + working endpoints

**Phase-6: Frontend Foundation (Week 6–8, parallel with Phase-5)**
- Entry criteria: Phase-1 OAuth, Phase-5 API stubs/mocks available
- Build: Pages, components, Redux, hooks, SSE, session sidebar, navigator
- Exit criteria: UI renders, Redux syncs, authentication works
- Gate: FRONTEND-READY
- Team: 3 engineers (frontend)
- Deliverable: Frontend dashboard + critical workflows

**Phase-7: Integration & End-to-End (Week 8–9)**
- Entry criteria: Phases 5, 6 complete
- Build: End-to-end workflows (OAuth → PR), recovery flows, error handling
- Exit criteria: One complete user flow works; concurrent users safe
- Gate: INTEGRATION-READY
- Team: 2 engineers (integration)
- Deliverable: E2E test suite + working workflows

**Phase-8: Validation & Testing (Week 9–10, parallel with Phase-7)**
- Entry criteria: Most components implemented (Phases 1–7 complete)
- Build: Unit tests, integration tests, E2E tests, snapshot tests, workflow tests
- Exit criteria: Coverage >80% (unit), >60% (integration), critical paths 100%
- Gate: TEST-READY
- Team: 2 engineers (QA)
- Deliverable: Comprehensive test suite + coverage reports

**Phase-9: Production Readiness & Performance (Week 10–11)**
- Entry criteria: Phase-8 TEST-READY
- Build: Observability (logging, tracing, metrics), runbooks, incident response, load testing
- Exit criteria: System stable under load, recovery procedures verified, monitoring active
- Gate: PRODUCTION-READY
- Team: 2 engineers (devops/sre)
- Deliverable: Monitoring dashboard + runbooks

**Phase-10: Deployment & Rollout (Week 11–12)**
- Entry criteria: Phase-9 PRODUCTION-READY
- Build: Blue-green deployment, canary rollout, observability validation
- Exit criteria: System live, monitoring working, rollback tested
- Gate: DEPLOYED
- Team: 1 engineer (devops) + SRE on-call
- Deliverable: Live system + rollback procedures

**Total duration: 12 weeks (3 months) for full production deployment**

**Critical path:**
- Phase-1 → Phase-2 → Phase-3 → Phase-4 → Phase-5 → Phase-7 → Phase-9 → Phase-10 (12 weeks)
- Parallel opportunities: Phase-2 start week 2, Phase-4 start week 4, Phase-6 start week 6, Phase-8 start week 8

**Team: 15–20 engineers total**
- Backend: 9–10
- Frontend: 3–4
- QA/DevOps: 3–4

**Cost estimate: TBD** (depends on team rates and location)

**Risk factors:**
- Knowledge registries delayed → Phase-3 delayed
- Database scaling issues → Phase-2 extended
- LangGraph node complexity → Phase-4 extended
- Testing gaps → Phase-8 extended

**Mitigation:**
- Freeze all architecture decisions upfront (✓ Done)
- Parallel work where possible (✓ Planned)
- Verification gates prevent downstream chaos (✓ Defined)
- Rollback procedures ready (✓ Planned for Phase-9)

PASS: Final implementation roadmap frozen.

---

SECTION 16 — FINAL PASS / FAIL MATRIX

| Item | Status | Evidence |
|------|--------|----------|
| Implementation Phase Inventory | PASS | 10 phases defined, entry/exit criteria clear |
| Dependency Graph | PASS | critical path identified, parallel work noted |
| Build Order Freeze | PASS | 16 components sequenced, dependencies clear |
| Phase-1 Scope | PASS | MVP + foundation frozen |
| Knowledge Layer Build | PASS | 7-step sequence frozen |
| LangGraph Build | PASS | 18 nodes sequenced |
| Database Build | PASS | 19 tables + migration order frozen |
| API Build | PASS | endpoints grouped, sequence frozen |
| Frontend Build | PASS | pages + components sequenced |
| Integration Plan | PASS | 5-stage integration + error handling |
| Testing Plan | PASS | 8 test categories + coverage targets |
| Verification Gates | PASS | 10 gates with pass/fail criteria |
| Architecture Drift Analysis | PASS | no violations detected |
| Forbidden Patterns | PASS | 15 dangerous shortcuts listed |
| Final Roadmap | PASS | 10-phase plan + timeline |
| Compliance with Steps 1–10 | PASS | no ownership/SoT violations |

**STEP-11 COMPLETE IMPLEMENTATION PLANNING FREEZE: PASS**

All implementation decisions frozen. Architecture compliance verified. No code written. No implementation generated. Planning frozen only.

Implementation teams may now begin Phase-1 with confidence that:
- Dependencies are clear
- Verification gates prevent drift
- Parallel work is safe
- Recovery paths are planned
- Production scale is achievable

Artifacts: this document (STEP-11_COMPLETE_IMPLEMENTATION_PLANNING_FREEZE.md)