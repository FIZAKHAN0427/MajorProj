from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from datetime import datetime
from loguru import logger

from .routes import router
from .schemas import HealthResponse
from ..config import settings
from ..utils import setup_logging, create_directory_structure
from ..database import db_manager

# Setup logging
setup_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    logger.info("Starting Crop Recommendation API")
    
    # Create directory structure
    create_directory_structure()
    
    # Connect to database (optional)
    try:
        db_manager.connect()
    except Exception as e:
        logger.warning(f"Database connection failed: {e}")
        logger.info("API will continue without database functionality")
    
    logger.info("API startup completed")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Crop Recommendation API")
    try:
        db_manager.disconnect()
    except Exception as e:
        logger.warning(f"Database disconnection error: {e}")
    
    logger.info("API shutdown completed")

# Create FastAPI application
app = FastAPI(
    title="Crop Recommendation API",
    description="AI-powered crop recommendation system using machine learning and satellite data",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix="/api/v1", tags=["predictions"])

@app.get("/", response_model=HealthResponse)
async def root():
    """Root endpoint with API information"""
    return HealthResponse(
        status="ok",
        timestamp=datetime.now().isoformat(),
        version="1.0.0"
    )

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="ok",
        timestamp=datetime.now().isoformat(),
        version="1.0.0"
    )

@app.get("/api/health", response_model=HealthResponse)
async def api_health_check():
    """API health check endpoint"""
    return HealthResponse(
        status="ok",
        timestamp=datetime.now().isoformat(),
        version="1.0.0"
    )

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Global exception: {exc}")
    return HTTPException(status_code=500, detail="Internal server error")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG
    )