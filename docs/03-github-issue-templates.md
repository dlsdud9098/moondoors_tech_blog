# GitHub Issue Templates Preview

This document shows what the GitHub issues will look like when created. These are samples from Phase 1 and Phase 2 to demonstrate the format.

---

## Issue #1: FastAPI Project Setup with Testing Infrastructure

**Labels:** `feature`, `backend/infrastructure`, `phase-1`, `complexity:low`

### Description
Initialize FastAPI project with Python 3.11+, configure development tools (pytest, black, mypy), set up testing infrastructure, and establish project structure. This provides the foundation for backend development with TDD methodology.

### Completion Criteria
- [ ] FastAPI 0.109+ project initialized
- [ ] Python virtual environment configured
- [ ] pytest with async support configured
- [ ] Project structure created (app/, tests/, alembic/)
- [ ] Requirements files created (requirements.txt, requirements-dev.txt)
- [ ] Basic health check endpoint works
- [ ] All setup tests pass
- [ ] README.md documents setup process

### Implementation Notes

**Files to Create:**
- `backend/app/main.py` - FastAPI application
- `backend/app/config.py` - Configuration management
- `backend/requirements.txt` - Production dependencies
- `backend/requirements-dev.txt` - Development dependencies
- `backend/pytest.ini` - Pytest configuration
- `backend/tests/conftest.py` - Test fixtures
- `backend/.env.example` - Environment variables template
- `backend/README.md` - Setup documentation

**Key Dependencies:**
```txt
# requirements.txt
fastapi==0.109.0
uvicorn[standard]==0.27.0
pydantic==2.5.0
pydantic-settings==2.1.0
python-multipart==0.0.6

# requirements-dev.txt
pytest==7.4.3
pytest-asyncio==0.21.1
pytest-cov==4.1.0
httpx==0.26.0
black==23.12.1
mypy==1.7.1
ruff==0.1.8
```

**Patterns from Research:**
- Use Pydantic Settings for configuration management
- Async/await pattern for all endpoints
- Structured logging from the start
- Health check endpoint for monitoring

**Testing Strategy:**
- Verify FastAPI app starts successfully
- Test health check endpoint returns 200
- Test pytest configuration works
- Verify all dev tools (black, mypy, ruff) run without errors

### Dependencies
None (first issue)

### Estimated Time
1-2 hours

### References
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [pytest-asyncio](https://pytest-asyncio.readthedocs.io/)

---

## Issue #4: Article CRUD API Endpoints

**Labels:** `feature`, `backend/api`, `phase-1`, `complexity:medium`

### Description
Implement RESTful API endpoints for article CRUD operations (Create, Read, Update, Delete) with pagination, filtering, and proper error handling. Use service layer pattern for business logic separation.

### Completion Criteria
- [ ] POST /api/v1/articles - Create article
- [ ] GET /api/v1/articles - List articles (paginated)
- [ ] GET /api/v1/articles/{slug} - Get article by slug
- [ ] PUT /api/v1/articles/{id} - Update article
- [ ] DELETE /api/v1/articles/{id} - Delete article
- [ ] Pagination working (page, size parameters)
- [ ] Draft/published filtering
- [ ] All API tests pass
- [ ] API documentation auto-generated (OpenAPI/Swagger)

### Implementation Notes

**Files to Create:**
- `backend/app/api/articles.py` - Article endpoints
- `backend/app/services/article_service.py` - Business logic
- `backend/tests/integration/test_articles_api.py` - Integration tests

**API Endpoints:**
```python
@router.post("/", response_model=ArticleResponse, status_code=201)
async def create_article(article: ArticleCreate, db: AsyncSession)

@router.get("/", response_model=list[ArticleResponse])
async def list_articles(page: int, size: int, draft: bool | None, db: AsyncSession)

@router.get("/{slug}", response_model=ArticleResponse)
async def get_article(slug: str, db: AsyncSession)

@router.put("/{id}", response_model=ArticleResponse)
async def update_article(id: UUID, article: ArticleUpdate, db: AsyncSession)

@router.delete("/{id}", status_code=204)
async def delete_article(id: UUID, db: AsyncSession)
```

**Service Layer Pattern:**
- Separate business logic from API routing
- Use slug for article URLs (SEO-friendly)
- Implement pagination with offset/limit
- Proper HTTP status codes (201 for create, 404 for not found)

**Testing Strategy:**
- Test create article returns 201 and correct data
- Test list articles with pagination
- Test get article by slug
- Test get article with invalid slug returns 404
- Test update article
- Test delete article
- Test draft filtering works correctly

### Dependencies
- Issue #3 (Models and schemas needed)

### Estimated Time
2-3 hours

### References
- [FastAPI Path Operations](https://fastapi.tiangolo.com/tutorial/path-params/)
- [RESTful API Design Best Practices](https://restfulapi.net/)

---

## Issue #6: File Upload Service with Validation

**Labels:** `feature`, `backend/services`, `phase-1`, `complexity:high`

### Description
Implement comprehensive file upload service with multi-layer validation (extension, MIME type, content-based magic bytes), file size limits, filename sanitization, and storage abstraction layer supporting both local filesystem and S3-compatible storage.

### Completion Criteria
- [ ] File validation implemented (extension, MIME, magic bytes)
- [ ] File size limits enforced per file type
- [ ] Filename sanitization prevents path traversal
- [ ] Local storage backend implemented
- [ ] S3 storage backend implemented (optional for MVP)
- [ ] Storage abstraction layer created
- [ ] All validation tests pass
- [ ] Security tests pass (malicious files rejected)

### Implementation Notes

**Files to Create:**
- `backend/app/services/upload_service.py` - Upload logic
- `backend/app/services/storage_service.py` - Storage abstraction
- `backend/app/utils/validator.py` - File validation utilities
- `backend/app/utils/file_utils.py` - File utilities
- `backend/tests/unit/test_upload_service.py` - Unit tests
- `backend/tests/integration/test_file_upload.py` - Integration tests

**Key Dependencies:**
```txt
python-magic==0.4.27  # Content-based file type detection
nh3==0.2.15           # HTML/Markdown sanitization
aiofiles==23.2.1      # Async file operations
Pillow==10.1.0        # Image processing
boto3==1.34.14        # Optional: S3 support
```

**Validation Layers (Security-Critical):**

1. **File Extension Check** - Quick initial filter
   - Reject files with dangerous extensions
   - Case-insensitive comparison

2. **MIME Type Check** - Content-Type header validation
   - Compare against allowed MIME types per file category
   - First line of defense

3. **Content-Based Validation** - Magic bytes inspection
   - Use python-magic to detect actual file type
   - Prevent extension spoofing attacks
   - Read first 2048 bytes for detection

4. **File Size Limits** - Prevent DoS attacks
   - Image: 10 MB max
   - Video: 100 MB max
   - Audio: 20 MB max
   - Document: 10 MB max

5. **Filename Sanitization** - Path traversal prevention
   - Remove directory traversal sequences (../, ..\)
   - Generate UUID-based filenames
   - Preserve original filename in metadata

**Storage Abstraction Pattern:**
- Abstract base class `StorageBackend`
- `LocalStorage` implementation for development
- `S3Storage` implementation for production (optional)
- Configuration-based backend selection
- Consistent interface for save/delete/get_url

**Testing Strategy:**
- Test valid file uploads for all types
- Test file extension validation rejects invalid extensions
- Test MIME type validation
- Test magic bytes detection catches spoofed files
- Test file size limits enforced
- Test filename sanitization prevents path traversal
- Test storage abstraction works with different backends
- Security test: upload file with .jpg extension but actually .exe content (should reject)
- Security test: upload file with "../" in filename (should sanitize)

### Dependencies
- Issue #5 (Media model needed for database records)

### Estimated Time
3 hours

### References
- [OWASP File Upload Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html)
- [FastAPI File Uploads](https://fastapi.tiangolo.com/tutorial/request-files/)
- [python-magic Documentation](https://github.com/ahupp/python-magic)

---

## Issue #9: React + Vite Project Setup with Testing

**Labels:** `feature`, `frontend/infrastructure`, `phase-2`, `complexity:low`

### Description
Initialize React project with Vite for fast development, TypeScript for type safety, configure comprehensive testing infrastructure (Vitest for unit/integration, React Testing Library for components, Playwright for E2E), and establish clean project structure.

### Completion Criteria
- [ ] React 18+ with Vite initialized
- [ ] TypeScript configured (strict mode enabled)
- [ ] Tailwind CSS configured and working
- [ ] Vitest and React Testing Library set up
- [ ] Playwright configured for E2E tests
- [ ] ESLint and Prettier configured
- [ ] Project structure created (components, pages, services, hooks)
- [ ] All setup tests pass
- [ ] README.md documents setup and available scripts

### Implementation Notes

**Files to Create:**
- `frontend/package.json` - Dependencies and scripts
- `frontend/vite.config.ts` - Vite configuration
- `frontend/vitest.config.ts` - Vitest configuration
- `frontend/playwright.config.ts` - Playwright configuration
- `frontend/tsconfig.json` - TypeScript configuration (strict mode)
- `frontend/tailwind.config.js` - Tailwind CSS configuration
- `frontend/.eslintrc.json` - ESLint rules
- `frontend/.prettierrc` - Prettier configuration
- `frontend/src/main.tsx` - App entry point
- `frontend/src/App.tsx` - Root component
- `frontend/src/vite-env.d.ts` - Vite type declarations
- `frontend/README.md` - Setup documentation

**Key Dependencies:**
```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.21.0",
    "@tanstack/react-query": "^5.17.0"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.2.1",
    "vite": "^5.0.10",
    "typescript": "^5.3.3",
    "vitest": "^1.1.0",
    "@testing-library/react": "^14.1.2",
    "@testing-library/jest-dom": "^6.1.5",
    "@testing-library/user-event": "^14.5.1",
    "@playwright/test": "^1.40.1",
    "tailwindcss": "^3.4.0",
    "autoprefixer": "^10.4.16",
    "postcss": "^8.4.32",
    "eslint": "^8.56.0",
    "eslint-plugin-react": "^7.33.2",
    "eslint-plugin-react-hooks": "^4.6.0",
    "prettier": "^3.1.1",
    "msw": "^2.0.11"
  }
}
```

**Project Structure:**
```
frontend/
├── src/
│   ├── components/
│   │   ├── common/
│   │   ├── layout/
│   │   ├── article/
│   │   └── editor/
│   ├── pages/
│   ├── hooks/
│   ├── services/
│   ├── types/
│   ├── utils/
│   ├── styles/
│   ├── App.tsx
│   └── main.tsx
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── public/
├── package.json
├── vite.config.ts
├── vitest.config.ts
├── playwright.config.ts
├── tsconfig.json
├── tailwind.config.js
└── README.md
```

**Patterns from Research:**
- Use Vite for 3.8x faster development than webpack
- Enable TypeScript strict mode from the start
- Configure Vitest with jsdom environment for DOM testing
- Set up MSW (Mock Service Worker) for API mocking in tests
- Use Tailwind CSS for rapid UI development

**Testing Strategy:**
- Test that Vite dev server starts successfully
- Test that TypeScript compilation works
- Test sample component renders
- Test ESLint and Prettier run without errors
- Verify Playwright can run a basic E2E test

### Dependencies
None (first frontend issue)

### Estimated Time
1-2 hours

### References
- [Vite Documentation](https://vitejs.dev/)
- [Vitest Documentation](https://vitest.dev/)
- [React Testing Library](https://testing-library.com/react)
- [Playwright Documentation](https://playwright.dev/)

---

## Issue #12: Article List Page with Pagination

**Labels:** `feature`, `frontend/ui`, `phase-2`, `complexity:medium`

### Description
Create home page displaying list of articles with pagination, comprehensive loading states, error handling, and responsive grid layout. Implement optimistic UI updates with React Query for better user experience.

### Completion Criteria
- [ ] Article list displays correctly with all required data
- [ ] Pagination controls working (prev/next, page numbers)
- [ ] Loading state displayed with skeleton loaders
- [ ] Error state handled with retry button
- [ ] Empty state shown when no articles exist
- [ ] Responsive grid (1 col mobile, 2 col tablet, 3 col desktop)
- [ ] All component tests pass (ArticleCard, ArticleList, Pagination)
- [ ] E2E test verifies complete article listing flow

### Implementation Notes

**Files to Create:**
- `frontend/src/pages/Home.tsx` - Home page container
- `frontend/src/components/article/ArticleCard.tsx` - Individual article card
- `frontend/src/components/article/ArticleList.tsx` - Article grid container
- `frontend/src/components/common/Pagination.tsx` - Pagination controls
- `frontend/src/components/common/Loading.tsx` - Loading spinner
- `frontend/src/components/common/SkeletonCard.tsx` - Skeleton loader
- `frontend/src/components/common/ErrorMessage.tsx` - Error display
- `frontend/tests/unit/components/article/ArticleCard.test.tsx`
- `frontend/tests/unit/components/article/ArticleList.test.tsx`
- `frontend/tests/unit/components/common/Pagination.test.tsx`
- `frontend/tests/e2e/article-list.spec.ts`

**ArticleCard Features:**
- Display title, description, excerpt
- Show tags as badges
- Display creation date (formatted)
- Display reading time estimate
- Hover effects for better UX
- Click navigates to article detail

**Pagination Features:**
- Previous/Next buttons
- Page number indicators
- Disable prev/next at boundaries
- Show current page
- Keyboard navigation support (arrow keys)

**Loading States:**
- Skeleton loaders while fetching
- Smooth transitions
- Prevent layout shift

**Error Handling:**
- Display friendly error message
- Retry button to refetch
- Different messages for different errors (network, 404, 500)

**Responsive Design:**
- 1 column on mobile (< 640px)
- 2 columns on tablet (640px - 1024px)
- 3 columns on desktop (>= 1024px)
- Proper spacing and gutters

**Testing Strategy:**
- Test ArticleCard renders all article data correctly
- Test ArticleCard click navigates to correct URL
- Test ArticleList renders correct number of cards
- Test ArticleList responsive grid breakpoints
- Test Pagination prev/next buttons work
- Test Pagination disables buttons at boundaries
- Test Loading component displays during data fetch
- Test ErrorMessage displays on error
- Test Empty state when no articles
- E2E test: Navigate to home, see articles, click pagination, see new page

### Dependencies
- Issue #10 (API client and React Query needed)
- Issue #11 (Router and layout needed for navigation)

### Estimated Time
2-3 hours

### References
- [React Query Pagination](https://tanstack.com/query/latest/docs/react/guides/paginated-queries)
- [Tailwind Grid](https://tailwindcss.com/docs/grid-template-columns)
- [React Testing Library Best Practices](https://kentcdodds.com/blog/common-mistakes-with-react-testing-library)

---

## Issue #15: Drag and Drop File Upload Component

**Labels:** `feature`, `frontend/ui`, `phase-3`, `complexity:medium`

### Description
Create reusable drag-and-drop file upload component using react-dropzone with support for multiple files, file type restrictions, size validation, upload progress, and preview thumbnails. Integrate with backend upload API.

### Completion Criteria
- [ ] Drag and drop zone functional
- [ ] Multiple file selection supported
- [ ] File type restrictions enforced (images, videos, audio, documents)
- [ ] File size validation (client-side pre-check)
- [ ] Upload progress indicator for each file
- [ ] Preview thumbnails for images
- [ ] Error handling for failed uploads
- [ ] Remove file from queue before upload
- [ ] All component tests pass
- [ ] E2E test verifies upload flow

### Implementation Notes

**Files to Create:**
- `frontend/src/components/editor/FileUpload.tsx` - Main upload component
- `frontend/src/components/editor/DropZone.tsx` - Drag & drop zone
- `frontend/src/components/editor/FilePreview.tsx` - File preview item
- `frontend/src/components/editor/UploadProgress.tsx` - Progress bar
- `frontend/src/hooks/useFileUpload.ts` - Upload logic hook
- `frontend/src/services/upload.ts` - Upload API service
- `frontend/tests/unit/components/editor/FileUpload.test.tsx`
- `frontend/tests/e2e/file-upload.spec.ts`

**Key Dependencies:**
```json
{
  "dependencies": {
    "react-dropzone": "^14.2.3"
  }
}
```

**Features:**
- **Drag & Drop:** Visual feedback on drag over
- **Click to Browse:** Alternative file selection method
- **File Type Validation:** Accept only allowed extensions
- **File Size Validation:** Check before upload (10MB images, 100MB videos, 20MB audio, 10MB docs)
- **Multiple Files:** Queue multiple files for upload
- **Preview:** Show image thumbnails, file icons for others
- **Progress:** Individual progress bar per file
- **Error Handling:** Display errors inline per file
- **Remove Files:** Allow removing from queue before upload
- **Upload State:** Pending, uploading, success, error

**Upload Flow:**
1. User selects/drops files
2. Validate file types and sizes client-side
3. Show previews in queue
4. User clicks "Upload" button
5. Upload files one by one with progress
6. Show success/error status
7. On success, add to media library

**Testing Strategy:**
- Test drag and drop triggers file selection
- Test click to browse works
- Test file type validation rejects invalid types
- Test file size validation rejects oversized files
- Test multiple files can be selected
- Test progress indicator updates during upload
- Test error handling for failed uploads
- Test remove file from queue
- E2E test: Complete upload flow with valid and invalid files

### Dependencies
- Issue #10 (API client needed for upload service)

### Estimated Time
2-3 hours

### References
- [react-dropzone Documentation](https://react-dropzone.js.org/)
- [File Upload UX Best Practices](https://www.smashingmagazine.com/2018/01/drag-drop-file-uploader-vanilla-js/)

---

## Summary of All 35 Issues

The complete list of 35 issues across 5 phases has been prepared. Above are detailed examples from each major phase. When you approve, I will:

1. Create all 35 GitHub issues using the `issue-creator` agent
2. Generate individual TDD plans (`docs/[N]-[feature]-tdd.md`) for each issue
3. Provide issue numbers and links for tracking

**Next step:** Should I proceed with creating these GitHub issues?
