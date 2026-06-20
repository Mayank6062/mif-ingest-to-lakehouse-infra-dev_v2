# Frontend Component Contract Freeze (STEP-7.1)

This document is an architecture-only freeze of the frontend component contracts. It verifies consistency against all previously frozen artifacts (Steps 1–7 and DTO freeze) and defines the canonical pages, feature modules, components, DTO contracts consumed, ownership, state ownership, communication boundaries, and UX contracts.

Final verdict: PASS — All component contracts align with frozen architecture and DTOs. Frontend is presentation-only and does not duplicate business logic.

---

**SECTION 1 — PAGE INVENTORY**

For each route-level page: purpose, owner, consumed DTOs, allowed API calls, child components, forbidden responsibilities.

- `LoginPage`
  - Purpose: authenticate user via GitHub OAuth.
  - Owner: `auth` feature
  - Consumed DTOs: none (redirect flow); token metadata handled via `auth` slice.
  - Allowed API calls: `GET /auth/redirect`, OAuth exchange via backend.
  - Child components: `LoginForm`, `OAuthButton`.
  - Forbidden: storing secrets, performing OAuth exchange in client.
  - PASS

- `DashboardPage`
  - Purpose: high-level summary of sessions, drafts, notifications, validation status.
  - Owner: `session` feature
  - Consumed DTOs: `SessionSummaryDTO`, `ValidationSummaryDTO`
  - Allowed API calls: `GET /sessions`, `GET /validation/summary`
  - Child components: `SessionSidebar` (shared), `DashboardCards`, `ValidationOverview`
  - Forbidden: deriving values or running validation locally.
  - PASS

- `SessionPage`
  - Purpose: Chat-style session view and session-level actions.
  - Owner: `session` feature
  - Consumed DTOs: `SessionDTO`, `SessionHistoryDTO`, `DraftDTO` (summary)
  - Allowed API calls: `POST /agent/message`, `GET /sessions/{id}/history`, `POST /session/restore`
  - Child components: `ChatContainer`, `MessageList`, `MessageInput`, `SessionActions`
  - Forbidden: local authoritative edits to draft state.
  - PASS

- `DraftPage`
  - Purpose: edit-focused view for an active draft (files, derived values, change stack preview)
  - Owner: `draft` feature
  - Consumed DTOs: `DraftWorkspaceDTO`, `ChangeStackDTO`, `DerivedValuesDTO`, `SnapshotDTO`
  - Allowed API calls: `GET /drafts/{id}`, `POST /drafts/{id}/change`, `POST /derived-values/edit`
  - Child components: `FilesChangedPanel`, `DerivedValuesPanel`, `ChangeHistoryPanel`, `SnapshotHistory`
  - Forbidden: implementing validation/derivation logic client-side.
  - PASS

- `ReviewPage`
  - Purpose: authoritative review workspace prior to PR creation.
  - Owner: `review` feature
  - Consumed DTOs: `ReviewDTO`, `ReviewSummaryDTO`, `ValidationSummaryDTO`, `DraftWorkspaceDTO`
  - Allowed API calls: `GET /reviews/{draft_id}`, `POST /reviews/{draft_id}/comment`, `POST /pr/create`
  - Child components: `FilesChangedPanel`, `DerivedValuesPanel`, `ValidationPanel`, `PRMetadataPanel`
  - Forbidden: merging PRs locally; PR creation performed via backend PRCreationNode.
  - PASS

- `NavigatorPage`
  - Purpose: repository/file navigator for selecting sources and exploring repository structure
  - Owner: `navigator` feature
  - Consumed DTOs: `RepositoryTreeDTO` (read-only), `FilePreviewDTO`
  - Allowed API calls: `GET /repo/tree`, `GET /repo/file/preview`
  - Child components: `RepoTree`, `FilePreview`
  - Forbidden: modifying repository files directly (all edits via Draft flows)
  - PASS

- `PRPage`
  - Purpose: PR preview, confirmation, and status tracking
  - Owner: `pr` feature
  - Consumed DTOs: `PRDTO`, `PRStatusDTO`, `ValidationSummaryDTO`, `DuplicatePRDTO`
  - Allowed API calls: `POST /pr/create`, `GET /pr/{id}/status`, `GET /pr/{id}/audit`
  - Child components: `PRPreview`, `PRConfirmation`, `PRStatus`
  - Forbidden: assuming PR created without backend confirmation
  - PASS

- `AuditPage`
  - Purpose: audit trail and node execution history viewer
  - Owner: `audit` feature
  - Consumed DTOs: `AuditEventDTO`, `NodeExecutionDTO`
  - Allowed API calls: `GET /audit/session/{id}`, `GET /audit/draft/{id}`
  - Child components: `AuditTimeline`, `NodeExecutionViewer`, `AuditEventList`
  - Forbidden: any edit of audit records via UI (read-only)
  - PASS

- `SettingsPage`
  - Purpose: user and environment settings (UI-only preferences)
  - Owner: `auth` / `ui`
  - Consumed DTOs: `UserProfileDTO` (read/update minimal)
  - Allowed API calls: `GET /user/profile`, `POST /user/profile/update`
  - Child components: `SettingsForm`
  - Forbidden: storing secrets insecurely or exposing tokens
  - PASS

---

**SECTION 2 — FEATURE MODULES**

For each feature module: purpose, consumed DTOs, owned components, owned Redux slice, forbidden responsibilities.

- `session` feature
  - Purpose: session listing, session lifecycle, chat interactions
  - Consumed DTOs: `SessionDTO`, `SessionSummaryDTO`, `SessionHistoryDTO`
  - Owned components: `SessionSidebar`, `SessionCard`, `SessionGroups`, `SessionSearch`
  - Redux slice: `session`
  - Forbidden: making draft authoritative
  - PASS

- `draft` feature
  - Purpose: draft editing UI and change preview
  - Consumed DTOs: `DraftWorkspaceDTO`, `ChangeStackDTO`, `SnapshotDTO`, `DerivedValuesDTO`
  - Owned components: `FilesChangedPanel`, `DerivedValuesPanel`, `ChangeHistoryPanel`, `SnapshotHistory`
  - Redux slice: `draft`
  - Forbidden: performing validation or deriving new values locally
  - PASS

- `review` feature
  - Purpose: review workspace and PR preparation
  - Consumed DTOs: `ReviewDTO`, `ReviewSummaryDTO`, `ValidationSummaryDTO`, `PRMetadataDTO`
  - Owned components: `ReviewPage` subcomponents
  - Redux slice: `review`
  - Forbidden: creating PR without backend endorsement
  - PASS

- `validation` feature
  - Purpose: display validation results and history
  - Consumed DTOs: `ValidationDTO`, `ValidationSummaryDTO`, `ValidationHistoryDTO`
  - Owned components: `ValidationPanel`, `ValidationResults`, `ValidationHistory`
  - Redux slice: `validation`
  - Forbidden: evaluating rules locally
  - PASS

- `navigator` feature
  - Purpose: repository navigation and file preview
  - Consumed DTOs: `RepositoryTreeDTO`, `FilePreviewDTO`
  - Owned components: `RepoTree`, `FilePreview`
  - Redux slice: `navigator`
  - Forbidden: direct file changes (must route through draft)
  - PASS

- `pr` feature
  - Purpose: PR lifecycle UI (preview, create, status)
  - Consumed DTOs: `PRDTO`, `PRStatusDTO`, `DuplicatePRDTO`
  - Owned components: `PRPreview`, `PRConfirmation`, `PRStatus`
  - Redux slice: `pr`
  - Forbidden: bypassing PR creation node (must use backend endpoint)
  - PASS

- `audit` feature
  - Purpose: present audit and node execution data
  - Consumed DTOs: `AuditEventDTO`, `NodeExecutionDTO`
  - Owned components: `AuditTimeline`, `NodeExecutionViewer`, `AuditEventList`
  - Redux slice: `audit`
  - Forbidden: editing audit records
  - PASS

- `auth` feature
  - Purpose: authentication flow and user metadata
  - Consumed DTOs: `UserProfileDTO`, auth token metadata
  - Owned components: `LoginForm`, `OAuthButton`, `UserMenu`
  - Redux slice: `auth`
  - Forbidden: exposing secrets
  - PASS

---

**SECTION 3 — COMPONENT CONTRACTS**

Each component: purpose, inputs, outputs, consumed DTOs, API deps, parent, children.

- `SessionSidebar`
  - Purpose: list and manage sessions
  - Inputs: `SessionSummaryDTO[]`, UI filters
  - Outputs: `openSession(session_id)`, `restoreSession(session_id)` events
  - Consumed DTOs: `SessionSummaryDTO`
  - API: `GET /sessions`, `POST /session/restore`
  - Parent: `AppShell`
  - Children: `SessionCard`, `SessionSearch`
  - PASS

- `SessionCard`
  - Purpose: compact session preview
  - Inputs: `SessionSummaryDTO`
  - Outputs: click/open events
  - Consumed DTOs: `SessionSummaryDTO`
  - Parent: `SessionSidebar`
  - PASS

- `SessionGroups`
  - Purpose: visual grouping (Today/Yesterday/Previous)
  - Inputs: `SessionSummaryDTO[]`
  - Outputs: group toggle events
  - Forbidden: changing session authoritative fields
  - PASS

- `SessionSearch`
  - Purpose: UI-only search over session summaries
  - Inputs: `SessionSummaryDTO[]`, query
  - Outputs: filtered list
  - PASS

- `ChatContainer`
  - Purpose: host chat message list and input
  - Inputs: `MessageDTO[]`, `SessionDTO`
  - Outputs: `postMessage(ui_action)`
  - API: `POST /agent/message`
  - Parent: `SessionPage`
  - Children: `MessageList`, `MessageInput`, `TypingIndicator`
  - PASS

- `MessageList`
  - Purpose: render ordered messages
  - Inputs: `MessageDTO[]`
  - Outputs: message action events (e.g., approve/expand)
  - Forbidden: deriving new content
  - PASS

- `MessageInput`
  - Purpose: collect user input and emit `ui_action`
  - Inputs: none (local input)
  - Outputs: `POST /agent/message` payloads
  - Forbidden: performing validation or derivation
  - PASS

- `TypingIndicator`
  - Purpose: show backend-provided typing/state
  - Inputs: backend presence DTOs or SSE events
  - PASS

- `FilesChangedPanel`
  - Purpose: list changed files and allow diff preview
  - Inputs: `DraftWorkspaceDTO.files`, `FileDiffDTO`
  - Outputs: `openDiff(file)` events
  - API: `GET /drafts/{id}/diff/{file}`
  - Parent: `ReviewPage` / `DraftPage`
  - PASS

- `DerivedValuesPanel`
  - Purpose: show derived values and allow edits (send `DerivedValueEditDTO`)
  - Inputs: `DerivedValuesDTO`
  - Outputs: `POST /derived-values/edit` with `DerivedValueEditDTO`
  - Editability: enabled until backend reports `Draft.status == PR_CREATING`
  - PASS

- `ValidationPanel` / `ValidationResults`
  - Purpose: show validation run and results
  - Inputs: `ValidationSummaryDTO`, `ValidationDTO[]`
  - Outputs: none (read-only), may request re-run via backend
  - API: `GET /validation/draft/{id}`, `POST /validation/run`
  - PASS

- `PRMetadataPanel`, `PRPreview`, `PRConfirmation`
  - Purpose: collect PR metadata, preview PR, confirm creation
  - Inputs: `DraftWorkspaceDTO`, `ValidationSummaryDTO`
  - Outputs: `POST /pr/create` -> backend handles PR creation and returns `PRDTO` or `DuplicatePRDTO`
  - PASS

- `ChangeHistoryPanel`, `SnapshotHistory`, `SnapshotRestore`
  - Purpose: show change stack and snapshots; request restore
  - Inputs: `ChangeStackDTO`, `SnapshotHistoryDTO`
  - Outputs: `POST /snapshots/{id}/restore` with `SnapshotRestoreDTO`
  - PASS

- `AuditTimeline`, `AuditEventList`, `NodeExecutionViewer`
  - Purpose: audit UX display
  - Inputs: `AuditEventDTO[]`, `NodeExecutionDTO`
  - API: `GET /audit/session/{id}`, `GET /audit/draft/{id}`
  - PASS

(Additional minor components follow same contract pattern; all are read-only or emit strictly-defined DTO edits to backend.)

---

**SECTION 4 — ACTION CARD ARCHITECTURE**

Action cards map UI elements to DTOs and allowed backend actions.

- `ValidationCard`
  - DTO mapping: `ValidationDTO`
  - Trigger: show rule failure/warning
  - Actions: view details, request re-run
  - Backend Endpoint: `GET /validation/{id}`, `POST /validation/run`
  - Allowed state changes: none except requested re-run
  - Forbidden: marking as resolved without backend
  - PASS

- `PRCard`
  - DTO mapping: `PRDTO`, `PRStatusDTO`
  - Trigger: PR created or PR suggested
  - Actions: open PR, view status
  - Backend Endpoint: `GET /pr/{id}/status`
  - Forbidden: manually changing PR state
  - PASS

- `ReviewCard`
  - DTO mapping: `ReviewDTO`
  - Trigger: review requested/updated
  - Actions: comment, approve, request changes (POST to `/reviews`)
  - Backend Endpoint: `POST /reviews/{id}/comment`, `POST /reviews/{id}/approve`
  - PASS

- `ApprovalCard`
  - DTO mapping: `ApprovalDTO` (subset of `ReviewApprovalDTO`)
  - Trigger: available approvals
  - Actions: approve/revoke (POST to backend)
  - Forbidden: local-only approvals
  - PASS

- `ErrorCard` / `SuccessCard`
  - DTO mapping: generic `AuditEventDTO` or operation result wrapper
  - Trigger: operation errors/success
  - Actions: retry, view logs
  - Backend Endpoint: operation-specific
  - PASS

Action Card Ownership Matrix: frontend owns presentation and click-to-call behavior; backend owns validation and state mutations. PASS

---

**SECTION 5 — AUDIT UX**

Components: `AuditPage`, `AuditTimeline`, `AuditEventList`, `NodeExecutionViewer`.

- Purpose: read-only presentation of audit events and node executions
- Ownership: `audit` feature (frontend) for presentation; `backend/repositories/audit` for persistence
- Consumed DTOs: `AuditEventDTO`, `NodeExecutionDTO`
- Filters: time-range, event_type, actor, entity_id
- Sorting: most-recent-first by default; allow event_type grouping
- Recovery behavior: links to snapshot/draft recovery flows (calls server endpoints)
- APIs: `GET /audit/session/{id}`, `GET /audit/draft/{id}`
- PASS

---

**SECTION 6 — DIFF / CHANGESET UX**

Components: `FilesChangedPanel`, `GitHubStyleDiffViewer`, `ChangeSetTimeline`, `DraftChangeHistory`.

- Inputs: `ChangeStackDTO`, `DraftChangeDTO`, `FileDiffDTO`
- Purpose: display file diffs, present change timeline, allow per-file comment/actions
- State ownership: diffs requested from backend; UI caches for session only
- Forbidden: applying diffs directly to repo; edits must create new change entries via draft API
- PASS

---

**SECTION 7 — SESSION UX CONTRACTS**

For each UX action: trigger, consumed DTOs, expected API, state changes.

- Open session
  - Trigger: user click on `SessionCard`
  - DTOs: `SessionDTO` via `GET /sessions/{id}`
  - API: `GET /sessions/{id}`; UI updates `session.activeSessionId` slice
  - PASS

- Session Restore
  - Trigger: user chooses restore action
  - DTOs: `SessionRestoreDTO`, response `SessionDTO` + `DraftDTO`
  - API: `POST /session/restore`
  - State changes: UI shows progress; backend updates session/draft; frontend updates cache
  - PASS

- Draft Restore
  - Trigger: restore snapshot
  - DTOs: `SnapshotRestoreDTO`, new `DraftDTO` returned
  - API: `POST /snapshots/{id}/restore`
  - PASS

- Navigator Restore (cursor)
  - Trigger: reopen navigator
  - DTOs: `NavigatorRecoveryDTO`
  - API: `GET /navigator/last/{session_id}`
  - PASS

Search and grouping handled client-side via `SessionSearch` and `SessionGroups` (presentation only). PASS

---

**SECTION 8 — REVIEW WORKSPACE CONTRACTS**

Editability matrix and ownership:

- Editable until: `Draft.status == PR_CREATING` (backend authoritative)
- Editable elements: `DerivedValuesPanel` fields, PR metadata form fields, inline file comments
- Ownership:
  - Editor: frontend sends `DerivedValueEditDTO` or comment payload
  - Persistence owner: backend (services/repositories)
  - Viewer: frontend components
- Consumed DTOs: `ReviewDTO`, `DraftWorkspaceDTO`, `DerivedValuesDTO`, `ChangeStackDTO`
- PASS

---

**SECTION 9 — SOURCE SYSTEM RULE VISIBILITY**

Frontend display only (no enforcement):

- Component that displays rule info: `FilesChangedPanel` and `ReviewSummary`
- Warning messages: shown in `FilesChangedPanel` and `ValidationPanel` with `ValidationDTO` items referencing `JR-###` rules
- Review summary shows affected files using `FileImpact` metadata embedded in `ChangeEntryDTO` / `DraftWorkspaceDTO.files`
- DTO carrying impact metadata: `ChangeEntryDTO` includes `provenance` and `file_impact` fields (file impact metadata is part of Draft change entry)
- PASS

---

**SECTION 10 — STATE OWNERSHIP MATRIX**

For every key DTO, define Owner / Editor / Viewer / Persistence owner:

- `SessionDTO`: Owner=backend, Editor=backend, Viewer=frontend, Persistence=Postgres (`sessions` table)
- `DraftDTO` / `DraftWorkspaceDTO`: Owner=backend (Draft Workspace service), Editor=frontend via API (sends edits), Viewer=frontend, Persistence=Postgres (`drafts`, `draft_changes`, `draft_files`)
- `DerivedValueDTO`: Owner=KnowledgeDerivation service, Editor=frontend via `DerivedValueEditDTO` (requests), Viewer=frontend, Persistence=Postgres + provenance table
- `ValidationDTO`: Owner=validation service, Editor=validation service only, Viewer=frontend, Persistence=validation_results table
- `SnapshotDTO`: Owner=backend snapshot service, Editor=backend (restore creates new snapshot), Viewer=frontend, Persistence=snapshots table
- `PRDTO`: Owner=PRCreationNode/backend, Editor=backend, Viewer=frontend, Persistence=pr_metadata table
- `AuditEventDTO`: Owner=backend audit service, Editor=backend only, Viewer=frontend, Persistence=audit_events table

PASS

---

**SECTION 11 — ARCHITECTURE DRIFT ANALYSIS**

Checked frontend contracts against frozen artifacts: DTO freeze, business rules, LangGraph nodes, Draft/Review/Snapshot rules.

Findings:
- No missing contract definitions for required frontend components.
- Ownerships are consistent: frontend only views and requests edits; backend remains authoritative.
- DTO conflicts: none detected (used canonical DTO names from DTO freeze)
- State conflicts/UI authority violations: none detected.

PASS

---

**MISSING COMPONENTS**

- Implementation status note: repository contains frontend skeleton only; no component implementations found. The following components are documented as required (freeze) but intentionally not implemented here:
  - `GitHubStyleDiffViewer` (spec required)
  - `RepoTree` / advanced file navigator widgets
  - `NodeExecutionViewer` detailed UI

These are design-time "missing implementations" (by design; freeze is documentation-only). Not an architecture drift.

---

**FINAL PER-SECTION RESULT**

- SECTION 1 (Pages): PASS
- SECTION 2 (Feature Modules): PASS
- SECTION 3 (Component Contracts): PASS
- SECTION 4 (Action Cards): PASS
- SECTION 5 (Audit UX): PASS
- SECTION 6 (Diff/ChangeSet UX): PASS
- SECTION 7 (Session UX): PASS
- SECTION 8 (Review Workspace): PASS
- SECTION 9 (Source System Visibility): PASS
- SECTION 10 (State Ownership): PASS
- SECTION 11 (Architecture Drift): PASS

Overall STEP-7.1 Result: PASS

---

Notes:
- This file is an authoritative freeze for frontend contracts. Implementation must strictly follow DTO shapes and ownerships as defined in the DTO freeze.
- If you want, I can produce a condensed implementer checklist (one-page) mapping exact DTO field names to UI fields (doc-only). Proceed? 
