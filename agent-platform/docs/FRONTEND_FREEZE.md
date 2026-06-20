# Frontend Structure Freeze

This document freezes the frontend architecture for the agent-platform. It is architecture-only: no implementation, no UI mockups, and no business logic. The frontend consumes frozen API/DTO contracts and must not perform derivation or validation decisions.

Summary Verdict: PASS — Frontend design follows frozen backend architecture and DTOs, does not introduce new workflows, does not contain business logic, and does not bypass Draft/Review/Validation.

---

**SECTION 1 — FRONTEND ARCHITECTURE**

Layers:
- Presentation Layer: page components, layout, visual-only components. (Owner: frontend/ui)
- Feature (Domain) Layer: feature modules composing pages; contains orchestration for presentation only (Owner: frontend/features)
- API Layer: thin adapters calling backend endpoints; strictly pass-through shapes (Owner: frontend/api)
- State Layer: Redux Toolkit slices for UI and cached read state (Owner: frontend/store)
- Shared Layer: UI primitives, icons, formatters, simple helpers (Owner: frontend/shared)

Module boundaries & ownership:
- `frontend/pages/` — route-level composition (presentation only)
- `frontend/features/` — feature module shells (no business logic, no derivation)
- `frontend/api/` — DTO pass-through adapters and typed request/response contracts
- `frontend/store/` — canonical slices: `auth`, `session`, `draft`, `review`, `validation`, `ui`

PASS: Layers, boundaries, and ownership align with frozen DTO/API contracts and LangGraph responsibilities.

---

**SECTION 2 — APPLICATION LAYOUT**

Hierarchy:
- App Shell (root): owns routing, authentication check, global error banner
  - Header: top bar, global actions, user menu (Owner: frontend/shared)
  - Sidebar: Session navigator, quick-actions (Owner: frontend/features/session)
  - Main Content Area: route outlet
  - Chat Area: main conversation UI (embedded in route or modal)
  - Review Area: review workspace page/area (route-level)
  - PR Area: PR preview/confirmation modals (transient)
  - Validation Area: floating/side validation panel (reads validation state)

Responsibilities:
- App Shell: layout only, passes DTOs to child pages
- Sidebar: presents session list and actions (read-only UI/commands that call backend endpoints)
- Chat Area: represents messages and input; no derivation or validation logic

PASS: Layout enforces separation of concerns and prevents business logic in presentation.

---

**SECTION 3 — CHATGPT-STYLE SESSION EXPERIENCE**

Must preserve ChatGPT-like UX: session-focused card list + chronological grouping.

Component inventory & ownership:
- `SessionSidebar` (frontend/features/session): groups sessions into `Today`, `Yesterday`, `Previous`; supports search/filter; issues commands (open, restore) via API.
- `SessionCard` (presentation): displays summary (SessionSummaryDTO)
- `SessionSearch` (presentation): client-side index over SessionSummaryDTO fields (no derivation)
- `SessionGroups` (presentation): grouping logic purely UX (client time grouping)
- `SessionActions` (api calls): open, restore, delete; call backend `POST /agent/message` or REST endpoints.

Session UX rules:
- One Session = One Active Draft (enforced by backend). Frontend shows `active_draft_id` and never assumes draft state authoritative locally.
- Session restore triggers backend restore flow; frontend shows progress via SSE/validation events.

PASS: Component ownership and UX preserve backend authority and DTO consumption.

---

**SECTION 4 — MAIN CHAT EXPERIENCE**

Components:
- `ChatContainer` (page-level)
- `MessageList` (presentation): owns rendering of `MessageDTO` items provided by API
- `MessageInput` (presentation): posts `ui_action` to backend; may provide client convenience (history autocomplete) but no derivation
- `TypingIndicator` (presentation): shows presence/status from backend/WS
- `SystemMessage`, `ValidationMessage`, `ApprovalMessage`, `ActionMessage` (presentation): render messages using DTO flags

Message model ownership:
- All message and state models are canonical from backend DTOs; frontend is read-only for authoritative fields.

PASS: Chat retains GPT-style flow and avoids wizard-like constraints.

---

**SECTION 5 — DYNAMIC WORKFLOW UX**

Flows (frontend displays inputs; backend derives values):
- Environment Selection UX: selection component that posts selection to backend; backend returns derived suggestions.
- Operation Selection UX: same pattern—frontend collects choice, sends to backend
- Source Type & Source System UX: pickers that call read endpoints, no derivation locally
- Schema Grain UX & Topic Preview: frontend displays derived topic(s) from backend DTOs

State ownership:
- Selected values (temporary UI state) in `ui` slice until persisted to backend
- Authoritative values (derived_values) come from `DraftWorkspaceDTO` / `DerivedValuesDTO` from backend

PASS: Frontend does not derive values; it only displays backend-derived DTOs.

---

**SECTION 6 — REVIEW WORKSPACE UI**

Critical: Review Workspace is authoritative before PR.

Components & hierarchy:
- `ReviewPage` (route) — container
  - `FilesChangedPanel` — shows file diffs (from `DraftWorkspaceDTO.files`)
  - `DerivedValuesPanel` — lists `DerivedValuesDTO` and allows edits that send `DerivedValueEditDTO` to backend
  - `ValidationPanel` — shows `ValidationSummaryDTO` and individual `ValidationDTO`s
  - `PRMetadataPanel` — collects PR title/description (local form until PR create call)
  - `ChangeHistoryPanel` — shows `ChangeStackDTO` entries

Editability rules (frontend enforced UX only; backend authoritative):
- Fields are editable in UI until Draft.status == PR_CREATING. Frontend must send edits to backend and respect rejection responses.
- Frontend may optimistically show edits but must reconcile with backend confirmation.

PASS: Review workspace UI respects editable-until-PR_CREATING and keeps authority server-side.

---

**SECTION 7 — VALIDATION UX**

Components:
- `ValidationResults` (list of `ValidationDTO`) — shows rule_id, severity, message
- `ValidationHistory` (per-draft timeline) — `ValidationHistoryDTO`
- `RuleIdBadge` — displays rule id and severity color mapping

Display rules:
- Severity colors: ERROR=red (FAIL), WARN=amber (WARN), INFO=blue (PASS)
- Clicking a rule opens details with `ValidationResultDTO` and fix suggestions (from backend)

PASS: Display-only; rule evaluation and decisioning remain server-side.

---

**SECTION 8 — SNAPSHOT UX**

Components & relationships:
- `SnapshotHistory` — shows `SnapshotHistoryDTO` entries for a draft
- `SnapshotRestore` — triggers `SnapshotRestoreDTO` flow; frontend shows confirmation modal and progress UI
- `Undo` / `Timeline` — renders change timeline from `ChangeStackDTO` and snapshots

Rules preserved:
- Snapshots are immutable; restore calls create a new snapshot on backend; frontend treats snapshots as read-only artifacts.

PASS.

---

**SECTION 9 — PR EXPERIENCE**

Components & flow:
- `PRPreview` — shows `PRMetadataDTO` and `ValidationSummaryDTO`
- `PRSummary` — summary list and diff
- `PRConfirmation` — calls PR creation endpoint; on submit UI shows `PRStatusDTO` updates via SSE
- `PRSuccess` / `PRFailure` modals — show final status
- Duplicate PR handling: backend returns `DuplicatePRDTO`; frontend renders that state and prevents duplicate action

State transitions:
- UI calls create PR; backend transitions Draft.status PR_CREATING and locks draft; frontend shows locked UI until response

PASS.

---

**SECTION 10 — STATE MANAGEMENT FREEZE**

Ownership matrix (frontend / backend / LangGraph):
- Frontend:
  - UI-only transient state (input buffers, modals, cursor positions)
  - Cached read-only DTOs for presentation
- Backend:
  - Authoritative session, draft, derived values, snapshots, validation, PR state
- LangGraph:
  - Orchestration and node-level decisions; nodes consume/emit DTOs but persistence done by services/repositories

Canonical slices (frontend/store):
- `auth` (tokens metadata only)
- `session` (SessionSummaryDTO cache; active session id)
- `draft` (active DraftWorkspaceDTO snapshot cache)
- `review` (ReviewDTO cache)
- `validation` (ValidationSummaryDTO and last run)
- `ui` (local UI state)

PASS: Draft workspace remains source-of-truth on backend; frontend never claims authority.

---

**SECTION 11 — ACTION CARDS ARCHITECTURE**

Action card types:
- `ApprovalCard`, `ValidationCard`, `ReviewCard`, `PRCard`, `ErrorCard`, `SuccessCard`

Model & relationships:
- Card is a UI model bound to specific DTOs (e.g., `ValidationCard` ↔ `ValidationDTO`)
- Actions: Approve, Reject, Retry, Restore, Create PR — these are API calls; UI shows progress/result

PASS: Action cards are presentation adapters over DTOs; no embedded business logic.

---

**SECTION 12 — RECOVERY UX**

Flows:
- Session Recovery: UI triggers `SessionRecoveryDTO` flow; backend restores session and returns updated SessionDTO
- Draft Recovery: UI triggers `DraftRecoveryDTO` flow; backend restores snapshot and returns new DraftDTO + SnapshotDTO
- Navigator Recovery: UI requests last cursor and applies to UI; authoritative cursor persisted server-side if required
- Browser Refresh: frontend reads last session/draft from backend and restores view; reconnect UX via SSE/WebSocket fallback to polling

Ownership: recovery decisioning and snapshot creation/restoration owned by backend services; frontend only displays progress and results.

PASS.

---

**SECTION 13 — SECURITY & UX BOUNDARIES**

Verify:
- No secrets stored in UI; tokens are ephemeral and never logged in client-side storage except secure session cookies or secure storage per deployment guidance.
- No GitHub token exposure; OAuth flow uses backend exchange only.
- No duplication of business logic or derivation; frontend displays DTOs and delegates decisions to backend/LangGraph.

PASS.

---

**SECTION 14 — ARCHITECTURE DRIFT ANALYSIS**

Validation against frozen artifacts (Architecture, LangGraph nodes, DTOs, Draft/Review/Snapshot rules):
- No drift detected. Frontend structure is strictly presentation-focused and consumes the frozen DTOs.
- No new workflows introduced. Editability rules and PR locks are preserved.

PASS.

---

**SECTION 15 — FINAL OUTPUT**

Deliverables (frozen):
1. Frontend Folder Structure (high-level): `pages/`, `features/`, `api/`, `store/`, `shared/`, `components/`, `assets/`, `tests/`
2. Pages Inventory: `Login`, `Dashboard`, `Session`, `Draft`, `Review`, `Navigator`, `PR`, `Settings`, `Audit`
3. Components Inventory: listed throughout sections (SessionSidebar, ChatContainer, MessageList, MessageInput, Review panels, Validation panels, SnapshotHistory, PRPreview, ActionCards)
4. Feature Modules Inventory: `session`, `draft`, `review`, `validation`, `pr`, `navigator`, `audit`
5. State Ownership Matrix: (see SECTION 10)
6. Session UX Architecture: (see SECTION 3)
7. Review Workspace Architecture: (see SECTION 6)
8. Validation UX Architecture: (see SECTION 7)
9. Snapshot UX Architecture: (see SECTION 8)
10. PR UX Architecture: (see SECTION 9)
11. Recovery UX Architecture: (see SECTION 12)
12. Final PASS / FAIL: PASS

---

Notes & next steps:
- This freeze is documentation-only. If you want, I can export a condensed checklist for frontend implementers that references DTO names and exact fields (documentation only, no code).
