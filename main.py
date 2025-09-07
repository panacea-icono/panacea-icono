#!/usr/bin/env python3
"""
🏥 PANACEA ICONO - Main Application
FastAPI application with AI models integration
"""

import os
import logging
from typing import Dict, Any, Optional
from pathlib import Path
from datetime import datetime

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import uvicorn

# Import Hugging Face manager
try:
    from huggingface_config import HuggingFaceManager
    HF_MANAGER_AVAILABLE = True
except ImportError:
    HuggingFaceManager = None
    HF_MANAGER_AVAILABLE = False

# Import GitHub Repository Manager
try:
    from github_repo_manager_mcp import GitHubRepoManagerMCP
    GITHUB_MANAGER_AVAILABLE = True
except ImportError:
    GitHubRepoManagerMCP = None
    GITHUB_MANAGER_AVAILABLE = False

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="🏥 PANACEA ICONO",
    description="AI-Powered Healthcare Solutions with Docker and Hugging Face Integration",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class HealthResponse(BaseModel):
    status: str = Field(description="Health status")
    timestamp: str = Field(description="Current timestamp")
    services: Dict[str, str] = Field(description="Service statuses")
    version: str = Field(description="Application version")

class TextRequest(BaseModel):
    text: str = Field(description="Input text for AI processing", min_length=1)
    task: Optional[str] = Field(description="AI task type", default="sentiment-analysis")

class TextResponse(BaseModel):
    result: Any = Field(description="AI processing result")
    task: str = Field(description="Task performed")
    model: str = Field(description="Model used")

class ModelInfo(BaseModel):
    name: str = Field(description="Model name")
    task: str = Field(description="Task type")
    status: str = Field(description="Model status")

# Global variables
hf_manager: Optional[HuggingFaceManager] = None
github_manager: Optional[GitHubRepoManagerMCP] = None

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    global hf_manager, github_manager
    
    logger.info("🚀 Starting PANACEA ICONO application...")
    
    # Initialize Hugging Face manager
    if HF_MANAGER_AVAILABLE and HuggingFaceManager:
        try:
            hf_manager = HuggingFaceManager()
            logger.info("✅ Hugging Face manager initialized")
        except Exception as e:
            logger.error(f"❌ Error initializing Hugging Face manager: {e}")
            hf_manager = None
    
    # Initialize GitHub Repository manager
    if GITHUB_MANAGER_AVAILABLE and GitHubRepoManagerMCP:
        try:
            github_manager = GitHubRepoManagerMCP()
            logger.info("✅ GitHub repository manager initialized")
        except Exception as e:
            logger.error(f"❌ Error initializing GitHub manager: {e}")
            github_manager = None
    
    logger.info("🎉 PANACEA ICONO application started successfully!")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("🛑 Shutting down PANACEA ICONO application...")

@app.get("/", response_model=Dict[str, str])
async def root():
    """Root endpoint"""
    return {
        "message": "🏥 Welcome to PANACEA ICONO!",
        "description": "AI-Powered Healthcare Solutions",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    from datetime import datetime
    
    # Check services
    services = {
        "app": "healthy",
        "huggingface": "healthy" if hf_manager else "unavailable",
        "github": "healthy" if github_manager else "unavailable",
        "docker": "healthy",
        "heroku": "healthy"
    }
    
    # Test Hugging Face connection if available
    if hf_manager:
        try:
            if hf_manager.verify_connection():
                services["huggingface"] = "healthy"
            else:
                services["huggingface"] = "unhealthy"
        except Exception as e:
            logger.error(f"Error checking Hugging Face health: {e}")
            services["huggingface"] = "error"
    
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow().isoformat(),
        services=services,
        version="1.0.0"
    )

@app.post("/ai/process", response_model=TextResponse)
async def process_text(request: TextRequest):
    """Process text with AI models"""
    if not hf_manager:
        raise HTTPException(
            status_code=503, 
            detail="Hugging Face service not available"
        )
    
    try:
        # Create pipeline for the requested task
        task = request.task or "sentiment-analysis"
        pipeline_obj = hf_manager.create_pipeline(task)
        if not pipeline_obj:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported task: {task}"
            )
        
        # Process the text
        result = pipeline_obj(request.text)
        
        return TextResponse(
            result=result,
            task=task,
            model=str(type(pipeline_obj).__name__)
        )
        
    except Exception as e:
        logger.error(f"Error processing text: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing text: {str(e)}"
        )

@app.get("/ai/models", response_model=Dict[str, Any])
async def list_models():
    """List available AI models"""
    if not hf_manager:
        raise HTTPException(
            status_code=503,
            detail="Hugging Face service not available"
        )
    
    try:
        # Get default models
        default_models = hf_manager.default_models
        
        # Get user models if available
        user_models = hf_manager.list_user_models()
        
        return {
            "default_models": default_models,
            "user_models": [model.get("name") for model in user_models[:10]],
            "total_user_models": len(user_models)
        }
        
    except Exception as e:
        logger.error(f"Error listing models: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error listing models: {str(e)}"
        )

@app.get("/ai/models/{model_name}")
async def get_model_info(model_name: str):
    """Get information about a specific model"""
    if not hf_manager:
        raise HTTPException(
            status_code=503,
            detail="Hugging Face service not available"
        )
    
    try:
        model_info = hf_manager.get_model_info(model_name)
        if not model_info:
            raise HTTPException(
                status_code=404,
                detail=f"Model {model_name} not found"
            )
        
        return model_info
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting model info: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error getting model info: {str(e)}"
        )

@app.post("/ai/models/{model_name}/download")
async def download_model(model_name: str, task: Optional[str] = None):
    """Download a specific model"""
    if not hf_manager:
        raise HTTPException(
            status_code=503,
            detail="Hugging Face service not available"
        )
    
    try:
        task_param = task or "text-generation"
        success = hf_manager.download_model(model_name, task_param)
        if success:
            return {"message": f"Model {model_name} downloaded successfully"}
        else:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to download model {model_name}"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error downloading model: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error downloading model: {str(e)}"
        )

@app.get("/info")
async def get_info():
    """Get application information"""
    return {
        "name": "PANACEA ICONO",
        "version": "1.0.0",
        "description": "AI-Powered Healthcare Solutions",
        "features": [
            "OpenAI Integration",
            "Hugging Face Models",
            "Dynamic Repository Management",
            "Docker Containerization",
            "Heroku Deployment",
            "FastAPI Web Framework",
            "Health Monitoring"
        ],
        "endpoints": {
            "root": "/",
            "health": "/health",
            "docs": "/docs",
            "ai_process": "/ai/process",
            "ai_models": "/ai/models",
            "repositories": "/api/repositories",
            "repository_stats": "/api/repositories/statistics",
            "info": "/info"
        }
    }

# === REPOSITORY API ENDPOINTS ===

@app.get("/api/repositories", response_model=Dict[str, Any])
async def list_repositories(
    language: Optional[str] = None,
    min_stars: Optional[int] = None,
    max_stars: Optional[int] = None,
    is_archived: Optional[bool] = None,
    has_topics: Optional[bool] = None,
    search: Optional[str] = None,
    force_refresh: bool = False
):
    """
    List repositories with optional filtering
    
    Args:
        language: Filter by programming language
        min_stars: Minimum number of stars
        max_stars: Maximum number of stars
        is_archived: Filter by archived status
        has_topics: Filter by presence of topics
        search: Search term for name/description
        force_refresh: Force refresh from GitHub API
    """
    if not github_manager:
        raise HTTPException(
            status_code=503,
            detail="GitHub repository service not available"
        )
    
    try:
        # Get all repositories
        repos = await github_manager.get_repositories(force_refresh=force_refresh)
        
        # Apply filters
        filtered_repos = github_manager.filter_repositories(
            repositories=repos,
            language=language,
            min_stars=min_stars,
            max_stars=max_stars,
            is_archived=is_archived,
            has_topics=has_topics,
            search_term=search
        )
        
        # Convert to dict format
        repo_data = []
        for repo in filtered_repos:
            repo_dict = repo.to_dict()
            repo_dict['last_updated_formatted'] = repo.last_updated_formatted
            repo_dict['topics_str'] = repo.topics_str
            repo_data.append(repo_dict)
        
        return {
            "repositories": repo_data,
            "total_count": len(repo_data),
            "filters_applied": {
                "language": language,
                "min_stars": min_stars,
                "max_stars": max_stars,
                "is_archived": is_archived,
                "has_topics": has_topics,
                "search": search
            },
            "last_updated": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error listing repositories: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error listing repositories: {str(e)}"
        )

@app.get("/api/repositories/statistics")
async def get_repository_statistics(force_refresh: bool = False):
    """Get statistics about all repositories"""
    if not github_manager:
        raise HTTPException(
            status_code=503,
            detail="GitHub repository service not available"
        )
    
    try:
        repos = await github_manager.get_repositories(force_refresh=force_refresh)
        stats = github_manager.get_statistics(repos)
        
        # Add timestamp
        stats['generated_at'] = datetime.utcnow().isoformat()
        
        return stats
        
    except Exception as e:
        logger.error(f"Error getting repository statistics: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error getting statistics: {str(e)}"
        )

@app.get("/api/repositories/{repo_name}")
async def get_repository(repo_name: str):
    """Get detailed information about a specific repository"""
    if not github_manager:
        raise HTTPException(
            status_code=503,
            detail="GitHub repository service not available"
        )
    
    try:
        repo = await github_manager.get_repository(repo_name)
        if not repo:
            raise HTTPException(
                status_code=404,
                detail=f"Repository '{repo_name}' not found"
            )
        
        repo_dict = repo.to_dict()
        repo_dict['last_updated_formatted'] = repo.last_updated_formatted
        repo_dict['topics_str'] = repo.topics_str
        
        return repo_dict
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting repository {repo_name}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error getting repository: {str(e)}"
        )

# Error handlers
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc),
            "type": type(exc).__name__
        }
    )

if __name__ == "__main__":
    # Get configuration from environment
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    debug = os.getenv("DEBUG", "false").lower() == "true"
    
    logger.info(f"Starting server on {host}:{port}")
    
    # Run the application
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=debug,
        log_level="info"
    )
