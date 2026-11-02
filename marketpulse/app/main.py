"""
MARKETPULSE — FastAPI Production Authoritative Backend.
Autonomous Business Intelligence and Evidence-Driven Deep Research Engine.
Exclusively powers the Next.js Stage 3 frontend.
Zero Gradio and Zero Jinja2 dependencies.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.db import initialize_database
from app.api.endpoints import router as api_router
from app.api.strategic_endpoints import router as strategic_api_router


# Initialize FastAPI application
app = FastAPI(
    title="MARKETPULSE",
    description="Autonomous Business Intelligence & Evidence-Driven Deep Research Engine",
    version="3.0.0",
)

# Enable CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3001",
        "*",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_event():
    """Ensure database schema tables are initialized safely."""
    initialize_database()


@app.get("/", tags=["Root"])
def root():
    """API Gateway root status endpoint."""
    return {
        "service": "MARKETPULSE Authoritative Intelligence Backend",
        "version": "3.0.0",
        "status": "online",
        "frontend": "http://localhost:3000",
        "docs": "/docs",
        "architecture": "FastAPI + Next.js App Router + LangGraph + SQLModel",
    }


# Mount REST API Routers
app.include_router(api_router)
app.include_router(strategic_api_router)
