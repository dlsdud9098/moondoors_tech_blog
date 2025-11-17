"""FastAPI application entry point."""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import close_db, init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan events.

    Args:
        app: FastAPI application instance

    Yields:
        None: Application runs during this period
    """
    # Startup: Initialize database
    await init_db()
    yield
    # Shutdown: Close database connections
    await close_db()


app = FastAPI(
    title="Moondoors Tech Blog API",
    version="0.1.0",
    description="Backend API for Moondoors Tech Blog",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure properly in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root() -> dict[str, str]:
    """Root endpoint."""
    return {"message": "Moondoors Tech Blog API"}


@app.get("/health")
async def health() -> dict[str, str]:
    """Health check endpoint.

    Returns:
        dict: Health status and version information
    """
    return {
        "status": "healthy",
        "version": app.version,
    }
