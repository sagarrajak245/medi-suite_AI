"""
FastAPI Application Entry Point
Medical Coding Pipeline API
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.api.v1.router import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan events.
    Runs on startup and shutdown.
    """
    # Startup
    print(f"🚀 Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    print(f"📍 Environment: {settings.ENVIRONMENT}")
    print(f"🔗 API Docs: http://{settings.HOST}:{settings.PORT}/docs")
    
    yield
    
    # Shutdown
    print(f"👋 Shutting down {settings.APP_NAME}")


# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    description="""
## 🏥 Medical Coding Pipeline API

A robust FastAPI backend for automated medical billing code assignment 
using CrewAI multi-agent architecture with RAG.

### Features:
- **Multi-Agent System**: CrewAI-powered agents for ICD-10-CM, CPT-4, and HCPCS coding
- **RAG Pipeline**: Pinecone vector database + LLM reasoning  
- **LLM as Judge**: Quality evaluation and compliance checking
- **PDF Support**: Extract and process medical reports from PDFs

### Endpoints:
- `/api/v1/health` - Health check
- `/api/v1/coding/process` - Process medical text
- `/api/v1/coding/process-pdf` - Upload and process PDF
- `/api/v1/coding/process-test-pdf` - Process test PDF from backend folder
    """,
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(
    api_router,
    prefix="/api/v1"
)


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information"""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "health": "/api/v1/health"
    }


# Run with: uvicorn app.main:app --reload
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
