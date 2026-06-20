# Architecture Specifications

## Frozen Architecture Reference

This project is governed by frozen architecture specifications from discovery, design, and planning phases.

### Frozen Steps (LOCKED)

- **Step-1**: Repository Discovery & Business Flow Analysis
- **Step-2**: Architecture Design & LangGraph Orchestration
- **Step-3**: Database Design & Verification
- **Step-4**: Project Structure & Folder Responsibilities
- **Step-5**: API Contract Specifications
- **Step-6**: Frontend Architecture & UX Design
- **Step-7**: Implementation Roadmap & Build Order
- **Step-8**: Repository Bootstrap & Project Skeleton

### Key Architectural Decisions (Frozen)

#### Orchestration
- **LangGraph-first**: All workflows routed through LangGraph nodes
- **Single API endpoint**: `POST /agent/message` for primary user interactions
- **Chat-first UX**: Conversational interface with structured forms

#### Backend
- **Framework**: FastAPI (async)
- **Agent**: LangGraph (embedded in FastAPI app)
- **Database**: PostgreSQL (source of truth)
- **Cache**: Redis (session state, ephemeral context)
- **Auth**: GitHub OAuth

#### Frontend
- **Framework**: React + Vite + TypeScript
- **State**: Redux Toolkit (global) + React hooks (local)
- **Routes**: Login, Dashboard, Session, Draft, Review, Navigator, Settings
- **Realtime**: Server-Sent Events (SSE) for validation/PR progress

#### Database
- **Core tables**: users, sessions, drafts, draft_glue_jobs, draft_files, draft_changes, snapshots, pr_metadata
- **Strategy**: Change stack (draft_changes) as source-of-truth; materialized views (draft_files) for reads
- **Relationships**: 1:N cascading relationships with FK constraints

#### API
- **Primary contract**: POST /agent/message (session_id, message, ui_action, context)
- **Response**: Standard wrapper with data, state_snapshot, actions[], next_actions
- **Error**: Standardized error format with code, message, details, trace_id
- **Read endpoints**: Minimal (KB summary, repo sources, file preview)

#### Folder Responsibilities (Frozen)
- `backend/models/` = ORM entities ONLY (no DTOs)
- `backend/schemas/` = Pydantic DTOs ONLY (no ORM)
- `backend/graph/nodes/` = Individual node implementations
- `backend/services/` = Domain services (no direct DB access)
- `backend/repositories/` = DB access layer ONLY
- `frontend/src/pages/` = Route-level page components
- `frontend/src/store/` = Redux slices (auth, session, draft, ui)
- `frontend/tests/` = All test files (NOT frontend/src/tests/)

### Future Connector Support (Extensible)

- **Kafka**: Primary Phase-1 connector (implemented)
- **JDBC**: Placeholder node; implement Phase-2
- **Flat File**: Placeholder node; implement Phase-2
- **API**: Placeholder node; implement Phase-2

### Nodes (LangGraph - 20 total)

**Frozen core nodes (Phase-1):**
1. GitHubOAuthNode
2. SessionNode
3. EnvironmentNode
4. OperationNode
5. RepositoryNavigatorNode
6. SourceTypeNode
7. KafkaNode
8. TopicValidationNode
9. DuplicateJobValidationNode
10. KnowledgeDerivationNode
11. DraftWorkspaceNode
12. ReviewWorkspaceNode
13. TerraformValidationNode
14. PRCreationNode
15. ConflictResolutionNode
16. OutOfScopeQuestionNode

**Placeholder nodes (Phase-2+):**
17. JdbcNode
18. FlatFileNode
19. ApiNode
20. (Future expansion nodes)

### Critical Business Rules (Frozen)

- **One Draft = One Commit = One PR** (enforced in PRCreationNode)
- **Draft lifecycle**: DRAFT_EDITING → REVIEW_READY → PR_CREATING → PR_CREATED
- **Lock rule**: Draft locked only during PR_CREATING; editing allowed until then
- **Change stack**: Supports discard-last-change via LIFO pop; append-only audit trail
- **Topic validation**: Static TF file checks only (confluent_minerva_dev/topics_*.tf)
- **Duplicate detection**: Check locals.tf glue_jobs map for duplicate job keys
- **Session restore**: Load session + latest draft snapshot; resume from last state

### Deployment Notes

- No microservices in Phase-1; single FastAPI backend
- No external Terraform worker; Phase-1 validates (init/fmt/validate) in-process
- No live Kafka/Schema Registry APIs; static TF file validation only
- GitHub OAuth credentials and Terraform sandbox credentials required for deployment (not architecture blockers)

## Implementation Roadmap

See Step-7 for detailed phases and task breakdown.

## Questions or Clarifications

All architectural decisions are frozen and locked. Any questions about architecture should reference the corresponding frozen step document.

For implementation details, see the relevant phase documentation.
