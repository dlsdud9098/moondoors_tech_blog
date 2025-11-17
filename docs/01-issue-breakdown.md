# Tech Blog - Issue Breakdown (React + FastAPI + Multimedia)

## Overview

This document contains the complete breakdown of the tech blog project into manageable, testable issues following TDD principles. The architecture uses React for frontend, FastAPI for backend, with full multimedia support (images, videos, audio, documents).

## Issue Summary

**Total issues:** 35 (grouped into 5 phases)

- **Phase 1 - Backend Foundation:** 8 issues (FastAPI, Database, Core APIs)
- **Phase 2 - Frontend Foundation:** 6 issues (React, Routing, Basic UI)
- **Phase 3 - Multimedia Features:** 8 issues (File Upload, Media Management)
- **Phase 4 - Content Management:** 7 issues (Editor, Tags, Search, SEO)
- **Phase 5 - Polish & Advanced:** 6 issues (Performance, Security, Testing)

---

## Phase 1: Backend Foundation (Issues #1-#8)

### Issue #1: FastAPI Project Setup with Testing Infrastructure

**Type:** feature
**Area:** backend/infrastructure
**Complexity:** low
**Estimated Time:** 1-2 hours

#### Description
Initialize FastAPI project with Python 3.11+, configure development tools (pytest, black, mypy), set up testing infrastructure, and establish project structure.

#### Completion Criteria
- [ ] FastAPI 0.109+ project initialized
- [ ] Python virtual environment configured
- [ ] pytest with async support configured
- [ ] Project structure created (app/, tests/, alembic/)
- [ ] Requirements files created (requirements.txt, requirements-dev.txt)
- [ ] Basic health check endpoint works
- [ ] All setup tests pass
- [ ] README.md documents setup process

#### Implementation Notes

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

#### Dependencies
- [ ] None (first issue)

---

### Issue #2: PostgreSQL Database Setup and Connection

**Type:** feature
**Area:** backend/database
**Complexity:** medium
**Estimated Time:** 2 hours

#### Description
Set up PostgreSQL database connection using SQLAlchemy 2.0 with async support. Configure connection pooling, database session management, and Alembic for migrations.

#### Completion Criteria
- [ ] PostgreSQL database connection configured
- [ ] SQLAlchemy async engine set up
- [ ] Database session dependency injection working
- [ ] Alembic migrations initialized
- [ ] Connection pool configured properly
- [ ] All database connection tests pass
- [ ] Migration commands documented

#### Implementation Notes

**Files to Create:**
- `backend/app/database.py` - Database connection and session
- `backend/alembic.ini` - Alembic configuration
- `backend/alembic/env.py` - Alembic environment
- `backend/alembic/versions/` - Migration directory
- `backend/tests/test_database.py` - Database tests

**Key Dependencies:**
```txt
sqlalchemy[asyncio]==2.0.25
asyncpg==0.29.0
alembic==1.13.1
```

**Database Configuration:**
```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+asyncpg://user:pass@localhost/dbname"

engine = create_async_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=False,
)

async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def get_db():
    async with async_session() as session:
        yield session
```

**Patterns from Research:**
- Use async PostgreSQL driver (asyncpg)
- Implement proper connection pooling
- Use dependency injection for sessions
- Set up test database separately

#### Dependencies
- [ ] Issue #1 (FastAPI setup needed)

---

### Issue #3: Article and Tag Database Models

**Type:** feature
**Area:** backend/models
**Complexity:** medium
**Estimated Time:** 2 hours

#### Description
Create SQLAlchemy models for articles and tags with proper relationships, constraints, and indexes. Implement Pydantic schemas for request/response validation.

#### Completion Criteria
- [ ] Article model with all fields created
- [ ] Tag model created
- [ ] Many-to-many relationship configured
- [ ] Database indexes added
- [ ] Pydantic schemas for validation
- [ ] Initial migration generated
- [ ] All model tests pass
- [ ] Schema validation tests pass

#### Implementation Notes

**Files to Create:**
- `backend/app/models/article.py` - Article SQLAlchemy model
- `backend/app/models/tag.py` - Tag SQLAlchemy model
- `backend/app/models/__init__.py` - Model exports
- `backend/app/schemas/article.py` - Article Pydantic schemas
- `backend/app/schemas/tag.py` - Tag Pydantic schemas
- `backend/tests/unit/test_models.py` - Model tests
- `backend/tests/unit/test_schemas.py` - Schema tests

**Article Model:**
```python
from sqlalchemy import Column, String, Text, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

class Article(Base):
    __tablename__ = "articles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, nullable=False, index=True)
    content = Column(Text, nullable=False)
    description = Column(Text)
    draft = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    published_at = Column(DateTime, nullable=True)

    tags = relationship("Tag", secondary="article_tags", back_populates="articles")
    media_files = relationship("MediaFile", back_populates="article", cascade="all, delete-orphan")
```

**Pydantic Schemas:**
```python
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from uuid import UUID

class ArticleBase(BaseModel):
    title: str = Field(..., max_length=255)
    content: str
    description: str | None = None
    draft: bool = True

class ArticleCreate(ArticleBase):
    tags: list[str] = []

class ArticleUpdate(ArticleBase):
    title: str | None = None
    content: str | None = None
    tags: list[str] | None = None

class ArticleResponse(ArticleBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    slug: str
    created_at: datetime
    updated_at: datetime
    published_at: datetime | None
    tags: list[str] = []
```

**Patterns from Research:**
- Use UUID for primary keys (better for distributed systems)
- Implement automatic slug generation
- Use server-side timestamps
- Separate create/update/response schemas

#### Dependencies
- [ ] Issue #2 (Database connection needed)

---

### Issue #4: Article CRUD API Endpoints

**Type:** feature
**Area:** backend/api
**Complexity:** medium
**Estimated Time:** 2-3 hours

#### Description
Implement RESTful API endpoints for article CRUD operations (Create, Read, Update, Delete) with pagination, filtering, and proper error handling.

#### Completion Criteria
- [ ] POST /api/v1/articles - Create article
- [ ] GET /api/v1/articles - List articles (paginated)
- [ ] GET /api/v1/articles/{slug} - Get article by slug
- [ ] PUT /api/v1/articles/{id} - Update article
- [ ] DELETE /api/v1/articles/{id} - Delete article
- [ ] Pagination working (page, size parameters)
- [ ] Draft/published filtering
- [ ] All API tests pass
- [ ] API documentation auto-generated

#### Implementation Notes

**Files to Create:**
- `backend/app/api/articles.py` - Article endpoints
- `backend/app/services/article_service.py` - Business logic
- `backend/tests/integration/test_articles_api.py` - Integration tests

**API Implementation:**
```python
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.article import ArticleCreate, ArticleResponse, ArticleUpdate
from app.services.article_service import ArticleService

router = APIRouter(prefix="/api/v1/articles", tags=["articles"])

@router.post("/", response_model=ArticleResponse, status_code=201)
async def create_article(
    article: ArticleCreate,
    db: AsyncSession = Depends(get_db)
):
    service = ArticleService(db)
    return await service.create_article(article)

@router.get("/", response_model=list[ArticleResponse])
async def list_articles(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    draft: bool | None = None,
    db: AsyncSession = Depends(get_db)
):
    service = ArticleService(db)
    return await service.list_articles(page, size, draft)

@router.get("/{slug}", response_model=ArticleResponse)
async def get_article(slug: str, db: AsyncSession = Depends(get_db)):
    service = ArticleService(db)
    article = await service.get_article_by_slug(slug)
    if not article:
        raise HTTPException(404, "Article not found")
    return article
```

**Service Layer:**
```python
from sqlalchemy import select
from app.models.article import Article
from app.schemas.article import ArticleCreate, ArticleUpdate

class ArticleService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_article(self, data: ArticleCreate) -> Article:
        slug = self._generate_slug(data.title)
        article = Article(slug=slug, **data.model_dump(exclude={"tags"}))
        self.db.add(article)
        await self.db.commit()
        await self.db.refresh(article)
        return article

    async def list_articles(
        self, page: int, size: int, draft: bool | None
    ) -> list[Article]:
        offset = (page - 1) * size
        query = select(Article)
        if draft is not None:
            query = query.where(Article.draft == draft)
        query = query.offset(offset).limit(size).order_by(Article.created_at.desc())
        result = await self.db.execute(query)
        return result.scalars().all()
```

**Patterns from Research:**
- Separate service layer for business logic
- Use slug for article URLs (SEO-friendly)
- Implement pagination with offset/limit
- Proper HTTP status codes (201 for create, 404 for not found)

#### Dependencies
- [ ] Issue #3 (Models and schemas needed)

---

### Issue #5: Media File Database Model

**Type:** feature
**Area:** backend/models
**Complexity:** medium
**Estimated Time:** 2 hours

#### Description
Create SQLAlchemy model for media files with support for images, videos, audio, and documents. Include fields for file metadata, dimensions, and relationships to articles.

#### Completion Criteria
- [ ] MediaFile model with all fields created
- [ ] Relationship to Article model configured
- [ ] File type enum implemented
- [ ] Database indexes added
- [ ] Pydantic schemas for validation
- [ ] Migration generated
- [ ] All model tests pass

#### Implementation Notes

**Files to Create:**
- `backend/app/models/media.py` - MediaFile model
- `backend/app/schemas/media.py` - Media Pydantic schemas
- `backend/tests/unit/test_media_models.py` - Model tests

**MediaFile Model:**
```python
import enum
from sqlalchemy import Column, String, Integer, Float, Text, DateTime, Enum, BigInteger
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey

class FileType(str, enum.Enum):
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    DOCUMENT = "document"

class MediaFile(Base):
    __tablename__ = "media_files"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    article_id = Column(UUID(as_uuid=True), ForeignKey("articles.id", ondelete="CASCADE"), index=True)
    filename = Column(String(255), nullable=False)
    original_filename = Column(String(255), nullable=False)
    file_type = Column(Enum(FileType), nullable=False, index=True)
    mime_type = Column(String(100), nullable=False)
    file_size = Column(BigInteger, nullable=False)
    file_path = Column(Text, nullable=False)
    url = Column(Text, nullable=False)

    # Image/Video specific
    width = Column(Integer, nullable=True)
    height = Column(Integer, nullable=True)

    # Video/Audio specific
    duration = Column(Float, nullable=True)

    # Video specific
    thumbnail_url = Column(Text, nullable=True)

    # Image specific
    alt_text = Column(Text, nullable=True)

    # General
    caption = Column(Text, nullable=True)
    uploaded_at = Column(DateTime, server_default=func.now())

    article = relationship("Article", back_populates="media_files")
```

**Pydantic Schemas:**
```python
class MediaFileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    article_id: UUID | None
    filename: str
    original_filename: str
    file_type: FileType
    mime_type: str
    file_size: int
    url: str
    width: int | None = None
    height: int | None = None
    duration: float | None = None
    thumbnail_url: str | None = None
    alt_text: str | None = None
    caption: str | None = None
    uploaded_at: datetime
```

**Patterns from Research:**
- Use enum for file types (type safety)
- Store both original and sanitized filenames
- Include metadata for different media types
- Cascade delete when article is deleted

#### Dependencies
- [ ] Issue #3 (Article model needed for relationship)

---

### Issue #6: File Upload Service with Validation

**Type:** feature
**Area:** backend/services
**Complexity:** high
**Estimated Time:** 3 hours

#### Description
Implement file upload service with multi-layer validation (extension, MIME type, content-based), file size limits, and sanitization. Support local and S3 storage backends.

#### Completion Criteria
- [ ] File validation implemented (extension, MIME, magic bytes)
- [ ] File size limits enforced
- [ ] Filename sanitization working
- [ ] Local storage backend implemented
- [ ] S3 storage backend implemented (optional)
- [ ] Storage abstraction layer
- [ ] All validation tests pass
- [ ] Security tests pass (malicious files rejected)

#### Implementation Notes

**Files to Create:**
- `backend/app/services/upload_service.py` - Upload logic
- `backend/app/services/storage_service.py` - Storage abstraction
- `backend/app/utils/validator.py` - File validation utilities
- `backend/app/utils/file_utils.py` - File utilities
- `backend/tests/unit/test_upload_service.py` - Unit tests
- `backend/tests/integration/test_file_upload.py` - Integration tests

**Key Dependencies:**
```txt
python-magic==0.4.27
nh3==0.2.15
aiofiles==23.2.1
Pillow==10.1.0
boto3==1.34.14  # For S3 support
```

**File Validation:**
```python
import magic
import os
from fastapi import UploadFile, HTTPException

ALLOWED_EXTENSIONS = {
    FileType.IMAGE: {'.jpg', '.jpeg', '.png', '.gif', '.webp'},
    FileType.VIDEO: {'.mp4', '.webm', '.mov'},
    FileType.AUDIO: {'.mp3', '.wav', '.ogg'},
    FileType.DOCUMENT: {'.pdf', '.doc', '.docx'}
}

ALLOWED_MIME_TYPES = {
    FileType.IMAGE: {'image/jpeg', 'image/png', 'image/gif', 'image/webp'},
    FileType.VIDEO: {'video/mp4', 'video/webm', 'video/quicktime'},
    FileType.AUDIO: {'audio/mpeg', 'audio/wav', 'audio/ogg'},
    FileType.DOCUMENT: {'application/pdf', 'application/msword'}
}

MAX_FILE_SIZES = {
    FileType.IMAGE: 10 * 1024 * 1024,      # 10 MB
    FileType.VIDEO: 100 * 1024 * 1024,     # 100 MB
    FileType.AUDIO: 20 * 1024 * 1024,      # 20 MB
    FileType.DOCUMENT: 10 * 1024 * 1024    # 10 MB
}

async def validate_file(file: UploadFile, file_type: FileType) -> bool:
    # 1. Extension check
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS[file_type]:
        raise HTTPException(400, f"Invalid file extension for {file_type}")

    # 2. MIME type check
    if file.content_type not in ALLOWED_MIME_TYPES[file_type]:
        raise HTTPException(400, "Invalid MIME type")

    # 3. File size check
    file.file.seek(0, 2)
    size = file.file.tell()
    file.file.seek(0)

    if size > MAX_FILE_SIZES[file_type]:
        raise HTTPException(400, f"File too large (max {MAX_FILE_SIZES[file_type] / 1024 / 1024}MB)")

    # 4. Magic bytes validation
    file_data = await file.read(2048)
    await file.seek(0)

    detected_mime = magic.from_buffer(file_data, mime=True)
    if detected_mime not in ALLOWED_MIME_TYPES[file_type]:
        raise HTTPException(400, "File content doesn't match extension")

    return True
```

**Storage Abstraction:**
```python
from abc import ABC, abstractmethod
import aiofiles
import uuid
from pathlib import Path

class StorageBackend(ABC):
    @abstractmethod
    async def save_file(self, file: UploadFile, path: str) -> str:
        pass

    @abstractmethod
    async def delete_file(self, path: str) -> bool:
        pass

    @abstractmethod
    def get_url(self, path: str) -> str:
        pass

class LocalStorage(StorageBackend):
    def __init__(self, base_path: str = "./uploads"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)

    async def save_file(self, file: UploadFile, path: str) -> str:
        full_path = self.base_path / path
        full_path.parent.mkdir(parents=True, exist_ok=True)

        async with aiofiles.open(full_path, 'wb') as out_file:
            while content := await file.read(1024 * 1024):  # 1MB chunks
                await out_file.write(content)

        return str(full_path)

    async def delete_file(self, path: str) -> bool:
        full_path = self.base_path / path
        if full_path.exists():
            full_path.unlink()
            return True
        return False

    def get_url(self, path: str) -> str:
        return f"/uploads/{path}"
```

**Patterns from Research:**
- Multi-layer validation (extension, MIME, magic bytes)
- Stream large files in chunks (avoid memory issues)
- Storage abstraction for easy S3 migration
- Sanitize filenames to prevent path traversal

#### Dependencies
- [ ] Issue #5 (Media model needed)

---

### Issue #7: Image Upload API Endpoint

**Type:** feature
**Area:** backend/api
**Complexity:** medium
**Estimated Time:** 2 hours

#### Description
Implement API endpoint for image uploads with validation, thumbnail generation, and automatic WebP conversion. Store metadata in database.

#### Completion Criteria
- [ ] POST /api/v1/upload/image endpoint works
- [ ] Image validation implemented
- [ ] Thumbnail generation working (200x200)
- [ ] WebP conversion implemented
- [ ] Image metadata extracted (dimensions)
- [ ] Database record created
- [ ] All upload tests pass
- [ ] Error handling for invalid images

#### Implementation Notes

**Files to Create:**
- `backend/app/api/upload.py` - Upload endpoints
- `backend/app/services/image_service.py` - Image processing
- `backend/tests/integration/test_image_upload.py` - Integration tests
- `backend/tests/fixtures/test_images/` - Test image files

**Image Upload Endpoint:**
```python
from fastapi import APIRouter, UploadFile, File, Depends
from app.services.upload_service import UploadService
from app.services.image_service import ImageService
from app.schemas.media import MediaFileResponse

router = APIRouter(prefix="/api/v1/upload", tags=["upload"])

@router.post("/image", response_model=MediaFileResponse, status_code=201)
async def upload_image(
    file: UploadFile = File(...),
    article_id: UUID | None = None,
    alt_text: str | None = None,
    caption: str | None = None,
    db: AsyncSession = Depends(get_db)
):
    # Validate file
    await validate_file(file, FileType.IMAGE)

    # Process image
    image_service = ImageService(db)
    media_file = await image_service.process_and_save_image(
        file, article_id, alt_text, caption
    )

    return media_file
```

**Image Processing Service:**
```python
from PIL import Image
import io
from pathlib import Path

class ImageService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.storage = LocalStorage()

    async def process_and_save_image(
        self, file: UploadFile, article_id: UUID | None,
        alt_text: str | None, caption: str | None
    ) -> MediaFile:
        # Generate unique filename
        ext = Path(file.filename).suffix
        filename = f"{uuid.uuid4()}{ext}"
        file_path = f"images/originals/{filename}"

        # Save original
        await self.storage.save_file(file, file_path)

        # Read image for processing
        await file.seek(0)
        content = await file.read()
        image = Image.open(io.BytesIO(content))

        # Extract dimensions
        width, height = image.size

        # Generate thumbnail
        thumbnail_path = await self._generate_thumbnail(image, filename)

        # Generate WebP version
        webp_path = await self._generate_webp(image, filename)

        # Create database record
        media_file = MediaFile(
            article_id=article_id,
            filename=filename,
            original_filename=file.filename,
            file_type=FileType.IMAGE,
            mime_type=file.content_type,
            file_size=len(content),
            file_path=file_path,
            url=self.storage.get_url(file_path),
            width=width,
            height=height,
            alt_text=alt_text,
            caption=caption
        )

        self.db.add(media_file)
        await self.db.commit()
        await self.db.refresh(media_file)

        return media_file

    async def _generate_thumbnail(self, image: Image, filename: str) -> str:
        thumb = image.copy()
        thumb.thumbnail((200, 200))
        thumb_filename = f"thumb_{filename}"
        thumb_path = f"images/thumbnails/{thumb_filename}"

        # Save thumbnail
        buffer = io.BytesIO()
        thumb.save(buffer, format=image.format)
        buffer.seek(0)

        # Convert to UploadFile-like
        # ... save using storage

        return thumb_path

    async def _generate_webp(self, image: Image, filename: str) -> str:
        webp_filename = Path(filename).stem + ".webp"
        webp_path = f"images/optimized/{webp_filename}"

        buffer = io.BytesIO()
        image.save(buffer, format="WEBP", quality=85)
        buffer.seek(0)

        # Save WebP version
        # ... save using storage

        return webp_path
```

**Patterns from Research:**
- Generate thumbnails automatically
- Create WebP versions for better performance
- Extract image metadata (dimensions)
- Store multiple versions (original, thumb, optimized)

#### Dependencies
- [ ] Issue #6 (Upload service needed)

---

### Issue #8: Video/Audio/Document Upload Endpoints

**Type:** feature
**Area:** backend/api
**Complexity:** medium
**Estimated Time:** 2-3 hours

#### Description
Implement API endpoints for uploading videos, audio files, and documents. Include validation and metadata extraction.

#### Completion Criteria
- [ ] POST /api/v1/upload/video endpoint works
- [ ] POST /api/v1/upload/audio endpoint works
- [ ] POST /api/v1/upload/document endpoint works
- [ ] Video duration extraction working
- [ ] Audio duration extraction working
- [ ] All file type validations working
- [ ] All upload tests pass

#### Implementation Notes

**Video/Audio Upload:**
```python
@router.post("/video", response_model=MediaFileResponse, status_code=201)
async def upload_video(
    file: UploadFile = File(...),
    article_id: UUID | None = None,
    caption: str | None = None,
    db: AsyncSession = Depends(get_db)
):
    await validate_file(file, FileType.VIDEO)

    video_service = VideoService(db)
    media_file = await video_service.process_and_save_video(
        file, article_id, caption
    )

    return media_file

@router.post("/audio", response_model=MediaFileResponse, status_code=201)
async def upload_audio(
    file: UploadFile = File(...),
    article_id: UUID | None = None,
    caption: str | None = None,
    db: AsyncSession = Depends(get_db)
):
    await validate_file(file, FileType.AUDIO)

    audio_service = AudioService(db)
    media_file = await audio_service.process_and_save_audio(
        file, article_id, caption
    )

    return media_file

@router.post("/document", response_model=MediaFileResponse, status_code=201)
async def upload_document(
    file: UploadFile = File(...),
    article_id: UUID | None = None,
    caption: str | None = None,
    db: AsyncSession = Depends(get_db)
):
    await validate_file(file, FileType.DOCUMENT)

    doc_service = DocumentService(db)
    media_file = await doc_service.process_and_save_document(
        file, article_id, caption
    )

    return media_file
```

**Key Dependencies:**
```txt
ffmpeg-python==0.2.0  # For video/audio metadata
mutagen==1.47.0       # For audio metadata
```

**Patterns from Research:**
- Extract duration for video/audio files
- Generate video thumbnails (first frame)
- Validate file integrity
- Store metadata for playback

#### Dependencies
- [ ] Issue #6 (Upload service needed)
- [ ] Issue #7 (Upload patterns established)

---

## Phase 2: Frontend Foundation (Issues #9-#14)

### Issue #9: React + Vite Project Setup with Testing

**Type:** feature
**Area:** frontend/infrastructure
**Complexity:** low
**Estimated Time:** 1-2 hours

#### Description
Initialize React project with Vite, TypeScript, configure testing infrastructure (Vitest, React Testing Library, Playwright), and establish project structure.

#### Completion Criteria
- [ ] React 18+ with Vite initialized
- [ ] TypeScript configured (strict mode)
- [ ] Tailwind CSS configured
- [ ] Vitest and React Testing Library set up
- [ ] Playwright configured for E2E tests
- [ ] ESLint and Prettier configured
- [ ] Project structure created
- [ ] All setup tests pass
- [ ] README.md documents setup

#### Implementation Notes

**Files to Create:**
- `frontend/package.json` - Dependencies
- `frontend/vite.config.ts` - Vite configuration
- `frontend/vitest.config.ts` - Vitest configuration
- `frontend/playwright.config.ts` - Playwright configuration
- `frontend/tsconfig.json` - TypeScript configuration
- `frontend/tailwind.config.js` - Tailwind configuration
- `frontend/.eslintrc.json` - ESLint rules
- `frontend/.prettierrc` - Prettier configuration
- `frontend/src/main.tsx` - App entry
- `frontend/src/App.tsx` - Root component

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
    "@testing-library/user-event": "^14.5.1",
    "@playwright/test": "^1.40.1",
    "tailwindcss": "^3.4.0",
    "eslint": "^8.56.0",
    "prettier": "^3.1.1"
  }
}
```

**Patterns from Research:**
- Use Vite for fast development (3.8x faster than webpack)
- Enable TypeScript strict mode from start
- Configure Vitest with jsdom environment
- Set up MSW for API mocking

#### Dependencies
- [ ] None (first frontend issue)

---

### Issue #10: API Client Service and React Query Setup

**Type:** feature
**Area:** frontend/services
**Complexity:** medium
**Estimated Time:** 2 hours

#### Description
Create API client service for backend communication with proper error handling, type safety, and React Query integration for state management and caching.

#### Completion Criteria
- [ ] Axios/Fetch client configured
- [ ] API base URL configuration
- [ ] Request/response interceptors
- [ ] React Query configured
- [ ] Type-safe API functions
- [ ] Error handling implemented
- [ ] All client tests pass

#### Implementation Notes

**Files to Create:**
- `frontend/src/services/api.ts` - Base API client
- `frontend/src/services/articles.ts` - Article API functions
- `frontend/src/services/upload.ts` - Upload API functions
- `frontend/src/types/api.ts` - API type definitions
- `frontend/src/types/article.ts` - Article types
- `frontend/src/types/media.ts` - Media types
- `frontend/tests/unit/services/api.test.ts` - API tests

**Key Dependencies:**
```json
{
  "dependencies": {
    "axios": "^1.6.5",
    "@tanstack/react-query": "^5.17.0",
    "zod": "^3.22.4"
  }
}
```

**API Client:**
```typescript
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 404) {
      // Handle 404
    }
    return Promise.reject(error);
  }
);
```

**Article Service:**
```typescript
import { apiClient } from './api';
import type { Article, ArticleCreate, ArticleUpdate } from '../types/article';

export const articlesApi = {
  list: async (page: number = 1, size: number = 20): Promise<Article[]> => {
    const response = await apiClient.get('/api/v1/articles', {
      params: { page, size },
    });
    return response.data;
  },

  get: async (slug: string): Promise<Article> => {
    const response = await apiClient.get(`/api/v1/articles/${slug}`);
    return response.data;
  },

  create: async (data: ArticleCreate): Promise<Article> => {
    const response = await apiClient.post('/api/v1/articles', data);
    return response.data;
  },

  update: async (id: string, data: ArticleUpdate): Promise<Article> => {
    const response = await apiClient.put(`/api/v1/articles/${id}`, data);
    return response.data;
  },

  delete: async (id: string): Promise<void> => {
    await apiClient.delete(`/api/v1/articles/${id}`);
  },
};
```

**React Query Hooks:**
```typescript
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { articlesApi } from '../services/articles';

export function useArticles(page: number = 1) {
  return useQuery({
    queryKey: ['articles', page],
    queryFn: () => articlesApi.list(page),
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
}

export function useArticle(slug: string) {
  return useQuery({
    queryKey: ['article', slug],
    queryFn: () => articlesApi.get(slug),
    enabled: !!slug,
  });
}

export function useCreateArticle() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: articlesApi.create,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['articles'] });
    },
  });
}
```

**Patterns from Research:**
- Use React Query for server state management
- Implement proper error handling and retries
- Type-safe API functions with TypeScript
- Cache invalidation on mutations

#### Dependencies
- [ ] Issue #9 (React setup needed)

---

### Issue #11: React Router and Basic Layout

**Type:** feature
**Area:** frontend/ui
**Complexity:** medium
**Estimated Time:** 2 hours

#### Description
Set up React Router for navigation, create basic layout components (Header, Footer, Navigation), and establish routing structure.

#### Completion Criteria
- [ ] React Router configured
- [ ] Header component created
- [ ] Footer component created
- [ ] Navigation component created
- [ ] Main layout component
- [ ] Routes defined (Home, Article, Editor)
- [ ] 404 page created
- [ ] All navigation tests pass

#### Implementation Notes

**Files to Create:**
- `frontend/src/components/layout/Header.tsx`
- `frontend/src/components/layout/Footer.tsx`
- `frontend/src/components/layout/Navigation.tsx`
- `frontend/src/components/layout/MainLayout.tsx`
- `frontend/src/pages/Home.tsx`
- `frontend/src/pages/ArticlePage.tsx`
- `frontend/src/pages/NotFound.tsx`
- `frontend/src/router.tsx` - Route configuration
- `frontend/tests/unit/components/layout/*.test.tsx`

**Router Setup:**
```typescript
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import MainLayout from './components/layout/MainLayout';
import Home from './pages/Home';
import ArticlePage from './pages/ArticlePage';
import EditorPage from './pages/EditorPage';
import NotFound from './pages/NotFound';

const router = createBrowserRouter([
  {
    path: '/',
    element: <MainLayout />,
    children: [
      { path: '/', element: <Home /> },
      { path: '/articles/:slug', element: <ArticlePage /> },
      { path: '/editor', element: <EditorPage /> },
      { path: '/editor/:id', element: <EditorPage /> },
      { path: '*', element: <NotFound /> },
    ],
  },
]);

export function App() {
  return <RouterProvider router={router} />;
}
```

**MainLayout:**
```typescript
import { Outlet } from 'react-router-dom';
import Header from './Header';
import Footer from './Footer';

export default function MainLayout() {
  return (
    <div className="min-h-screen flex flex-col">
      <Header />
      <main className="flex-1 container mx-auto px-4 py-8">
        <Outlet />
      </main>
      <Footer />
    </div>
  );
}
```

**Patterns from Research:**
- Use nested routes with layout
- Implement responsive navigation
- Mobile hamburger menu
- Active link highlighting

#### Dependencies
- [ ] Issue #9 (React setup needed)

---

### Issue #12: Article List Page with Pagination

**Type:** feature
**Area:** frontend/ui
**Complexity:** medium
**Estimated Time:** 2-3 hours

#### Description
Create home page displaying list of articles with pagination, loading states, and error handling. Implement responsive grid layout.

#### Completion Criteria
- [ ] Article list displays correctly
- [ ] Pagination controls working
- [ ] Loading state displayed
- [ ] Error state handled
- [ ] Empty state shown when no articles
- [ ] Responsive grid (1-3 columns)
- [ ] All component tests pass
- [ ] E2E test for article listing

#### Implementation Notes

**Files to Create:**
- `frontend/src/pages/Home.tsx` - Home page
- `frontend/src/components/article/ArticleCard.tsx` - Article card
- `frontend/src/components/article/ArticleList.tsx` - Article list
- `frontend/src/components/common/Pagination.tsx` - Pagination
- `frontend/src/components/common/Loading.tsx` - Loading spinner
- `frontend/src/components/common/ErrorMessage.tsx` - Error display
- `frontend/tests/unit/components/article/*.test.tsx`
- `frontend/tests/e2e/article-list.spec.ts`

**Home Page:**
```typescript
import { useState } from 'react';
import { useArticles } from '../hooks/useArticles';
import ArticleList from '../components/article/ArticleList';
import Pagination from '../components/common/Pagination';
import Loading from '../components/common/Loading';
import ErrorMessage from '../components/common/ErrorMessage';

export default function Home() {
  const [page, setPage] = useState(1);
  const { data: articles, isLoading, error } = useArticles(page);

  if (isLoading) return <Loading />;
  if (error) return <ErrorMessage error={error} />;
  if (!articles || articles.length === 0) {
    return <div>No articles found</div>;
  }

  return (
    <div>
      <h1 className="text-4xl font-bold mb-8">Latest Articles</h1>
      <ArticleList articles={articles} />
      <Pagination
        currentPage={page}
        onPageChange={setPage}
        hasMore={articles.length === 20}
      />
    </div>
  );
}
```

**ArticleCard:**
```typescript
import { Link } from 'react-router-dom';
import type { Article } from '../../types/article';

interface ArticleCardProps {
  article: Article;
}

export default function ArticleCard({ article }: ArticleCardProps) {
  return (
    <Link
      to={`/articles/${article.slug}`}
      className="block border rounded-lg p-6 hover:shadow-lg transition-shadow"
    >
      <h2 className="text-2xl font-bold mb-2">{article.title}</h2>
      <p className="text-gray-600 mb-4">{article.description}</p>
      <div className="flex gap-2">
        {article.tags.map((tag) => (
          <span
            key={tag}
            className="bg-blue-100 text-blue-800 px-2 py-1 rounded text-sm"
          >
            {tag}
          </span>
        ))}
      </div>
      <time className="text-sm text-gray-500 mt-4 block">
        {new Date(article.created_at).toLocaleDateString()}
      </time>
    </Link>
  );
}
```

**ArticleList:**
```typescript
import ArticleCard from './ArticleCard';
import type { Article } from '../../types/article';

interface ArticleListProps {
  articles: Article[];
}

export default function ArticleList({ articles }: ArticleListProps) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {articles.map((article) => (
        <ArticleCard key={article.id} article={article} />
      ))}
    </div>
  );
}
```

**Patterns from Research:**
- Loading and error states
- Responsive grid layout
- Optimistic updates with React Query
- Skeleton loaders for better UX

#### Dependencies
- [ ] Issue #10 (API client needed)
- [ ] Issue #11 (Router and layout needed)

---

### Issue #13: Article Detail Page with Markdown Rendering

**Type:** feature
**Area:** frontend/ui
**Complexity:** medium
**Estimated Time:** 2-3 hours

#### Description
Create article detail page with secure markdown rendering, syntax highlighting for code blocks, and proper typography.

#### Completion Criteria
- [ ] Article detail page displays correctly
- [ ] Markdown content renders properly
- [ ] Syntax highlighting works
- [ ] External links secured
- [ ] Loading and error states
- [ ] 404 for invalid slugs
- [ ] All rendering tests pass
- [ ] E2E test for article reading

#### Implementation Notes

**Files to Create:**
- `frontend/src/pages/ArticlePage.tsx` - Article detail page
- `frontend/src/components/article/ArticleDetail.tsx` - Article content
- `frontend/src/components/article/MarkdownRenderer.tsx` - Markdown component
- `frontend/src/components/article/CodeBlock.tsx` - Code syntax highlighting
- `frontend/tests/unit/components/article/MarkdownRenderer.test.tsx`
- `frontend/tests/e2e/article-detail.spec.ts`

**Key Dependencies:**
```json
{
  "dependencies": {
    "react-markdown": "^9.0.1",
    "remark-gfm": "^4.0.0",
    "rehype-sanitize": "^6.0.0",
    "rehype-highlight": "^7.0.0",
    "remark-external-links": "^9.0.1"
  }
}
```

**Article Page:**
```typescript
import { useParams } from 'react-router-dom';
import { useArticle } from '../hooks/useArticles';
import ArticleDetail from '../components/article/ArticleDetail';
import Loading from '../components/common/Loading';
import ErrorMessage from '../components/common/ErrorMessage';
import NotFound from './NotFound';

export default function ArticlePage() {
  const { slug } = useParams<{ slug: string }>();
  const { data: article, isLoading, error } = useArticle(slug!);

  if (isLoading) return <Loading />;
  if (error?.response?.status === 404) return <NotFound />;
  if (error) return <ErrorMessage error={error} />;
  if (!article) return <NotFound />;

  return <ArticleDetail article={article} />;
}
```

**Markdown Renderer:**
```typescript
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import rehypeSanitize from 'rehype-sanitize';
import rehypeHighlight from 'rehype-highlight';
import remarkExternalLinks from 'remark-external-links';
import CodeBlock from './CodeBlock';

interface MarkdownRendererProps {
  content: string;
}

export default function MarkdownRenderer({ content }: MarkdownRendererProps) {
  return (
    <ReactMarkdown
      remarkPlugins={[
        remarkGfm,
        [remarkExternalLinks, { target: '_blank', rel: 'noopener noreferrer' }],
      ]}
      rehypePlugins={[rehypeSanitize, rehypeHighlight]}
      components={{
        code: CodeBlock,
      }}
      className="prose prose-lg max-w-none"
    >
      {content}
    </ReactMarkdown>
  );
}
```

**Code Block:**
```typescript
import 'highlight.js/styles/github-dark.css';

interface CodeBlockProps {
  inline?: boolean;
  className?: string;
  children?: React.ReactNode;
}

export default function CodeBlock({ inline, className, children }: CodeBlockProps) {
  if (inline) {
    return <code className="bg-gray-100 px-1 rounded">{children}</code>;
  }

  return (
    <div className="relative">
      <pre className={className}>
        <code>{children}</code>
      </pre>
    </div>
  );
}
```

**Patterns from Research:**
- Use react-markdown (secure by default)
- Sanitize with rehype-sanitize
- Syntax highlighting with rehype-highlight
- Typography with Tailwind prose

#### Dependencies
- [ ] Issue #10 (API client needed)
- [ ] Issue #11 (Router and layout needed)

---

### Issue #14: Responsive Design and Mobile Optimization

**Type:** feature
**Area:** frontend/ui
**Complexity:** medium
**Estimated Time:** 2 hours

#### Description
Ensure entire frontend is fully responsive across all device sizes with mobile-first approach. Optimize touch interactions and navigation.

#### Completion Criteria
- [ ] All pages responsive (mobile, tablet, desktop)
- [ ] Mobile-first CSS approach
- [ ] Touch-friendly tap targets (min 44x44px)
- [ ] Mobile navigation menu working
- [ ] All responsive tests pass
- [ ] Visual regression tests at breakpoints
- [ ] Lighthouse mobile score > 85

#### Implementation Notes

**Tailwind Breakpoints:**
```javascript
// tailwind.config.js
module.exports = {
  theme: {
    screens: {
      'sm': '640px',
      'md': '768px',
      'lg': '1024px',
      'xl': '1280px',
      '2xl': '1536px',
    },
  },
};
```

**Mobile Navigation:**
```typescript
import { useState } from 'react';
import { Link } from 'react-router-dom';

export default function Navigation() {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <nav className="bg-white shadow">
      <div className="container mx-auto px-4">
        <div className="flex justify-between items-center h-16">
          <Link to="/" className="text-xl font-bold">
            Tech Blog
          </Link>

          {/* Mobile menu button */}
          <button
            className="md:hidden p-2"
            onClick={() => setIsOpen(!isOpen)}
            aria-label="Toggle menu"
          >
            {/* Hamburger icon */}
            <svg className="w-6 h-6" fill="none" stroke="currentColor">
              {isOpen ? (
                <path d="M6 18L18 6M6 6l12 12" />
              ) : (
                <path d="M4 6h16M4 12h16M4 18h16" />
              )}
            </svg>
          </button>

          {/* Desktop menu */}
          <div className="hidden md:flex gap-4">
            <Link to="/">Home</Link>
            <Link to="/editor">Write</Link>
          </div>
        </div>

        {/* Mobile menu */}
        {isOpen && (
          <div className="md:hidden py-4">
            <Link to="/" className="block py-2">Home</Link>
            <Link to="/editor" className="block py-2">Write</Link>
          </div>
        )}
      </div>
    </nav>
  );
}
```

**Patterns from Research:**
- Mobile-first approach
- Test on real devices
- Minimum tap target size (44x44px)
- Hamburger menu for mobile

#### Dependencies
- [ ] All UI components (Issues #11-#13)

---

(Continuing in next response due to length...)
