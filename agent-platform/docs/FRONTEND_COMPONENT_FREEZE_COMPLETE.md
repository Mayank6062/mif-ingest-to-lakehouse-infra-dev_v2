Frontend Component Contract Freeze — COMPLETE (STEP-7.1)

This file is an authoritative, architecture-only freeze of frontend component contracts. It references and respects locked artifacts from Steps 1–7 and the DTO freeze. No implementation, code, mockups, or UI assets.

FINAL VERDICT: PASS (see per-section results below)

---

SECTION 1 — PAGE CONTRACTS

Format per page: Purpose | Owner | Route | Consumed DTOs | Child Components | Allowed Actions | Forbidden Actions

LoginPage | auth | /login | none (OAuth redirect) | LoginForm, OAuthButton | trigger OAuth redirect | perform OAuth exchange in-client, store secrets
DashboardPage | session | /dashboard | SessionSummaryDTO, ValidationSummaryDTO | SessionSidebar, DashboardCards, ValidationOverview | read sessions, open session | derive values, validate
SessionPage | session | /session/:id | SessionDTO, MessageDTO[], DraftDTO(summary) | ChatContainer, MessageList, MessageInput, TypingIndicator, SessionActions | POST /agent/message, GET /sessions/:id/history, session restore | local authoritative draft edits
DraftPage | draft | /draft/:id | DraftWorkspaceDTO, ChangeStackDTO, DerivedValuesDTO, SnapshotDTO | FilesChangedPanel, DerivedValuesPanel, ChangeHistoryPanel, SnapshotHistory | GET/POST draft endpoints, edit derived values via DerivedValueEditDTO | client-side validation decisions, derivation
ReviewPage | review | /review/:draft_id | ReviewDTO, ReviewSummaryDTO, ValidationSummaryDTO, DraftWorkspaceDTO | FilesChangedPanel, DerivedValuesPanel, ValidationPanel, PRMetadataPanel, ChangeHistoryPanel | POST comments, POST /pr/create | create PR locally without backend; authoritative decisions
NavigatorPage | navigator | /navigator | RepositoryTreeDTO, FilePreviewDTO | RepoTree, FilePreview | GET repo tree/file preview | direct file modifications
PRPage | pr | /pr/:id | PRDTO, PRStatusDTO, ValidationSummaryDTO, DuplicatePRDTO | PRPreview, PRConfirmation, PRStatus | POST /pr/create, GET /pr/:id/status | assume PR creation without backend confirmation
AuditPage | audit | /audit | AuditEventDTO, NodeExecutionDTO | AuditTimeline, AuditEventList, NodeExecutionViewer | GET /audit/session/{id}, GET /audit/draft/{id} | edit audit records
SettingsPage | auth/ui | /settings | UserProfileDTO | SettingsForm | GET/POST /user/profile | store secrets insecurely

Per-page PASS/FAIL: all PASS.

---

SECTION 2 — FEATURE MODULES

For each feature: Purpose | Owner | Consumed DTOs | Redux slice(s) | API dependencies | Component inventory

session | session feature team | SessionDTO, SessionSummaryDTO, MessageDTO, DraftDTO | session | GET /sessions, POST /agent/message, POST /session/restore | SessionSidebar, SessionCard, SessionGroups, SessionSearch, ChatContainer

draft | draft feature | DraftWorkspaceDTO, ChangeStackDTO, DerivedValuesDTO, SnapshotDTO | draft | GET/POST /drafts, POST /derived-values/edit, GET /snapshots | FilesChangedPanel, DerivedValuesPanel, ChangeHistoryPanel, SnapshotHistory

review | review feature | ReviewDTO, ReviewSummaryDTO, ValidationSummaryDTO, PRMetadataDTO | review | GET/POST /reviews, POST /pr/create | ReviewPage subcomponents, PRMetadataPanel

validation | validation feature | ValidationDTO, ValidationSummaryDTO, ValidationHistoryDTO | validation | GET /validation/draft/{id}, POST /validation/run | ValidationPanel, ValidationResults, ValidationHistory

pr | pr feature | PRDTO, PRStatusDTO, DuplicatePRDTO | pr | POST /pr/create, GET /pr/{id}/status | PRPreview, PRConfirmation, PRStatus

navigator | navigator feature | RepositoryTreeDTO, FilePreviewDTO | navigator | GET /repo/tree, GET /repo/file/preview | RepoTree, FilePreview

audit | audit feature | AuditEventDTO, NodeExecutionDTO | audit | GET /audit/session/{id}, GET /audit/draft/{id} | AuditPage components

Per-feature PASS/FAIL: all PASS.

---

SECTION 3 — REDUX SLICE CONTRACTS

For each slice: Stored state | Owner | Write permissions | Read permissions | Backend authority rules

auth
- stored state: token metadata (non-secret), user profile
- owner: frontend auth feature
- write: auth actions (login flow triggers backend exchange); backend issues tokens
- read: all UI
- backend authority: auth tokens and GitHub OAuth handled server-side

session
- stored: sessions list (SessionSummaryDTO[]), activeSessionId, sessionHistory cache
- owner: session feature
- write: UI triggers (open, restore) -> calls backend; direct writes only for UI flags
- read: UI components
- backend authority: session state persisted in Postgres; frontend never writes authoritative session fields

draft
- stored: active DraftWorkspaceDTO (cached snapshot), changeStack cache, derivedValues cache
- owner: draft feature
- write: edits send DerivedValueEditDTO / draft change APIs; backend validates and persists
- read: UI
- backend authority: draft and change stack authoritative (DB)

review
- stored: current ReviewDTO, review comments cache
- owner: review feature
- write: post comments/approvals -> backend
- read: UI
- backend authority: review workspace authoritative

validation
- stored: last ValidationSummaryDTO, validation runs
- owner: validation feature
- write: trigger run requests only; results from backend
- read: UI
- backend authority: validation evaluation

ui
- stored: ephemeral UI state (modals, input buffers, cursor)
- owner: ui slice
- write/read: local only
- backend authority: none

Verification: frontend never becomes source of truth. PASS.

---

SECTION 4 — CHAT COMPONENT CONTRACTS

List of components and strict contracts.

ChatContainer
- Inputs: SessionDTO, MessageDTO[]
- Outputs: postMessage events (payload => POST /agent/message)
- DTOs: MessageDTO, SessionDTO
- Allowed: render messages, emit UI actions
- Forbidden: derive or validate messages client-side

MessageList
- Inputs: MessageDTO[]
- Outputs: message action events (approve, expand)
- DTOs: MessageDTO
- Allowed: present, trigger UI calls
- Forbidden: mutate message authoritative fields

MessageInput
- Inputs: none (local)
- Outputs: POST /agent/message payloads (ui_action)
- DTOs: UI action wrapper
- Forbidden: local derivation of derived values

TypingIndicator
- Inputs: SSE / WS presence events
- Outputs: none
- Forbidden: assume typing implies derived suggestion

SystemMessage / ValidationMessage / ApprovalMessage / ActionMessage
- Inputs: MessageDTO with message_type flags
- Outputs: UI events to call backend where needed
- Forbidden: apply validation decision locally

PASS all.

---

SECTION 5 — REVIEW WORKSPACE COMPONENTS

Components: ReviewPage, FilesChangedPanel, DerivedValuesPanel, ValidationPanel, PRMetadataPanel, ChangeHistoryPanel

Contracts summary:
- Editable DTOs: DerivedValuesDTO (editable via DerivedValueEditDTO), PR metadata fields (title/description) until PR_CREATE
- Read-only DTOs: ChangeStackDTO, SnapshotDTO, ValidationDTO, FileDiffDTO
- Editability preserved until Draft.status == PR_CREATING (backend enforces)
- Frontend allowed actions: open diffs, edit derived value (sends edit DTO), create comment, request PR creation
- Forbidden: local locking decisions; trust backend lock confirmation before disabling edits

PASS.

---

SECTION 6 — ACTION CARD DTO MAPPING

Card | DTO consumed | API triggered | State transitions | Allowed actions

ValidationCard | ValidationDTO | GET /validation/{id}, POST /validation/run | affects validation slice (read-only until run) | view, request re-run
PRCard | PRDTO/PRStatusDTO | GET /pr/{id}/status | UI shows PRStatus | open, view
ReviewCard | ReviewDTO | POST /reviews/{id}/comment, POST /reviews/{id}/approve | review slice update after backend persists | comment, approve
ApprovalCard | ReviewApprovalDTO | POST /reviews/{id}/approve | updates review status from backend | approve/reject via backend
ErrorCard | AuditEventDTO or operation-result | retry endpoint (operation specific) | UI only | retry/view logs
SuccessCard | operation-result DTO | none | display-only | none

Cards are presentation-only; no business logic. PASS.

---

SECTION 7 — AUDIT UX

Components: AuditPage, AuditTimeline, AuditEventList, NodeExecutionHistory

DTOs required: AuditEventDTO, NodeExecutionDTO
APIs: GET /audit/session/{id}, GET /audit/draft/{id}
Ownership: frontend presents; backend persists and owns events (audit service + audit_events table)
Filters: time range, event_type, actor, entity_id; sorting most-recent-first
Recovery behavior: links to SnapshotRestore / DraftRecovery APIs; UI triggers backend flows
PASS.

---

SECTION 8 — DIFF / CHANGESET UX

Components: DiffView (GitHub style), ChangeSetView, FilesChangedPanel, PRPreviewDiff
DTOs required: ChangeStackDTO, DraftChangeDTO, FileDiffDTO, FileManifest/FileDescriptor
APIs: GET /drafts/{id}/diff/{file}, GET /drafts/{id}/changes, GET /repo/file/preview
Ownership: diffs generated by backend (diff engine); UI requests and displays
Features supported: Added/Modified/Deleted file views, inline comments forwarded via review APIs
Forbidden: client-side application of diffs to repo; must be done via draft change APIs
PASS.

---

SECTION 9 — SNAPSHOT UX

Components: SnapshotHistory, SnapshotRestore, Undo, Timeline
Contracts:
- Immutable snapshots presented read-only
- Auto-snapshot on mutations is backend responsibility; UI shows snapshot entries
- Restore calls POST /snapshots/{id}/restore (SnapshotRestoreDTO); backend creates a new snapshot and returns updated DraftDTO
- UI must treat restore as creating new draft snapshot; do not mutate cached snapshot objects
PASS.

---

SECTION 10 — SESSION UX

Components: SessionSidebar, SessionGroups, SessionCard, SessionSearch
Contracts:
- Grouping: Today / Yesterday / Previous (client-side grouping only)
- Actions: open, restore, delete (POST /session/restore, DELETE /sessions/{id})
- One Session = One Active Draft enforced by backend; UI reads `active_draft_id` from SessionDTO
- Navigator restore: UI calls GET /navigator/last/{session_id} or helper endpoint
PASS.

---

SECTION 11 — BUSINESS RULE VISIBILITY

Frontend displays source-system rules and impacts but does not enforce.

Mapping:
- Display location: FilesChangedPanel (high visibility), ReviewSummary, ValidationPanel
- DTO carrying impact metadata: ChangeEntryDTO contains `file_impact` + `provenance` fields; DraftWorkspaceDTO.files includes flags for `existing_source` vs `new_source`
- Warnings rendered based on ValidationDTO entries (e.g., JR-001 duplicate detection) and file impact metadata
- Enforcement: KnowledgeDerivationService and DraftWorkspaceService (backend) only
PASS.

---

SECTION 12 — ARCHITECTURE DRIFT ANALYSIS

Comparison basis: Steps 1–7 frozen artifacts and DTO freeze.

Results summary:
- Component contracts consistent with DTO freeze and LangGraph responsibilities.
- No UI authority violations detected: frontend does not become source of truth anywhere.
- DTO ownership maintained: backend services own editing/persistence.
- Missing UI implementations (expected): GitHubStyleDiffViewer, NodeExecutionViewer detailed views, advanced RepoTree widget. These are implementation gaps, not architecture drift.

Per-section status: all PASS.

Identified potential clarifications (not drift):
- Confirm exact DTO field names for `FileImpact` and `RepositoryTreeDTO` (document currently references them conceptually). Suggest adding small DTO index doc if desired.

---

SECTION 13 — OUTPUT MATRICES (concise)

1) Component Inventory (list): SessionSidebar, SessionCard, SessionGroups, SessionSearch, ChatContainer, MessageList, MessageInput, TypingIndicator, FilesChangedPanel, DerivedValuesPanel, ValidationPanel, PRMetadataPanel, ChangeHistoryPanel, SnapshotHistory, SnapshotRestore, ValidationResults, ValidationHistory, PRPreview, PRSummary, PRConfirmation, AuditTimeline, AuditEventList, NodeExecutionViewer, RepoTree, FilePreview, GitHubStyleDiffViewer

2) Component Ownership Matrix (component -> owner): see SECTION 2 mapping (session/draft/review/validation/pr/navigator/audit/auth)

3) DTO Consumption Matrix (component -> DTOs): summarized across sections; major mappings:
- Session components -> SessionDTO, SessionSummaryDTO, MessageDTO
- Draft/Review components -> DraftWorkspaceDTO, ChangeStackDTO, DerivedValuesDTO, SnapshotDTO, ValidationDTO
- PR components -> PRDTO, PRStatusDTO, DuplicatePRDTO
- Audit components -> AuditEventDTO, NodeExecutionDTO
- Diff components -> FileDiffDTO, DraftChangeDTO

4) Redux Ownership Matrix (slice -> owner): auth, session, draft, review, validation, pr, navigator, audit, ui — owners per SECTION 2; write/read perms in SECTION 3

5) Action Card DTO Mapping Matrix: see SECTION 6 table

6) Audit UX Matrix: see SECTION 7

7) Diff/ChangeSet UX Matrix: see SECTION 8

8) Snapshot UX Matrix: see SECTION 9

9) Session UX Matrix: see SECTION 10

10) Architecture Drift Report: PASS — no drift; missing implementation components listed

11) Missing Components Report:
- GitHubStyleDiffViewer (spec exists, not implemented)
- NodeExecutionViewer (detailed execution UI not yet present)
- RepoTree advanced features (lazy-loading, file-type icons)
- DTO index doc for `FileImpact` / `RepositoryTreeDTO` field-level spec (recommended)

12) FINAL PASS/FAIL: PASS (all sections PASS)

---

If you want, I will (documentation-only) produce a one-page implementer checklist mapping exact DTO fields to UI fields for the most critical components (DerivedValuesPanel, FilesChangedPanel, PR flow). Proceed? 
