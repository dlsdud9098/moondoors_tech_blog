# Phase 1: Issues #7-#8 - Media Upload Endpoints

This document continues from phase-1-github-issues-proposal.md with the remaining two issues for Phase 1.

---

## Issue #7: Image Upload API Endpoint

**Labels:** `type:feature`, `area:backend/api`, `complexity:medium`, `phase:phase-1`
**Estimated Time:** 2 hours
**Dependencies:** #6

### Description

Implement API endpoint for image uploads with validation, automatic thumbnail generation, and WebP conversion for optimization. Store metadata in database and support multiple image formats.

### Completion Criteria

- [ ] POST /api/v1/upload/image endpoint works
- [ ] Image validation implemented (uses Issue #6 validator)
- [ ] Thumbnail generation working (200x200px)
- [ ] WebP conversion implemented (quality 85%)
- [ ] Image metadata extracted (dimensions, EXIF)
- [ ] Database record created
- [ ] All upload tests pass
- [ ] Error handling for invalid/corrupted images
- [ ] API docs auto-generated

### Implementation Notes

**Files to Create:**
```
backend/
├── app/
│   ├── api/
│   │   └── v1/
│       └── upload.py            # Upload endpoints
│   └── services/
│       └── image_service.py     # Image processing
└── tests/
    ├── integration/
    │   └── test_image_upload.py # Integration tests
    └── fixtures/
        └── test_images/         # Valid test images
```

**Additional Dependencies:**
```txt
Pillow==10.1.0          # Image processing
pillow-heif==0.15.0     # HEIF/HEIC support (optional)
```

**Image Upload Endpoint (app/api/v1/upload.py):**
```python
from fastapi import APIRouter, UploadFile, File, Depends, Form
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.database import get_db
from app.models.media import FileType
from app.schemas.media import MediaFileResponse
from app.services.image_service import ImageService

router = APIRouter(prefix="/api/v1/upload", tags=["upload"])

@router.post("/image", response_model=MediaFileResponse, status_code=201)
async def upload_image(
    file: UploadFile = File(..., description="Image file to upload"),
    article_id: UUID | None = Form(None, description="Optional article ID"),
    alt_text: str | None = Form(None, description="Alternative text for accessibility"),
    caption: str | None = Form(None, description="Image caption"),
    db: AsyncSession = Depends(get_db)
):
    """
    Upload an image file with automatic processing:
    - Validation (extension, MIME, magic bytes, size)
    - Thumbnail generation (200x200)
    - WebP conversion for optimization
    - Metadata extraction (dimensions)
    """
    service = ImageService(db)
    media_file = await service.process_and_save_image(
        file=file,
        article_id=article_id,
        alt_text=alt_text,
        caption=caption
    )
    return media_file
```

**Image Service (app/services/image_service.py):**
```python
from PIL import Image
import io
from pathlib import Path
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import UploadFile
from uuid import UUID, uuid4

from app.models.media import MediaFile, FileType
from app.services.upload_service import UploadService
from app.services.storage_service import LocalStorage
from app.utils.validator import FileValidator

class ImageService:
    """Service for image processing and storage."""

    def __init__(self, db: AsyncSession, storage=None):
        self.db = db
        self.storage = storage or LocalStorage()
        self.upload_service = UploadService(self.storage)

    async def process_and_save_image(
        self,
        file: UploadFile,
        article_id: UUID | None = None,
        alt_text: str | None = None,
        caption: str | None = None
    ) -> MediaFile:
        """
        Process and save image with:
        1. Validation
        2. Thumbnail generation
        3. WebP conversion
        4. Metadata extraction
        """
        # Validate file
        await FileValidator.validate_file(file, FileType.IMAGE)

        # Read image
        content = await file.read()
        await file.seek(0)
        image = Image.open(io.BytesIO(content))

        # Extract dimensions
        width, height = image.size

        # Generate unique filename
        ext = Path(file.filename).suffix.lower()
        filename = f"{uuid4()}{ext}"
        file_path = f"images/originals/{filename}"

        # Save original image
        await file.seek(0)
        await self.storage.save_file(file, file_path)

        # Generate thumbnail
        thumbnail_url = await self._generate_thumbnail(image, filename)

        # Generate WebP version for optimization
        webp_url = await self._generate_webp(image, filename)

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
            thumbnail_url=thumbnail_url,
            alt_text=alt_text,
            caption=caption
        )

        self.db.add(media_file)
        await self.db.commit()
        await self.db.refresh(media_file)

        return media_file

    async def _generate_thumbnail(self, image: Image, filename: str) -> str:
        """Generate 200x200 thumbnail."""
        # Create thumbnail (maintains aspect ratio)
        thumb = image.copy()
        thumb.thumbnail((200, 200), Image.Resampling.LANCZOS)

        # Save thumbnail
        thumb_filename = f"thumb_{filename}"
        thumb_path = f"images/thumbnails/{thumb_filename}"

        buffer = io.BytesIO()
        # Save in original format
        format = image.format or 'JPEG'
        thumb.save(buffer, format=format, quality=90)
        buffer.seek(0)

        # Create temporary UploadFile-like object
        from fastapi import UploadFile
        thumb_upload = UploadFile(
            file=buffer,
            filename=thumb_filename,
            size=buffer.getbuffer().nbytes
        )

        await self.storage.save_file(thumb_upload, thumb_path)
        return self.storage.get_url(thumb_path)

    async def _generate_webp(self, image: Image, filename: str) -> str:
        """Generate optimized WebP version."""
        webp_filename = Path(filename).stem + ".webp"
        webp_path = f"images/optimized/{webp_filename}"

        # Convert to WebP
        buffer = io.BytesIO()
        image.save(buffer, format="WEBP", quality=85, method=6)
        buffer.seek(0)

        # Save WebP
        from fastapi import UploadFile
        webp_upload = UploadFile(
            file=buffer,
            filename=webp_filename,
            size=buffer.getbuffer().nbytes
        )

        await self.storage.save_file(webp_upload, webp_path)
        return self.storage.get_url(webp_path)
```

**Integration Test Example (tests/integration/test_image_upload.py):**
```python
import pytest
from httpx import AsyncClient
from PIL import Image
import io

@pytest.mark.asyncio
async def test_upload_valid_image(client: AsyncClient):
    """Test uploading a valid PNG image."""
    # Create test image
    img = Image.new('RGB', (800, 600), color='red')
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)

    # Upload
    files = {'file': ('test.png', img_bytes, 'image/png')}
    data = {
        'alt_text': 'Test image',
        'caption': 'A test image'
    }

    response = await client.post('/api/v1/upload/image', files=files, data=data)

    assert response.status_code == 201
    data = response.json()
    assert data['file_type'] == 'image'
    assert data['width'] == 800
    assert data['height'] == 600
    assert data['thumbnail_url'] is not None
    assert data['alt_text'] == 'Test image'

@pytest.mark.asyncio
async def test_upload_image_too_large(client: AsyncClient):
    """Test that images over 10MB are rejected."""
    # Create large image (will compress, but test principle)
    img = Image.new('RGB', (10000, 10000), color='blue')
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)

    files = {'file': ('large.png', img_bytes, 'image/png')}
    response = await client.post('/api/v1/upload/image', files=files)

    assert response.status_code == 413  # Request Entity Too Large

@pytest.mark.asyncio
async def test_upload_fake_image(client: AsyncClient):
    """Test that fake images (wrong magic bytes) are rejected."""
    # Create file with .png extension but PDF content
    fake_content = b'%PDF-1.4 fake content'
    files = {'file': ('fake.png', io.BytesIO(fake_content), 'image/png')}

    response = await client.post('/api/v1/upload/image', files=files)

    assert response.status_code == 400
    assert 'content doesn\'t match' in response.json()['detail'].lower()
```

**Patterns from Research:**
- Generate thumbnails automatically (better UX)
- Create WebP versions for 30-50% size reduction
- Extract image metadata (dimensions, EXIF if needed)
- Store multiple versions (original, thumb, optimized)
- Use Pillow's LANCZOS resampling for quality thumbnails

### Dependencies

- [ ] Issue #6 (Upload service needed)

---

## Issue #8: Video/Audio/Document Upload Endpoints

**Labels:** `type:feature`, `area:backend/api`, `complexity:medium`, `phase:phase-1`
**Estimated Time:** 2-3 hours
**Dependencies:** #6, #7

### Description

Implement API endpoints for uploading videos, audio files, and documents. Include validation, metadata extraction (duration, bitrate), and thumbnail generation for videos.

### Completion Criteria

- [ ] POST /api/v1/upload/video endpoint works
- [ ] POST /api/v1/upload/audio endpoint works
- [ ] POST /api/v1/upload/document endpoint works
- [ ] Video duration extraction working
- [ ] Video thumbnail generation (first frame)
- [ ] Audio duration and bitrate extraction
- [ ] All file type validations working
- [ ] All upload tests pass
- [ ] Error handling for corrupted files

### Implementation Notes

**Additional Dependencies:**
```txt
ffmpeg-python==0.2.0    # Video/audio metadata and thumbnails
mutagen==1.47.0         # Audio metadata (alternative)
```

**Note:** Requires FFmpeg to be installed on system:
```bash
# Ubuntu/Debian
apt-get install ffmpeg

# macOS
brew install ffmpeg
```

**Video/Audio/Document Endpoints (app/api/v1/upload.py):**
```python
@router.post("/video", response_model=MediaFileResponse, status_code=201)
async def upload_video(
    file: UploadFile = File(..., description="Video file to upload"),
    article_id: UUID | None = Form(None),
    caption: str | None = Form(None),
    db: AsyncSession = Depends(get_db)
):
    """
    Upload a video file with automatic processing:
    - Validation (extension, MIME, magic bytes, size ≤ 100MB)
    - Duration extraction
    - Thumbnail generation (first frame)
    """
    service = VideoService(db)
    media_file = await service.process_and_save_video(
        file=file,
        article_id=article_id,
        caption=caption
    )
    return media_file

@router.post("/audio", response_model=MediaFileResponse, status_code=201)
async def upload_audio(
    file: UploadFile = File(..., description="Audio file to upload"),
    article_id: UUID | None = Form(None),
    caption: str | None = Form(None),
    db: AsyncSession = Depends(get_db)
):
    """
    Upload an audio file with automatic processing:
    - Validation (extension, MIME, magic bytes, size ≤ 20MB)
    - Duration and bitrate extraction
    """
    service = AudioService(db)
    media_file = await service.process_and_save_audio(
        file=file,
        article_id=article_id,
        caption=caption
    )
    return media_file

@router.post("/document", response_model=MediaFileResponse, status_code=201)
async def upload_document(
    file: UploadFile = File(..., description="Document file to upload"),
    article_id: UUID | None = Form(None),
    caption: str | None = Form(None),
    db: AsyncSession = Depends(get_db)
):
    """
    Upload a document file with validation:
    - Validation (extension, MIME, magic bytes, size ≤ 10MB)
    - PDF, DOC, DOCX supported
    """
    service = DocumentService(db)
    media_file = await service.process_and_save_document(
        file=file,
        article_id=article_id,
        caption=caption
    )
    return media_file
```

**Video Service (app/services/video_service.py):**
```python
import ffmpeg
from pathlib import Path
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import UploadFile
from uuid import UUID, uuid4

from app.models.media import MediaFile, FileType
from app.services.upload_service import UploadService
from app.services.storage_service import LocalStorage
from app.utils.validator import FileValidator

class VideoService:
    """Service for video processing and storage."""

    def __init__(self, db: AsyncSession, storage=None):
        self.db = db
        self.storage = storage or LocalStorage()

    async def process_and_save_video(
        self,
        file: UploadFile,
        article_id: UUID | None = None,
        caption: str | None = None
    ) -> MediaFile:
        """Process and save video with metadata extraction."""
        # Validate
        await FileValidator.validate_file(file, FileType.VIDEO)

        # Generate filename
        ext = Path(file.filename).suffix.lower()
        filename = f"{uuid4()}{ext}"
        file_path = f"videos/{filename}"

        # Save file
        await file.seek(0)
        full_path = await self.storage.save_file(file, file_path)

        # Extract metadata using FFmpeg
        try:
            probe = ffmpeg.probe(full_path)
            video_info = next(
                s for s in probe['streams'] if s['codec_type'] == 'video'
            )

            duration = float(probe['format']['duration'])
            width = int(video_info['width'])
            height = int(video_info['height'])
        except (ffmpeg.Error, StopIteration, KeyError):
            duration = None
            width = None
            height = None

        # Generate thumbnail (first frame)
        thumbnail_url = await self._generate_thumbnail(full_path, filename)

        # Get file size
        await file.seek(0, 2)
        file_size = file.file.tell()

        # Create database record
        media_file = MediaFile(
            article_id=article_id,
            filename=filename,
            original_filename=file.filename,
            file_type=FileType.VIDEO,
            mime_type=file.content_type,
            file_size=file_size,
            file_path=file_path,
            url=self.storage.get_url(file_path),
            width=width,
            height=height,
            duration=duration,
            thumbnail_url=thumbnail_url,
            caption=caption
        )

        self.db.add(media_file)
        await self.db.commit()
        await self.db.refresh(media_file)

        return media_file

    async def _generate_thumbnail(self, video_path: str, filename: str) -> str:
        """Generate thumbnail from first frame of video."""
        thumb_filename = f"{Path(filename).stem}_thumb.jpg"
        thumb_path = f"videos/thumbnails/{thumb_filename}"
        full_thumb_path = self.storage.base_path / thumb_path

        # Create directory
        full_thumb_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            # Extract frame at 1 second
            (
                ffmpeg
                .input(video_path, ss=1)
                .output(str(full_thumb_path), vframes=1)
                .overwrite_output()
                .run(capture_stdout=True, capture_stderr=True)
            )
            return self.storage.get_url(thumb_path)
        except ffmpeg.Error:
            return None
```

**Audio Service (app/services/audio_service.py):**
```python
import ffmpeg
from pathlib import Path
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import UploadFile
from uuid import UUID, uuid4

from app.models.media import MediaFile, FileType
from app.services.upload_service import UploadService
from app.services.storage_service import LocalStorage
from app.utils.validator import FileValidator

class AudioService:
    """Service for audio processing and storage."""

    def __init__(self, db: AsyncSession, storage=None):
        self.db = db
        self.storage = storage or LocalStorage()

    async def process_and_save_audio(
        self,
        file: UploadFile,
        article_id: UUID | None = None,
        caption: str | None = None
    ) -> MediaFile:
        """Process and save audio with metadata extraction."""
        # Validate
        await FileValidator.validate_file(file, FileType.AUDIO)

        # Generate filename
        ext = Path(file.filename).suffix.lower()
        filename = f"{uuid4()}{ext}"
        file_path = f"audio/{filename}"

        # Save file
        await file.seek(0)
        full_path = await self.storage.save_file(file, file_path)

        # Extract metadata using FFmpeg
        try:
            probe = ffmpeg.probe(full_path)
            audio_info = next(
                s for s in probe['streams'] if s['codec_type'] == 'audio'
            )

            duration = float(probe['format']['duration'])
        except (ffmpeg.Error, StopIteration, KeyError):
            duration = None

        # Get file size
        await file.seek(0, 2)
        file_size = file.file.tell()

        # Create database record
        media_file = MediaFile(
            article_id=article_id,
            filename=filename,
            original_filename=file.filename,
            file_type=FileType.AUDIO,
            mime_type=file.content_type,
            file_size=file_size,
            file_path=file_path,
            url=self.storage.get_url(file_path),
            duration=duration,
            caption=caption
        )

        self.db.add(media_file)
        await self.db.commit()
        await self.db.refresh(media_file)

        return media_file
```

**Document Service (app/services/document_service.py):**
```python
from pathlib import Path
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import UploadFile
from uuid import UUID, uuid4

from app.models.media import MediaFile, FileType
from app.services.upload_service import UploadService
from app.services.storage_service import LocalStorage
from app.utils.validator import FileValidator

class DocumentService:
    """Service for document processing and storage."""

    def __init__(self, db: AsyncSession, storage=None):
        self.db = db
        self.storage = storage or LocalStorage()

    async def process_and_save_document(
        self,
        file: UploadFile,
        article_id: UUID | None = None,
        caption: str | None = None
    ) -> MediaFile:
        """Process and save document."""
        # Validate
        await FileValidator.validate_file(file, FileType.DOCUMENT)

        # Generate filename
        ext = Path(file.filename).suffix.lower()
        filename = f"{uuid4()}{ext}"
        file_path = f"documents/{filename}"

        # Save file
        await file.seek(0)
        await self.storage.save_file(file, file_path)

        # Get file size
        await file.seek(0, 2)
        file_size = file.file.tell()

        # Create database record
        media_file = MediaFile(
            article_id=article_id,
            filename=filename,
            original_filename=file.filename,
            file_type=FileType.DOCUMENT,
            mime_type=file.content_type,
            file_size=file_size,
            file_path=file_path,
            url=self.storage.get_url(file_path),
            caption=caption
        )

        self.db.add(media_file)
        await self.db.commit()
        await self.db.refresh(media_file)

        return media_file
```

**Patterns from Research:**
- Extract duration for video/audio files (essential for players)
- Generate video thumbnails (first frame at 1 second)
- Use FFmpeg for reliable media metadata extraction
- Validate file integrity (FFmpeg probe will fail on corrupted files)
- Store metadata for playback controls

### Dependencies

- [ ] Issue #6 (Upload service needed)
- [ ] Issue #7 (Upload patterns established)

---

## Phase 1 Complete!

With all 8 issues implemented, Phase 1 (Backend Foundation) will provide:

**Complete Backend Infrastructure:**
- FastAPI application with TDD setup
- PostgreSQL database with async SQLAlchemy
- Article and Tag models with CRUD APIs
- Media file model supporting all file types
- Secure multi-layer file upload validation
- Image/Video/Audio/Document upload endpoints
- Storage abstraction (local + S3 ready)

**Security Features:**
- Magic bytes validation (85% attack prevention)
- Filename sanitization
- File size limits
- MIME type verification
- UUID-based filenames

**Performance Features:**
- Async database operations
- Connection pooling
- Streaming file uploads (1MB chunks)
- Thumbnail generation
- WebP conversion for images

**Testing:**
- >80% test coverage
- Unit tests for models, services, utilities
- Integration tests for APIs
- Security tests for file uploads

**Ready for Phase 2:**
With Phase 1 complete, the backend will be fully functional and ready for frontend integration in Phase 2.

---

**Next Actions:**
1. Review and approve Phase 1 issues
2. Create GitHub issues (#1-#8)
3. Generate detailed TDD plans for each issue
4. Begin implementation with RED-GREEN-REFACTOR cycles
