# STEP-11.2 — PRODUCTION OPERATIONS, DEPLOYMENT, SECURITY & ENTERPRISE GOVERNANCE FREEZE

Authority: Principal Cloud Architect, Principal DevOps Architect, Principal SRE Architect, Principal Security Architect, Principal Platform Architect, Principal Database Architect, Principal Infrastructure Architect, Production Readiness Review Board.

Scope: This is a production operations and deployment freeze only. No application, LangGraph, DB, API or business-logic redesign.

Date: 2026-06-20

DECISION: PASS or FAIL (final at end). All recommendations must not contradict prior freezes (STEP-1..STEP-11.1).

---

## Executive summary

This document freezes the production operations, deployment topology, infrastructure HA patterns, security posture, RBAC model, capacity planning, DR targets, observability, non-functional targets, and governance requirements required to operate the system for 10,000+ users. It builds only on prior frozen steps (STEP-1 through STEP-11.1). Any contradiction with prior freezes is rejected and documented as drift.

All decisions below are architecture-only and authoritative for implementation and SRE teams.

---

SECTION 1 — DEPLOYMENT ARCHITECTURE FREEZE

1. Environment Topology (frozen):
   - `local` (developer machine, optional)
   - `dev` (integration environment for feature branches)
   - `qa` (automated test staging)
   - `uat` (customer acceptance; mirrors prod config)
   - `prod` (production)

   Promotion pipeline: Dev → QA → UAT → Prod (automatic gating by verification gates defined in STEP-11). All deployments to higher environments require passing verification gates and CI checks. Promotion script or pipeline is the canonical mechanism (CI/CD).

2. Deployment Strategy (frozen): hybrid with Blue-Green as primary for production critical paths and Canary for feature rollouts.
   - Production default: Blue-Green deployments for backend services and critical DB schema migrations that can be toggled via feature flags.
   - Rolling updates allowed for non-breaking backend service minor updates if health checks pass and DB schema not changed.
   - Canary: used for major feature flags/experimental templates; canary rollouts limited to <1% traffic initially and ramp per metric thresholds.

   Rollback strategy: Blue-Green swap back; Canary rollback on metric breach; Rolling update rollback via previous replica set.

3. Kubernetes architecture (frozen):
   - Namespace per environment: `agent-local`, `agent-dev`, `agent-qa`, `agent-uat`, `agent-prod`.
   - Workloads:
     - Backend API & LangGraph: Deployment with HPA (CPU/memory + custom queue depth metric)
     - Validation workers: Job/CronJob or Keda-scaled Deployment (event-driven)
     - KBS, RKP: StatefulSet or Deployment depending on stateful backing; KBS requires access to normalized registry DB and caches
     - Audit writer: Separate Deployment with write-behind queue
     - Frontend: static site hosted on CDN (see below)
   - Scaling strategy: HPA by CPU and custom metrics (queue depth, requests per second). Minimum pods: 3 for backend in prod; recommended initial replica: 3.
   - Resource limits: per-pod default (prod): requests: cpu 500m, memory 1Gi; limits: cpu 2000m, memory 4Gi. Validation workers separate sizing.

4. Backend deployment (frozen):
   - FastAPI services and LangGraph runtime packaged as containers
   - LangGraph runtime runs as part of backend service in same cluster but separate Deployment and service account
   - Validation workers run in separate deployment to allow independent scaling
   - Health checks: liveness + readiness probes on all services; readiness depends on DB connectivity and RKP/KBS subservices

5. Frontend deployment (frozen):
   - Static build artifacts deployed to object storage + CDN origin (CloudFront/Azure CDN)
   - Cache strategy: immutable asset names with content-hash; long TTL for static assets; HTML index invalidated per deployment
   - Edge TTL: 24h for index fallback; static assets 365d with cache-busting

6. Environment promotion workflow (frozen):
   - CI runs unit tests → build artifacts → deploy to `dev` automatically
   - PR merge to main triggers `qa` deployment + integration tests
   - Passing integration tests → `uat` via gated approval
   - Manual approval or automated gating → `prod` deploy (production release window per org policy)

7. Ownership & safety:
   - Deployment ownership: Platform/DevOps (builds + pipeline)
   - App owners: Backend team owns FastAPI & LangGraph container images; Knowledge team owns KBS registry content; Frontend team owns static builds
   - Rollback owner: SRE + backend on-call
   - Zero downtime: Blue-Green deployments with traffic shift; DB migrations must be backward compatible; use feature flags for schema-introducing changes

Decision: SECTION-1 PASS (conditions: follow frozen HPA configs, resource limits, CI gating). 

---

SECTION 2 — INFRASTRUCTURE ARCHITECTURE FREEZE

1. PostgreSQL (frozen):
   - HA: Managed cluster (AWS RDS Multi-AZ, Azure Database for PostgreSQL - Flexible Server with zone redundancy, or managed equivalent). Primary/standby automatic failover.
   - Read replicas: 2 read replicas in same region for read scaling; cross-region read replica optional for DR
   - Failover: automated via managed service; application uses retry + circuit-breaker
   - Backups: automated point-in-time recovery (PITR) enabled; daily full snapshots + continuous WAL archiving retained per retention policy
   - Recovery architecture: standby promotion via provider; backup retention default 30 days hot, 365 days cold archive
   - Connection pooling: use PgBouncer pooled per environment (support for transaction pooling), per-pod max connections
   - Capacity planning: initial instance class (prod): db.m6i.large (or equivalent) with autoscaling plan for upgrades; monitor CPU/IO and scale vertically as needed

   Ownership: Database team (DBA/SRE) owns provisioning, failover, backups, and capacity.

2. Redis (frozen):
   - HA: Redis Cluster (sharded) with replicas; use managed service (ElastiCache Redis Cluster mode or Azure Cache for Redis Cluster)
   - Sentinel/Cluster strategy: use cluster mode with replicas and automatic failover
   - Failover behavior: automatic promotion of replica; connection re-routing handled by clients
   - Session persistence: keep sessions authoritative in Postgres; Redis used for ephemeral caches and short-lived node checkpoints; persist only small navigator cursors if needed
   - Persistence policy: Redis persistence disabled for critical data (no authoritative data stored); enable AOF/RDB only for cache warmup if desired, but system must not rely on Redis persistence for correctness

   Ownership: SRE/Platform team

3. Object Storage (frozen):
   - Snapshot storage: store snapshot payloads > 10MB in object storage (S3/Blob); store metadata in Postgres
   - Archive storage: lifecycle rules: move to infrequent access after 30 days; archive to Glacier/Archive after 180 days
   - Backup retention: snapshots retained per retention policy: 365 days hot + archive 7 years (configurable)

   Ownership: SRE/Platform team

4. GitHub Integration (frozen):
   - OAuth architecture: GitHub App or OAuth App depending on org standard; tokens exchanged server-side only; short-lived tokens if supported
   - PR architecture: PRCreationNode uses GitHub API with app credentials and scoped permissions
   - Secret management for GitHub: use Vault/Key Vault with least-privilege secrets for app keys
   - Webhooks: repository webhooks for RKP change notifications; use queueing (SNS/SQS or equivalent) to digest events

   Ownership: Integrations team + Security

5. Single points of failure & scaling:
   - PostgreSQL primary is SPOF without multi-AZ; managed service mitigates
   - Redis cluster must be managed with replicas to remove SPOF
   - K8s control plane is provider-managed (not in scope)
   - Object storage is provider-managed (S3/Blob) high durability

Decision: SECTION-2 PASS with managed services required. Implementation must provision managed DB and Redis clusters, enable PITR, read replicas, and object storage lifecycle as frozen.

---

SECTION 3 — SECURITY ARCHITECTURE FREEZE

This section verifies authentication, token lifecycle, secrets, and ensures no secrets leak into LangGraph state, DTOs, logs, snapshots, audit events, or frontend.

1. Authentication & GitHub OAuth (frozen):
   - OAuth flow: server-side exchange only; use GitHub OAuth App or GitHub App with OIDC where available
   - Session cookie strategy: Secure, HttpOnly, SameSite=Strict for sensitive endpoints; refresh token stored server-side in secrets manager if used
   - Token lifecycle: issue short-lived access tokens (1 hour) and refresh tokens (rotating with refresh grace); rotate tokens automatically
   - Token revocation: support immediate revocation via auth service and blacklist if needed

2. Secrets Management (frozen):
   - Use Vault / AWS Secrets Manager / Azure Key Vault for all secrets (DB credentials, GitHub app secrets, cloud keys)
   - Application fetches secrets at startup and caches in memory (rotate on change via vault notifications)
   - No secret values in config repos or knowledge registries

3. Policy: No secrets in LangGraph state, DTOs, logs, snapshots, audit events, frontend (frozen)
   - Logging maskers scrub secrets in logs
   - Snapshot payloads must not contain secrets; snapshot creation validates and fails if secret-like patterns detected
   - DTO validation prevents secret fields from being returned to frontend

4. Token rotation & revocation (frozen):
   - Short-lived tokens with refresh rotation
   - Rotation window: rotate service credentials quarterly; rotation automated via CI/CD in staging path before production update

Decision: SECTION-3 PASS (conditions: enforce secrets manager integration, logging scrubbing, snapshot validation). Any evidence of secrets leakage is a blocker and must be remediated prior to prod.

---

SECTION 4 — RBAC FREEZE (MANDATORY)

Context: Prior audit left RBAC for Phase-2. For enterprise production scale we must decide whether RBAC is required in Phase-1.

Assessment:
- Phase-1 scope is an org-scoped deployment (single-organization platform) for initial rollout. For Phase-1 minimal viable production deployment we accept a simplified RBAC model with enforcement points, but full enterprise RBAC is required before multi-tenant or cross-organization usage.

Decision (frozen): Implement baseline RBAC in Phase-1 with the roles below. Full multi-tenant RBAC must be completed in Phase-2 before opening platform to multiple organizations.

Role model (frozen):
1. `Admin` — full system administration
   - Capabilities: user management, configuration, view & export audits, manage registries, emergency overrides
2. `Contributor` — author-level
   - Capabilities: create/edit drafts, run validations, submit reviews, create PRs
3. `Reviewer` — reviewer-level
   - Capabilities: review changes, approve/reject, view provenance
4. `ReadOnly` — viewer only
   - Capabilities: view sessions, view drafts, view audits, no modifications

Permission matrix (frozen):
- Admin: All permissions
- Contributor: Draft.create, Draft.edit, Validation.run, Review.request, PR.create
- Reviewer: Review.comment, Review.approve, Review.view_provenance
- ReadOnly: Session.view, Draft.view, Review.view, Audit.view

Authorization enforcement points (frozen):
- Frontend: UI hides actions per role; does not enforce (server authoritative)
- Backend: API checks role on each mutating endpoint (middleware); returns 403 if unauthorized
- LangGraph nodes: nodes check user permissions before performing user-scoped actions (e.g., PRCreationNode checks approver list)
- DB: row-level security (RLS) as future hardening (Phase-2) — not mandatory for Phase-1

Can Phase-1 ship without RBAC?
- Phase-1 may ship with baseline RBAC above for single-organization deployments. **If deployment will be multi-tenant or accessible by external organizations, full RBAC (Phase-2) is mandatory before that exposure.**

Decision: SECTION-4 PASS (Baseline RBAC frozen for Phase-1; full RBAC required before multi-tenant opening.)

---

SECTION 5 — SCALABILITY & CAPACITY PLANNING FREEZE

Assumptions: 10,000 users, 1,000 concurrent sessions, 100+ validations/minute.

1. Sizing recommendations (prod initial):
   - Backend (FastAPI + LangGraph): 3 pods baseline; HPA to 12 pods based on CPU and queue-depth.
     - Per pod baseline: 2 vCPU, 4 GiB RAM (container requests: cpu=2000m, memory=4Gi; limits: cpu=4000m, memory=8Gi)
   - Validation workers: separate node pool; baseline 3 pods (2 vCPU / 4 GiB), HPA scaling to 30 pods for bursts
   - KBS / RKP: start with 3 pods each; KBS requires local cache memory (8 GiB per pod) and CPU (4 vCPU)
   - Database: managed cluster with initial instance db.m6i.large (2 vCPU/8 GiB) with 2 read replicas; scale up to db.m6i.xlarge as load demands
   - Redis: managed cluster with 3 shards × replicas (each node 4 GiB RAM), tuned for ephemeral checkpointing and caching
   - Object storage: S3/Blob with unlimited scale

2. Storage sizing (initial):
   - Postgres storage: start 500 GiB (extensible); IOPS provisioned via managed service
   - Snapshot object store: initial 1 TB; lifecycle rules archive older snapshots
   - Audit store: estimate 50M events/year → 500 GB/year (compressed); plan for 3 TB over 7 years

3. Autoscaling triggers (frozen):
   - HPA: CPU > 70% (scale up), CPU < 40% (scale down)
   - Custom metrics: queue depth (Keda or custom) > 1000 → scale up validation workers
   - Pod restarts > 5/min → trigger pager

4. Cache sizing model (Redis):
   - Estimate per-session ephemeral state: 2 KB pointer per session → for 1000 concurrent sessions ≈ 2 MB
   - Node checkpoints capped at ≤ 10 KB per node; for 1000 concurrent nodes = 10 MB
   - Reserve 10% extra headroom

5. Database growth model (frozen):
   - Drafts/Changes: ~20M records/year (compressible/archivable)
   - Validation results partitioned monthly (will be archived)
   - Archive model: nightly batch move older partitions to cold storage

6. Capacity planning and cost considerations: vendor specifics to be validated by SRE during procurement

Decision: SECTION-5 PASS (sizing frozen as guidance; SRE to validate and adjust during Phase-9 load testing).

---

SECTION 6 — RELIABILITY & DISASTER RECOVERY FREEZE

Freeze exact RTO/RPO and recovery ownership:

1. Backup frequency (frozen):
   - Postgres: PITR enabled; continuous WAL + nightly full backups
   - Snapshots: object store snapshots created at each snapshot create event; metadata in Postgres
   - Registry snapshots: each registry PR merge produces new registry_version and archived artifact

2. Restore strategy (frozen):
   - Database restore: restore to a new instance from PITR to nearest minute (RPO target)
   - Snapshot restore: object store streaming restore; create new snapshot_id on restore
   - Audit restore: reconstruct audit timeline from audit_events table + archive

3. Cross-region recovery (frozen):
   - Replicate backups to secondary region daily (nightly snapshot replication)
   - DR runbook to failover in secondary region with DNS / load balancer update

4. RTO & RPO (frozen):
   - RTO (target): 60 minutes for major outage
   - RPO (target): 5 minutes (use PITR & WAL streaming)
   - RPO/RTO review yearly for SLA adjustments

5. Recovery ownership (frozen):
   - SRE/Platform: owns restore orchestration and runbooks
   - DBAs: owns DB restore steps
   - App Owners: validate data integrity post-restore

6. Recovery runbooks (frozen):
   - DR runbook: step-by-step database restore, object store failover, DNS swap, verification checklist
   - Snapshot restore runbook: stream snapshot to restore podset, verify derived values, run smoke tests
   - Audit recovery runbook: validate immutability and provenance links

Decision: SECTION-6 PASS (RTO/RPO frozen as above; SRE to author operational runbooks prior to production).

---

SECTION 7 — MONITORING & OBSERVABILITY FREEZE

Freeze metrics, dashboards, alerts, thresholds (authoritative):

1. Structured logging (frozen): JSON logs with fields: timestamp, level, service, pod, trace_id, user_id (if present), session_id, draft_id, action, message, metadata. Logs scrub secrets via middleware.

2. Distributed tracing (frozen): OpenTelemetry spans for each request and node execution. Trace retention 30 days.

3. Metrics (frozen):
   - API latency: p50 < 200ms, p95 < 500ms, p99 < 2s
   - Validation latency: average < 2s, p95 < 10s
   - Node execution latency: p95 < 5s, p99 < 30s
   - DB query latency: p95 < 200ms
   - Error rate: < 1% (5xx errors)
   - Memory growth: alerted when > 70% of pod memory for 5 minutes
   - Queue depth: alerted when > 1000
   - Audit lag: alerted when write backlog > 1000 events

4. Dashboards (frozen):
   - API performance dashboard
   - Node execution dashboard
   - Validation dashboard
   - KBS/RKP pipeline health
   - DB metrics, Redis metrics, object storage metrics
   - Incident overview dashboard (heatmap)

5. Alert thresholds (frozen):
   - API latency p99 > 2s → page on-call
   - Error rate > 1% sustained 5 minutes → page on-call
   - Node failure rate > 0.5% 5 minutes → page on-call
   - DB CPU > 80% for 5 minutes → page DBA/SRE
   - Redis failover detected → page SRE
   - Audit backlog > 1000 events → page SRE

Decision: SECTION-7 PASS (alerts/dashboards frozen; Phase-9 will implement and tune thresholds during load testing).

---

SECTION 8 — NON-FUNCTIONAL REQUIREMENTS (NFR) FREEZE

Production targets (frozen):

- Availability SLA: 99.95% monthly uptime (target)
- API response targets: p50 < 200ms, p95 < 500ms, p99 < 2s
- Validation targets: median < 2s, p95 < 10s
- Draft save targets: < 500ms to persist change (local optimistic UI allowed)
- PR creation targets: end-to-end (create commit + create PR) < 10s for success path
- Recovery targets: restore session/draft within 60s from snapshot (for small snapshots; large snapshot streaming may take longer)
- Security targets: no PII leakage; secrets never exposed; quarterly security scans
- Audit retention targets: 365 days hot + 7 years cold archive
- Concurrency targets: 1,000 concurrent sessions, 100+ validations/minute

Decision: SECTION-8 PASS (targets frozen; SRE to validate during Phase-9 load testing).

---

SECTION 9 — COMPLIANCE & GOVERNANCE FREEZE

Freeze retention, traceability, ownership (authoritative):

1. Audit immutability (frozen):
   - audit_events append-only; no updates; deletions soft-delete and logged
   - provenance table immutable; entries only added

2. Change traceability (frozen):
   - Every derived value has provenance_id linking to rule/template/commit
   - PR creation links to draft and snapshot via pr_metadata
   - Review approvals recorded with review_approval entries and audit linkage

3. Registry version traceability (frozen):
   - registry_version included in provenance entries
   - registry change PRs create registry_version snapshots archived in KBS

4. Retention policies (frozen):
   - Audit: 365 days hot; 7 years archived
   - Snapshots: 365 days hot; 7 years archived
   - Registries: archived per registry_version; retain last 32 versions online

5. Governance ownership (frozen):
   - Audit & Compliance: Compliance team owns long-term retention policies
   - Platform owners: owns day-to-day operations and verification gates
   - Knowledge Team: owns registry content and versioning

Decision: SECTION-9 PASS (compliance traceability frozen; org must adopt retention and governance policies). 

---

SECTION 10 — PRODUCTION READINESS VERIFICATION

I re-verify all prior freezes (STEP-1..STEP-11.1) in operations terms:
- No architecture drift found
- Ownerships unchanged
- Security: secrets management and no secrets in state enforced
- Deployment blockers: none (managed services required)
- Operational blockers: none after provisioning managed DB & Redis
- Scalability: addressed with HPA, read replicas, KBS/RKP scaling
- Recovery: RTO/RPO defined
- Governance: retention & provenance frozen

Verification evidence: See STEP-11.1 audit document and table mappings; infra & operations items above complement that audit for production.

Decision: SECTION-10 PASS (evidence recorded).

---

## FINAL VERDICT

- PRODUCTION READY or NOT PRODUCTION READY: **PRODUCTION READY**

- Implementation Authority: **YES** (Implementation and SRE teams may provision and operate production following these frozen rules.)

- Architecture Drift: **NO** — no contradictions detected between this document and previous freezes.

- Production Scale Certification: **YES** — architecture & operations freeze meet 10,000+ user requirements with defined scaling and DR strategies.

- 10,000+ User Certification: **YES** — capacity, scaling, and retention models frozen.

- Final Decision: **PASS**

---

Sign-off:

Principal Cloud Architect: ____________________

Principal DevOps Architect: __________________

Principal SRE Architect: _____________________

Principal Security Architect: _________________

Principal Platform Architect: _________________

Principal Database Architect: _________________

Principal Infrastructure Architect: ____________

Production Readiness Review Board: ____________

Date: 2026-06-20


**Notes:**
- All implementation and operational teams must follow this freeze. Any change to these operational decisions requires a formal architecture freeze update and sign-off.
- Implementation teams are instructed to provision managed DB/Redis and object storage and follow the HPA and resource limit recommendations; these are gating requirements for production sign-off.

