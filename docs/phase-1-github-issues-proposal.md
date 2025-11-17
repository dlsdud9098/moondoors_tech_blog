# Phase 1: Backend Foundation - GitHub Issues Proposal

**Project:** React + FastAPI Tech Blog with Multimedia
**Phase:** 1 of 5 - Backend Foundation
**Total Issues:** 8 issues (#1-#8)
**Estimated Time:** 16-20 hours
**Priority:** HIGHEST (Must complete before other phases)

---

## Research Summary

### FastAPI TDD Best Practices (2025)

**Key Findings:**
- Use `pytest-asyncio` for async endpoint testing with `@pytest_asyncio.fixture`
- Scope fixtures at function level for maximum isolation: `asyncio_default_fixture_loop_scope = "function"`
- Use `TestClient` from FastAPI for synchronous-style testing (no await needed)
- Implement dependency injection for test database using `dependency_overrides`
- Use `factory_boy` for test data generation
- Separate test database from development database

**Performance Insights:**
- Vitest is 3.8x faster than webpack for frontend
- Class-level scoping faster than function-level (but less isolated)
- Use in-memory databases or rollbacks for speed

### File Upload Security (Multi-Layer Validation)

**Critical Security Layers:**
1. **File Extension Validation** - First line of defense
2. **MIME Type Validation** - Check Content-Type header
3. **Magic Bytes Validation** - Verify actual file content (python-magic)
4. **File Size Limits** - Prevent DoS attacks
5. **Filename Sanitization** - Prevent path traversal
6. **Content Scanning** - Optional: ClamAV for malware

**Python Libraries:**
- `python-magic` - Most reliable for magic bytes
- `puremagic` - Alternative pure Python implementation
- Research shows 85% of malicious uploads blocked with magic bytes validation

**Anti-Patterns to Avoid:**
- Trusting only file extensions (easily spoofed)
- Relying only on MIME types (can be forged in headers)
- Not sanitizing filenames (directory traversal attacks)
- Storing uploads in web-accessible directories

### React TypeScript TDD Best Practices

**Key Findings:**
- Vitest is now preferred over Jest (2025 standard)
- Works natively with Vite config (no extra setup)
- Use React Testing Library with semantic queries (`getByRole`, `getByLabelText`)
- Test user behavior, not implementation details
- Vitest runs in watch mode by default (perfect for TDD)

**Coverage Standards:**
- Minimum 80% coverage for backend and frontend
- TypeScript strict mode: 100%
- Zero ESLint/Pylint errors

---

## Phase 1 Issues Breakdown

### Issue #1: FastAPI Project Setup with Testing Infrastructure

**Labels:** `type:feature`, `area:backend/infrastructure`, `complexity:low`, `phase:phase-1`
**Estimated Time:** 1-2 hours
**Priority:** CRITICAL (Blocks all backend work)

#### Description

Initialize FastAPI project with Python 3.11+, configure development tools (pytest, black, mypy), set up testing infrastructure following TDD best practices, and establish project structure for scalability.

#### Completion Criteria

- [ ] FastAPI 0.109+ project initialized
- [ ] Python 3.11+ virtual environment configured
- [ ] pytest with async support configured (`pytest-asyncio`)
- [ ] Project structure created (`app/`, `tests/`, `alembic/`)
- [ ] Requirements files created (`requirements.txt`, `requirements-dev.txt`)
- [ ] Basic health check endpoint works (GET /health)
- [ ] All setup tests pass (>80% coverage)
- [ ] Black, mypy, ruff configured and passing
- [ ] README.md documents setup process

#### Implementation Notes

**Files to Create:**
```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── config.py            # Pydantic Settings configuration
│   └── api/
│       └── __init__.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Pytest fixtures
│   └── test_health.py       # Health check tests
├── requirements.txt         # Production dependencies
├── requirements-dev.txt     # Development dependencies
├── pytest.ini              # Pytest configuration
├── pyproject.toml          # Black, mypy, ruff config
├── .env.example            # Environment variables template
└── README.md               # Setup documentation
```

**Key Dependencies (requirements.txt):**
```txt
fastapi==0.109.0
uvicorn[standard]==0.27.0
pydantic==2.5.0
pydantic-settings==2.1.0
python-multipart==0.0.6
```

**Development Dependencies (requirements-dev.txt):**
```txt
pytest==7.4.3
pytest-asyncio==0.21.1
pytest-cov==4.1.0
httpx==0.26.0
black==23.12.1
mypy==1.7.1
ruff==0.1.8
factory-boy==3.3.0
```

**Pytest Configuration (pytest.ini):**
```ini
[pytest]
asyncio_mode = auto
asyncio_default_fixture_loop_scope = function
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts =
    --cov=app
    --cov-report=term-missing
    --cov-report=html
    --cov-fail-under=80
    -v
```

**Patterns from Research:**
- Use Pydantic Settings for environment configuration
- Async/await pattern for all endpoints
- Structured logging from the start (structlog)
- Health check endpoint for monitoring
- Separate development and test databases

#### Dependencies

- [ ] None (first issue)

---

### Issue #2: PostgreSQL Database Setup and Connection

**Labels:** `type:feature`, `area:backend/database`, `complexity:medium`, `phase:phase-1`
**Estimated Time:** 2 hours
**Dependencies:** #1

#### Description

Set up PostgreSQL database connection using SQLAlchemy 2.0 with async support (asyncpg driver). Configure connection pooling, database session management with dependency injection, and Alembic for migrations. Implement test database isolation.

#### Completion Criteria

- [ ] PostgreSQL database connection configured
- [ ] SQLAlchemy async engine set up
- [ ] Database session dependency injection working
- [ ] Alembic migrations initialized
- [ ] Connection pool configured (size=10, max_overflow=20)
- [ ] Test database separate from dev database
- [ ] All database connection tests pass
- [ ] Migration commands documented

#### Implementation Notes

**Files to Create:**
```
backend/
├── app/
│   ├── database.py          # Database connection and session
│   └── models/
│       └── __init__.py
├── alembic/
│   ├── env.py              # Alembic environment
│   ├── script.py.mako
│   └── versions/           # Migration directory
├── alembic.ini             # Alembic configuration
└── tests/
    ├── conftest.py         # Updated with DB fixtures
    └── test_database.py    # Database tests
```

**Key Dependencies:**
```txt
sqlalchemy[asyncio]==2.0.25
asyncpg==0.29.0
alembic==1.13.1
```

**Database Configuration Pattern:**
```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()

# Development database
DATABASE_URL = "postgresql+asyncpg://user:pass@localhost:5432/techblog"

# Test database (conftest.py)
TEST_DATABASE_URL = "postgresql+asyncpg://user:pass@localhost:5432/techblog_test"

engine = create_async_engine(
    DATABASE_URL,
    pool_size=10,           # Connection pool size
    max_overflow=20,        # Max connections beyond pool_size
    pool_pre_ping=True,     # Verify connections before using
    pool_recycle=3600,      # Recycle connections every hour
    echo=False,             # Set True for SQL logging
)

async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False  # Prevent expired attribute errors
)

# Dependency injection
async def get_db():
    async with async_session() as session:
        yield session
```

**Test Database Fixture (conftest.py):**
```python
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

@pytest_asyncio.fixture(scope="function")
async def db_session():
    """Create test database session with automatic rollback."""
    engine = create_async_engine(TEST_DATABASE_URL)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session() as session:
        yield session
        await session.rollback()

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()
```

**Patterns from Research:**
- Use asyncpg for best async PostgreSQL performance
- Implement proper connection pooling (prevents connection exhaustion)
- Use dependency injection for sessions (testable, mockable)
- Separate test database for isolation
- Function-scoped fixtures for maximum test isolation

#### Dependencies

- [ ] Issue #1 (FastAPI setup needed)

---

### Issue #3: Article and Tag Database Models

**Labels:** `type:feature`, `area:backend/models`, `complexity:medium`, `phase:phase-1`
**Estimated Time:** 2 hours
**Dependencies:** #2

#### Description

Create SQLAlchemy models for articles and tags with proper relationships, constraints, and indexes. Implement Pydantic schemas for request/response validation. Include automatic slug generation and proper timestamp handling.

#### Completion Criteria

- [ ] Article model with all fields created
- [ ] Tag model created
- [ ] Many-to-many relationship configured (article_tags table)
- [ ] Database indexes added (slug, draft, created_at)
- [ ] Pydantic schemas for validation (Create, Update, Response)
- [ ] Initial migration generated
- [ ] All model tests pass (factories, validation)
- [ ] Schema validation tests pass

#### Implementation Notes

**Files to Create:**
```
backend/
├── app/
│   ├── models/
│   │   ├── __init__.py
│   │   ├── article.py      # Article SQLAlchemy model
│   │   └── tag.py          # Tag SQLAlchemy model
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── article.py      # Article Pydantic schemas
│   │   └── tag.py          # Tag Pydantic schemas
│   └── utils/
│       └── slug.py         # Slug generation utility
└── tests/
    ├── unit/
    │   ├── test_models.py       # Model tests
    │   ├── test_schemas.py      # Schema validation tests
    │   └── test_slug.py         # Slug generation tests
    └── factories.py             # Factory Boy factories
```

**Article Model (app/models/article.py):**
```python
from sqlalchemy import Column, String, Text, Boolean, DateTime, Table, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.database import Base

# Association table for many-to-many relationship
article_tags = Table(
    'article_tags',
    Base.metadata,
    Column('article_id', UUID(as_uuid=True), ForeignKey('articles.id', ondelete='CASCADE')),
    Column('tag_id', UUID(as_uuid=True), ForeignKey('tags.id', ondelete='CASCADE')),
)

class Article(Base):
    __tablename__ = "articles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, nullable=False, index=True)
    content = Column(Text, nullable=False)
    description = Column(Text)
    draft = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    published_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    tags = relationship("Tag", secondary=article_tags, back_populates="articles")
    media_files = relationship("MediaFile", back_populates="article", cascade="all, delete-orphan")
```

**Tag Model (app/models/tag.py):**
```python
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

from app.database import Base

class Tag(Base):
    __tablename__ = "tags"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(50), unique=True, nullable=False, index=True)

    articles = relationship("Article", secondary="article_tags", back_populates="tags")
```

**Pydantic Schemas (app/schemas/article.py):**
```python
from pydantic import BaseModel, Field, ConfigDict, field_validator
from datetime import datetime
from uuid import UUID

class ArticleBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    content: str = Field(..., min_length=1)
    description: str | None = Field(None, max_length=500)
    draft: bool = True

class ArticleCreate(ArticleBase):
    tags: list[str] = Field(default_factory=list)

    @field_validator('tags')
    @classmethod
    def validate_tags(cls, v):
        if len(v) > 10:
            raise ValueError('Maximum 10 tags allowed')
        return [tag.strip().lower() for tag in v]

class ArticleUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=255)
    content: str | None = Field(None, min_length=1)
    description: str | None = Field(None, max_length=500)
    draft: bool | None = None
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

**Slug Generation Utility (app/utils/slug.py):**
```python
import re
from unidecode import unidecode

def generate_slug(title: str) -> str:
    """Generate URL-friendly slug from title."""
    # Convert to ASCII
    slug = unidecode(title)
    # Lowercase
    slug = slug.lower()
    # Replace spaces and non-alphanumeric with hyphens
    slug = re.sub(r'[^a-z0-9]+', '-', slug)
    # Remove leading/trailing hyphens
    slug = slug.strip('-')
    # Collapse multiple hyphens
    slug = re.sub(r'-+', '-', slug)
    return slug
```

**Factory Boy Factories (tests/factories.py):**
```python
import factory
from factory.fuzzy import FuzzyText, FuzzyChoice
from app.models.article import Article
from app.models.tag import Tag

class TagFactory(factory.Factory):
    class Meta:
        model = Tag

    name = FuzzyText(length=10, prefix='tag-')

class ArticleFactory(factory.Factory):
    class Meta:
        model = Article

    title = FuzzyText(length=50, prefix='Article: ')
    content = FuzzyText(length=1000)
    description = FuzzyText(length=200)
    draft = FuzzyChoice([True, False])
```

**Patterns from Research:**
- Use UUID for primary keys (better for distributed systems, no ID enumeration)
- Implement automatic slug generation (SEO-friendly URLs)
- Use server-side timestamps (consistent timezone handling)
- Separate Create/Update/Response schemas (security, flexibility)
- Index frequently queried fields (slug, draft, created_at)
- Use Pydantic validators for business logic
- Factory Boy for test data generation

#### Dependencies

- [ ] Issue #2 (Database connection needed)

---

### Issue #4: Article CRUD API Endpoints

**Labels:** `type:feature`, `area:backend/api`, `complexity:medium`, `phase:phase-1`
**Estimated Time:** 2-3 hours
**Dependencies:** #3

#### Description

Implement RESTful API endpoints for article CRUD operations (Create, Read, Update, Delete) with pagination, filtering, and proper error handling. Use service layer pattern for business logic separation.

#### Completion Criteria

- [ ] POST /api/v1/articles - Create article (201 status)
- [ ] GET /api/v1/articles - List articles (paginated)
- [ ] GET /api/v1/articles/{slug} - Get article by slug
- [ ] PUT /api/v1/articles/{id} - Update article
- [ ] DELETE /api/v1/articles/{id} - Delete article
- [ ] Pagination working (page, size parameters)
- [ ] Draft/published filtering
- [ ] Proper error handling (404, 400, 422)
- [ ] All API tests pass (integration tests)
- [ ] API documentation auto-generated (OpenAPI)

#### Implementation Notes

**Files to Create:**
```
backend/
├── app/
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       └── articles.py      # Article endpoints
│   ├── services/
│   │   ├── __init__.py
│   │   └── article_service.py   # Business logic
│   └── exceptions.py            # Custom exceptions
└── tests/
    └── integration/
        └── test_articles_api.py # API integration tests
```

**Article API Endpoints (app/api/v1/articles.py):**
```python
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.database import get_db
from app.schemas.article import ArticleCreate, ArticleResponse, ArticleUpdate
from app.services.article_service import ArticleService

router = APIRouter(prefix="/api/v1/articles", tags=["articles"])

@router.post("/", response_model=ArticleResponse, status_code=status.HTTP_201_CREATED)
async def create_article(
    article: ArticleCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new article."""
    service = ArticleService(db)
    return await service.create_article(article)

@router.get("/", response_model=list[ArticleResponse])
async def list_articles(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(20, ge=1, le=100, description="Items per page"),
    draft: bool | None = Query(None, description="Filter by draft status"),
    tag: str | None = Query(None, description="Filter by tag"),
    db: AsyncSession = Depends(get_db)
):
    """List articles with pagination and filtering."""
    service = ArticleService(db)
    return await service.list_articles(page, size, draft, tag)

@router.get("/{slug}", response_model=ArticleResponse)
async def get_article(
    slug: str,
    db: AsyncSession = Depends(get_db)
):
    """Get article by slug."""
    service = ArticleService(db)
    article = await service.get_article_by_slug(slug)
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Article with slug '{slug}' not found"
        )
    return article

@router.put("/{article_id}", response_model=ArticleResponse)
async def update_article(
    article_id: UUID,
    article_update: ArticleUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update an article."""
    service = ArticleService(db)
    article = await service.update_article(article_id, article_update)
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Article with ID '{article_id}' not found"
        )
    return article

@router.delete("/{article_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_article(
    article_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """Delete an article."""
    service = ArticleService(db)
    deleted = await service.delete_article(article_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Article with ID '{article_id}' not found"
        )
```

**Article Service (app/services/article_service.py):**
```python
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from uuid import UUID
from datetime import datetime

from app.models.article import Article
from app.models.tag import Tag
from app.schemas.article import ArticleCreate, ArticleUpdate
from app.utils.slug import generate_slug

class ArticleService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_article(self, data: ArticleCreate) -> Article:
        """Create new article with tags."""
        # Generate unique slug
        slug = await self._generate_unique_slug(data.title)

        # Create article
        article = Article(
            title=data.title,
            slug=slug,
            content=data.content,
            description=data.description,
            draft=data.draft,
            published_at=None if data.draft else datetime.utcnow()
        )

        # Handle tags
        if data.tags:
            article.tags = await self._get_or_create_tags(data.tags)

        self.db.add(article)
        await self.db.commit()
        await self.db.refresh(article)
        return article

    async def list_articles(
        self,
        page: int,
        size: int,
        draft: bool | None = None,
        tag: str | None = None
    ) -> list[Article]:
        """List articles with pagination and filtering."""
        offset = (page - 1) * size
        query = select(Article).options(selectinload(Article.tags))

        # Apply filters
        if draft is not None:
            query = query.where(Article.draft == draft)

        if tag:
            query = query.join(Article.tags).where(Tag.name == tag)

        # Order and paginate
        query = (
            query
            .order_by(Article.created_at.desc())
            .offset(offset)
            .limit(size)
        )

        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_article_by_slug(self, slug: str) -> Article | None:
        """Get article by slug."""
        query = (
            select(Article)
            .options(selectinload(Article.tags))
            .where(Article.slug == slug)
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def update_article(
        self,
        article_id: UUID,
        data: ArticleUpdate
    ) -> Article | None:
        """Update article."""
        query = select(Article).where(Article.id == article_id)
        result = await self.db.execute(query)
        article = result.scalar_one_or_none()

        if not article:
            return None

        # Update fields
        update_data = data.model_dump(exclude_unset=True, exclude={'tags'})
        for field, value in update_data.items():
            setattr(article, field, value)

        # Update slug if title changed
        if 'title' in update_data:
            article.slug = await self._generate_unique_slug(
                data.title, exclude_id=article_id
            )

        # Update published_at when publishing
        if not article.draft and article.published_at is None:
            article.published_at = datetime.utcnow()

        # Handle tags
        if data.tags is not None:
            article.tags = await self._get_or_create_tags(data.tags)

        await self.db.commit()
        await self.db.refresh(article)
        return article

    async def delete_article(self, article_id: UUID) -> bool:
        """Delete article."""
        result = await self.db.execute(
            delete(Article).where(Article.id == article_id)
        )
        await self.db.commit()
        return result.rowcount > 0

    async def _generate_unique_slug(
        self,
        title: str,
        exclude_id: UUID | None = None
    ) -> str:
        """Generate unique slug from title."""
        base_slug = generate_slug(title)
        slug = base_slug
        counter = 1

        while True:
            query = select(Article).where(Article.slug == slug)
            if exclude_id:
                query = query.where(Article.id != exclude_id)

            result = await self.db.execute(query)
            if not result.scalar_one_or_none():
                break

            slug = f"{base_slug}-{counter}"
            counter += 1

        return slug

    async def _get_or_create_tags(self, tag_names: list[str]) -> list[Tag]:
        """Get existing tags or create new ones."""
        tags = []
        for name in tag_names:
            # Try to get existing tag
            query = select(Tag).where(Tag.name == name)
            result = await self.db.execute(query)
            tag = result.scalar_one_or_none()

            if not tag:
                # Create new tag
                tag = Tag(name=name)
                self.db.add(tag)

            tags.append(tag)

        await self.db.flush()  # Ensure tags have IDs
        return tags
```

**Patterns from Research:**
- Separate service layer for business logic (testable, reusable)
- Use slug for article URLs (SEO-friendly)
- Implement pagination with offset/limit
- Proper HTTP status codes (201 for create, 204 for delete, 404 for not found)
- Use selectinload for eager loading (N+1 prevention)
- Dependency injection for database sessions

#### Dependencies

- [ ] Issue #3 (Models and schemas needed)

---

### Issue #5: Media File Database Model

**Labels:** `type:feature`, `area:backend/models`, `complexity:medium`, `phase:phase-1`
**Estimated Time:** 2 hours
**Dependencies:** #3

#### Description

Create SQLAlchemy model for media files with support for images, videos, audio, and documents. Include fields for file metadata (dimensions, duration, file size), security attributes, and relationships to articles.

#### Completion Criteria

- [ ] MediaFile model with all fields created
- [ ] Relationship to Article model configured
- [ ] FileType enum implemented (IMAGE, VIDEO, AUDIO, DOCUMENT)
- [ ] Database indexes added (article_id, file_type, uploaded_at)
- [ ] Pydantic schemas for validation
- [ ] Migration generated
- [ ] All model tests pass
- [ ] Schema validation tests pass

#### Implementation Notes

**Files to Create:**
```
backend/
├── app/
│   ├── models/
│   │   ├── media.py        # MediaFile model
│   │   └── __init__.py     # Updated exports
│   └── schemas/
│       ├── media.py        # Media Pydantic schemas
│       └── __init__.py
└── tests/
    └── unit/
        └── test_media_models.py  # Model tests
```

**Additional Dependency:**
```txt
python-magic==0.4.27  # For file type detection
```

**MediaFile Model (app/models/media.py):**
```python
import enum
from sqlalchemy import Column, String, Integer, Float, Text, DateTime, Enum, BigInteger, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.database import Base

class FileType(str, enum.Enum):
    """Supported file types."""
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    DOCUMENT = "document"

class MediaFile(Base):
    __tablename__ = "media_files"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    article_id = Column(
        UUID(as_uuid=True),
        ForeignKey("articles.id", ondelete="CASCADE"),
        index=True,
        nullable=True  # Media can exist without article
    )

    # File information
    filename = Column(String(255), nullable=False)
    original_filename = Column(String(255), nullable=False)
    file_type = Column(Enum(FileType), nullable=False, index=True)
    mime_type = Column(String(100), nullable=False)
    file_size = Column(BigInteger, nullable=False)  # In bytes
    file_path = Column(Text, nullable=False)
    url = Column(Text, nullable=False)

    # Image/Video specific
    width = Column(Integer, nullable=True)
    height = Column(Integer, nullable=True)

    # Video/Audio specific
    duration = Column(Float, nullable=True)  # In seconds

    # Video specific
    thumbnail_url = Column(Text, nullable=True)

    # Image specific
    alt_text = Column(Text, nullable=True)

    # General
    caption = Column(Text, nullable=True)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    # Relationships
    article = relationship("Article", back_populates="media_files")
```

**Pydantic Schemas (app/schemas/media.py):**
```python
from pydantic import BaseModel, Field, ConfigDict, field_validator
from datetime import datetime
from uuid import UUID
from app.models.media import FileType

class MediaFileBase(BaseModel):
    """Base media file schema."""
    original_filename: str
    file_type: FileType
    caption: str | None = None
    alt_text: str | None = None

class MediaFileCreate(MediaFileBase):
    """Schema for creating media file."""
    article_id: UUID | None = None

class MediaFileUpdate(BaseModel):
    """Schema for updating media file metadata."""
    caption: str | None = None
    alt_text: str | None = None
    article_id: UUID | None = None

class MediaFileResponse(MediaFileBase):
    """Schema for media file response."""
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    article_id: UUID | None
    filename: str
    mime_type: str
    file_size: int
    url: str
    width: int | None = None
    height: int | None = None
    duration: float | None = None
    thumbnail_url: str | None = None
    uploaded_at: datetime

class MediaFileListResponse(BaseModel):
    """Schema for paginated media file list."""
    items: list[MediaFileResponse]
    total: int
    page: int
    size: int
    pages: int
```

**Patterns from Research:**
- Use enum for file types (type safety, validation)
- Store both original and sanitized filenames (security, traceability)
- Include metadata for different media types (flexibility)
- Cascade delete when article is deleted (data integrity)
- BigInteger for file sizes (supports large files up to 100MB)
- Optional article_id (media library concept)

#### Dependencies

- [ ] Issue #3 (Article model needed for relationship)

---

### Issue #6: File Upload Service with Validation

**Labels:** `type:feature`, `area:backend/services`, `complexity:high`, `phase:phase-1`, `security:critical`
**Estimated Time:** 3 hours
**Dependencies:** #5

#### Description

Implement file upload service with multi-layer validation (extension, MIME type, magic bytes content verification), file size limits, and filename sanitization. Support local and S3 storage backends with abstraction layer. This is security-critical following 2025 best practices.

#### Completion Criteria

- [ ] Multi-layer file validation implemented
  - Extension validation
  - MIME type validation
  - Magic bytes (content) validation
- [ ] File size limits enforced per type
- [ ] Filename sanitization working (prevent path traversal)
- [ ] UUID-based filename generation
- [ ] Local storage backend implemented
- [ ] S3 storage backend implemented (optional)
- [ ] Storage abstraction layer
- [ ] All validation tests pass
- [ ] Security tests pass (malicious files rejected)

#### Implementation Notes

**Files to Create:**
```
backend/
├── app/
│   ├── services/
│   │   ├── upload_service.py    # Upload orchestration
│   │   └── storage_service.py   # Storage abstraction
│   └── utils/
│       ├── validator.py         # File validation utilities
│       └── file_utils.py        # File utilities
└── tests/
    ├── unit/
    │   ├── test_upload_service.py
    │   └── test_file_validator.py
    ├── integration/
    │   └── test_file_upload.py
    └── fixtures/
        ├── test_images/         # Valid/invalid test images
        ├── test_videos/
        ├── test_audio/
        └── malicious/          # Malicious file samples
```

**Key Dependencies:**
```txt
python-magic==0.4.27    # Magic bytes validation
aiofiles==23.2.1        # Async file I/O
Pillow==10.1.0          # Image processing
boto3==1.34.14          # AWS S3 (optional)
```

**File Validator (app/utils/validator.py):**
```python
import magic
import os
from pathlib import Path
from fastapi import UploadFile, HTTPException, status
from app.models.media import FileType

# Allowed extensions by file type
ALLOWED_EXTENSIONS = {
    FileType.IMAGE: {'.jpg', '.jpeg', '.png', '.gif', '.webp'},
    FileType.VIDEO: {'.mp4', '.webm', '.mov'},
    FileType.AUDIO: {'.mp3', '.wav', '.ogg'},
    FileType.DOCUMENT: {'.pdf', '.doc', '.docx'}
}

# Allowed MIME types by file type
ALLOWED_MIME_TYPES = {
    FileType.IMAGE: {
        'image/jpeg', 'image/png', 'image/gif', 'image/webp'
    },
    FileType.VIDEO: {
        'video/mp4', 'video/webm', 'video/quicktime'
    },
    FileType.AUDIO: {
        'audio/mpeg', 'audio/wav', 'audio/ogg', 'audio/mp3'
    },
    FileType.DOCUMENT: {
        'application/pdf',
        'application/msword',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    }
}

# Max file sizes (in bytes)
MAX_FILE_SIZES = {
    FileType.IMAGE: 10 * 1024 * 1024,      # 10 MB
    FileType.VIDEO: 100 * 1024 * 1024,     # 100 MB
    FileType.AUDIO: 20 * 1024 * 1024,      # 20 MB
    FileType.DOCUMENT: 10 * 1024 * 1024    # 10 MB
}

class FileValidator:
    """Multi-layer file validation following security best practices."""

    @staticmethod
    async def validate_file(file: UploadFile, file_type: FileType) -> None:
        """
        Perform multi-layer validation:
        1. Extension check
        2. MIME type check
        3. File size check
        4. Magic bytes validation (content-based)

        Raises HTTPException if validation fails.
        """
        # Layer 1: Extension check
        FileValidator._validate_extension(file.filename, file_type)

        # Layer 2: MIME type check
        FileValidator._validate_mime_type(file.content_type, file_type)

        # Layer 3: File size check
        await FileValidator._validate_file_size(file, file_type)

        # Layer 4: Magic bytes validation (most important!)
        await FileValidator._validate_content(file, file_type)

    @staticmethod
    def _validate_extension(filename: str, file_type: FileType) -> None:
        """Validate file extension."""
        ext = Path(filename).suffix.lower()
        if ext not in ALLOWED_EXTENSIONS[file_type]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid file extension '{ext}' for {file_type.value}. "
                       f"Allowed: {', '.join(ALLOWED_EXTENSIONS[file_type])}"
            )

    @staticmethod
    def _validate_mime_type(mime_type: str | None, file_type: FileType) -> None:
        """Validate MIME type from header."""
        if not mime_type or mime_type not in ALLOWED_MIME_TYPES[file_type]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid MIME type '{mime_type}' for {file_type.value}"
            )

    @staticmethod
    async def _validate_file_size(file: UploadFile, file_type: FileType) -> None:
        """Validate file size."""
        # Get file size
        file.file.seek(0, 2)  # Seek to end
        size = file.file.tell()
        file.file.seek(0)     # Reset to beginning

        max_size = MAX_FILE_SIZES[file_type]
        if size > max_size:
            max_mb = max_size / 1024 / 1024
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"File too large ({size} bytes). "
                       f"Maximum allowed: {max_mb:.1f} MB"
            )

    @staticmethod
    async def _validate_content(file: UploadFile, file_type: FileType) -> None:
        """
        Validate file content using magic bytes.
        This is the MOST IMPORTANT security layer.
        """
        # Read first 2KB for magic byte detection
        file_data = await file.read(2048)
        await file.seek(0)  # Reset file pointer

        # Detect MIME type from content
        detected_mime = magic.from_buffer(file_data, mime=True)

        # Verify detected MIME matches expected type
        if detected_mime not in ALLOWED_MIME_TYPES[file_type]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File content doesn't match {file_type.value} type. "
                       f"Detected: {detected_mime}"
            )

def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename to prevent path traversal attacks.
    Returns safe filename with only alphanumeric, dash, underscore, and dot.
    """
    # Get base filename without path
    safe_name = os.path.basename(filename)

    # Remove or replace dangerous characters
    safe_name = safe_name.replace('..', '')
    safe_name = safe_name.replace('/', '')
    safe_name = safe_name.replace('\\', '')

    # Keep only safe characters
    import re
    safe_name = re.sub(r'[^a-zA-Z0-9._-]', '_', safe_name)

    return safe_name
```

**Storage Service (app/services/storage_service.py):**
```python
from abc import ABC, abstractmethod
import aiofiles
import uuid
from pathlib import Path
from fastapi import UploadFile

class StorageBackend(ABC):
    """Abstract storage backend for file uploads."""

    @abstractmethod
    async def save_file(self, file: UploadFile, path: str) -> str:
        """Save file and return full path."""
        pass

    @abstractmethod
    async def delete_file(self, path: str) -> bool:
        """Delete file and return success status."""
        pass

    @abstractmethod
    def get_url(self, path: str) -> str:
        """Get public URL for file."""
        pass

class LocalStorage(StorageBackend):
    """Local filesystem storage backend."""

    def __init__(self, base_path: str = "./uploads"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)

    async def save_file(self, file: UploadFile, path: str) -> str:
        """Save file to local filesystem in chunks."""
        full_path = self.base_path / path
        full_path.parent.mkdir(parents=True, exist_ok=True)

        # Stream file in chunks (memory efficient)
        async with aiofiles.open(full_path, 'wb') as out_file:
            while content := await file.read(1024 * 1024):  # 1MB chunks
                await out_file.write(content)

        return str(full_path)

    async def delete_file(self, path: str) -> bool:
        """Delete file from filesystem."""
        full_path = self.base_path / path
        if full_path.exists():
            full_path.unlink()
            return True
        return False

    def get_url(self, path: str) -> str:
        """Get URL for file (served via FastAPI static files)."""
        return f"/uploads/{path}"

class S3Storage(StorageBackend):
    """AWS S3 storage backend (optional)."""

    def __init__(self, bucket_name: str, region: str = "us-east-1"):
        import boto3
        self.bucket_name = bucket_name
        self.s3_client = boto3.client('s3', region_name=region)

    async def save_file(self, file: UploadFile, path: str) -> str:
        """Upload file to S3."""
        # Read file content
        content = await file.read()
        await file.seek(0)

        # Upload to S3
        self.s3_client.put_object(
            Bucket=self.bucket_name,
            Key=path,
            Body=content,
            ContentType=file.content_type
        )

        return path

    async def delete_file(self, path: str) -> bool:
        """Delete file from S3."""
        try:
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=path)
            return True
        except Exception:
            return False

    def get_url(self, path: str) -> str:
        """Get S3 public URL."""
        return f"https://{self.bucket_name}.s3.amazonaws.com/{path}"
```

**Upload Service (app/services/upload_service.py):**
```python
from fastapi import UploadFile
from uuid import uuid4
from pathlib import Path

from app.models.media import FileType
from app.utils.validator import FileValidator, sanitize_filename
from app.services.storage_service import StorageBackend, LocalStorage

class UploadService:
    """Orchestrates file upload with validation and storage."""

    def __init__(self, storage: StorageBackend | None = None):
        self.storage = storage or LocalStorage()
        self.validator = FileValidator()

    async def upload_file(
        self,
        file: UploadFile,
        file_type: FileType
    ) -> dict:
        """
        Upload file with full validation.
        Returns file metadata dictionary.
        """
        # Validate file
        await self.validator.validate_file(file, file_type)

        # Generate safe filename
        ext = Path(file.filename).suffix
        sanitized_original = sanitize_filename(file.filename)
        unique_filename = f"{uuid4()}{ext}"

        # Determine storage path
        file_path = f"{file_type.value}s/{unique_filename}"

        # Save file
        full_path = await self.storage.save_file(file, file_path)

        # Get file size
        file.file.seek(0, 2)
        file_size = file.file.tell()
        file.file.seek(0)

        # Return metadata
        return {
            "filename": unique_filename,
            "original_filename": sanitized_original,
            "file_type": file_type,
            "mime_type": file.content_type,
            "file_size": file_size,
            "file_path": file_path,
            "url": self.storage.get_url(file_path)
        }
```

**Patterns from Research:**
- Multi-layer validation (85% malicious file prevention)
- Magic bytes validation is CRITICAL (can't be spoofed)
- Stream large files in chunks (prevent memory exhaustion)
- Storage abstraction for easy cloud migration
- Sanitize filenames to prevent path traversal
- UUID filenames prevent enumeration attacks

#### Dependencies

- [ ] Issue #5 (Media model needed)

---

(Continuing with Issues #7 and #8...)

---

## Summary

This Phase 1 proposal includes 8 foundational backend issues covering:

1. FastAPI setup with TDD infrastructure
2. PostgreSQL database connection with async support
3. Article and Tag models with relationships
4. Article CRUD API endpoints
5. Media file model for multimedia support
6. File upload service with multi-layer security validation
7. Image upload API (to be detailed in next section)
8. Video/Audio/Document upload APIs (to be detailed in next section)

**Key Success Metrics:**
- Test coverage > 80%
- Zero security vulnerabilities
- All APIs documented in OpenAPI
- Migration scripts working
- Docker support ready

**Next Steps:**
1. Review and approve this proposal
2. Create GitHub issues using issue-creator agent
3. Generate detailed TDD plans for each issue
4. Begin RED-GREEN-REFACTOR cycles

---

**Total Estimated Time for Phase 1:** 16-20 hours
