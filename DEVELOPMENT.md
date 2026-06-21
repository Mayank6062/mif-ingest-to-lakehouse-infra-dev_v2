# Local Development Guide

Phase-1 Implementation: GitHub OAuth + Session Persistence

---

## Prerequisites

### Required Software

- Python 3.9+ ([download](https://www.python.org/downloads/))
- Node.js 18+ ([download](https://nodejs.org/))
- PostgreSQL 14+ ([download](https://www.postgresql.org/download/)) or Docker
- Redis 6+ ([download](https://redis.io/download)) or Docker
- Git

### GitHub OAuth App Setup

1. Go to https://github.com/settings/developers
2. Click "New OAuth App"
3. Fill in:
   - Application name: `Minerva Agent (Local)`
   - Homepage URL: `http://localhost:3000`
   - Authorization callback URL: `http://localhost:8000/api/v1/auth/github/callback`
4. Note down Client ID and Client Secret
5. Update `.env.local` with credentials

---

## Option 1: Local Development with Docker (Recommended)

### Step 1: Setup

```bash
# Clone repository
git clone <repo>
cd mif-ingest-to-lakehouse-infra-dev_v2

# Copy environment files
cp backend/.env.example backend/.env.local
cp frontend/.env.example frontend/.env.local
cp .env.local.example .env.local

# Edit .env.local and add GitHub OAuth credentials
```

### Step 2: Start Services

```bash
# Start all services (PostgreSQL, Redis, Backend, Frontend)
docker-compose up

# In another terminal, verify services
curl http://localhost:8000/health           # Backend health
curl http://localhost:6379                  # Redis (should be open)
psql -h localhost -U minerva_user -d minerva_agent_db  # PostgreSQL
```

### Step 3: Verify Setup

```bash
# Backend logs should show:
# INFO:     Uvicorn running on http://0.0.0.0:8000

# Frontend logs should show:
#   VITE v4.x.x  ready in XXX ms
#   Local: http://localhost:5173

# Open browser:
# Backend: http://localhost:8000
# Frontend: http://localhost:5173
```

### Step 4: Run Tests

```bash
# Backend tests
docker-compose exec backend pytest tests/ -v

# Frontend tests
docker-compose exec frontend npm run test

# View coverage
docker-compose exec backend pytest tests/ --cov=backend --cov-report=html
```

---

## Option 2: Local Development (Manual Setup)

### Step 1: Backend Setup

```bash
# Create Python virtual environment
python -m venv venv

# Activate venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install backend dependencies
cd backend
pip install -e .
pip install -e ".[dev]"

# Copy environment file
cp .env.example .env.local

# Edit .env.local:
# - DATABASE_URL=postgresql://localhost:5432/minerva_agent_db
# - REDIS_URL=redis://localhost:6379/0
# - Add GitHub OAuth credentials
```

### Step 2: Database Setup

```bash
# Create PostgreSQL database
createdb -U postgres minerva_agent_db

# Or use psql
psql -U postgres
CREATE DATABASE minerva_agent_db;
CREATE USER minerva_user WITH PASSWORD 'minerva_password';
GRANT ALL PRIVILEGES ON DATABASE minerva_agent_db TO minerva_user;
```

### Step 3: Start Redis

```bash
# Start Redis server
redis-server

# Or Docker:
docker run -d -p 6379:6379 redis:7-alpine
```

### Step 4: Run Backend

```bash
cd backend

# Run migrations (Phase-1)
alembic upgrade head

# Start backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Backend should be available at http://localhost:8000
```

### Step 5: Frontend Setup

```bash
# Open another terminal
cd frontend

# Install dependencies
npm install

# Copy environment file
cp .env.example .env.local

# Start development server
npm run dev

# Frontend should be available at http://localhost:5173
```

### Step 6: Run Tests

```bash
# Backend tests (in backend directory)
pytest tests/ -v
pytest tests/unit/ -v
pytest tests/integration/ -v

# Frontend tests (in frontend directory)
npm run test
npm run test -- --coverage
```

---

## Development Workflow

### Phase-1 Scope

**DO:**
- Implement GitHub OAuth (backend/auth/)
- Implement Session Service (backend/services/session.py)
- Create Session persistence (backend/database/, backend/repositories/)
- Write unit tests (backend/tests/unit/)
- Write integration tests (backend/tests/integration/)
- Add environment configuration
- Update CI/CD workflows

**DON'T:**
- Implement LangGraph nodes (Phase-4)
- Implement Knowledge layer (Phase-3)
- Build full API layer (Phase-5)
- Build frontend components (Phase-6)

### Committing Changes

1. Create feature branch from `develop`
   ```bash
   git checkout -b feature/oauth-session
   ```

2. Make changes with tests
   ```bash
   # Write code
   # Write tests
   # Run tests locally
   pytest tests/ -v
   npm run test
   ```

3. Commit with traceability
   ```bash
   git commit -m "STEP-1.2: Implement GitHub OAuth callback
   
   - Reference: STEP-2 Section 2, Architecture OAuth
   - Files: backend/auth/github.py, backend/models/user.py
   - Tests: tests/unit/auth/test_github.py
   - Exit Criteria: OAuth callback test PASS
   "
   ```

4. Push and create PR
   ```bash
   git push origin feature/oauth-session
   ```

5. PR checks:
   - ✓ CI pipeline passes (tests, coverage, linting)
   - ✓ Architecture compliance check passes
   - ✓ Code ownership validation passes (Phase-1 scope only)
   - ✓ DTO compatibility check passes
   - ✓ Review from code owner

---

## Architecture Compliance

### Files Allowed in Phase-1

```
backend/auth/           ✓ OAuth implementation
backend/core/           ✓ Core utilities
backend/database/       ✓ DB config, connections
backend/models/         ✓ ORM models (users, sessions)
backend/repositories/   ✓ Session repository
backend/schemas/        ✓ DTOs (UserDTO, SessionDTO)
backend/services/       ✓ Session service
backend/tests/          ✓ Unit & integration tests
.github/                ✓ CI/CD workflows
```

### Files NOT Allowed in Phase-1

```
backend/graph/          ✗ LangGraph nodes (Phase-4)
backend/api/            ✗ Full API layer (Phase-5)
frontend/src/           ✗ Frontend components (Phase-6)
```

### Verification

Before committing:

```bash
# Check no deviations
git diff --name-only

# Expected: only backend/auth/, backend/database/, backend/services/, etc.
# NOT backend/graph/, backend/api/, frontend/src/
```

---

## Troubleshooting

### PostgreSQL Connection Error

```
psycopg2.OperationalError: could not connect to server
```

**Fix:**
```bash
# Check PostgreSQL is running
# Option 1: Verify service
sudo systemctl status postgresql

# Option 2: Start PostgreSQL manually
# macOS: brew services start postgresql
# Windows: Check PostgreSQL Service in Services

# Option 3: Use Docker
docker run -d -p 5432:5432 -e POSTGRES_PASSWORD=minerva_password postgres:15-alpine
```

### Redis Connection Error

```
redis.exceptions.ConnectionError: Error 111 connecting to localhost:6379
```

**Fix:**
```bash
# Check Redis is running
redis-cli ping

# Should return: PONG

# If not running:
redis-server

# Or Docker:
docker run -d -p 6379:6379 redis:7-alpine
```

### Tests Failing

```bash
# Run with verbose output
pytest tests/ -vv --tb=short

# Run specific test
pytest tests/unit/auth/test_github.py::test_oauth_callback -vv

# Run with logging
pytest tests/ -vv --log-cli-level=DEBUG
```

### Database Schema Out of Sync

```bash
# Rollback migrations
alembic downgrade -1

# Reapply migrations
alembic upgrade head

# Verify schema
psql -d minerva_agent_db -c "\dt"
```

---

## Useful Commands

### Backend

```bash
# Run specific test module
pytest tests/unit/session/test_session_service.py -v

# Run tests matching pattern
pytest -k "test_create_session" -v

# Generate coverage report
pytest tests/ --cov=backend --cov-report=html
open htmlcov/index.html

# Format code with black
black backend/

# Check types with mypy
mypy backend/ --ignore-missing-imports

# Lint with flake8
flake8 backend/
```

### Frontend

```bash
# Run specific test
npm run test -- --testPathPattern=auth

# Run with coverage
npm run test -- --coverage

# Format code
npm run format

# Lint code
npm run lint

# Build for production
npm run build
```

### Database

```bash
# Connect to PostgreSQL
psql -d minerva_agent_db

# List tables
\dt

# Show table schema
\d sessions

# Run SQL file
psql -d minerva_agent_db -f migrations.sql
```

---

## Phase-1 Exit Criteria Checklist

Before requesting Phase-2 authorization:

- [ ] GitHub OAuth implementation complete
- [ ] GitHub OAuth callback handler working
- [ ] Session Service implemented
- [ ] Session table created and migrated
- [ ] Session repository (ORM) working
- [ ] Session persistence verified
- [ ] Session restore working
- [ ] Health endpoint responding
- [ ] Environment configuration validated
- [ ] Redis connectivity verified
- [ ] Database connectivity verified
- [ ] Logging foundation setup
- [ ] Error handling implemented
- [ ] Unit tests all PASS
- [ ] Integration tests all PASS
- [ ] Coverage report generated (>80%)
- [ ] CI pipeline runs successfully
- [ ] Docker Compose runs successfully
- [ ] No architecture deviations found
- [ ] No security vulnerabilities found

Once all items checked:

```bash
# Phase-1 Complete
# Request authorization for Phase-2
```

---

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Redis Documentation](https://redis.io/documentation)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [React Documentation](https://react.dev/)
- [Redux Toolkit Documentation](https://redux-toolkit.js.org/)

---

**Last Updated:** 2026-06-20

**Phase:** 1 (OAuth + Session Persistence)

**Questions?** See README.md or contact Architecture Team
