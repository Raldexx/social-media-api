
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.db.session import init_db
from app.api.v1.endpoints import auth, users, roles




# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)


# CORS middleware (allows frontend to call API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,  # ["http://localhost:3000", ...]
    allow_credentials=True,  # Allow cookies
    allow_methods=["*"],  # Allow all methods (GET, POST, PUT, DELETE)
    allow_headers=["*"],  # Allow all headers
)


# Startup event (runs when app starts)
@app.on_event("startup")
def on_startup():
    """
    Initialize database on app startup
    Creates all tables if they don't exist
    """
    print("🚀 Starting application...")
    print("📊 Initializing database...")
    init_db()  # Create tables
    print("✅ Database initialized successfully!")


# Root endpoint
@app.get("/")
def root():
    """
    Root endpoint
    Returns API info and available endpoints
    """
    return {
        "message": "Welcome to Social Media API! 🚀",
        "version": settings.VERSION,
        "docs": "/docs",  # Swagger documentation
        "endpoints": {
            "auth": "/api/v1/auth",
            "users": "/api/v1/users",
            "roles": "/api/v1/roles"
        }
    }


# Health check endpoint
@app.get("/health")
def health_check():
    """
    Health check endpoint
    Used by monitoring tools to check if API is running
    """
    return {
        "status": "healthy",
        "version": settings.VERSION
    }


# Include routers (register all endpoints)
app.include_router(
    auth.router,  # Auth endpoints (/register, /login, /refresh)
    prefix=settings.API_V1_STR  # /api/v1
)

app.include_router(
    users.router,  # User endpoints (/me, /search, /{username})
    prefix=settings.API_V1_STR  # /api/v1
)

app.include_router(
    roles.router,  # Role endpoints (admin only)
    prefix=settings.API_V1_STR  # /api/v1
)


# Run with: uvicorn app.main:app --reload