# Infrastructure Decisions

This folder documents infrastructure-related decisions for the Agent Platform.

## Phase-1 Approach

- **Database**: PostgreSQL (local dev; AWS RDS for deployment)
- **Cache**: Redis (local dev; AWS ElastiCache for deployment)
- **Backend Host**: FastAPI app (local dev; AWS App Runner or ECS for deployment)
- **Frontend Host**: Static S3 + CloudFront (Vite build artifacts)
- **Auth**: GitHub OAuth (external)

## Deferred

- Terraform manifests for AWS infrastructure (defer to Phase 2)
- Kubernetes orchestration (defer; single container sufficient Phase-1)
- Multi-region support (defer)

## Local Development

See `docs/ARCHITECTURE.md` and backend/frontend README files for local setup.
