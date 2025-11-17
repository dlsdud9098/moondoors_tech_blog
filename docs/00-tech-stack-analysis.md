# Tech Blog - Technology Stack Analysis (React + FastAPI + Multimedia)

## Executive Summary

This document provides comprehensive technology stack recommendations for building a production-ready tech blog with multimedia support. The architecture uses React for the frontend, FastAPI for the backend API, and PostgreSQL for data persistence, following modern best practices and TDD methodology.

## Research Summary

### Architecture Choice: React + FastAPI

#### React 18+ (Frontend - RECOMMENDED)
**Strengths:**
- Industry-standard UI library with massive ecosystem
- Component-based architecture for reusability
- Virtual DOM for optimal performance
- Excellent developer experience with hot reload
- Strong TypeScript support
- Rich ecosystem of libraries and tools
- Flexible routing with React Router
- Battle-tested in production at scale

**Weaknesses:**
- Requires more setup than Next.js (no built-in SSR)
- SEO requires additional configuration
- Build tooling needs separate setup (Vite)

#### FastAPI (Backend - RECOMMENDED)
**Strengths:**
- Extremely fast performance (based on Starlette and Pydantic)
- Automatic API documentation (OpenAPI/Swagger)
- Built-in data validation with Pydantic
- Excellent async/await support
- Type hints provide IDE autocomplete and validation
- Easy file upload handling with python-multipart
- Modern Python 3.11+ features
- Growing ecosystem and community

**Weaknesses:**
- Younger than Django/Flask (but stable)
- Less built-in features than Django
- Requires separate ORM (SQLAlchemy)

**Rationale:** This stack provides optimal balance of performance, developer experience, type safety, and modern architecture patterns suitable for a content-rich blog with multimedia features.

## Recommended Technology Stack

### Frontend Stack

#### Core Framework
- **React 18+** - UI library
- **TypeScript 5+** - Type safety
- **Vite 5+** - Build tool and dev server (3.8x faster than webpack)
- **React Router 6** - Client-side routing

#### UI & Styling
- **Tailwind CSS 4** - Utility-first CSS framework
- **Headless UI** or **Radix UI** - Accessible component primitives
- **Lucide React** - Icon library
- **react-hot-toast** - Toast notifications

#### Content Rendering
- **react-markdown 9+** - Secure markdown rendering
- **remark-gfm** - GitHub Flavored Markdown support
- **rehype-sanitize** - HTML sanitization (XSS prevention)
- **remark-external-links** - Secure external link handling
- **Shiki** - Syntax highlighting for code blocks

#### File Upload & Media
- **react-dropzone** - Drag and drop file upload
- **@uiw/react-md-editor** - Markdown editor with preview
- **react-player** - Video player component
- **react-h5-audio-player** - Audio player component
- **react-image-gallery** - Image gallery component

#### State Management
- **Zustand** or **React Context** - Simple state management
- **TanStack Query (React Query)** - Server state management, caching
- **React Hook Form** - Form state management

#### Testing
- **Vitest** - Unit/integration test runner (3.8x faster than Jest)
- **React Testing Library** - Component testing
- **Playwright** - E2E testing
- **MSW (Mock Service Worker)** - API mocking

### Backend Stack

#### Core Framework
- **FastAPI 0.109+** - Modern Python web framework
- **Python 3.11+** - Latest Python with performance improvements
- **Uvicorn** - ASGI server for production
- **python-multipart** - File upload support

#### Database & ORM
- **PostgreSQL 15+** - Primary database (metadata, articles)
- **SQLAlchemy 2.0** or **SQLModel** - ORM with async support
- **Alembic** - Database migrations
- **asyncpg** - Async PostgreSQL driver

#### File Storage
- **Local filesystem** (development)
- **AWS S3** or **Cloudflare R2** (production)
- **boto3** - AWS SDK for S3 operations
- **Pillow (PIL)** - Image processing and optimization

#### Security & Validation
- **Pydantic V2** - Data validation and serialization
- **python-jose** - JWT token handling (if adding auth)
- **passlib** - Password hashing (if adding auth)
- **nh3** - HTML/Markdown sanitization (Rust-based, faster than bleach)
- **python-magic** - File type validation (content-based)

#### Testing
- **pytest** - Test framework
- **pytest-asyncio** - Async test support
- **httpx** - Async HTTP client for testing
- **factory-boy** - Test data generation
- **pytest-cov** - Code coverage

### Storage Strategy

#### Media Files
**Decision:** File system for development, S3-compatible storage for production

**Structure:**
```
uploads/
├── images/
│   ├── originals/          # Original uploaded images
│   ├── thumbnails/         # Generated thumbnails
│   └── optimized/          # Optimized versions (WebP, AVIF)
├── videos/
│   ├── originals/
│   └── transcoded/         # Optional: transcoded versions
├── audio/
│   └── files/
└── documents/
    └── files/
```

**Metadata Storage (PostgreSQL):**
- File paths and URLs
- MIME types and file sizes
- Upload timestamps
- Relationships to articles
- Image dimensions
- Video durations
- Processing status

#### Database Schema (Articles + Media)

```sql
-- Articles table
CREATE TABLE articles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    slug VARCHAR(255) UNIQUE NOT NULL,
    content TEXT NOT NULL,  -- Markdown content
    description TEXT,
    draft BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    published_at TIMESTAMP
);

-- Tags table
CREATE TABLE tags (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL
);

-- Article-Tag relationship
CREATE TABLE article_tags (
    article_id UUID REFERENCES articles(id) ON DELETE CASCADE,
    tag_id INTEGER REFERENCES tags(id) ON DELETE CASCADE,
    PRIMARY KEY (article_id, tag_id)
);

-- Media files table
CREATE TABLE media_files (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    article_id UUID REFERENCES articles(id) ON DELETE CASCADE,
    filename VARCHAR(255) NOT NULL,
    original_filename VARCHAR(255) NOT NULL,
    file_type VARCHAR(50) NOT NULL,  -- image, video, audio, document
    mime_type VARCHAR(100) NOT NULL,
    file_size BIGINT NOT NULL,
    file_path TEXT NOT NULL,
    url TEXT NOT NULL,
    width INTEGER,          -- For images/videos
    height INTEGER,         -- For images/videos
    duration FLOAT,         -- For videos/audio
    thumbnail_url TEXT,     -- For videos
    alt_text TEXT,          -- For images
    caption TEXT,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_article_id (article_id),
    INDEX idx_file_type (file_type)
);
```

## Essential Features Breakdown

### Priority 1: Core Backend (MVP)
1. FastAPI project setup with PostgreSQL
2. Article CRUD endpoints (create, read, update, delete)
3. Database models and migrations
4. File upload endpoint with validation
5. Basic CORS configuration

### Priority 2: Core Frontend (MVP)
1. React + Vite project setup
2. Article listing page with pagination
3. Article detail page with markdown rendering
4. Responsive design (mobile-first)
5. Basic routing

### Priority 3: Multimedia Features
1. Image upload with drag & drop
2. Image preview and gallery
3. Video upload and player
4. Audio upload and player
5. File attachment upload
6. File type and size validation

### Priority 4: Content Management
1. Markdown editor with preview
2. Draft/publish functionality
3. Tag system
4. Search functionality
5. SEO meta tags

### Priority 5: Advanced Features
1. Image optimization (thumbnails, WebP conversion)
2. Video thumbnail generation
3. Multiple file uploads per article
4. File deletion and cleanup
5. Storage quota tracking

## Architecture Decisions

### 1. Frontend-Backend Separation
**Decision:** Complete separation with REST API

**Rationale:**
- Independent scaling of frontend and backend
- Flexibility to swap frontend/backend independently
- Better development workflow (parallel teams)
- API can serve multiple clients (web, mobile)

**Trade-offs:**
- More complex deployment
- CORS configuration needed
- API authentication required for admin features

### 2. File Storage Strategy
**Decision:** Hybrid approach (local dev, S3 production)

**Rationale:**
- Local storage for development simplicity
- S3/R2 for production scalability and CDN
- Separate metadata (DB) from binary files (storage)
- Easy migration path

**Implementation:**
```python
# Storage abstraction layer
class StorageBackend(ABC):
    @abstractmethod
    async def upload_file(self, file: UploadFile, path: str) -> str:
        pass

    @abstractmethod
    async def delete_file(self, path: str) -> bool:
        pass

class LocalStorage(StorageBackend):
    # For development
    pass

class S3Storage(StorageBackend):
    # For production
    pass
```

### 3. Markdown Processing Pipeline
**Decision:** Store markdown, render on frontend

**Rationale:**
- Frontend rendering with react-markdown (secure by default)
- Backend stores raw markdown (editable)
- Separation of concerns
- Markdown can be indexed for search

**Security:**
- Sanitize markdown with nh3 on backend before storage
- Use rehype-sanitize on frontend rendering
- Block dangerous protocols (javascript:, vbscript:)

### 4. API Design Pattern
**Decision:** RESTful API with consistent patterns

**Endpoints:**
```
POST   /api/v1/articles              Create article
GET    /api/v1/articles              List articles (paginated)
GET    /api/v1/articles/{id}         Get article
PUT    /api/v1/articles/{id}         Update article
DELETE /api/v1/articles/{id}         Delete article

POST   /api/v1/upload/image          Upload image
POST   /api/v1/upload/video          Upload video
POST   /api/v1/upload/audio          Upload audio
POST   /api/v1/upload/document       Upload document

GET    /api/v1/media                 List media files
DELETE /api/v1/media/{id}            Delete media file

GET    /api/v1/tags                  List all tags
GET    /api/v1/search?q={query}      Search articles
```

## Security Best Practices

### File Upload Security

**Validation Layers:**
1. **File Extension Check** - Initial filter
2. **MIME Type Check** - Content-Type header validation
3. **Content-Based Validation** - Magic bytes inspection
4. **File Size Limits** - Prevent DoS attacks
5. **Filename Sanitization** - Prevent path traversal

**Implementation:**
```python
from fastapi import UploadFile, HTTPException
import magic
import os

ALLOWED_EXTENSIONS = {
    'image': {'.jpg', '.jpeg', '.png', '.gif', '.webp'},
    'video': {'.mp4', '.webm', '.mov'},
    'audio': {'.mp3', '.wav', '.ogg'},
    'document': {'.pdf', '.doc', '.docx'}
}

ALLOWED_MIME_TYPES = {
    'image': {'image/jpeg', 'image/png', 'image/gif', 'image/webp'},
    'video': {'video/mp4', 'video/webm', 'video/quicktime'},
    'audio': {'audio/mpeg', 'audio/wav', 'audio/ogg'},
    'document': {'application/pdf', 'application/msword'}
}

MAX_FILE_SIZES = {
    'image': 10 * 1024 * 1024,      # 10 MB
    'video': 100 * 1024 * 1024,     # 100 MB
    'audio': 20 * 1024 * 1024,      # 20 MB
    'document': 10 * 1024 * 1024    # 10 MB
}

async def validate_file(file: UploadFile, file_type: str) -> bool:
    # Check file extension
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS[file_type]:
        raise HTTPException(400, f"Invalid file extension for {file_type}")

    # Check MIME type
    if file.content_type not in ALLOWED_MIME_TYPES[file_type]:
        raise HTTPException(400, f"Invalid MIME type")

    # Check file size
    file.file.seek(0, 2)  # Seek to end
    size = file.file.tell()
    file.file.seek(0)     # Reset

    if size > MAX_FILE_SIZES[file_type]:
        raise HTTPException(400, f"File too large")

    # Content-based validation (magic bytes)
    file_data = await file.read(2048)
    await file.seek(0)

    detected_mime = magic.from_buffer(file_data, mime=True)
    if detected_mime not in ALLOWED_MIME_TYPES[file_type]:
        raise HTTPException(400, "File content doesn't match extension")

    return True
```

### Markdown Sanitization

**Backend (FastAPI):**
```python
import nh3

ALLOWED_TAGS = {
    'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'p', 'br', 'strong', 'em', 'u', 'strike',
    'ul', 'ol', 'li', 'blockquote', 'code', 'pre',
    'a', 'img', 'table', 'thead', 'tbody', 'tr', 'th', 'td'
}

ALLOWED_ATTRIBUTES = {
    'a': {'href', 'title', 'rel'},
    'img': {'src', 'alt', 'title', 'width', 'height'},
    'code': {'class'}  # For syntax highlighting
}

def sanitize_markdown(content: str) -> str:
    # Sanitize with nh3 (Rust-based, fast and secure)
    return nh3.clean(
        content,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        link_rel="noopener noreferrer"  # Security for external links
    )
```

**Frontend (React):**
```typescript
import ReactMarkdown from 'react-markdown';
import rehypeSanitize from 'rehype-sanitize';
import remarkGfm from 'remark-gfm';

function ArticleContent({ content }: { content: string }) {
  return (
    <ReactMarkdown
      remarkPlugins={[remarkGfm]}
      rehypePlugins={[rehypeSanitize]}
    >
      {content}
    </ReactMarkdown>
  );
}
```

### CORS Configuration

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3777",      # React dev server
        "https://yourdomain.com"       # Production frontend
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
```

## Testing Strategy

### Backend Testing (pytest)

**Test Structure:**
```
tests/
├── conftest.py                 # Fixtures
├── unit/
│   ├── test_models.py         # SQLAlchemy models
│   ├── test_schemas.py        # Pydantic schemas
│   ├── test_services.py       # Business logic
│   └── test_utils.py          # Utility functions
├── integration/
│   ├── test_articles_api.py   # Article CRUD
│   ├── test_upload_api.py     # File uploads
│   ├── test_media_api.py      # Media management
│   └── test_search_api.py     # Search functionality
└── fixtures/
    ├── sample_articles.json
    └── test_files/            # Sample upload files
```

**Test Patterns:**
```python
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_create_article(client: AsyncClient):
    """Test article creation via API"""
    article_data = {
        "title": "Test Article",
        "content": "# Test Content",
        "draft": False
    }

    response = await client.post("/api/v1/articles", json=article_data)

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == article_data["title"]
    assert "id" in data
    assert "created_at" in data

@pytest.mark.asyncio
async def test_upload_image_validation(client: AsyncClient):
    """Test image upload with invalid file type"""
    files = {"file": ("test.txt", b"not an image", "text/plain")}

    response = await client.post("/api/v1/upload/image", files=files)

    assert response.status_code == 400
    assert "Invalid" in response.json()["detail"]
```

### Frontend Testing (Vitest + React Testing Library)

**Test Structure:**
```
tests/
├── unit/
│   ├── components/
│   │   ├── ArticleCard.test.tsx
│   │   ├── MarkdownEditor.test.tsx
│   │   └── FileUpload.test.tsx
│   ├── hooks/
│   │   ├── useArticles.test.ts
│   │   └── useFileUpload.test.ts
│   └── utils/
│       ├── markdown.test.ts
│       └── validation.test.ts
├── integration/
│   ├── ArticleList.test.tsx
│   ├── ArticleDetail.test.tsx
│   └── ArticleEditor.test.tsx
└── e2e/
    ├── article-flow.spec.ts
    ├── upload-flow.spec.ts
    └── search-flow.spec.ts
```

**Test Patterns:**
```typescript
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { ArticleEditor } from './ArticleEditor';
import { setupServer } from 'msw/node';
import { rest } from 'msw';

const server = setupServer(
  rest.post('/api/v1/articles', (req, res, ctx) => {
    return res(ctx.json({ id: '123', ...req.body }));
  })
);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

test('creates article on submit', async () => {
  const user = userEvent.setup();
  render(<ArticleEditor />);

  await user.type(screen.getByLabelText(/title/i), 'New Article');
  await user.type(screen.getByLabelText(/content/i), '# Content');
  await user.click(screen.getByRole('button', { name: /publish/i }));

  await waitFor(() => {
    expect(screen.getByText(/published successfully/i)).toBeInTheDocument();
  });
});
```

## Common Pitfalls & Mitigation

### 1. File Upload Issues

**Pitfall:** Memory exhaustion from large file uploads

**Mitigation:**
- Stream files to disk instead of loading into memory
- Use chunked uploads for large files
- Implement file size limits
- Use async file operations

```python
from fastapi import UploadFile
import aiofiles

async def save_upload_file(upload_file: UploadFile, destination: str):
    async with aiofiles.open(destination, 'wb') as out_file:
        while content := await upload_file.read(1024 * 1024):  # 1MB chunks
            await out_file.write(content)
```

### 2. CORS Problems

**Pitfall:** CORS errors blocking API requests

**Mitigation:**
- Configure CORS middleware properly
- Use specific origins (not wildcard in production)
- Include credentials if needed
- Test with actual frontend origin

### 3. Database Connection Pool Exhaustion

**Pitfall:** Running out of database connections

**Mitigation:**
```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

engine = create_async_engine(
    DATABASE_URL,
    pool_size=10,              # Adjust based on load
    max_overflow=20,
    pool_pre_ping=True,        # Verify connections
    pool_recycle=3600,         # Recycle after 1 hour
)

async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)
```

### 4. N+1 Query Problems

**Pitfall:** Loading relationships inefficiently

**Mitigation:**
```python
from sqlalchemy.orm import selectinload

# Eager load relationships
stmt = select(Article).options(
    selectinload(Article.tags),
    selectinload(Article.media_files)
)
articles = await session.execute(stmt)
```

### 5. Frontend State Management

**Pitfall:** Prop drilling, stale cache, redundant requests

**Mitigation:**
- Use TanStack Query for server state
- Use Zustand/Context for UI state
- Implement proper cache invalidation

```typescript
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';

function useArticles() {
  return useQuery({
    queryKey: ['articles'],
    queryFn: () => fetch('/api/v1/articles').then(r => r.json()),
    staleTime: 5 * 60 * 1000,  // 5 minutes
  });
}

function useCreateArticle() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (article) =>
      fetch('/api/v1/articles', {
        method: 'POST',
        body: JSON.stringify(article),
      }).then(r => r.json()),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['articles'] });
    },
  });
}
```

## Performance Optimization

### Backend Optimizations

1. **Database Indexing:**
```sql
CREATE INDEX idx_articles_slug ON articles(slug);
CREATE INDEX idx_articles_published ON articles(published_at) WHERE draft = false;
CREATE INDEX idx_media_article ON media_files(article_id);
CREATE INDEX idx_tags_slug ON tags(slug);
```

2. **Response Caching:**
```python
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache

@app.get("/api/v1/articles/{slug}")
@cache(expire=300)  # Cache for 5 minutes
async def get_article(slug: str):
    # ...
```

3. **Async Operations:**
```python
import asyncio

async def process_uploaded_image(file_path: str):
    # Generate thumbnail and optimized versions concurrently
    await asyncio.gather(
        generate_thumbnail(file_path),
        optimize_image(file_path),
        generate_webp_version(file_path)
    )
```

### Frontend Optimizations

1. **Code Splitting:**
```typescript
import { lazy, Suspense } from 'react';

const ArticleEditor = lazy(() => import('./ArticleEditor'));
const MediaGallery = lazy(() => import('./MediaGallery'));

function App() {
  return (
    <Suspense fallback={<Loading />}>
      <Routes>
        <Route path="/editor" element={<ArticleEditor />} />
        <Route path="/gallery" element={<MediaGallery />} />
      </Routes>
    </Suspense>
  );
}
```

2. **Image Optimization:**
```typescript
function ArticleImage({ src, alt }: ImageProps) {
  return (
    <img
      src={src}
      alt={alt}
      loading="lazy"
      decoding="async"
      srcSet={`
        ${src}?w=400 400w,
        ${src}?w=800 800w,
        ${src}?w=1200 1200w
      `}
      sizes="(max-width: 640px) 400px, (max-width: 1024px) 800px, 1200px"
    />
  );
}
```

3. **Virtual Scrolling** (for large lists):
```typescript
import { useVirtualizer } from '@tanstack/react-virtual';

function ArticleList({ articles }: Props) {
  const parentRef = useRef<HTMLDivElement>(null);

  const virtualizer = useVirtualizer({
    count: articles.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 200,
  });

  return (
    <div ref={parentRef} style={{ height: '600px', overflow: 'auto' }}>
      <div style={{ height: `${virtualizer.getTotalSize()}px` }}>
        {virtualizer.getVirtualItems().map(item => (
          <ArticleCard
            key={item.key}
            article={articles[item.index]}
            style={{
              transform: `translateY(${item.start}px)`,
            }}
          />
        ))}
      </div>
    </div>
  );
}
```

## Project Structure

```
moondoors_tech_blog/
├── backend/                    # FastAPI backend
│   ├── alembic/               # Database migrations
│   │   └── versions/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py            # FastAPI app
│   │   ├── config.py          # Configuration
│   │   ├── database.py        # DB connection
│   │   ├── models/            # SQLAlchemy models
│   │   │   ├── __init__.py
│   │   │   ├── article.py
│   │   │   ├── tag.py
│   │   │   └── media.py
│   │   ├── schemas/           # Pydantic schemas
│   │   │   ├── __init__.py
│   │   │   ├── article.py
│   │   │   ├── tag.py
│   │   │   └── media.py
│   │   ├── api/               # API routes
│   │   │   ├── __init__.py
│   │   │   ├── articles.py
│   │   │   ├── upload.py
│   │   │   ├── media.py
│   │   │   ├── tags.py
│   │   │   └── search.py
│   │   ├── services/          # Business logic
│   │   │   ├── __init__.py
│   │   │   ├── article_service.py
│   │   │   ├── upload_service.py
│   │   │   └── storage_service.py
│   │   └── utils/             # Utilities
│   │       ├── __init__.py
│   │       ├── sanitizer.py
│   │       ├── validator.py
│   │       └── file_utils.py
│   ├── tests/                 # Backend tests
│   │   ├── conftest.py
│   │   ├── unit/
│   │   ├── integration/
│   │   └── fixtures/
│   ├── uploads/               # Local file storage (dev)
│   ├── requirements.txt
│   ├── requirements-dev.txt
│   └── pytest.ini
│
├── frontend/                  # React frontend
│   ├── public/
│   ├── src/
│   │   ├── main.tsx          # App entry point
│   │   ├── App.tsx           # Root component
│   │   ├── components/       # React components
│   │   │   ├── common/
│   │   │   │   ├── Button.tsx
│   │   │   │   ├── Input.tsx
│   │   │   │   └── Loading.tsx
│   │   │   ├── layout/
│   │   │   │   ├── Header.tsx
│   │   │   │   ├── Footer.tsx
│   │   │   │   └── Navigation.tsx
│   │   │   ├── article/
│   │   │   │   ├── ArticleCard.tsx
│   │   │   │   ├── ArticleList.tsx
│   │   │   │   ├── ArticleDetail.tsx
│   │   │   │   └── MarkdownRenderer.tsx
│   │   │   ├── editor/
│   │   │   │   ├── MarkdownEditor.tsx
│   │   │   │   ├── FileUpload.tsx
│   │   │   │   └── MediaManager.tsx
│   │   │   └── media/
│   │   │       ├── ImageGallery.tsx
│   │   │       ├── VideoPlayer.tsx
│   │   │       ├── AudioPlayer.tsx
│   │   │       └── FileDownload.tsx
│   │   ├── pages/            # Page components
│   │   │   ├── Home.tsx
│   │   │   ├── ArticlePage.tsx
│   │   │   ├── EditorPage.tsx
│   │   │   ├── TagsPage.tsx
│   │   │   └── NotFound.tsx
│   │   ├── hooks/            # Custom hooks
│   │   │   ├── useArticles.ts
│   │   │   ├── useFileUpload.ts
│   │   │   └── useSearch.ts
│   │   ├── services/         # API services
│   │   │   ├── api.ts
│   │   │   ├── articles.ts
│   │   │   ├── upload.ts
│   │   │   └── media.ts
│   │   ├── utils/            # Utilities
│   │   │   ├── markdown.ts
│   │   │   ├── validation.ts
│   │   │   └── format.ts
│   │   ├── types/            # TypeScript types
│   │   │   ├── article.ts
│   │   │   ├── media.ts
│   │   │   └── api.ts
│   │   └── styles/           # Global styles
│   │       └── index.css
│   ├── tests/                # Frontend tests
│   │   ├── unit/
│   │   ├── integration/
│   │   └── e2e/
│   ├── package.json
│   ├── vite.config.ts
│   ├── vitest.config.ts
│   ├── playwright.config.ts
│   ├── tailwind.config.js
│   └── tsconfig.json
│
├── docs/                     # TDD plans
│   ├── 00-tech-stack-analysis.md
│   ├── 01-issue-breakdown.md
│   └── [N]-[feature]-tdd.md
│
├── .github/
│   └── workflows/           # CI/CD
│       ├── backend-tests.yml
│       └── frontend-tests.yml
│
├── .claude/                 # Agent configs
│   └── agents/
│       ├── tdd-planner.md
│       └── issue-creator.md
│
└── README.md
```

## Deployment Strategy

### Development Environment
```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements-dev.txt
uvicorn app.main:app --reload --port 8777

# Frontend
cd frontend
npm install
npm run dev -- --port 3777
```

### Production Deployment Options

**Backend:**
- **Docker + Docker Compose** (recommended)
- **Railway** or **Render** (simple deployment)
- **AWS ECS** or **Google Cloud Run** (scalable)

**Frontend:**
- **Vercel** or **Netlify** (static hosting with CDN)
- **Cloudflare Pages**
- **AWS S3 + CloudFront**

**Database:**
- **Render PostgreSQL** or **Railway PostgreSQL** (managed)
- **AWS RDS** or **Google Cloud SQL** (enterprise)
- **Supabase** (PostgreSQL + storage)

## Success Metrics

### Performance Targets
- **Backend API:** Response time < 200ms (p95)
- **Frontend:** First Contentful Paint < 1.5s
- **Frontend:** Time to Interactive < 3s
- **File Upload:** Support up to 100MB files
- **Database Queries:** < 50ms average

### Code Quality Targets
- **Test Coverage:** > 80% (backend and frontend)
- **Type Safety:** 100% TypeScript strict mode
- **Linting:** Zero ESLint/Pylint errors
- **Security:** Zero critical vulnerabilities (Snyk scan)

### Scalability Targets
- Support 10,000 articles
- Support 100,000 media files
- Handle 1,000 concurrent users
- 99.9% uptime SLA

## References

### Backend Resources
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [FastAPI File Upload Best Practices](https://betterstack.com/community/guides/scaling-python/uploading-files-using-fastapi/)
- [SQLAlchemy 2.0 Documentation](https://docs.sqlalchemy.org/en/20/)
- [Pydantic V2 Documentation](https://docs.pydantic.dev/latest/)
- [nh3 HTML Sanitization](https://github.com/messense/nh3-python)

### Frontend Resources
- [React Documentation](https://react.dev/)
- [Vite Documentation](https://vitejs.dev/)
- [React Router Documentation](https://reactrouter.com/)
- [TanStack Query](https://tanstack.com/query/latest)
- [react-markdown Documentation](https://github.com/remarkjs/react-markdown)
- [React Testing Library](https://testing-library.com/react)

### Security Resources
- [OWASP File Upload Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html)
- [OWASP XSS Prevention](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html)
- [Content Security Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP)

### Testing Resources
- [pytest Documentation](https://docs.pytest.org/)
- [Vitest Documentation](https://vitest.dev/)
- [Playwright Documentation](https://playwright.dev/)
- [MSW (Mock Service Worker)](https://mswjs.io/)
