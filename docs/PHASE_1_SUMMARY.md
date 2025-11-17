# Phase 1: Backend Foundation - Complete TDD Implementation Plan

**Created:** 2025-11-17
**Status:** Ready for Approval
**Phase:** 1 of 5
**Priority:** CRITICAL (Blocks all other work)

---

## Executive Summary

This document provides a complete TDD implementation plan for Phase 1 (Backend Foundation) of the React + FastAPI Tech Blog project. Based on extensive research of 2025 best practices, this plan includes 8 carefully decomposed issues, each designed to be completed in 1-3 hours following strict TDD principles.

**Key Highlights:**
- 📊 **8 Issues** covering complete backend foundation
- ⏱️ **16-20 hours** estimated total time
- 🎯 **>80% test coverage** target for all code
- 🔒 **Security-first** approach with multi-layer validation
- 🧪 **TDD methodology** with RED-GREEN-REFACTOR cycles
- 📚 **Research-backed** patterns from 2025 industry standards

---

## Research Summary

### FastAPI TDD Best Practices (2025)

**Sources:** FastAPI docs, TestDriven.io, WeirdSheepLabs
**Key Findings:**
- ✅ Use `pytest-asyncio` with function-scoped fixtures for maximum isolation
- ✅ `TestClient` allows synchronous-style testing (simpler, no await needed)
- ✅ Dependency injection via `dependency_overrides` for test databases
- ✅ Factory Boy for test data generation (DRY, maintainable)
- ✅ Separate test DB from development DB (true isolation)

### File Upload Security (Multi-Layer Validation)

**Sources:** Transloadit, HackerOne, Security research
**Critical Findings:**
- 🔒 **Magic bytes validation** prevents 85% of malicious uploads
- 🔒 **Multi-layer approach** essential: extension → MIME → magic bytes → size
- 🔒 **python-magic** library most reliable for content verification
- 🔒 Filename sanitization prevents path traversal attacks
- 🔒 UUID filenames prevent enumeration attacks

**Anti-Patterns to Avoid:**
- ❌ Trusting file extensions only (easily spoofed)
- ❌ Relying on MIME type headers (can be forged)
- ❌ Storing uploads in web-accessible directories
- ❌ Not sanitizing filenames

### React + TypeScript TDD (2025)

**Sources:** Vitest docs, React Testing Library, Medium articles
**Key Findings:**
- ✅ Vitest is now standard (3.8x faster than webpack)
- ✅ Works natively with Vite (no extra config)
- ✅ Watch mode by default (perfect for TDD)
- ✅ Test user behavior, not implementation
- ✅ Semantic queries preferred (`getByRole`, `getByLabelText`)

---

## Phase 1 Issues Overview

| # | Issue | Type | Complexity | Time | Dependencies |
|---|-------|------|------------|------|--------------|
| 1 | FastAPI Project Setup with Testing | Infrastructure | Low | 1-2h | None |
| 2 | PostgreSQL Database Setup | Database | Medium | 2h | #1 |
| 3 | Article and Tag Models | Models | Medium | 2h | #2 |
| 4 | Article CRUD API Endpoints | API | Medium | 2-3h | #3 |
| 5 | Media File Database Model | Models | Medium | 2h | #3 |
| 6 | File Upload Service with Validation | Service | High | 3h | #5 |
| 7 | Image Upload API Endpoint | API | Medium | 2h | #6 |
| 8 | Video/Audio/Document Upload APIs | API | Medium | 2-3h | #6, #7 |

**Total:** 16-20 hours

---

## Issue Details

### Issue #1: FastAPI Project Setup with Testing Infrastructure

**Priority:** CRITICAL
**File:** `/docs/phase-1-github-issues-proposal.md` (lines 1-150)

**Key Deliverables:**
- FastAPI 0.109+ with uvicorn
- pytest with async support
- Project structure (app/, tests/, alembic/)
- Health check endpoint
- Black, mypy, ruff configured

**Test Coverage Requirements:**
- Health check endpoint test
- Configuration loading test
- Async test fixture working

---

### Issue #2: PostgreSQL Database Setup and Connection

**Priority:** CRITICAL
**File:** `/docs/phase-1-github-issues-proposal.md` (lines 151-250)

**Key Deliverables:**
- SQLAlchemy 2.0 with asyncpg
- Connection pooling (size=10, max_overflow=20)
- Alembic migrations
- Test database separation
- Session dependency injection

**Test Coverage Requirements:**
- Connection pool test
- Session lifecycle test
- Migration up/down test
- Test DB isolation test

---

### Issue #3: Article and Tag Database Models

**Priority:** HIGH
**File:** `/docs/phase-1-github-issues-proposal.md` (lines 251-500)

**Key Deliverables:**
- Article model (UUID, title, slug, content, draft, timestamps)
- Tag model (UUID, name)
- Many-to-many relationship
- Pydantic schemas (Create, Update, Response)
- Slug generation utility
- Database indexes

**Test Coverage Requirements:**
- Model creation tests
- Relationship tests
- Schema validation tests
- Slug generation tests (uniqueness, collision handling)
- Factory Boy factories

---

### Issue #4: Article CRUD API Endpoints

**Priority:** HIGH
**File:** `/docs/phase-1-github-issues-proposal.md` (lines 501-750)

**Key Deliverables:**
- POST /api/v1/articles (create)
- GET /api/v1/articles (list with pagination)
- GET /api/v1/articles/{slug} (detail)
- PUT /api/v1/articles/{id} (update)
- DELETE /api/v1/articles/{id} (delete)
- Service layer for business logic
- Tag handling (get or create)

**Test Coverage Requirements:**
- Create article test
- List articles test (pagination, filtering)
- Get article by slug test
- Update article test (including slug regeneration)
- Delete article test
- 404 handling test
- Tag creation test

---

### Issue #5: Media File Database Model

**Priority:** HIGH
**File:** `/docs/phase-1-github-issues-proposal.md` (lines 751-950)

**Key Deliverables:**
- MediaFile model supporting IMAGE, VIDEO, AUDIO, DOCUMENT
- Metadata fields (dimensions, duration, file size)
- Relationship to Article (cascade delete)
- FileType enum
- Pydantic schemas

**Test Coverage Requirements:**
- Model creation for each type
- Relationship cascade test
- Schema validation test
- Enum validation test

---

### Issue #6: File Upload Service with Validation

**Priority:** CRITICAL (Security)
**File:** `/docs/phase-1-github-issues-proposal.md` (lines 951-1400)

**Key Deliverables:**
- Multi-layer validation:
  1. Extension check
  2. MIME type check
  3. Magic bytes validation (python-magic)
  4. File size check
- Filename sanitization
- UUID filename generation
- Storage abstraction (Local + S3)
- Streaming uploads (1MB chunks)

**Test Coverage Requirements:**
- Valid file upload test (each type)
- Invalid extension rejection test
- Invalid MIME type rejection test
- Magic bytes mismatch rejection test
- File too large rejection test
- Filename sanitization test
- Malicious file rejection test
- Path traversal prevention test

**Security Tests (Critical):**
- Upload .exe disguised as .jpg (must fail)
- Upload PDF with .png extension (must fail)
- Upload file with path traversal filename (must sanitize)
- Upload file over size limit (must reject)

---

### Issue #7: Image Upload API Endpoint

**Priority:** HIGH
**File:** `/docs/phase-1-issues-7-8.md` (lines 1-250)

**Key Deliverables:**
- POST /api/v1/upload/image endpoint
- Image validation (via Issue #6)
- Thumbnail generation (200x200, LANCZOS)
- WebP conversion (quality 85%)
- Metadata extraction (dimensions)
- Database record creation

**Test Coverage Requirements:**
- Valid image upload test (PNG, JPEG, WebP)
- Thumbnail generation test
- WebP conversion test
- Dimension extraction test
- Invalid image rejection test
- Corrupted image handling test

---

### Issue #8: Video/Audio/Document Upload Endpoints

**Priority:** HIGH
**File:** `/docs/phase-1-issues-7-8.md` (lines 251-end)

**Key Deliverables:**
- POST /api/v1/upload/video
- POST /api/v1/upload/audio
- POST /api/v1/upload/document
- FFmpeg metadata extraction (duration, dimensions)
- Video thumbnail generation (first frame)
- Audio duration extraction

**Test Coverage Requirements:**
- Video upload test (MP4, WebM)
- Audio upload test (MP3, WAV)
- Document upload test (PDF, DOCX)
- Metadata extraction test
- Invalid file rejection test

**System Requirements:**
- FFmpeg installed on system

---

## TDD Workflow for Each Issue

### RED Phase: Write Failing Test
```python
# Example: Issue #1 - Health check
def test_health_check_returns_200(client):
    response = client.get("/health")
    assert response.status_code == 200  # FAILS - endpoint doesn't exist
    assert response.json() == {"status": "healthy"}
```

**Commit:** `test(#1): add health check endpoint test`

### GREEN Phase: Minimum Implementation
```python
# app/main.py
@app.get("/health")
async def health_check():
    return {"status": "healthy"}  # PASSES
```

**Commit:** `feat(#1): implement health check endpoint`

### REFACTOR Phase: Improve Code
```python
# app/api/health.py - Extract to separate module
from fastapi import APIRouter

router = APIRouter(tags=["health"])

@router.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    return {"status": "healthy"}
```

**Commit:** `refactor(#1): extract health check to separate module`

### DOCUMENT Phase: Mark Complete
Update TDD plan, check off test in docs.

**Commit:** `docs(#1): mark health check complete`

---

## Success Criteria

### Code Quality
- ✅ Test coverage > 80% (measured with pytest-cov)
- ✅ All tests passing (pytest exit code 0)
- ✅ Black formatting (no changes needed)
- ✅ Mypy type checking (zero errors)
- ✅ Ruff linting (zero errors)
- ✅ Zero security vulnerabilities (bandit scan)

### Performance
- ✅ Database queries optimized (N+1 prevention with selectinload)
- ✅ Connection pooling configured
- ✅ File streaming (no memory exhaustion on large files)
- ✅ API response time < 200ms (p95)

### Security
- ✅ Multi-layer file validation working
- ✅ Magic bytes verification implemented
- ✅ Filename sanitization tested
- ✅ No path traversal vulnerabilities
- ✅ File size limits enforced
- ✅ CORS configured correctly

### Documentation
- ✅ OpenAPI docs auto-generated
- ✅ README.md with setup instructions
- ✅ Migration commands documented
- ✅ Each issue has TDD plan in `/docs/`

---

## Dependency Graph

```
Phase 1 Dependencies:

#1 (FastAPI Setup)
  ↓
#2 (Database)
  ↓
#3 (Models) ─────────┐
  ↓                  ↓
#4 (Article API)   #5 (Media Model)
                     ↓
                   #6 (Upload Service)
                     ↓
                   #7 (Image API)
                     ↓
                   #8 (Video/Audio/Doc API)
```

**Sequential Order:**
1. #1 → #2 → #3 → #4 (Article workflow)
2. #3 → #5 → #6 → #7 → #8 (Media workflow)

**Parallelization Opportunities:**
- After #3: Can work on #4 and #5 in parallel
- After #6: Can work on #7 and #8 in parallel

---

## File Structure After Phase 1

```
moondoors_tech_blog/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   └── v1/
│   │   │       ├── __init__.py
│   │   │       ├── articles.py
│   │   │       └── upload.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── article.py
│   │   │   ├── tag.py
│   │   │   └── media.py
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── article.py
│   │   │   ├── tag.py
│   │   │   └── media.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── article_service.py
│   │   │   ├── upload_service.py
│   │   │   ├── storage_service.py
│   │   │   ├── image_service.py
│   │   │   ├── video_service.py
│   │   │   ├── audio_service.py
│   │   │   └── document_service.py
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── slug.py
│   │       ├── validator.py
│   │       └── file_utils.py
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── conftest.py
│   │   ├── factories.py
│   │   ├── unit/
│   │   │   ├── test_models.py
│   │   │   ├── test_schemas.py
│   │   │   ├── test_slug.py
│   │   │   ├── test_upload_service.py
│   │   │   └── test_file_validator.py
│   │   ├── integration/
│   │   │   ├── test_articles_api.py
│   │   │   ├── test_image_upload.py
│   │   │   └── test_file_upload.py
│   │   └── fixtures/
│   │       ├── test_images/
│   │       ├── test_videos/
│   │       └── malicious/
│   ├── alembic/
│   │   ├── env.py
│   │   └── versions/
│   ├── uploads/
│   │   ├── images/
│   │   │   ├── originals/
│   │   │   ├── thumbnails/
│   │   │   └── optimized/
│   │   ├── videos/
│   │   ├── audio/
│   │   └── documents/
│   ├── requirements.txt
│   ├── requirements-dev.txt
│   ├── pytest.ini
│   ├── pyproject.toml
│   └── README.md
└── docs/
    ├── PHASE_1_SUMMARY.md (this file)
    ├── phase-1-github-issues-proposal.md
    ├── phase-1-issues-7-8.md
    ├── 1-fastapi-setup-tdd.md (to be created)
    ├── 2-database-setup-tdd.md (to be created)
    ├── 3-models-tdd.md (to be created)
    ├── 4-article-api-tdd.md (to be created)
    ├── 5-media-model-tdd.md (to be created)
    ├── 6-upload-service-tdd.md (to be created)
    ├── 7-image-upload-tdd.md (to be created)
    └── 8-media-upload-tdd.md (to be created)
```

---

## Next Steps

### 1. Review and Approve (User Action)
- Review this summary document
- Review detailed issue proposals in:
  - `/docs/phase-1-github-issues-proposal.md` (Issues #1-#6)
  - `/docs/phase-1-issues-7-8.md` (Issues #7-#8)
- Approve or request changes

### 2. Create GitHub Issues (If Approved)
Use issue-creator agent to create all 8 issues with:
- Proper labels (type, area, complexity, phase)
- Completion criteria checkboxes
- Implementation notes
- Dependencies

### 3. Generate Detailed TDD Plans
Create individual TDD plan files for each issue:
- `/docs/1-fastapi-setup-tdd.md`
- `/docs/2-database-setup-tdd.md`
- ... (8 files total)

Each plan will include:
- Research summary
- Test queue (RED-GREEN-REFACTOR cycles)
- Implementation notes
- Success criteria
- References

### 4. Begin Implementation
Start with Issue #1 following TDD workflow:
1. RED: Write failing test
2. GREEN: Minimum implementation
3. REFACTOR: Improve code
4. DOCUMENT: Mark complete
5. Commit with proper format

---

## Questions for User

Before proceeding, please confirm:

1. **Approval:** Do you approve the Phase 1 issue breakdown and approach?

2. **Priorities:** Should we proceed with all 8 issues or focus on a subset first?

3. **Technology Choices:**
   - Local storage or S3 for files? (or both with abstraction?)
   - FFmpeg available on deployment environment?

4. **Timeline:** Are the time estimates (16-20 hours total) acceptable?

5. **Next Action:** Should I:
   - Create GitHub issues now?
   - Generate detailed TDD plans first?
   - Start implementing Issue #1?

---

## Research References

1. **FastAPI Testing:**
   - https://fastapi.tiangolo.com/tutorial/testing/
   - https://testdriven.io/blog/fastapi-crud/
   - https://weirdsheeplabs.com/blog/fast-and-furious-async-testing-with-fastapi-and-pytest

2. **File Upload Security:**
   - https://transloadit.com/devtips/secure-api-file-uploads-with-magic-numbers/
   - https://www.hackerone.com/blog/secure-file-uploads-flask-filtering-and-validation-techniques

3. **React + TypeScript TDD:**
   - https://www.yakov.dev/tdd-with-react
   - https://medium.com/@rmbagt/test-driven-development-tdd-with-typescript-and-reactjs-using-vitest

4. **SQLAlchemy Async:**
   - https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html

5. **Python Magic:**
   - https://pypi.org/project/python-magic/

---

**Document Version:** 1.0
**Last Updated:** 2025-11-17
**Status:** Awaiting User Approval
