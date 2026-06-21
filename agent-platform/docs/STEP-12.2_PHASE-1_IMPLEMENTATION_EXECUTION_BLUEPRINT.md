# STEP-12.2 — PHASE-1 IMPLEMENTATION EXECUTION BLUEPRINT

**Authority:** Implementation Planning Board, Architecture Governance Board, Repository Verification Board

**Mission:** Produce the definitive Phase-1 execution sequence with zero ambiguity.

**Methodology:** Freeze documents (requirements) + STEP-12.1 audit (reality) = Build order.

**Status:** PLANNING ONLY — No code, no modifications, analysis-based only.

---

# SECTION-1 — PHASE-1 COMPONENT INVENTORY

## Complete Inventory with Current Status

All frozen Phase-1 components classified against repository reality.

---

### LAYER: AUTHENTICATION & SESSION

| Component | Freeze Source | Current Status | Repository Evidence | Owner | Blockers |
|-----------|---|---|---|---|---|
| GitHub OAuth Flow | STEP-2, STEP-6 | COMPLETE | `backend/api/auth.py`, `backend/services/github_oauth.py` | OAuth Service | None |
| Session Creation | STEP-2, STEP-6 | COMPLETE | `backend/services/session.py` | Session Service | None |
| User Model (ORM) | STEP-10 | COMPLETE | `backend/models/__init__.py` User class | Database Layer | None |
| Session Model (ORM) | STEP-10 | COMPLETE | `backend/models/__init__.py` Session class | Database Layer | None |
| UserDTO | STEP-6.1 | COMPLETE | `backend/schemas/__init__.py` | API Layer | None |
| SessionDTO | STEP-6.1 | COMPLETE | `backend/schemas/__init__.py` | API Layer | None |
| OAuth Request/Response DTOs | STEP-6.1 | COMPLETE | `backend/schemas/__init__.py` | API Layer | None |
| Session Recovery | STEP-11 | MISSING | None | Session Service | No session recovery logic |
| Session Cleanup (background) | STEP-11 | MISSING | None | Session Service | No background job |
| Token Rotation | STEP-11.3 | MISSING | None | OAuth Service | No refresh token logic |

**Authentication Summary:**
- COMPLETE: 3 components
- PARTIAL: 0 components
- MISSING: 3 components
- **Status:** Core OAuth works; session lifecycle incomplete

---

### LAYER: DATABASE

| Component | Freeze Source | Current Status | Repository Evidence | Owner | Blockers |
|-----------|---|---|---|---|---|
| User Table | STEP-10 | COMPLETE | ORM model present | Database | None |
| Session Table | STEP-10 | COMPLETE | ORM model present | Database | None |
| Drafts Table | STEP-10 | MISSING | No ORM model | Database | BLOCKS all draft operations |
| DraftChanges Table | STEP-10 | MISSING | No ORM model | Database | BLOCKS draft stack operations |
| DraftFiles Table | STEP-10 | MISSING | No ORM model | Database | BLOCKS file persistence |
| Snapshots Table | STEP-10 | MISSING | No ORM model | Database | BLOCKS snapshot lineage |
| ValidationRuns Table | STEP-10 | MISSING | No ORM model | Database | BLOCKS validation tracking |
| ValidationResults Table | STEP-10 | MISSING | No ORM model | Database | BLOCKS validation storage |
| Reviews Table | STEP-10 | MISSING | No ORM model | Database | BLOCKS review workflow |
| ReviewComments Table | STEP-10 | MISSING | No ORM model | Database | BLOCKS comment persistence |
| ReviewApprovals Table | STEP-10 | MISSING | No ORM model | Database | BLOCKS approval tracking |
| PRMetadata Table | STEP-10 | MISSING | No ORM model | Database | BLOCKS PR tracking |
| AuditEvents Table | STEP-10 | MISSING | No ORM model | Database | BLOCKS audit logging |
| NodeExecutionLogs Table | STEP-10 | MISSING | No ORM model | Database | BLOCKS node debugging |
| Provenance Table | STEP-10 | MISSING | No ORM model | Database | BLOCKS knowledge tracking |
| RepositoryVersions Table | STEP-10 | MISSING | No ORM model | Database | BLOCKS repo cache |
| RepositoryFacts Table | STEP-10 | MISSING | No ORM model | Database | BLOCKS RKP output |
| KnowledgeRegistryVersions Table | STEP-10 | MISSING | No ORM model | Database | BLOCKS registry versioning |
| DerivedValues Table | STEP-10 | MISSING | No ORM model | Database | BLOCKS KBS output |
| Database Connection Pool | STEP-11.2 | PARTIAL | `backend/database/__init__.py` DatabaseManager | Database | Migrations missing |
| Alembic Migrations | STEP-10, STEP-11 | MISSING | No migration files | Database | BLOCKS all table creation |
| UserRepository | STEP-10 | PARTIAL | `backend/repositories/__init__.py` partial | Database | Complete |
| SessionRepository | STEP-10 | PARTIAL | `backend/repositories/__init__.py` referenced only | Database | Complete |
| DraftRepository | STEP-10 | MISSING | None | Database | BLOCKS draft service |
| SnapshotRepository | STEP-10 | MISSING | None | Database | BLOCKS snapshot service |
| ValidationRepository | STEP-10 | MISSING | None | Database | BLOCKS validation service |
| ReviewRepository | STEP-10 | MISSING | None | Database | BLOCKS review service |
| PRRepository | STEP-10 | MISSING | None | Database | BLOCKS PR service |
| AuditRepository | STEP-10 | MISSING | None | Database | BLOCKS audit service |
| ProvenanceRepository | STEP-10 | MISSING | None | Database | BLOCKS provenance service |

**Database Summary:**
- COMPLETE: 2 components
- PARTIAL: 3 components
- MISSING: 24 components (17 tables + 7 repositories + migrations)
- **Status:** Foundation only; core schema incomplete — **CRITICAL BLOCKER**

---

### LAYER: KNOWLEDGE

| Component | Freeze Source | Current Status | Repository Evidence | Owner | Blockers |
|-----------|---|---|---|---|---|
| RKP (RepositoryKnowledgeProvider) | STEP-8 | MISSING | No service class | Knowledge | BLOCKS KBS input |
| KBS (KnowledgeBaseService) | STEP-8 | MISSING | No service class | Knowledge | BLOCKS validation, derivation |
| Validation Rules Registry | STEP-8, STEP-9.1 | MISSING | Not in `knowledge_base/` | Knowledge | BLOCKS validation engine |
| Terraform Templates Registry | STEP-8, STEP-9.1 | MISSING | Not in `knowledge_base/` | Knowledge | BLOCKS template matching |
| Repo Patterns Registry | STEP-8, STEP-9.1 | MISSING | Not in `knowledge_base/` | Knowledge | BLOCKS pattern matching |
| Source Systems Registry | STEP-8, STEP-9.1 | MISSING | Not in `knowledge_base/` | Knowledge | BLOCKS source classification |
| ValidationRuns Table | STEP-10 | MISSING | No ORM model | Database | BLOCKS validation storage |
| ValidationResults Table | STEP-10 | MISSING | No ORM model | Database | BLOCKS result persistence |
| Provenance Table | STEP-10 | MISSING | No ORM model | Database | BLOCKS derivation tracking |
| RepositoryFacts Table | STEP-10 | MISSING | No ORM model | Database | BLOCKS RKP output storage |
| KnowledgeRegistryVersions Table | STEP-10 | MISSING | No ORM model | Database | BLOCKS registry versioning |
| DerivedValues Table | STEP-10 | MISSING | No ORM model | Database | BLOCKS derived output storage |
| Validation Service | STEP-11 | MISSING | No service class | Knowledge | BLOCKS topic validation |
| Provenance Service | STEP-11 | MISSING | No service class | Knowledge | BLOCKS provenance creation |
| Registry Versioning | STEP-11.4 | MISSING | No versioning logic | Knowledge | BLOCKS registry consistency |

**Knowledge Summary:**
- COMPLETE: 0 components
- PARTIAL: 0 components
- MISSING: 15 components
- **Status:** Completely missing — **CRITICAL BLOCKER**

---

### LAYER: LANGGRAPH ORCHESTRATION

| Component | Freeze Source | Current Status | Repository Evidence | Owner | Blockers |
|-----------|---|---|---|---|---|
| GitHubOAuthNode | STEP-5 | MISSING | Directory empty | LangGraph | BLOCKS session workflow |
| SessionNode | STEP-5 | MISSING | Directory empty | LangGraph | BLOCKS session lifecycle |
| EnvironmentNode | STEP-5 | MISSING | Directory empty | LangGraph | BLOCKS env detection |
| OperationNode | STEP-5 | MISSING | Directory empty | LangGraph | BLOCKS operation routing |
| RepositoryNavigatorNode | STEP-5 | MISSING | No directory/file | LangGraph | BLOCKS repo browsing |
| SourceTypeNode | STEP-5 | MISSING | No directory/file | LangGraph | BLOCKS source classification |
| KafkaNode | STEP-5 | MISSING | No directory/file | LangGraph | BLOCKS Kafka config |
| TopicValidationNode | STEP-5 | MISSING | No directory/file | LangGraph | BLOCKS topic validation |
| DuplicateJobValidationNode | STEP-5 | MISSING | No directory/file | LangGraph | BLOCKS duplicate check |
| KnowledgeDerivationNode | STEP-5 | MISSING | No directory/file | LangGraph | BLOCKS name derivation |
| DraftWorkspaceNode | STEP-5 | MISSING | No directory/file | LangGraph | BLOCKS draft creation |
| ReviewWorkspaceNode | STEP-5 | MISSING | No directory/file | LangGraph | BLOCKS review flow |
| TerraformValidationNode | STEP-5 | MISSING | No directory/file | LangGraph | BLOCKS TF validation |
| PRCreationNode | STEP-5 | MISSING | No directory/file | LangGraph | BLOCKS PR creation |
| ConflictResolutionNode | STEP-5 | MISSING | No directory/file | LangGraph | BLOCKS conflict handling |
| OutOfScopeQuestionNode | STEP-5 | MISSING | Directory empty | LangGraph | BLOCKS OOS handling |
| SessionPersistNode | STEP-5 | MISSING | No directory/file | LangGraph | BLOCKS state persistence |
| FinalConfirmationNode | STEP-5 | MISSING | No directory/file | LangGraph | BLOCKS final approval |
| LangGraph State Model | STEP-9, STEP-9.1 | MISSING | `backend/graph/state/` empty | LangGraph | BLOCKS state management |
| Routing Logic | STEP-5.1 | MISSING | `backend/graph/routers/` empty | LangGraph | BLOCKS node transitions |
| Checkpoint/Recovery | STEP-11 | MISSING | No recovery code | LangGraph | BLOCKS session recovery |

**LangGraph Summary:**
- COMPLETE: 0 components
- PARTIAL: 0 components
- MISSING: 21 components
- **Status:** Completely missing — **CRITICAL BLOCKER**

---

### LAYER: API CONTRACTS & DTOs

| Component | Freeze Source | Current Status | Repository Evidence | Owner | Blockers |
|-----------|---|---|---|---|---|
| UserDTO | STEP-6.1 | COMPLETE | Present in schemas | API | None |
| SessionDTO | STEP-6.1 | COMPLETE | Present in schemas | API | None |
| GitHubOAuthCallbackRequest | STEP-6.1 | COMPLETE | Present in schemas | API | None |
| GitHubOAuthCallbackResponse | STEP-6.1 | COMPLETE | Present in schemas | API | None |
| HealthResponse | STEP-6.1 | COMPLETE | Present in schemas | API | None |
| DraftWorkspaceDTO | STEP-6.1 | MISSING | Not in schemas | API | BLOCKS draft API |
| ValidationDTO | STEP-6.1 | MISSING | Not in schemas | API | BLOCKS validation API |
| ValidationSummaryDTO | STEP-6.1 | MISSING | Not in schemas | API | BLOCKS validation API |
| ReviewDTO | STEP-6.1 | MISSING | Not in schemas | API | BLOCKS review API |
| ReviewApprovalDTO | STEP-6.1 | MISSING | Not in schemas | API | BLOCKS review API |
| PRDTO | STEP-6.1 | MISSING | Not in schemas | API | BLOCKS PR API |
| DuplicatePRDTO | STEP-6.1 | MISSING | Not in schemas | API | BLOCKS duplicate check API |
| RepositoryTreeDTO | STEP-6.1 | MISSING | Not in schemas | API | BLOCKS navigator API |
| FileImpactDTO | STEP-6.1 | MISSING | Not in schemas | API | BLOCKS impact analysis API |
| NavigatorRecoveryDTO | STEP-6.1 | MISSING | Not in schemas | API | BLOCKS recovery API |
| TemplateRegistryDTO | STEP-6.1 | MISSING | Not in schemas | API | BLOCKS registry API |
| DerivedValueDTO | STEP-6.1 | MISSING | Not in schemas | API | BLOCKS KBS output API |
| AuditEventDTO | STEP-6.1 | MISSING | Not in schemas | API | BLOCKS audit API |
| POST /agent/message | STEP-6 | MISSING | Not in `backend/api/` | API | BLOCKS primary workflow |
| Draft Endpoints (CRUD) | STEP-6 | MISSING | Not in `backend/api/` | API | BLOCKS draft management |
| Validation Endpoints | STEP-6 | MISSING | Not in `backend/api/` | API | BLOCKS validation trigger |
| Review Endpoints (CRUD) | STEP-6 | MISSING | Not in `backend/api/` | API | BLOCKS review workflow |
| PR Endpoints | STEP-6 | MISSING | Not in `backend/api/` | API | BLOCKS PR workflow |
| Audit Endpoints (query, export) | STEP-6 | MISSING | Not in `backend/api/` | API | BLOCKS audit access |
| Session Recovery Endpoint | STEP-6 | MISSING | Not in `backend/api/` | API | BLOCKS recovery workflow |
| Navigator Endpoints | STEP-6 | MISSING | Not in `backend/api/` | API | BLOCKS repo browsing |

**API Summary:**
- COMPLETE: 5 components (DTOs only)
- PARTIAL: 0 components
- MISSING: 21 components (9 DTOs + 9 endpoints)
- **Status:** Skeleton only; business logic endpoints missing — **CRITICAL BLOCKER**

---

### LAYER: FRONTEND

| Component | Freeze Source | Current Status | Repository Evidence | Owner | Blockers |
|-----------|---|---|---|---|---|
| Login Page | STEP-7 | MISSING | `frontend/src/pages/` empty | Frontend | BLOCKS user access |
| Dashboard Page | STEP-7 | MISSING | `frontend/src/pages/` empty | Frontend | BLOCKS main interface |
| Session Page | STEP-7 | MISSING | `frontend/src/pages/` empty | Frontend | BLOCKS session display |
| Draft Page | STEP-7 | MISSING | `frontend/src/pages/` empty | Frontend | BLOCKS draft editing |
| Review Page | STEP-7 | MISSING | `frontend/src/pages/` empty | Frontend | BLOCKS review interface |
| Navigator Page | STEP-7 | MISSING | `frontend/src/pages/` empty | Frontend | BLOCKS repo browsing UI |
| PR Page | STEP-7 | MISSING | `frontend/src/pages/` empty | Frontend | BLOCKS PR display |
| Audit Page | STEP-7 | MISSING | `frontend/src/pages/` empty | Frontend | BLOCKS audit UI |
| Settings Page | STEP-7 | MISSING | `frontend/src/pages/` empty | Frontend | BLOCKS user settings |
| Redux Auth Slice | STEP-7.1 | MISSING | `frontend/src/store/` empty | Frontend | BLOCKS auth state |
| Redux Session Slice | STEP-7.1 | MISSING | `frontend/src/store/` empty | Frontend | BLOCKS session state |
| Redux Draft Slice | STEP-7.1 | MISSING | `frontend/src/store/` empty | Frontend | BLOCKS draft state |
| Redux Review Slice | STEP-7.1 | MISSING | `frontend/src/store/` empty | Frontend | BLOCKS review state |
| Redux Validation Slice | STEP-7.1 | MISSING | `frontend/src/store/` empty | Frontend | BLOCKS validation state |
| Redux UI Slice | STEP-7.1 | MISSING | `frontend/src/store/` empty | Frontend | BLOCKS UI state |
| Components (20+) | STEP-7.1 | MISSING | `frontend/src/components/` empty | Frontend | BLOCKS UI rendering |

**Frontend Summary:**
- COMPLETE: 0 components
- PARTIAL: 0 components
- MISSING: 25+ components (9 pages + 6 Redux slices + 20+ components)
- **Status:** Completely missing — **BLOCKER (non-critical; downstream)**

---

### LAYER: WORKFLOWS & SERVICES

| Component | Freeze Source | Current Status | Repository Evidence | Owner | Blockers |
|-----------|---|---|---|---|---|
| Draft Service | STEP-11 | MISSING | No service class | Services | BLOCKS draft operations |
| Review Service | STEP-11 | MISSING | No service class | Services | BLOCKS review operations |
| PR Service | STEP-11 | MISSING | No service class | Services | BLOCKS PR operations |
| Snapshot Service | STEP-11 | MISSING | No service class | Services | BLOCKS snapshot management |
| Validation Service | STEP-8, STEP-11 | MISSING | No service class | Services | BLOCKS validation execution |
| Provenance Service | STEP-8, STEP-11 | MISSING | No service class | Services | BLOCKS provenance tracking |
| RKP Service | STEP-8 | MISSING | No service class | Services | BLOCKS knowledge derivation |
| KBS Service | STEP-8 | MISSING | No service class | Services | BLOCKS validation coordination |
| Audit Service | STEP-11.3 | MISSING | No service class | Services | BLOCKS event tracking |

**Services Summary:**
- COMPLETE: 2 (GitHub OAuth, Session) — pre-existing
- PARTIAL: 0 components
- MISSING: 9 components
- **Status:** Core only; business logic services missing — **BLOCKER**

---

### LAYER: SECURITY & RBAC

| Component | Freeze Source | Current Status | Repository Evidence | Owner | Blockers |
|-----------|---|---|---|---|---|
| RoleType Enum | STEP-10, STEP-11.3 | COMPLETE | In `backend/models/__init__.py` | Security | None |
| User.role Field | STEP-10 | COMPLETE | In User ORM model | Security | None |
| Authorization Middleware | STEP-11.3 | MISSING | No middleware | Security | BLOCKS endpoint protection |
| Permission Checks | STEP-11.3 | MISSING | Not in endpoints | Security | BLOCKS RBAC enforcement |
| RBAC Test Matrix | STEP-11.3 | MISSING | No tests | Testing | BLOCKS validation |
| Vault Integration | STEP-11.3 | MISSING | No Vault client | Security | BLOCKS secrets management |
| Secrets Rotation | STEP-11.3 | MISSING | No rotation logic | Security | BLOCKS key lifecycle |

**Security Summary:**
- COMPLETE: 2 components (enum + field)
- PARTIAL: 0 components
- MISSING: 5 components
- **Status:** Infrastructure only; enforcement missing — **BLOCKER for production**

---

### LAYER: CI/CD & VALIDATION

| Component | Freeze Source | Current Status | Repository Evidence | Owner | Blockers |
|-----------|---|---|---|---|---|
| Build Validation | STEP-11.3 | MISSING | `.github/workflows/ci.yml` placeholder | CI/CD | BLOCKS build gating |
| Linting Gate | STEP-11.3 | MISSING | Placeholder only | CI/CD | BLOCKS code quality |
| Testing Gate | STEP-11.3 | MISSING | Placeholder only | CI/CD | BLOCKS test validation |
| Security Scanning | STEP-11.3 | MISSING | No scanning | CI/CD | BLOCKS vulnerability check |
| DTO Validation | STEP-11.4 | MISSING | No gate | CI/CD | BLOCKS contract validation |
| Registry Validation | STEP-11.4 | MISSING | No gate | CI/CD | BLOCKS registry consistency |
| Secrets Scanning | STEP-11.3 | MISSING | No scanning | CI/CD | BLOCKS leak prevention |
| Architecture Compliance | STEP-11.3 | MISSING | No checking | CI/CD | BLOCKS design validation |

**CI/CD Summary:**
- COMPLETE: 0 components
- PARTIAL: 0 components
- MISSING: 8 components (all placeholder)
- **Status:** Non-functional — **BLOCKER for production**

---

### LAYER: AUDIT & COMPLIANCE

| Component | Freeze Source | Current Status | Repository Evidence | Owner | Blockers |
|-----------|---|---|---|---|---|
| AuditEvents Table | STEP-10 | MISSING | No ORM model | Database | BLOCKS audit storage |
| Audit Service | STEP-11.3 | MISSING | No service | Services | BLOCKS event tracking |
| Provenance Table | STEP-10 | MISSING | No ORM model | Database | BLOCKS derivation tracking |
| Provenance Service | STEP-11.3 | MISSING | No service | Services | BLOCKS provenance creation |
| Retention Policies | STEP-11.3 | MISSING | No policy code | Compliance | BLOCKS archival |
| Export/Archival | STEP-11.3 | MISSING | No export code | Compliance | BLOCKS compliance reporting |

**Audit Summary:**
- COMPLETE: 0 components
- PARTIAL: 0 components
- MISSING: 6 components
- **Status:** Completely missing — **BLOCKER for enterprise**

---

## PHASE-1 COMPONENT SUMMARY

| Category | Complete | Partial | Missing | Total | Status |
|----------|----------|---------|---------|-------|--------|
| Authentication | 3 | 0 | 3 | 6 | Partial |
| Database | 2 | 3 | 24 | 29 | Critical |
| Knowledge | 0 | 0 | 15 | 15 | Critical |
| LangGraph | 0 | 0 | 21 | 21 | Critical |
| API & DTOs | 5 | 0 | 21 | 26 | Critical |
| Frontend | 0 | 0 | 25+ | 25+ | Blocker |
| Services | 2 | 0 | 9 | 11 | Critical |
| Security | 2 | 0 | 5 | 7 | Critical |
| CI/CD | 0 | 0 | 8 | 8 | Critical |
| Audit | 0 | 0 | 6 | 6 | Critical |
| **TOTAL** | **14** | **3** | **137+** | **154+** | **12% Complete** |

---

# SECTION-2 — DEPENDENCY GRAPH

## Complete Dependency Chain

```
┌─────────────────────────────────────────────────────┐
│  WAVE-1: DATABASE FOUNDATION                        │
├─────────────────────────────────────────────────────┤
│                                                     │
│  Alembic Migrations Setup                          │
│         ↓                                           │
│  ORM Models (19 tables):                           │
│    - users (✓ exists)                             │
│    - sessions (✓ exists)                          │
│    - drafts ✗                                     │
│    - draft_changes ✗                              │
│    - draft_files ✗                                │
│    - snapshots ✗                                  │
│    - validation_runs ✗                            │
│    - validation_results ✗                         │
│    - reviews ✗                                    │
│    - review_comments ✗                            │
│    - review_approvals ✗                           │
│    - pr_metadata ✗                                │
│    - audit_events ✗                               │
│    - node_execution_logs ✗                        │
│    - provenance ✗                                 │
│    - repository_versions ✗                        │
│    - repository_facts ✗                           │
│    - knowledge_registry_versions ✗                │
│    - derived_values ✗                             │
│         ↓                                           │
│  Repositories Layer:                              │
│    - UserRepository (partial)                     │
│    - SessionRepository (partial)                  │
│    - DraftRepository ✗                            │
│    - SnapshotRepository ✗                         │
│    - ValidationRepository ✗                       │
│    - ReviewRepository ✗                           │
│    - PRRepository ✗                               │
│    - AuditRepository ✗                            │
│    - ProvenanceRepository ✗                       │
└─────────────────────────────────────────────────────┘
                         ↓
         (UNBLOCKS: Knowledge, LangGraph, Services)
```

**Why:**
- All services depend on database persistence
- No feature can store state without database tables
- Repositories are the data access abstraction
- ORM models must exist before services can query
- Migrations must be executable before tables can be populated

**Repository Evidence:**
- `backend/database/__init__.py`: Connection pool configured
- `backend/models/__init__.py`: 2 of 19 models present
- `backend/repositories/__init__.py`: Partial repositories (stubs only)
- No Alembic configuration present

---

```
┌─────────────────────────────────────────────────────┐
│  WAVE-2: KNOWLEDGE LAYER                            │
├─────────────────────────────────────────────────────┤
│  Depends on: Wave-1 (Database)                      │
│                                                     │
│  Registries (4 JSON files):                        │
│    - validation_rules.json ✗                      │
│    - terraform_templates.json ✗                   │
│    - repo_patterns.json ✗                         │
│    - source_systems.json ✗                        │
│         ↓                                           │
│  RKP Service (RepositoryKnowledgeProvider)        │
│    Depends on: Registry files                     │
│    Outputs to: RepositoryFacts table (DB)         │
│    Operations:                                    │
│      - Scan repository                            │
│      - Parse TF files                             │
│      - Extract source systems                     │
│      - Normalize facts                            │
│         ↓                                           │
│  KBS Service (KnowledgeBaseService)               │
│    Depends on: RKP output + Registries            │
│    Stores in: DerivedValues table (DB)            │
│    Operations:                                    │
│      - Apply derivation rules                     │
│      - Generate topic/job names                   │
│      - Coordinate validation                      │
│      - Create provenance records                  │
│         ↓                                           │
│  Validation Service                               │
│    Depends on: KBS + ValidationRuns table         │
│    Stores in: ValidationResults table (DB)        │
│    Operations:                                    │
│      - Apply validation rules                     │
│      - Store results                              │
│                                                     │
│  Provenance Service                               │
│    Depends on: All services                       │
│    Stores in: Provenance table (DB)               │
│    Operations:                                    │
│      - Track derivations                          │
│      - Link transformations                       │
└─────────────────────────────────────────────────────┘
                         ↓
         (UNBLOCKS: LangGraph, Validation Nodes)
```

**Why:**
- Registries must exist as frozen artifacts (not code-generated)
- RKP reads repository and normalizes facts
- KBS applies frozen rules to RKP output
- Both services must persist results in database
- Validation engine depends on all prior services
- Provenance tracks entire derivation chain

**Repository Evidence:**
- No RKP service class
- No KBS service class
- No registry JSON files in `knowledge_base/`
- No validation engine
- No provenance service

---

```
┌─────────────────────────────────────────────────────┐
│  WAVE-3: LANGGRAPH ORCHESTRATION                    │
├─────────────────────────────────────────────────────┤
│  Depends on: Wave-1 (Database) + Wave-2 (Knowledge)│
│                                                     │
│  State Model Classes:                              │
│    - SessionState ✗                               │
│    - DraftState ✗                                 │
│    - ValidationState ✗                            │
│    - ReviewState ✗                                │
│    - PRState ✗                                    │
│    - SnapshotState ✗                              │
│    - ProvenanceState ✗                            │
│         ↓                                           │
│  18 LangGraph Nodes:                              │
│    Primary workflow nodes:                        │
│      1. GitHubOAuthNode → SessionNode             │
│         (Auth flow; uses UserRepository)          │
│      2. SessionNode                               │
│         (Load/validate session)                   │
│      3. EnvironmentNode                           │
│         (Detect repo environment)                 │
│      4. OperationNode                             │
│         (Route to operation handler)              │
│                                                   │
│    Topic derivation nodes:                        │
│      5. RepositoryNavigatorNode                   │
│         (Browse repository; read repository)      │
│      6. SourceTypeNode                            │
│         (Classify source type)                    │
│      7. KafkaNode                                 │
│         (Detect Kafka config)                     │
│      8. TopicValidationNode                       │
│         (Validate topic name)                     │
│      9. DuplicateJobValidationNode                │
│         (Check for duplicates)                    │
│     10. KnowledgeDerivationNode                   │
│         (Derive topic/job name via KBS)           │
│     11. DraftWorkspaceNode                        │
│         (Create draft; store in DB)               │
│     12. SnapshotNode                              │
│         (Create snapshot; store in DB)            │
│                                                   │
│    Review & PR nodes:                             │
│     13. ReviewWorkspaceNode                       │
│         (Create review; store in DB)              │
│     14. TerraformValidationNode                   │
│         (Validate TF syntax)                      │
│     15. PRCreationNode                            │
│         (Create GitHub PR)                        │
│     16. ConflictResolutionNode                    │
│         (Handle conflicts)                        │
│                                                   │
│    Exception handling:                            │
│     17. OutOfScopeQuestionNode                    │
│         (Handle OOS queries)                      │
│     18. SessionPersistNode                        │
│         (Final state persistence)                 │
│         ↓                                          │
│  Routing Logic:                                   │
│    - Node-to-node transitions                     │
│    - Conditional branching                        │
│    - Error handling                               │
│    - State accumulation                           │
│         ↓                                          │
│  Checkpoint/Recovery:                             │
│    - Savepoint creation                           │
│    - Resume from checkpoint                       │
│    - Session history tracking                     │
└─────────────────────────────────────────────────────┘
                         ↓
         (UNBLOCKS: API Layer, Primary Endpoint)
```

**Why:**
- State model defines persistent contract for LangGraph
- Each node is a step in the workflow
- Early nodes (OAuth, Session) are already built
- Middle nodes (Knowledge derivation) depend on Wave-2 services
- Later nodes (Draft, Review, PR) depend on database tables
- All nodes ultimately feed into API responses

**Repository Evidence:**
- `backend/graph/nodes/`: 5 directories present but empty
- `backend/graph/state/`: Empty directory
- `backend/graph/routers/`: Empty directory
- No state model classes
- No node implementations

---

```
┌─────────────────────────────────────────────────────┐
│  WAVE-4: API LAYER & DTOs                           │
├─────────────────────────────────────────────────────┤
│  Depends on: Wave-1 (DB), Wave-2 (Knowledge),      │
│            Wave-3 (LangGraph)                      │
│                                                     │
│  DTOs (Schema Definitions):                        │
│    Existing (5):                                  │
│    - UserDTO ✓                                    │
│    - SessionDTO ✓                                 │
│    - GitHubOAuthCallbackRequest ✓                 │
│    - GitHubOAuthCallbackResponse ✓                │
│    - HealthResponse ✓                             │
│                                                     │
│    Missing (9):                                   │
│    - DraftWorkspaceDTO ✗                          │
│    - ValidationDTO ✗                              │
│    - ValidationSummaryDTO ✗                       │
│    - ReviewDTO ✗                                  │
│    - ReviewApprovalDTO ✗                          │
│    - PRDTO ✗                                      │
│    - DuplicatePRDTO ✗                             │
│    - RepositoryTreeDTO ✗                          │
│    - FileImpactDTO ✗                              │
│    - NavigatorRecoveryDTO ✗                       │
│    - TemplateRegistryDTO ✗                        │
│    - DerivedValueDTO ✗                            │
│    - AuditEventDTO ✗                              │
│         ↓                                           │
│  Endpoints:                                        │
│    Auth (existing):                               │
│    - GET /api/v1/auth/github/authorize ✓          │
│    - GET /api/v1/auth/github/callback ✓           │
│    - GET /api/v1/auth/session/{session_id} ✓      │
│    - POST /api/v1/auth/logout ✓                   │
│    - GET /api/v1/health ✓                         │
│                                                     │
│    PRIMARY (NEW):                                 │
│    - POST /agent/message ✗                        │
│      Input: {session_id, message, ui_action}      │
│      Output: LangGraph execution result           │
│      Depends on: All LangGraph nodes              │
│                                                     │
│    Draft Management:                              │
│    - GET /api/v1/drafts ✗                         │
│    - POST /api/v1/drafts ✗                        │
│    - GET /api/v1/drafts/{draft_id} ✗              │
│    - PUT /api/v1/drafts/{draft_id} ✗              │
│    - DELETE /api/v1/drafts/{draft_id} ✗           │
│      Depends on: DraftRepository, DraftService    │
│                                                     │
│    Validation:                                    │
│    - POST /api/v1/drafts/{id}/validate ✗          │
│    - GET /api/v1/validations/{run_id} ✗           │
│      Depends on: ValidationService, ValidationDTO │
│                                                     │
│    Review Workflow:                               │
│    - POST /api/v1/reviews ✗                       │
│    - GET /api/v1/reviews/{review_id} ✗            │
│    - POST /api/v1/reviews/{id}/comments ✗         │
│    - POST /api/v1/reviews/{id}/approve ✗          │
│      Depends on: ReviewService, ReviewDTO         │
│                                                     │
│    PR Management:                                 │
│    - POST /api/v1/prs ✗                           │
│    - GET /api/v1/prs/{pr_id} ✗                    │
│      Depends on: PRService, PRDTO                 │
│                                                     │
│    Navigator:                                     │
│    - GET /api/v1/repo/tree ✗                      │
│    - GET /api/v1/repo/file/{path} ✗               │
│      Depends on: RKP, RepositoryTreeDTO           │
│                                                     │
│    Audit:                                         │
│    - GET /api/v1/audit/events ✗                   │
│    - POST /api/v1/audit/export ✗                  │
│      Depends on: AuditService, AuditEventDTO      │
│                                                     │
│    Session Recovery:                              │
│    - GET /api/v1/sessions/{id}/recovery ✗         │
│      Depends on: NavigatorRecoveryDTO, SessionNode│
└─────────────────────────────────────────────────────┘
                         ↓
         (UNBLOCKS: Frontend, Full integration)
```

**Why:**
- DTOs are contracts between backend and frontend
- Each DTO must match frozen schema exactly (STEP-6.1)
- Endpoints orchestrate services and database access
- Primary endpoint `/agent/message` is the integration point
- All endpoints depend on LangGraph for workflow orchestration
- Frontend cannot render without endpoint DTOs

**Repository Evidence:**
- `backend/schemas/__init__.py`: 5 DTOs present
- `backend/api/__init__.py`: Only auth and health routers
- `backend/api/auth.py`: OAuth endpoints present
- `backend/api/health.py`: Health endpoint present
- No business logic endpoints
- No message endpoint

---

```
┌─────────────────────────────────────────────────────┐
│  WAVE-5: FRONTEND LAYER                             │
├─────────────────────────────────────────────────────┤
│  Depends on: Wave-4 (API endpoints)               │
│                                                     │
│  Redux Store:                                      │
│    - auth slice (login state)                     │
│    - session slice (user session)                 │
│    - draft slice (draft state)                    │
│    - review slice (review state)                  │
│    - validation slice (test results)              │
│    - ui slice (modal/sidebar state)               │
│         ↓                                           │
│  Pages (React Components):                         │
│    - Login Page                                   │
│      (GitHub OAuth redirect handling)             │
│    - Dashboard Page                               │
│      (Main UI; message input; session display)    │
│    - Session Page                                 │
│      (Current session overview)                   │
│    - Draft Page                                   │
│      (Draft editor; change history)               │
│    - Review Page                                  │
│      (Review interface; comment display)          │
│    - Navigator Page                               │
│      (Repository browser)                         │
│    - PR Page                                      │
│      (PR details; status)                         │
│    - Audit Page                                   │
│      (Event log display)                          │
│    - Settings Page                                │
│      (User preferences)                           │
│         ↓                                           │
│  Components (20+):                                │
│    - MessageChat component                        │
│    - DraftEditor component                        │
│    - ReviewComments component                     │
│    - SessionSidebar component                     │
│    - FileTree component                           │
│    - etc. (defined in STEP-7.1)                   │
│         ↓                                           │
│  API Client Integration:                           │
│    - Fetch/Axios client for endpoints             │
│    - SSE handler for real-time updates            │
│    - Redux middleware for async actions           │
└─────────────────────────────────────────────────────┘
                         ↓
         (Unblocks: Full UI)
```

**Why:**
- Redux slices manage frontend state
- Pages are page-level components
- Components are reusable UI elements
- All depend on Wave-4 API contracts
- Cannot build frontend without endpoint DTOs

**Repository Evidence:**
- `frontend/src/pages/`: Empty directory
- `frontend/src/components/`: Empty directory
- `frontend/src/store/`: Empty directory
- `frontend/src/`: Only assets/, hooks/, services/, utils/ directories

---

```
┌─────────────────────────────────────────────────────┐
│  WAVE-6: SECURITY & RBAC                            │
├─────────────────────────────────────────────────────┤
│  Depends on: All prior waves                       │
│                                                     │
│  RBAC Foundation (✓ exists):                       │
│    - RoleType enum (ADMIN, CONTRIBUTOR,           │
│      REVIEWER, READ_ONLY)                         │
│    - User.role field                              │
│                                                     │
│  Authorization Enforcement (✗ missing):            │
│    - Authorization middleware                     │
│    - Decorator for permission checks              │
│    - Per-endpoint RBAC rules                      │
│    - Test matrix for all role combinations        │
│                                                     │
│  Secrets Management (✗ missing):                   │
│    - Vault client integration                     │
│    - Secret rotation logic                        │
│    - Key lifecycle management                     │
│                                                     │
│  Audit Trail (depends on Wave-2):                  │
│    - Audit events stored in DB                    │
│    - Query/export functionality                   │
└─────────────────────────────────────────────────────┘
                         ↓
         (Enables: Enterprise deployment)
```

**Why:**
- RBAC enum exists but enforcement is missing
- Every endpoint must check permissions
- Vault integration prevents secrets in code
- Audit trail enables compliance

---

```
┌─────────────────────────────────────────────────────┐
│  WAVE-7: CI/CD & VALIDATION                         │
├─────────────────────────────────────────────────────┤
│  Depends on: All prior waves (complete)            │
│                                                     │
│  CI Pipeline Gates:                                │
│    - Linting (Python, JavaScript)                 │
│    - Unit tests                                   │
│    - Integration tests                            │
│    - Security scanning (SAST, dependency check)   │
│    - DTO validation (schema conformance)          │
│    - Registry validation (JSON schema)            │
│    - Architecture compliance check                │
│         ↓                                           │
│  All gates must be BLOCKING for prod.              │
└─────────────────────────────────────────────────────┘
                         ↓
         (Enables: Safe deployment)
```

---

## DEPENDENCY SUMMARY

**Critical Path:**
```
Database (Wave-1)
    ↓
Knowledge Layer (Wave-2)
    ↓
LangGraph Orchestration (Wave-3)
    ↓
API Layer (Wave-4)
    ↓
Frontend (Wave-5)
    ↓
Security & Vault (Wave-6, parallel)
    ↓
CI/CD (Wave-7, parallel)
```

**Key Blockers:**
1. Database layer: Cannot store anything without tables
2. Knowledge layer: Cannot derive without registries + services
3. LangGraph: Cannot orchestrate without state model + nodes
4. API layer: Cannot integrate without endpoints
5. Frontend: Cannot render without endpoints
6. Security: Cannot deploy without RBAC enforcement
7. CI/CD: Cannot safely release without gates

---

# SECTION-3 — IMPLEMENTATION WAVES

## Wave Structure and Sequencing

---

### WAVE-1: DATABASE FOUNDATION

**Objective:** Establish all data persistence infrastructure

**Duration Estimate:** 1-2 weeks

**Entry Criteria:**
- ✓ Alembic migration framework installed
- ✓ PostgreSQL connection configured
- ✓ ORM declarative base ready

**Tasks (in order):**

**Wave-1a — Migration Infrastructure**
1. Create Alembic configuration
2. Create initial migration template
3. Verify migration execution path

**Wave-1b — ORM Model Implementation**
1. Implement Draft table + ORM model
2. Implement DraftChange table + ORM model
3. Implement DraftFile table + ORM model
4. Implement Snapshot table + ORM model
5. Implement ValidationRun table + ORM model
6. Implement ValidationResult table + ORM model
7. Implement Review table + ORM model
8. Implement ReviewComment table + ORM model
9. Implement ReviewApproval table + ORM model
10. Implement PRMetadata table + ORM model
11. Implement AuditEvent table + ORM model
12. Implement NodeExecutionLog table + ORM model
13. Implement Provenance table + ORM model
14. Implement RepositoryVersion table + ORM model
15. Implement RepositoryFact table + ORM model
16. Implement KnowledgeRegistryVersion table + ORM model
17. Implement DerivedValue table + ORM model

**Wave-1c — Repository Layer**
1. Implement DraftRepository (CRUD)
2. Implement SnapshotRepository (CRUD)
3. Implement ValidationRepository (CRUD)
4. Implement ReviewRepository (CRUD)
5. Implement PRRepository (CRUD)
6. Implement AuditRepository (append-only)
7. Implement ProvenanceRepository (query)
8. Complete UserRepository (partial)
9. Complete SessionRepository (partial)

**Wave-1d — Migration Execution**
1. Generate migration scripts from all 17 models
2. Execute migrations against test database
3. Validate all tables created
4. Verify indexes and constraints

**Exit Criteria:**
- ✓ All 19 tables exist in database
- ✓ Alembic migrations are version-controlled
- ✓ All repositories compile without errors
- ✓ CRUD operations testable against all tables

**Depends On:** Nothing (first wave)

**Unblocks:** Wave-2, Wave-3, Wave-4, Wave-5

---

### WAVE-2: KNOWLEDGE LAYER

**Objective:** Implement knowledge derivation system

**Duration Estimate:** 2-3 weeks

**Entry Criteria:**
- ✓ Wave-1 complete (all database tables)
- ✓ RepositoryFacts, DerivedValues, KnowledgeRegistryVersions tables available
- ✓ Registries frozen (STEP-9.1)

**Tasks (in order):**

**Wave-2a — Registry Definition**
1. Create `knowledge/validation_rules.json` with frozen schema (from STEP-9.1)
2. Create `knowledge/terraform_templates.json` with frozen schema
3. Create `knowledge/repo_patterns.json` with frozen schema
4. Create `knowledge/source_systems.json` with frozen schema
5. Validate all JSON against schema (registry_version, version, created_at, released_by, approval_metadata, entries)

**Wave-2b — RKP Service**
1. Create RKP class (RepositoryKnowledgeProvider)
2. Implement repository scanning logic
3. Implement TF file parsing
4. Implement fact extraction
5. Implement fact normalization
6. Implement storage to RepositoryFacts table (via RepositoryVersions)
7. Implement registry versioning

**Wave-2c — KBS Service**
1. Create KBS class (KnowledgeBaseService)
2. Implement derivation rule engine
3. Implement topic/job name derivation
4. Implement validation coordination
5. Implement provenance record creation
6. Implement storage to DerivedValues table
7. Implement registry caching

**Wave-2d — Validation Service**
1. Create ValidationService class
2. Implement rule matching against ValidationRules registry
3. Implement validation result storage (ValidationResults table)
4. Implement validation status tracking

**Wave-2e — Provenance Service**
1. Create ProvenanceService class
2. Implement provenance record creation
3. Implement derivation chain tracking
4. Implement storage to Provenance table

**Exit Criteria:**
- ✓ All 4 registries are frozen JSON files
- ✓ RKP service reads repository and stores facts
- ✓ KBS service applies rules and stores derived values
- ✓ Validation service executes and stores results
- ✓ Provenance service tracks all derivations
- ✓ Registry versioning works end-to-end

**Depends On:** Wave-1 (database layer)

**Unblocks:** Wave-3 (LangGraph knowledge derivation node), Wave-4 (validation API)

---

### WAVE-3: LANGGRAPH ORCHESTRATION

**Objective:** Implement workflow orchestration

**Duration Estimate:** 3-4 weeks

**Entry Criteria:**
- ✓ Wave-1 complete (database)
- ✓ Wave-2 complete (knowledge layer)
- ✓ LangGraph library installed
- ✓ State model definitions available

**Tasks (in order):**

**Wave-3a — State Model Definition**
1. Create SessionState class (from STEP-9.1 frozen spec)
2. Create DraftState class
3. Create ValidationState class
4. Create ReviewState class
5. Create PRState class
6. Create SnapshotState class
7. Create ProvenanceState class
8. Verify all state classes match frozen contracts

**Wave-3b — Early Node Implementation** (already exist partially)
1. GitHubOAuthNode (use existing github_oauth service)
2. SessionNode (use existing session service)
3. OutOfScopeQuestionNode (simple pass-through)

**Wave-3c — Core Node Implementation**
1. EnvironmentNode (detect environment from repository)
2. OperationNode (route to operation handler)
3. RepositoryNavigatorNode (use RKP to browse)
4. SourceTypeNode (classify source system)
5. KafkaNode (detect Kafka configuration)

**Wave-3d — Derivation Node Implementation**
1. TopicValidationNode (validate topic name)
2. DuplicateJobValidationNode (check duplicates)
3. KnowledgeDerivationNode (use KBS to derive names)

**Wave-3e — Draft/Snapshot Node Implementation**
1. DraftWorkspaceNode (create draft in DB)
2. SnapshotNode (create snapshot in DB; implicit—may be part of DraftNode)

**Wave-3f — Review & PR Node Implementation**
1. ReviewWorkspaceNode (create review in DB)
2. TerraformValidationNode (validate TF syntax)
3. PRCreationNode (GitHub API integration)

**Wave-3g — Exception & Finalization**
1. ConflictResolutionNode (handle conflicts)
2. SessionPersistNode (final state persistence)

**Wave-3h — Routing & Transitions**
1. Implement routing logic (node-to-node transitions)
2. Implement conditional branching (based on node outputs)
3. Implement error handling (exceptions → OutOfScopeNode)

**Wave-3i — Checkpoint & Recovery**
1. Implement checkpointing (save state at key points)
2. Implement resume logic (recover from checkpoint)

**Exit Criteria:**
- ✓ All 18 nodes implemented and compilable
- ✓ State model fully typed
- ✓ Routing transitions defined
- ✓ Checkpoint/recovery logic working
- ✓ LangGraph execution plan completes

**Depends On:** Wave-1 (database), Wave-2 (knowledge services)

**Unblocks:** Wave-4 (API layer, primary endpoint)

---

### WAVE-4: API LAYER & DTOs

**Objective:** Implement all API contracts and endpoints

**Duration Estimate:** 2-3 weeks

**Entry Criteria:**
- ✓ Wave-3 complete (LangGraph nodes)
- ✓ All services available (OAuth, Session, Knowledge, Validation)
- ✓ Database repositories available

**Tasks (in order):**

**Wave-4a — DTO Implementation**
1. Create DraftWorkspaceDTO (from STEP-6.1)
2. Create ValidationDTO
3. Create ValidationSummaryDTO
4. Create ReviewDTO
5. Create ReviewApprovalDTO
6. Create PRDTO
7. Create DuplicatePRDTO
8. Create RepositoryTreeDTO
9. Create FileImpactDTO
10. Create NavigatorRecoveryDTO
11. Create TemplateRegistryDTO
12. Create DerivedValueDTO
13. Create AuditEventDTO

**Wave-4b — Primary Endpoint**
1. Create `POST /agent/message` handler
2. Input: {session_id, message, ui_action, context}
3. Operation: Load session → invoke LangGraph → collect output → return response
4. Output: LangGraph execution result (DraftWorkspaceDTO or similar)
5. Error handling: Validation, session not found, LangGraph failures

**Wave-4c — Draft Endpoints**
1. Create `GET /api/v1/drafts` (list user's drafts)
2. Create `POST /api/v1/drafts` (create new draft)
3. Create `GET /api/v1/drafts/{draft_id}` (retrieve draft)
4. Create `PUT /api/v1/drafts/{draft_id}` (update draft)
5. Create `DELETE /api/v1/drafts/{draft_id}` (delete draft)

**Wave-4d — Validation Endpoints**
1. Create `POST /api/v1/drafts/{draft_id}/validate` (run validation)
2. Create `GET /api/v1/validations/{run_id}` (get validation results)

**Wave-4e — Review Endpoints**
1. Create `POST /api/v1/reviews` (create review)
2. Create `GET /api/v1/reviews/{review_id}` (get review)
3. Create `POST /api/v1/reviews/{review_id}/comments` (add comment)
4. Create `POST /api/v1/reviews/{review_id}/approve` (approve review)

**Wave-4f — PR Endpoints**
1. Create `POST /api/v1/prs` (create PR)
2. Create `GET /api/v1/prs/{pr_id}` (get PR status)

**Wave-4g — Navigator Endpoints**
1. Create `GET /api/v1/repo/tree` (get repository tree)
2. Create `GET /api/v1/repo/file/{path}` (get file contents)

**Wave-4h — Audit Endpoints**
1. Create `GET /api/v1/audit/events` (query audit events)
2. Create `POST /api/v1/audit/export` (export audit log)

**Wave-4i — Session Recovery Endpoint**
1. Create `GET /api/v1/sessions/{session_id}/recovery` (recover session state)

**Exit Criteria:**
- ✓ All 14 DTOs implemented
- ✓ All 9+ endpoints implemented
- ✓ Primary `/agent/message` endpoint works end-to-end
- ✓ All endpoints return correct DTOs
- ✓ Error handling consistent

**Depends On:** Wave-3 (LangGraph), Wave-1 (database)

**Unblocks:** Wave-5 (frontend)

---

### WAVE-5: FRONTEND LAYER

**Objective:** Implement React UI

**Duration Estimate:** 3-4 weeks

**Entry Criteria:**
- ✓ Wave-4 complete (all API endpoints)
- ✓ DTOs finalized
- ✓ Frontend skeleton created (package.json, src/, public/)

**Tasks (in order):**

**Wave-5a — Redux Store**
1. Create auth slice (login, logout, user)
2. Create session slice (session_id, status, active_draft)
3. Create draft slice (draft state, changes, status)
4. Create review slice (review state, comments)
5. Create validation slice (validation results)
6. Create ui slice (modals, sidebar state)

**Wave-5b — Pages**
1. Create Login page (OAuth redirect)
2. Create Dashboard page (main UI)
3. Create Session page (session display)
4. Create Draft page (draft editor)
5. Create Review page (review interface)
6. Create Navigator page (repo browser)
7. Create PR page (PR display)
8. Create Audit page (event log)
9. Create Settings page (user settings)

**Wave-5c — Components**
1. Create message chat component
2. Create draft editor component
3. Create review comments component
4. Create session sidebar component
5. Create file tree component
6. Create validation results display
7. Create PR display
8. Create audit event list
9. Plus remaining ~12 components (from STEP-7.1)

**Wave-5d — API Integration**
1. Create API client (fetch/axios wrapper)
2. Create SSE handler for real-time updates
3. Integrate Redux middleware for async actions
4. Connect all components to API endpoints

**Wave-5e — Routing & Navigation**
1. Create React Router configuration
2. Define page routes
3. Implement navigation guards (auth check)

**Exit Criteria:**
- ✓ All 9 pages implemented
- ✓ Redux store fully functional
- ✓ All 20+ components implemented
- ✓ API integration working
- ✓ Navigation working end-to-end

**Depends On:** Wave-4 (API endpoints)

**Unblocks:** Full UI functionality

---

### WAVE-6: SECURITY & RBAC (Parallel with Wave-5)

**Objective:** Implement authorization enforcement

**Duration Estimate:** 1-2 weeks

**Entry Criteria:**
- ✓ Wave-1 complete (database, RoleType enum exists)
- ✓ Wave-4 started (endpoints exist to protect)

**Tasks (in order):**

**Wave-6a — Authorization Middleware**
1. Create authorization middleware (FastAPI dependency)
2. Extract role from session
3. Check permission against resource

**Wave-6b — Endpoint Protection**
1. Add authorization checks to all endpoints
2. Enforce role-based access (Admin, Contributor, Reviewer, ReadOnly)
3. Define permission matrix (role → allowed operations)

**Wave-6c — RBAC Test Matrix**
1. Create tests for each role
2. Create tests for each endpoint
3. Verify: Admin can do all, Contributor limited, Reviewer read-only, ReadOnly minimal

**Wave-6d — Vault Integration**
1. Create Vault client configuration
2. Implement secret retrieval (GitHub OAuth token, DB password, etc.)
3. Implement secret rotation logic (background job)

**Exit Criteria:**
- ✓ Authorization middleware active on all endpoints
- ✓ RBAC tests all passing
- ✓ Vault client configured and functional
- ✓ Secret rotation working

**Depends On:** Wave-1 (database), Wave-4 (endpoints)

**Can run parallel to:** Wave-5 (frontend)

---

### WAVE-7: CI/CD & VALIDATION (Parallel with Waves 5-6)

**Objective:** Implement build and deployment gating

**Duration Estimate:** 1-2 weeks

**Entry Criteria:**
- ✓ All code layers complete enough to build
- ✓ GitHub Actions workflow file exists

**Tasks (in order):**

**Wave-7a — Linting & Type Checking**
1. Configure Python linter (Black, Pylint)
2. Configure JavaScript/TypeScript linter (ESLint)
3. Configure TypeScript type checking (tsc)
4. Make linting gates blocking

**Wave-7b — Unit Tests**
1. Configure pytest for Python
2. Configure Jest for JavaScript
3. Make test gates blocking

**Wave-7c — Integration Tests**
1. Create database integration tests
2. Create API endpoint tests
3. Make integration test gates blocking

**Wave-7d — Security Scanning**
1. Configure SAST (Bandit for Python, npm audit for JavaScript)
2. Configure dependency scanning (Safety, Snyk)
3. Configure secrets scanning (Truffelhog)
4. Make security gates blocking

**Wave-7e — DTO Validation**
1. Verify all DTOs match frozen schema (STEP-6.1)
2. Create schema validation tests
3. Make DTO gate blocking

**Wave-7f — Registry Validation**
1. Verify all registries match frozen JSON schema
2. Create registry validation tests
3. Make registry gate blocking

**Wave-7g — Architecture Compliance**
1. Verify directory structure matches STEP-4
2. Verify layer separation (models, schemas, services, repositories)
3. Create architecture validation tests
4. Make architecture gate blocking

**Exit Criteria:**
- ✓ All CI gates implemented and blocking
- ✓ Build passes all gates
- ✓ Security scanning passing
- ✓ DTO validation passing
- ✓ Registry validation passing

**Depends On:** All code layers

**Can run parallel to:** Waves 5-6

---

## Wave Dependencies Summary

```
Wave-1: Database
    ↓
Wave-2: Knowledge
    ↓
Wave-3: LangGraph
    ↓
Wave-4: API
    ↓
Wave-5: Frontend
    ↓
Wave-6: Security (can start after Wave-1)
    ↓
Wave-7: CI/CD (can start after Wave-1)
```

**Critical Path:** Wave-1 → Wave-2 → Wave-3 → Wave-4 → Wave-5

**Parallel Opportunities:** Wave-6 and Wave-7 can run parallel to Wave-5

---

# SECTION-4 — DATABASE EXECUTION PLAN

## All Missing Tables (17 Total)

Grouped by implementation order.

---

### Group-1: Draft Workspace Persistence (3 tables, Phase-1A)

**Why first:** Draft is the core entity; all work starts with draft creation.

**Tables:**
1. **drafts**
   - Frozen in: STEP-10
   - Fields: draft_id (PK), user_id (FK), session_id (FK), status (ENUM), created_at, updated_at, metadata_json
   - Relationships: users.user_id, sessions.session_id
   - Constraint: Soft-delete (deleted_at nullable)
   - Index: (user_id, status)

2. **draft_changes**
   - Frozen in: STEP-10
   - Fields: change_id (PK), draft_id (FK), change_index, change_type (ENUM), previous_value, new_value, timestamp
   - Relationships: drafts.draft_id
   - Constraint: Immutable (no updates, only inserts)
   - Index: (draft_id, change_index DESC)
   - Purpose: LIFO change stack (from STEP-5.1)

3. **draft_files**
   - Frozen in: STEP-10
   - Fields: file_id (PK), draft_id (FK), file_path, content, status (ENUM), created_at, updated_at
   - Relationships: drafts.draft_id
   - Constraint: Soft-delete
   - Index: (draft_id, file_path)
   - Purpose: Track files modified by draft (new/existing source logic from STEP-5.1)

**Implementation Order:** drafts → draft_changes → draft_files

**Depends On:** Database connection pool, User/Session tables

**Unblocks:** DraftService, DraftWorkspaceNode

---

### Group-2: Snapshot & State Management (1 table, Phase-1A)

**Why early:** Snapshots are created per draft; needed for state recovery.

**Table:**
1. **snapshots**
   - Frozen in: STEP-10
   - Fields: snapshot_id (PK), draft_id (FK), snapshot_index, state_json, created_at
   - Relationships: drafts.draft_id
   - Constraint: Immutable
   - Index: (draft_id, snapshot_index DESC)
   - Purpose: Lineage tracking (from STEP-5.1, STEP-9)

**Depends On:** drafts table

**Unblocks:** SnapshotService, recovery workflows

---

### Group-3: Validation Persistence (2 tables, Phase-1B)

**Why before review:** Validation must run before review can happen.

**Tables:**
1. **validation_runs**
   - Frozen in: STEP-10
   - Fields: run_id (PK), draft_id (FK), status (ENUM: PENDING/RUNNING/PASSED/FAILED), started_at, completed_at
   - Relationships: drafts.draft_id
   - Index: (draft_id, status)
   - Purpose: Track validation execution

2. **validation_results**
   - Frozen in: STEP-10
   - Fields: result_id (PK), run_id (FK), check_type (VARCHAR), passed (BOOLEAN), message, detail_json
   - Relationships: validation_runs.run_id
   - Constraint: Append-only
   - Index: (run_id, check_type)
   - Purpose: Store validation outcomes

**Implementation Order:** validation_runs → validation_results

**Depends On:** drafts table, ValidationService

**Unblocks:** Review workflow

---

### Group-4: Review & Approval (3 tables, Phase-1B)

**Why before PR:** Review must occur before PR creation.

**Tables:**
1. **reviews**
   - Frozen in: STEP-10
   - Fields: review_id (PK), draft_id (FK), reviewer_id (FK), status (ENUM: OPEN/APPROVED/REJECTED), created_at, updated_at
   - Relationships: drafts.draft_id, users.user_id (reviewer_id)
   - Index: (draft_id, status)
   - Purpose: Review workspace

2. **review_comments**
   - Frozen in: STEP-10
   - Fields: comment_id (PK), review_id (FK), author_id (FK), content, created_at, updated_at
   - Relationships: reviews.review_id, users.user_id (author_id)
   - Index: (review_id, created_at)
   - Purpose: Comment persistence

3. **review_approvals**
   - Frozen in: STEP-10
   - Fields: approval_id (PK), review_id (FK), reviewer_id (FK), approved (BOOLEAN), approved_at
   - Relationships: reviews.review_id, users.user_id (reviewer_id)
   - Index: (review_id, reviewer_id)
   - Purpose: Approval tracking (from STEP-6.1)

**Implementation Order:** reviews → review_comments → review_approvals

**Depends On:** users, drafts

**Unblocks:** ReviewService, ReviewWorkspaceNode, PR creation

---

### Group-5: PR Metadata (1 table, Phase-1C)

**Why after review:** PR creation happens only after review approval.

**Table:**
1. **pr_metadata**
   - Frozen in: STEP-10
   - Fields: pr_id (PK), draft_id (FK), github_pr_number, github_url, status (ENUM: CREATED/MERGED/CLOSED), created_at, merged_at
   - Relationships: drafts.draft_id
   - Index: (draft_id, status)
   - Purpose: GitHub PR tracking (from STEP-6.1)

**Depends On:** Review approval logic

**Unblocks:** PRService, PR endpoints

---

### Group-6: Knowledge & Derivation Persistence (4 tables, Phase-1B)

**Why alongside validation:** Knowledge layer outputs stored here.

**Tables:**
1. **repository_versions**
   - Frozen in: STEP-10
   - Fields: version_id (PK), scan_timestamp, repository_url, branch, commit_sha, created_at
   - Purpose: Track repository snapshots (RKP output baseline)
   - Index: (scan_timestamp DESC, repository_url)

2. **repository_facts**
   - Frozen in: STEP-10
   - Fields: fact_id (PK), version_id (FK), fact_type, fact_value, context_json
   - Relationships: repository_versions.version_id
   - Index: (version_id, fact_type)
   - Purpose: Normalized facts from RKP scanning

3. **derived_values**
   - Frozen in: STEP-10
   - Fields: value_id (PK), version_id (FK), derivation_rule, derived_value, confidence, detail_json
   - Relationships: repository_versions.version_id
   - Index: (version_id, derivation_rule)
   - Purpose: Topic/job names derived by KBS

4. **knowledge_registry_versions**
   - Frozen in: STEP-10
   - Fields: registry_id (PK), registry_name, registry_version, released_at, approval_metadata_json
   - Purpose: Registry versioning (from STEP-9.1)
   - Index: (registry_name, registry_version DESC)

**Implementation Order:** repository_versions → repository_facts → derived_values → knowledge_registry_versions

**Depends On:** Database connection pool

**Unblocks:** RKP, KBS, knowledge derivation node

---

### Group-7: Audit & Debugging (2 tables, Phase-1C)

**Why last:** Audit is supplementary; logging can be added after core functionality.

**Tables:**
1. **audit_events**
   - Frozen in: STEP-10
   - Fields: event_id (PK), user_id (FK), event_type (VARCHAR), resource_id, resource_type, action, timestamp, detail_json
   - Relationships: users.user_id
   - Constraint: Append-only, no soft delete
   - Index: (timestamp DESC, user_id)
   - Purpose: Enterprise audit trail (STEP-11.3)

2. **node_execution_logs**
   - Frozen in: STEP-10
   - Fields: log_id (PK), draft_id (FK), node_name, execution_order, status, input_json, output_json, error_message, timestamp
   - Relationships: drafts.draft_id
   - Constraint: Append-only
   - Index: (draft_id, execution_order)
   - Purpose: LangGraph node execution debugging

**Implementation Order:** audit_events → node_execution_logs

**Depends On:** users, drafts

**Unblocks:** Audit service, monitoring

---

### Group-8: Provenance (1 table, Phase-1B)

**Why with knowledge:** Provenance tracks all derivations.

**Table:**
1. **provenance**
   - Frozen in: STEP-10, STEP-9
   - Fields: provenance_id (PK), parent_id (FK nullable), derivation_rule, input_facts_json, output_value, timestamp, depth (integer)
   - Relationships: provenance.provenance_id (self-referential for lineage)
   - Constraint: Append-only
   - Index: (timestamp DESC, parent_id)
   - Purpose: Derivation chain tracking (STEP-9 frozen)

**Depends On:** Knowledge layer services

**Unblocks:** Provenance queries, audit compliance

---

## Database Implementation Sequence (Exact Order)

**Phase-1A (Week 1):**
1. Alembic migration setup
2. drafts ORM + migration
3. draft_changes ORM + migration
4. draft_files ORM + migration
5. snapshots ORM + migration

**Phase-1B (Week 1-2):**
6. validation_runs ORM + migration
7. validation_results ORM + migration
8. reviews ORM + migration
9. review_comments ORM + migration
10. review_approvals ORM + migration
11. repository_versions ORM + migration
12. repository_facts ORM + migration
13. derived_values ORM + migration
14. knowledge_registry_versions ORM + migration
15. provenance ORM + migration

**Phase-1C (Week 2):**
16. pr_metadata ORM + migration
17. audit_events ORM + migration
18. node_execution_logs ORM + migration

**Repositories (parallel with ORM):**
- Wave-1c: All 9 repositories (DraftRepository, ValidationRepository, etc.)

---

# SECTION-5 — KNOWLEDGE LAYER EXECUTION PLAN

## Knowledge Layer Components

---

### RKP (RepositoryKnowledgeProvider)

**Frozen in:** STEP-8

**Purpose:** Scan repository, parse Terraform files, extract normalized facts

**Input:**
- Repository path (from session context)
- Registries (repo_patterns.json, source_systems.json)

**Output:**
- RepositoryFacts entries stored in database
- RepositoryVersions entry (baseline snapshot)

**Implementation Tasks:**
1. Create RKP service class
   - Method: `scan_repository(repo_path: str) → RepositoryVersion`
   - Method: `extract_source_systems() → List[SourceSystem]`
   - Method: `parse_terraform_files() → List[TerraformModule]`
   - Method: `normalize_facts() → List[RepositoryFact]`
   - Method: `store_facts(facts: List) → uuid` (returns version_id)

2. Implement repository scanning
   - Walk directory tree
   - Identify .tf files
   - Identify locals.tf vs. main.tf patterns
   - Extract variables, resources, modules

3. Implement TF file parsing
   - Parse HCL syntax
   - Extract kafka_source blocks
   - Extract topic definitions
   - Extract job definitions

4. Implement source system classification
   - Use source_systems.json registry to classify
   - Map saptcc/saptce to source systems
   - Extract connection details

5. Implement fact normalization
   - Convert raw parse output to RepositoryFact schema
   - Standardize naming (lowercase, underscores)
   - Store to database with version_id foreign key

**Dependencies:**
- RepositoryVersions table (Wave-1B)
- RepositoryFacts table (Wave-1B)
- repo_patterns.json registry (Wave-2a)
- source_systems.json registry (Wave-2a)

**Exit Criteria:**
- ✓ RKP service compiles
- ✓ Can scan sample repository
- ✓ Facts stored to database
- ✓ Version tracking working

---

### KBS (KnowledgeBaseService)

**Frozen in:** STEP-8, STEP-5.1

**Purpose:** Apply frozen derivation rules; generate topic/job names; coordinate validation; create provenance records

**Input:**
- RKP output (RepositoryFacts)
- Registries (validation_rules.json, terraform_templates.json)
- Draft context

**Output:**
- DerivedValues entries stored in database
- Provenance entries showing derivation chain
- ValidationRuns entries (trigger for validation)

**Implementation Tasks:**
1. Create KBS service class
   - Method: `derive_topic_name(source_system: str, existing: bool) → str`
   - Method: `derive_job_name(topic: str) → str`
   - Method: `apply_derivation_rules(facts: List[RepositoryFact]) → List[DerivedValue]`
   - Method: `create_provenance(rule: str, inputs: List, output: str) → ProvenanceRecord`
   - Method: `coordinate_validation(draft_id: uuid) → ValidationRun`

2. Implement derivation rules engine
   - Load validation_rules.json
   - Match facts against rules
   - Execute rule functions
   - Store results to DerivedValues table

3. Implement topic/job name derivation
   - Use frozen business rules from STEP-5.1
   - Existing source: modify locals.tf only
   - New source: create folder structure
   - Name pattern: "mif_" + source_system + "_" + entity_type

4. Implement validation coordination
   - Trigger ValidationService after derivation
   - Create ValidationRuns entry
   - Execute validation rules
   - Store ValidationResults

5. Implement provenance tracking
   - Create Provenance record for each derivation
   - Link parent derivations (lineage)
   - Track depth for cycle detection
   - Store to database

**Dependencies:**
- Wave-1B complete (database tables)
- RKP service complete
- validation_rules.json registry (Wave-2a)
- terraform_templates.json registry (Wave-2a)
- ValidationService (Wave-2d)

**Exit Criteria:**
- ✓ KBS service compiles
- ✓ Derivation rules execute
- ✓ Topic names generated correctly
- ✓ Provenance records created
- ✓ Validation coordination working

---

### Validation Service

**Frozen in:** STEP-8, STEP-11

**Purpose:** Apply validation rules; store results

**Input:**
- Derived values from KBS
- Validation rules from validation_rules.json registry
- Draft context

**Output:**
- ValidationResults entries stored in database
- Validation status (PASSED/FAILED)

**Implementation Tasks:**
1. Create ValidationService class
   - Method: `run_validation(run_id: uuid) → List[ValidationResult]`
   - Method: `apply_rule(rule: str, value: str) → ValidationResult`
   - Method: `check_duplicate_topic(topic: str) → bool`
   - Method: `check_naming_convention(name: str) → bool`
   - Method: `store_results(results: List) → None`

2. Implement rule application
   - Load validation_rules.json
   - For each rule, apply to derived value
   - Check naming conventions
   - Check for duplicates across drafts
   - Check for conflicts with existing Terraform

3. Implement result storage
   - Create ValidationResults entries
   - Set status (PASSED or FAILED with message)
   - Link to ValidationRun
   - Update ValidationRun.status

**Dependencies:**
- ValidationRuns table (Wave-1B)
- ValidationResults table (Wave-1B)
- KBS service
- validation_rules.json registry

**Exit Criteria:**
- ✓ ValidationService compiles
- ✓ Rules execute
- ✓ Results stored to database
- ✓ Duplicate detection working

---

### Provenance Service

**Frozen in:** STEP-9, STEP-9.1

**Purpose:** Track all derivations; create lineage records

**Input:**
- Derivation rule name
- Input facts
- Output value

**Output:**
- Provenance entries stored in database

**Implementation Tasks:**
1. Create ProvenanceService class
   - Method: `track_derivation(rule: str, inputs: List, output: str, parent_id: uuid = None) → uuid`
   - Method: `get_derivation_chain(provenance_id: uuid) → List[Provenance]`
   - Method: `check_cycle(provenance_id: uuid) → bool`

2. Implement lineage tracking
   - Create Provenance entry for each derivation
   - Link parent derivations (provenance.parent_id)
   - Track depth to prevent cycles
   - Store all inputs in input_facts_json

3. Implement chain retrieval
   - Walk provenance.parent_id chain
   - Reconstruct full derivation history
   - Return ordered list (root → leaf)

**Dependencies:**
- Provenance table (Wave-1B)
- KBS service

**Exit Criteria:**
- ✓ ProvenanceService compiles
- ✓ Derivation tracking working
- ✓ Chain retrieval working
- ✓ Cycle detection working

---

### Registry Definitions (4 JSON files)

**Frozen in:** STEP-9.1, STEP-11.4

**Location:** `knowledge/` directory (frozen artifact)

**Files:**

1. **validation_rules.json**
   ```
   {
     "registry_version": "1.0.0",
     "version": "2026-01-01",
     "created_at": "2026-01-01T00:00:00Z",
     "released_by": "Architecture Board",
     "approval_metadata": {"status": "APPROVED", "approvers": ["..."]},
     "entries": [
       {
         "rule_id": "naming_convention",
         "rule_type": "NAMING",
         "pattern": "^mif_[a-z]{3,}_[a-z]{3,}$",
         "description": "Topics must follow mif_XXX_YYY pattern"
       },
       {
         "rule_id": "duplicate_check",
         "rule_type": "DUPLICATE",
         "scope": "GLOBAL",
         "description": "Topic name must be unique across all drafts"
       },
       ...more rules from STEP-11.4
     ]
   }
   ```

2. **terraform_templates.json**
   - Contains: Template definitions for new sources (folder structure, locals.tf, main.tf)
   - Key entries: topic_template, job_template
   - From: STEP-5.1 frozen business rules

3. **repo_patterns.json**
   - Contains: Directory patterns for source system detection
   - Key entries: Pattern → source_system mapping
   - Example: "saptcc/" → "SAP TCC", "saptce/" → "SAP TCE"

4. **source_systems.json**
   - Contains: Source system definitions
   - Key fields: system_id, system_name, connection_details_template, supported_entities
   - From: STEP-5.1, STEP-8 frozen specifications

**Implementation Tasks:**
1. Create `knowledge/validation_rules.json` with all frozen rules
2. Create `knowledge/terraform_templates.json` with all frozen templates
3. Create `knowledge/repo_patterns.json` with all frozen patterns
4. Create `knowledge/source_systems.json` with all frozen definitions
5. Validate all JSON against schema
6. Add registry_version tracking (for future updates)

**Exit Criteria:**
- ✓ All 4 registries exist in repository
- ✓ All JSON valid
- ✓ All schemas match frozen requirements
- ✓ CI gate validates registry schema

---

## Knowledge Layer Sequence

1. Create 4 registry JSON files (Wave-2a)
2. Implement RKP service (Wave-2b)
3. Implement KBS service (Wave-2c)
4. Implement ValidationService (Wave-2d)
5. Implement ProvenanceService (Wave-2e)
6. End-to-end test: RKP → KBS → Validation → Provenance

---

# SECTION-6 — LANGGRAPH EXECUTION PLAN

## All 18 Core Nodes

---

### Node Inventory (Exact Order)

**Group-1: Authentication & Session (Early dependencies)**

1. **GitHubOAuthNode**
   - Frozen in: STEP-5, STEP-2
   - Purpose: GitHub OAuth flow
   - Inputs: {code, state}
   - Outputs: {user_id, session_id, access_token}
   - Dependencies: GitHubOAuthService, UserRepository, SessionRepository
   - Tables: users (read/write), sessions (write)
   - Existing Code: `backend/services/github_oauth.py`, `backend/api/auth.py`
   - Status: PARTIAL (endpoint exists; node wrapper needed)

2. **SessionNode**
   - Frozen in: STEP-5, STEP-2
   - Purpose: Load and validate session
   - Inputs: {session_id}
   - Outputs: {user, session, is_valid}
   - Dependencies: SessionRepository, SessionService
   - Tables: sessions (read), users (read)
   - Existing Code: `backend/services/session.py`
   - Status: PARTIAL (service exists; node wrapper needed)

**Group-2: Context & Environment Detection**

3. **EnvironmentNode**
   - Frozen in: STEP-5
   - Purpose: Detect repository environment
   - Inputs: {repository_path}
   - Outputs: {environment: {dev, test, prod}}
   - Dependencies: Repository file system
   - Tables: None
   - Status: MISSING (implementation needed)

4. **OperationNode**
   - Frozen in: STEP-5
   - Purpose: Route to appropriate handler based on user input
   - Inputs: {message, context}
   - Outputs: {operation_type, router_result}
   - Dependencies: Message parser
   - Tables: None
   - Status: MISSING (implementation needed)

**Group-3: Repository Analysis**

5. **RepositoryNavigatorNode**
   - Frozen in: STEP-5
   - Purpose: Browse repository structure
   - Inputs: {path, depth}
   - Outputs: {tree, files}
   - Dependencies: RKP (repository scanning)
   - Tables: repository_versions (read), repository_facts (read)
   - DTO Output: RepositoryTreeDTO
   - Status: MISSING (implementation needed)

6. **SourceTypeNode**
   - Frozen in: STEP-5
   - Purpose: Classify source system
   - Inputs: {repository_path, facts}
   - Outputs: {source_type, classification_score}
   - Dependencies: source_systems.json registry, RKP
   - Tables: repository_facts (read)
   - Status: MISSING (implementation needed)

7. **KafkaNode**
   - Frozen in: STEP-5
   - Purpose: Detect Kafka configuration
   - Inputs: {source_type, repository_path}
   - Outputs: {kafka_config: {brokers, topics, partitions}}
   - Dependencies: TF parsing, RKP
   - Tables: repository_facts (read)
   - Status: MISSING (implementation needed)

**Group-4: Validation & Derivation**

8. **TopicValidationNode**
   - Frozen in: STEP-5
   - Purpose: Validate topic name
   - Inputs: {topic_name, draft_context}
   - Outputs: {is_valid, validation_errors}
   - Dependencies: ValidationService, validation_rules.json
   - Tables: validation_rules (implicit via ValidationService)
   - Status: MISSING (implementation needed)

9. **DuplicateJobValidationNode**
   - Frozen in: STEP-5, STEP-5.1
   - Purpose: Check for duplicate topics
   - Inputs: {topic_name}
   - Outputs: {is_duplicate, existing_draft_id}
   - Dependencies: DraftRepository, ValidationService
   - Tables: drafts (read)
   - Status: MISSING (implementation needed)

10. **KnowledgeDerivationNode**
    - Frozen in: STEP-5, STEP-8
    - Purpose: Derive topic/job name via KBS
    - Inputs: {source_system, entity_type, existing: bool}
    - Outputs: {derived_topic_name, derived_job_name, confidence}
    - Dependencies: KBS, terraform_templates.json
    - Tables: derived_values (read/write), repository_facts (read)
    - DTO Output: DerivedValueDTO
    - Status: MISSING (implementation needed)

**Group-5: Draft & Snapshot Management**

11. **DraftWorkspaceNode**
    - Frozen in: STEP-5, STEP-5.1
    - Purpose: Create draft workspace
    - Inputs: {user_id, session_id, draft_changes}
    - Outputs: {draft_id, draft_status, change_stack}
    - Dependencies: DraftRepository, DraftChangeRepository
    - Tables: drafts (write), draft_changes (write), draft_files (write)
    - DTO Output: DraftWorkspaceDTO
    - Business Rule: Change stack LIFO (from STEP-5.1)
    - Status: MISSING (implementation needed)

12. **SnapshotNode** (implicit in DraftWorkspaceNode)
    - Frozen in: STEP-5, STEP-9
    - Purpose: Create snapshot of draft state
    - Inputs: {draft_id, draft_state}
    - Outputs: {snapshot_id, snapshot_index}
    - Dependencies: SnapshotRepository
    - Tables: snapshots (write)
    - Status: MISSING (implementation needed)

**Group-6: Review & PR**

13. **ReviewWorkspaceNode**
    - Frozen in: STEP-5, STEP-5.1
    - Purpose: Create review workspace
    - Inputs: {draft_id, reviewer_id}
    - Outputs: {review_id, review_status}
    - Dependencies: ReviewRepository
    - Tables: reviews (write), review_comments (write)
    - DTO Output: ReviewDTO
    - Status: MISSING (implementation needed)

14. **TerraformValidationNode**
    - Frozen in: STEP-5
    - Purpose: Validate Terraform syntax
    - Inputs: {terraform_files, draft_context}
    - Outputs: {is_valid, syntax_errors, plan_output}
    - Dependencies: Terraform CLI or parser
    - Tables: None (external tool)
    - Status: MISSING (implementation needed)

15. **PRCreationNode**
    - Frozen in: STEP-5, STEP-5.1
    - Purpose: Create GitHub PR
    - Inputs: {draft_id, branch_name, commit_message}
    - Outputs: {pr_id, pr_url, pr_number}
    - Dependencies: GitHub API client, PRRepository
    - Tables: pr_metadata (write)
    - DTO Output: PRDTO
    - Business Rule: One draft = one PR (from STEP-5.1)
    - Status: MISSING (implementation needed)

**Group-7: Exception & Finalization**

16. **ConflictResolutionNode**
    - Frozen in: STEP-5
    - Purpose: Handle conflicts (e.g., duplicate PR)
    - Inputs: {conflict_type, conflict_context}
    - Outputs: {resolution_action, resolution_status}
    - Dependencies: DraftRepository, PRRepository
    - Tables: drafts (read), pr_metadata (read)
    - Status: MISSING (implementation needed)

17. **OutOfScopeQuestionNode**
    - Frozen in: STEP-5, STEP-5.1
    - Purpose: Handle out-of-scope questions
    - Inputs: {message}
    - Outputs: {response, out_of_scope_reason}
    - Dependencies: LLM or predefined responses
    - Tables: None
    - Status: PARTIAL (empty directory exists)

18. **SessionPersistNode**
    - Frozen in: STEP-5, STEP-9
    - Purpose: Final session state persistence
    - Inputs: {session_id, final_state}
    - Outputs: {persistence_status}
    - Dependencies: SessionRepository, NodeExecutionLogRepository
    - Tables: sessions (write), node_execution_logs (write)
    - Status: MISSING (implementation needed)

---

## Node Implementation Sequence

**Phase-1 (OAuth & Session — already partially done):**
1. GitHubOAuthNode (wrap existing service)
2. SessionNode (wrap existing service)

**Phase-2 (Context & Environment):**
3. EnvironmentNode
4. OperationNode

**Phase-3 (Repository Analysis — depends on RKP):**
5. RepositoryNavigatorNode
6. SourceTypeNode
7. KafkaNode

**Phase-4 (Validation — depends on ValidationService):**
8. TopicValidationNode
9. DuplicateJobValidationNode
10. KnowledgeDerivationNode

**Phase-5 (Draft & Snapshot):**
11. DraftWorkspaceNode
12. SnapshotNode (or implicit in DraftWorkspaceNode)

**Phase-6 (Review & PR):**
13. ReviewWorkspaceNode
14. TerraformValidationNode
15. PRCreationNode

**Phase-7 (Exception & Finalization):**
16. ConflictResolutionNode
17. OutOfScopeQuestionNode
18. SessionPersistNode

---

## State Model Definition

**Frozen in:** STEP-9, STEP-9.1

**Classes needed:**

1. **SessionState**
   - Fields: session_id, user_id, user_role, created_at, last_activity
   - Purpose: User session context

2. **DraftState**
   - Fields: draft_id, status, changes[], current_change_index, draft_files[]
   - Purpose: Draft workspace state

3. **ValidationState**
   - Fields: validation_run_id, rules_applied[], results[]
   - Purpose: Validation execution state

4. **ReviewState**
   - Fields: review_id, reviewer_id, comments[], approval_status
   - Purpose: Review workspace state

5. **PRState**
   - Fields: pr_id, github_pr_number, status, created_at
   - Purpose: PR creation state

6. **SnapshotState**
   - Fields: snapshot_id, snapshot_index, state_json
   - Purpose: State checkpoint for recovery

7. **ProvenanceState**
   - Fields: provenance_id[], derivation_chain
   - Purpose: Derivation tracking

---

## Routing Logic

**State Accumulation Pattern:**
```
Input Message
    ↓
GitHubOAuthNode (if new user)
    ↓
SessionNode (load or create session)
    ↓
EnvironmentNode (detect context)
    ↓
OperationNode (route based on message)
    ↓
[Repository Analysis] (if browsing)
  - RepositoryNavigatorNode
  - SourceTypeNode
  - KafkaNode
    ↓
[Derivation] (if creating new topic)
  - TopicValidationNode
  - DuplicateJobValidationNode
  - KnowledgeDerivationNode
    ↓
[Draft Creation]
  - DraftWorkspaceNode
  - SnapshotNode
    ↓
[Review & PR]
  - ReviewWorkspaceNode
  - TerraformValidationNode
  - PRCreationNode
    ↓
[Exception Handling]
  - ConflictResolutionNode (if errors)
  - OutOfScopeQuestionNode (if OOS)
    ↓
SessionPersistNode (final state save)
    ↓
Output DTO to API response
```

---

## Checkpoint & Recovery

**Checkpoints:**
- After SessionNode: Save session + user context
- After EnvironmentNode: Save environment detection
- After DraftWorkspaceNode: Save draft creation
- After ReviewWorkspaceNode: Save review creation
- After PRCreationNode: Save PR creation

**Recovery:**
- Load latest checkpoint
- Resume from next node
- Reconstruct partial state from database
- Return NavigatorRecoveryDTO if resuming navigation

---

# SECTION-7 — API EXECUTION PLAN

## Endpoint Implementation Sequence

---

### Primary Endpoint (Priority-1)

**POST /agent/message**

- Frozen in: STEP-6, STEP-7.1
- Purpose: Primary conversational interface
- Request Body:
  ```json
  {
    "session_id": "uuid",
    "message": "user message",
    "ui_action": "browse|derive|create|review|approve",
    "context": {optional object}
  }
  ```
- Response: LangGraph execution result (various DTOs)
  ```json
  {
    "execution_id": "uuid",
    "result_type": "REPOSITORY_TREE|DRAFT_CREATED|VALIDATION_PASSED|REVIEW_READY|PR_CREATED",
    "result": {...DTO}
  }
  ```
- Implementation Tasks:
  1. Create `/agent/message` endpoint handler
  2. Validate session_id (load from SessionRepository)
  3. Create LangGraph execution context
  4. Invoke LangGraph with message
  5. Collect node execution logs to node_execution_logs table
  6. Return appropriate DTO based on execution result

---

### Draft Management Endpoints (Priority-2)

**GET /api/v1/drafts**
- Load all user's drafts
- Output: DraftWorkspaceDTO[]

**POST /api/v1/drafts**
- Create new draft
- Input: {topic_name, source_system}
- Output: DraftWorkspaceDTO

**GET /api/v1/drafts/{draft_id}**
- Retrieve draft details
- Output: DraftWorkspaceDTO

**PUT /api/v1/drafts/{draft_id}**
- Update draft (add/remove changes)
- Input: {change} or {discard_change_index}
- Output: DraftWorkspaceDTO

**DELETE /api/v1/drafts/{draft_id}**
- Delete draft
- Output: {status: "deleted"}

---

### Validation Endpoints (Priority-2)

**POST /api/v1/drafts/{draft_id}/validate**
- Run validation on draft
- Output: ValidationDTO

**GET /api/v1/validations/{run_id}**
- Get validation results
- Output: ValidationDTO

---

### Review Endpoints (Priority-3)

**POST /api/v1/reviews**
- Create review for draft
- Input: {draft_id, reviewer_id}
- Output: ReviewDTO

**GET /api/v1/reviews/{review_id}**
- Get review details
- Output: ReviewDTO

**POST /api/v1/reviews/{review_id}/comments**
- Add comment to review
- Input: {content}
- Output: ReviewDTO (with new comment)

**POST /api/v1/reviews/{review_id}/approve**
- Approve review
- Input: {approval_status: APPROVED|REJECTED}
- Output: ReviewApprovalDTO

---

### PR Endpoints (Priority-3)

**POST /api/v1/prs**
- Create GitHub PR
- Input: {draft_id}
- Output: PRDTO

**GET /api/v1/prs/{pr_id}**
- Get PR status
- Output: PRDTO

---

### Navigator Endpoints (Priority-4)

**GET /api/v1/repo/tree**
- Get repository tree
- Query: {path, depth}
- Output: RepositoryTreeDTO

**GET /api/v1/repo/file/{path}**
- Get file contents
- Output: {content, encoding}

---

### Audit Endpoints (Priority-4)

**GET /api/v1/audit/events**
- Query audit events
- Query: {start_date, end_date, user_id, event_type}
- Output: AuditEventDTO[]

**POST /api/v1/audit/export**
- Export audit log
- Input: {format: JSON|CSV, time_range}
- Output: File download

---

### Session Recovery Endpoint (Priority-5)

**GET /api/v1/sessions/{session_id}/recovery**
- Recover session state
- Output: NavigatorRecoveryDTO

---

## DTO Implementation Sequence

**Phase-1 (Required for Phase-1 endpoints):**
1. DraftWorkspaceDTO
2. ValidationDTO
3. ValidationSummaryDTO
4. ReviewDTO
5. ReviewApprovalDTO
6. PRDTO
7. RepositoryTreeDTO
8. FileImpactDTO

**Phase-2 (Additional):**
9. DuplicatePRDTO
10. NavigatorRecoveryDTO
11. TemplateRegistryDTO
12. DerivedValueDTO
13. AuditEventDTO

---

# SECTION-8 — FRONTEND EXECUTION PLAN

## Redux Store Implementation

**Store Structure:**
```
redux/
├── slices/
│   ├── authSlice.ts
│   ├── sessionSlice.ts
│   ├── draftSlice.ts
│   ├── reviewSlice.ts
│   ├── validationSlice.ts
│   └── uiSlice.ts
├── selectors/
│   └── ...
├── thunks/
│   ├── authThunks.ts
│   ├── draftThunks.ts
│   └── ...
└── store.ts
```

**Implementation Order:**
1. authSlice (login, logout, user context)
2. sessionSlice (current session, active_draft_id)
3. draftSlice (draft state, changes, files)
4. reviewSlice (review comments, approvals)
5. validationSlice (validation results)
6. uiSlice (modals, notifications, sidebars)

---

## Pages Implementation

**Order (by dependency):**
1. Login page (OAuth flow)
2. Dashboard page (main interface, message input)
3. Session page (current session display)
4. Draft page (draft editor with change history)
5. Review page (review interface, comments)
6. Navigator page (repo browser)
7. PR page (PR status display)
8. Audit page (event log)
9. Settings page (user preferences)

---

## Components Implementation

**Groups:**
1. **Common Components** (used by multiple pages)
   - MessageChat
   - Sidebar
   - Header
   - Navigation
   - Loading spinner
   - Error boundary

2. **Draft Components**
   - DraftEditor
   - ChangeHistory
   - ChangeStack (LIFO display)
   - FileImpactView

3. **Review Components**
   - ReviewComments
   - ApprovalControls
   - CommentForm

4. **Navigator Components**
   - FileTree
   - FileBrowser
   - CodeViewer

5. **Shared Components**
   - Modal
   - Button
   - Input
   - Form
   - Badge
   - Table

---

# SECTION-9 — SECURITY EXECUTION PLAN

## RBAC Enforcement (Priority-1)

**Authorization Middleware:**
1. Create `backend/middleware/auth.py`
   - FastAPI dependency for role extraction
   - Permission matrix definition
   - Endpoint protection decorator

2. Endpoint Protection:
   - Add `@authorize(required_role="CONTRIBUTOR")` decorator
   - Define permission matrix per endpoint
   - Roles: ADMIN, CONTRIBUTOR, REVIEWER, READ_ONLY

3. RBAC Test Matrix:
   - Test each role against each protected endpoint
   - Test role transitions (CONTRIBUTOR → REVIEWER)
   - Test permission denials

---

## Vault Integration (Priority-2)

**Secrets Management:**
1. Create Vault client
2. Load secrets (GitHub OAuth token, DB password)
3. Implement secret rotation (background job)
4. Update configuration to use Vault

---

## Audit Logging (Priority-2)

**Audit Trails:**
1. Log all mutations (drafts, reviews, PRs)
2. Log all role changes
3. Log all secret access
4. Store to audit_events table

---

# SECTION-10 — CI/CD EXECUTION PLAN

## GitHub Actions Workflow

**File:** `.github/workflows/ci.yml`

**Gates (in order):**

1. **Lint**
   - Backend: Black, Pylint
   - Frontend: ESLint, Prettier
   - Status: BLOCKING

2. **Type Check**
   - Backend: mypy
   - Frontend: TypeScript compiler
   - Status: BLOCKING

3. **Unit Tests**
   - Backend: pytest
   - Frontend: Jest
   - Coverage requirement: >80%
   - Status: BLOCKING

4. **Integration Tests**
   - Database tests
   - API endpoint tests
   - Status: BLOCKING

5. **Security Scanning**
   - SAST: Bandit (Python), ESLint (JS)
   - Dependency scanning: Safety, Snyk
   - Secrets scanning: Truffelhog
   - Status: BLOCKING

6. **DTO Validation**
   - Verify all DTOs match frozen schema (STEP-6.1)
   - Status: BLOCKING

7. **Registry Validation**
   - Validate all JSON registries against schema
   - Status: BLOCKING

8. **Architecture Validation**
   - Verify directory structure
   - Verify layer separation
   - Status: BLOCKING

---

# SECTION-11 — PHASE-1 BUILD ORDER (MASTER SEQUENCE)

## Exact Implementation Sequence

This is the definitive order for Phase-1 implementation. Each item depends on all prior items.

---

### WEEK-1: FOUNDATION

**Task-1: Database Migration Infrastructure**
- Freeze: STEP-10, STEP-11
- Output: Alembic configured, migrations executable
- Repo Evidence: Create `backend/database/migrations/`

**Task-2: ORM Model Implementation (Wave-1a & 1b)**
- Freeze: STEP-10
- Tables: drafts, draft_changes, draft_files, snapshots, validation_runs, validation_results, reviews, review_comments, review_approvals, pr_metadata, repository_versions, repository_facts, derived_values, knowledge_registry_versions, provenance, audit_events, node_execution_logs
- Output: 17 ORM models + migrations

**Task-3: Repository Layer (Wave-1c)**
- Freeze: STEP-10
- Classes: DraftRepository, SnapshotRepository, ValidationRepository, ReviewRepository, PRRepository, AuditRepository, ProvenanceRepository, UserRepository (complete), SessionRepository (complete)
- Output: 9 repository classes

**Task-4: Database Integration Testing**
- Verify: All 19 tables created, migrations executable
- Output: Database layer ready for services

---

### WEEK-1-2: KNOWLEDGE LAYER

**Task-5: Registry Creation (Wave-2a)**
- Freeze: STEP-9.1, STEP-11.4
- Files: `knowledge/validation_rules.json`, `knowledge/terraform_templates.json`, `knowledge/repo_patterns.json`, `knowledge/source_systems.json`
- Output: 4 frozen registries

**Task-6: RKP Service (Wave-2b)**
- Freeze: STEP-8
- Class: RepositoryKnowledgeProvider
- Methods: scan_repository, extract_source_systems, parse_terraform_files, normalize_facts, store_facts
- Output: RKP service compiles, scans repository, stores facts

**Task-7: KBS Service (Wave-2c)**
- Freeze: STEP-8, STEP-5.1
- Class: KnowledgeBaseService
- Methods: derive_topic_name, derive_job_name, apply_derivation_rules, create_provenance, coordinate_validation
- Output: KBS applies rules, generates names, creates provenance

**Task-8: Validation Service (Wave-2d)**
- Freeze: STEP-8, STEP-11
- Class: ValidationService
- Methods: run_validation, apply_rule, check_duplicate_topic, store_results
- Output: Validation rules execute, results stored

**Task-9: Provenance Service (Wave-2e)**
- Freeze: STEP-9, STEP-9.1
- Class: ProvenanceService
- Methods: track_derivation, get_derivation_chain, check_cycle
- Output: Provenance tracking working

---

### WEEK-2-3: LANGGRAPH ORCHESTRATION

**Task-10: State Model Definition (Wave-3a)**
- Freeze: STEP-9, STEP-9.1
- Classes: SessionState, DraftState, ValidationState, ReviewState, PRState, SnapshotState, ProvenanceState
- Output: State classes typed and ready

**Task-11: Node Implementations (Wave-3b through 3g)**
- Phase-3a: GitHubOAuthNode, SessionNode (wrap existing)
- Phase-3b: EnvironmentNode, OperationNode
- Phase-3c: RepositoryNavigatorNode, SourceTypeNode, KafkaNode
- Phase-3d: TopicValidationNode, DuplicateJobValidationNode, KnowledgeDerivationNode
- Phase-3e: DraftWorkspaceNode, SnapshotNode
- Phase-3f: ReviewWorkspaceNode, TerraformValidationNode, PRCreationNode
- Phase-3g: ConflictResolutionNode, OutOfScopeQuestionNode, SessionPersistNode
- Freeze: STEP-5, STEP-5.1
- Output: All 18 nodes implemented, tested end-to-end

**Task-12: Routing & Recovery (Wave-3h & 3i)**
- Freeze: STEP-5.1, STEP-11
- Features: Node-to-node transitions, conditional branching, checkpointing, resume logic
- Output: LangGraph execution plan runs end-to-end

---

### WEEK-2-3: API LAYER (parallel with LangGraph)

**Task-13: DTO Implementation (Wave-4a)**
- Freeze: STEP-6.1, STEP-9.1
- DTOs: DraftWorkspaceDTO, ValidationDTO, ValidationSummaryDTO, ReviewDTO, ReviewApprovalDTO, PRDTO, DuplicatePRDTO, RepositoryTreeDTO, FileImpactDTO, NavigatorRecoveryDTO, TemplateRegistryDTO, DerivedValueDTO, AuditEventDTO
- Output: All 13 missing DTOs implemented

**Task-14: Primary Endpoint (Wave-4b)**
- Freeze: STEP-6
- Endpoint: `POST /agent/message`
- Handler: Load session → invoke LangGraph → return result DTO
- Output: Primary endpoint functional

**Task-15: Secondary Endpoints (Wave-4c through 4i)**
- Draft: GET/POST/PUT/DELETE /api/v1/drafts[/{id}]
- Validation: POST /validate, GET /validations/{id}
- Review: POST /reviews, GET /reviews/{id}, POST /comments, POST /approve
- PR: POST /prs, GET /prs/{id}
- Navigator: GET /repo/tree, GET /repo/file/{path}
- Audit: GET /audit/events, POST /audit/export
- Recovery: GET /sessions/{id}/recovery
- Freeze: STEP-6
- Output: All 9 endpoint groups functional

---

### WEEK-3-4: FRONTEND (blocked until Wave-4 complete)

**Task-16: Redux Store (Wave-5a)**
- Freeze: STEP-7
- Slices: auth, session, draft, review, validation, ui
- Output: Redux store functional

**Task-17: Pages Implementation (Wave-5b)**
- Freeze: STEP-7
- Pages: Login, Dashboard, Session, Draft, Review, Navigator, PR, Audit, Settings
- Output: All 9 pages render

**Task-18: Components Implementation (Wave-5c)**
- Freeze: STEP-7.1
- Components: MessageChat, DraftEditor, ReviewComments, FileTree, etc. (20+)
- Output: All components render

**Task-19: API Integration (Wave-5d)**
- Freeze: STEP-6
- Features: API client, SSE handler, Redux async middleware
- Output: Frontend calls API endpoints

**Task-20: Routing & Navigation (Wave-5e)**
- Features: React Router, page navigation, auth guards
- Output: Full navigation working end-to-end

---

### WEEK-1 PARALLEL: SECURITY (Wave-6)

**Task-21: RBAC Enforcement**
- Freeze: STEP-11.3
- Features: Authorization middleware, endpoint protection, role matrix
- Output: All endpoints protected by RBAC

**Task-22: Vault Integration**
- Freeze: STEP-11.3
- Features: Vault client, secret loading, rotation automation
- Output: Secrets managed by Vault

---

### WEEK-1 PARALLEL: CI/CD (Wave-7)

**Task-23: CI Pipeline Implementation**
- Freeze: STEP-11.3, STEP-11.4
- Gates: Lint, Type Check, Unit Tests, Integration Tests, Security Scanning, DTO Validation, Registry Validation, Architecture Validation
- Output: All gates blocking for production

---

### WEEK-4: INTEGRATION & TESTING

**Task-24: End-to-End Testing**
- Flow: OAuth → Session → Message → LangGraph → Draft → Review → PR
- Output: Full workflow tested

**Task-25: Performance Testing**
- Database query performance
- LangGraph execution time
- API response time
- Output: Performance baseline established

**Task-26: Security Testing**
- RBAC enforcement verified
- Secrets not in logs/errors
- Vault rotation tested
- Output: Security checklist passed

---

# SECTION-12 — IMPLEMENTATION AUTHORIZATION CHECK

## Questions & Answers

---

### Question-1: Can coding start immediately?

**Answer: NO**

**Reason:**
- Planning is only partially complete (this document)
- Architecture conflicts exist (STEP-11.3 vs. STEP-11.4 contradiction)
- Database schema not finalized (17 tables frozen but design details incomplete)
- Registry schemas frozen but machine-readable validation not yet coded
- CI/CD gates defined but not implemented

**Missing Before Coding:**
- ✗ Alembic migration framework configuration
- ✗ Test database setup
- ✗ Linting/type checking environment
- ✗ GitHub Actions secrets configured
- ✗ Vault access credentials
- ✗ GitHub OAuth integration testing

---

### Question-2: What planning gaps remain?

**Answer: The following items require clarification before coding:**

1. **Database Indexing Strategy**
   - Frozen: Table definitions
   - Missing: Index placement (performance optimization)
   - Resolution: DBA review of query patterns

2. **LangGraph State Accumulation**
   - Frozen: State model definition
   - Missing: Exact state transition rules per node
   - Resolution: Finalize state flow diagram

3. **API Error Handling**
   - Frozen: DTOs
   - Missing: Error response schema
   - Resolution: Define ErrorDTO

4. **Frontend State Persistence**
   - Frozen: Redux slices
   - Missing: Local storage strategy
   - Resolution: Define persistence layer

5. **CI/CD Secret Management**
   - Frozen: Vault integration
   - Missing: CI/CD job role definition
   - Resolution: Define GitHub Actions secrets

---

### Question-3: If YES, what is the exact first implementation task?

**(Question not applicable — answer to Question-1 is NO)**

---

### Question-4: What is the exact first implementation wave?

**Answer: WAVE-1 (Database Foundation)**

**Exact First Tasks (in order):**

1. **Task-1: Alembic Setup**
   - Create `backend/database/migrations/env.py`
   - Create `backend/database/migrations/script.py.mako`
   - Verify: `alembic revision --autogenerate -m "Initial schema"` works
   - Repo location: `backend/database/migrations/`
   - Dependency: PostgreSQL connection configured, SQLAlchemy models defined

2. **Task-2: Draft Table**
   - Create ORM model in `backend/models/__init__.py`
   - Run migration
   - Verify table created with correct schema
   - Dependency: Alembic setup complete

3. **Task-3: Draft Change Table**
   - Create ORM model
   - Run migration
   - Verify FK to drafts table
   - Dependency: Draft table exists

4. **Task-4: Draft Files Table**
   - Create ORM model
   - Run migration
   - Verify FK to drafts table
   - Dependency: Draft table exists

... (continue with remaining 14 tables in Wave-1 sequence)

---

# FINAL OUTPUT SECTION

---

# A. PHASE-1 COMPONENT INVENTORY

**Component Summary:**
- Total Frozen Components: ~154
- Currently Implemented: 14 (9%)
- Partially Implemented: 3
- Missing: 137 (91%)

**By Layer:**

| Layer | Complete | Partial | Missing | Total |
|-------|----------|---------|---------|-------|
| Auth | 3 | 0 | 3 | 6 |
| Database | 2 | 3 | 24 | 29 |
| Knowledge | 0 | 0 | 15 | 15 |
| LangGraph | 0 | 0 | 21 | 21 |
| API & DTOs | 5 | 0 | 21 | 26 |
| Frontend | 0 | 0 | 25+ | 25+ |
| Services | 2 | 0 | 9 | 11 |
| Security | 2 | 0 | 5 | 7 |
| CI/CD | 0 | 0 | 8 | 8 |
| Audit | 0 | 0 | 6 | 6 |
| **TOTAL** | **14** | **3** | **137+** | **154+** |

---

# B. DEPENDENCY GRAPH

```
┌─────────────────────────────────────────────┐
│ Wave-1: Database (1-2 weeks)                │
│ - 19 tables, Alembic, 9 repositories        │
│ CRITICAL PATH BLOCKER                       │
└─────────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────┐
│ Wave-2: Knowledge (2-3 weeks)               │
│ - RKP, KBS, 4 registries, validation        │
│ CRITICAL PATH BLOCKER                       │
└─────────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────┐
│ Wave-3: LangGraph (3-4 weeks)               │
│ - All 18 nodes, state model, routing        │
│ CRITICAL PATH BLOCKER                       │
└─────────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────┐
│ Wave-4: API (2-3 weeks)                     │
│ - 13 DTOs, primary + 9 secondary endpoints  │
│ CRITICAL PATH BLOCKER                       │
└─────────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────┐
│ Wave-5: Frontend (3-4 weeks)                │
│ - Redux, 9 pages, 20+ components            │
└─────────────────────────────────────────────┘
              ↓
         UNBLOCKS: Full UI

┌─────────────────────────────────────────────┐
│ Wave-6: Security (1-2 weeks) — PARALLEL    │
│ - RBAC, Vault, audit                        │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│ Wave-7: CI/CD (1-2 weeks) — PARALLEL       │
│ - All 8 gates                               │
└─────────────────────────────────────────────┘
```

---

# C. IMPLEMENTATION WAVES

**7 Sequential Waves:**

1. **Wave-1 (1-2 weeks): Database Foundation**
   - Entry: PostgreSQL configured, SQLAlchemy ready
   - Tasks: 17 ORM models + Alembic + 9 repositories
   - Exit: All 19 tables created, CRUD operations working
   - Unblocks: Knowledge, LangGraph, Services

2. **Wave-2 (2-3 weeks): Knowledge Layer**
   - Entry: Wave-1 complete, registries frozen
   - Tasks: RKP, KBS, 4 registries, validation, provenance
   - Exit: Full knowledge pipeline end-to-end
   - Unblocks: LangGraph derivation nodes

3. **Wave-3 (3-4 weeks): LangGraph Orchestration**
   - Entry: Wave-1, Wave-2 complete
   - Tasks: All 18 nodes, state model, routing, recovery
   - Exit: Full workflow orchestration working
   - Unblocks: API layer

4. **Wave-4 (2-3 weeks): API Layer**
   - Entry: Wave-3 complete
   - Tasks: 13 DTOs, 1 primary + 9 secondary endpoints
   - Exit: All endpoints callable, return correct DTOs
   - Unblocks: Frontend

5. **Wave-5 (3-4 weeks): Frontend**
   - Entry: Wave-4 complete
   - Tasks: Redux, 9 pages, 20+ components, API integration
   - Exit: Full UI functional end-to-end
   - Unblocks: User testing

6. **Wave-6 (1-2 weeks): Security & RBAC** (parallel after Wave-1)
   - Entry: Wave-1 complete
   - Tasks: Authorization, Vault, audit logging
   - Exit: All endpoints protected, secrets managed
   - Unblocks: Production deployment

7. **Wave-7 (1-2 weeks): CI/CD** (parallel after Wave-1)
   - Entry: Wave-1 complete
   - Tasks: All 8 gates (lint, test, security, validation, architecture)
   - Exit: All gates blocking, build gated
   - Unblocks: Safe deployment

**Total Duration:** 12-16 weeks (critical path)

---

# D. EXACT BUILD ORDER

**Master Sequence (all 26 tasks in order):**

**WEEK-1:**
- Task-1: Alembic migration setup
- Task-2: 17 ORM models + migrations (drafts, validation, reviews, pr, audit, provenance, registries, etc.)
- Task-3: Repository layer (9 classes)
- Task-4: Database integration testing
- Task-5: Registry creation (4 JSON files)
- Task-21: RBAC enforcement (parallel)
- Task-23: CI pipeline implementation (parallel)

**WEEK-1-2:**
- Task-6: RKP service
- Task-7: KBS service
- Task-8: Validation service
- Task-9: Provenance service
- Task-22: Vault integration (parallel)

**WEEK-2-3:**
- Task-10: State model definition
- Task-11: All 18 node implementations
- Task-12: Routing & recovery
- Task-13: 13 DTO implementations
- Task-14: Primary `/agent/message` endpoint
- Task-15: 9 secondary endpoint groups

**WEEK-3-4:**
- Task-16: Redux store (all 6 slices)
- Task-17: 9 pages
- Task-18: 20+ components
- Task-19: API client integration
- Task-20: React Router setup

**WEEK-4:**
- Task-24: End-to-end workflow testing
- Task-25: Performance testing
- Task-26: Security testing

---

# E. CRITICAL PATH

```
Database (2w) → Knowledge (3w) → LangGraph (4w) → API (3w) → Frontend (4w)
= 16 weeks on critical path
```

**Cannot be parallelized:**
- Database must exist before knowledge layer (persists RKP/KBS output)
- Knowledge layer must exist before LangGraph (derivation nodes depend on KBS)
- LangGraph must exist before API (primary endpoint orchestrates nodes)
- API must exist before frontend (UI calls endpoints)

**Can be parallelized:**
- Wave-6 (Security) after Wave-1
- Wave-7 (CI/CD) after Wave-1
- Frontend components can be stubbed in parallel with backend

---

# F. EARLIEST SAFE CODING STARTING POINT

**Answer: After planning document completion + stakeholder sign-off**

**Pre-Coding Checklist:**
- ✓ This blueprint complete (STEP-12.2)
- ✓ Database schema finalized (migration scripts approved)
- ✓ Registry schemas frozen in JSON (validation gates defined)
- ✓ LangGraph state model typed (no design changes)
- ✓ API contracts frozen (all DTOs final)
- ✓ CI/CD environment ready (GitHub Actions secrets configured)
- ✓ Vault access configured (for CI/CD jobs)
- ✓ Stakeholder sign-off (Planning Board approves build order)
- ✓ Architecture conflicts resolved (STEP-11.3 vs STEP-11.4 clarified)

**Exact First Coding Task:**
Task-1 (Alembic Migration Setup) in Week-1, Day-1

**Exact First File to Create:**
`backend/database/migrations/env.py` (Alembic configuration)

---

# G. FINAL VERDICT

## Implementation Authorization Decision

**STATUS: CONDITIONAL PROCEED**

**Verdict Logic:**

1. **Can Phase-1 coding begin?**
   - Answer: YES, after pre-coding checklist
   - Reason: Architecture frozen, frozen requirements clear, build order defined
   - Condition: Stakeholder sign-off required

2. **Is Phase-1 ready for implementation?**
   - Answer: YES
   - Reason: All 154 components inventoried, all dependencies mapped, all waves sequenced
   - Evidence: This blueprint document

3. **Are all blockers identified?**
   - Answer: YES
   - Critical Blockers:
     - Database layer (17 tables must exist before anything else works)
     - Knowledge layer (RKP/KBS must exist before LangGraph derivation nodes)
     - LangGraph orchestration (must exist before API endpoints)
     - Primary API endpoint (must exist before frontend integration)

4. **Is there any architecture conflict?**
   - Answer: YES — One Category-B contradiction exists
   - Conflict: STEP-11.3 (Enterprise Ready: NO) vs. STEP-11.4 (Implementation may begin immediately)
   - Resolution Status: DOCUMENTED but UNRESOLVED
   - Impact: Does not block Phase-1 coding; affects enterprise readiness gate

5. **What is the implementation score?**
   - Repository Score: 12% (bootstrap only)
   - Estimated completion: 8-12 weeks at current team size
   - Critical path: Wave-1 → Wave-2 → Wave-3 → Wave-4 → Wave-5 (16 weeks)

---

## FINAL CLASSIFICATION

**READY FOR STEP-12.3:** YES (pending stakeholder sign-off)

**BLUEPRINT GAPS EXIST:** NO (all components inventoried)

**FREEZE CONFLICT EXISTS:** YES (STEP-11.3 vs STEP-11.4 contradiction documented but not resolved)

---

**Blueprint Completed:** 2026-06-21

**Authority:** Implementation Planning Board

**Evidence Source:** Freeze documents (STEP-1 → STEP-11.4) + STEP-12.1 audit + repository reality

---

**NEXT STEP:** STEP-12.3 (Implementation Execution Approval)

Awaiting stakeholder sign-off to begin Wave-1 coding.
