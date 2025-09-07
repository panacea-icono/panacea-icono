#!/usr/bin/env python3
"""
🏥 PANACEA ICONO - Main Application
FastAPI application with AI models integration
"""

import os
import logging
from typing import Dict, Any, Optional, List
from pathlib import Path

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import uvicorn

# Import Hugging Face manager and ecosystem components
try:
    from huggingface_config import HuggingFaceManager
    from ecosystem_manager import EcosystemManager
    from github_integration import GitHubManager
    from package_manager import PackageManager
    HF_MANAGER_AVAILABLE = True
    ECOSYSTEM_AVAILABLE = True
except ImportError as e:
    logger.warning(f"⚠️ Some ecosystem components not available: {e}")
    HuggingFaceManager = None
    EcosystemManager = None
    GitHubManager = None
    PackageManager = None
    HF_MANAGER_AVAILABLE = False
    ECOSYSTEM_AVAILABLE = False

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

class EcosystemRequest(BaseModel):
    operation: str = Field(description="Ecosystem operation to perform", 
                          enum=["sync", "report", "readme", "audit", "status"])
    repository: Optional[str] = Field(description="Target repository name", default=None)

class EcosystemResponse(BaseModel):
    operation: str = Field(description="Operation performed")
    success: bool = Field(description="Operation success status")
    data: Any = Field(description="Operation result data")
    message: str = Field(description="Status message")

class IssueRequest(BaseModel):
    repository: str = Field(description="Target repository name", min_length=1)
    title: str = Field(description="Issue title", min_length=1)
    body: Optional[str] = Field(description="Issue body", default="")
    labels: Optional[List[str]] = Field(description="Issue labels", default=[])

# Global variables
hf_manager: Optional[HuggingFaceManager] = None
ecosystem_manager: Optional[EcosystemManager] = None

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    global hf_manager, ecosystem_manager
    
    logger.info("🚀 Starting PANACEA ICONO application...")
    
    # Initialize Hugging Face manager
    if HF_MANAGER_AVAILABLE and HuggingFaceManager:
        try:
            hf_manager = HuggingFaceManager()
            logger.info("✅ Hugging Face manager initialized")
        except Exception as e:
            logger.error(f"❌ Error initializing Hugging Face manager: {e}")
            hf_manager = None
    
    # Initialize Ecosystem manager
    if ECOSYSTEM_AVAILABLE and EcosystemManager:
        try:
            ecosystem_manager = EcosystemManager()
            logger.info("✅ Ecosystem manager initialized")
        except Exception as e:
            logger.error(f"❌ Error initializing Ecosystem manager: {e}")
            ecosystem_manager = None
    
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
        "ecosystem": "healthy" if ecosystem_manager else "unavailable",
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

@app.post("/ecosystem/manage", response_model=EcosystemResponse)
async def manage_ecosystem(request: EcosystemRequest):
    """Manage ecosystem operations"""
    if not ecosystem_manager:
        raise HTTPException(
            status_code=503,
            detail="Ecosystem manager not available"
        )
    
    try:
        operation = request.operation
        logger.info(f"🌍 Executing ecosystem operation: {operation}")
        
        if operation == "sync":
            result = ecosystem_manager.run_full_ecosystem_sync()
            success = result.get("summary", {}).get("success", False)
            message = f"Synchronization {'completed' if success else 'completed with errors'}"
            
        elif operation == "report":
            result = ecosystem_manager.generate_ecosystem_report()
            success = "error" not in result
            message = f"Report generated for {result.get('ecosystem', {}).get('total_repositories', 0)} repositories"
            
        elif operation == "readme":
            result = {"updated": ecosystem_manager.update_repository_readme()}
            success = result["updated"]
            message = "README updated" if success else "README update failed"
            
        elif operation == "audit":
            result = ecosystem_manager.package_manager.analyze_repository_packages(Path.cwd())
            success = "error" not in result
            vulnerabilities = result.get("summary", {}).get("vulnerabilities", 0)
            message = f"Audit completed. Found {vulnerabilities} vulnerabilities"
            
        elif operation == "status":
            github_ok = ecosystem_manager.github_manager.test_connection()
            hf_ok = ecosystem_manager.hf_manager.verify_connection() if ecosystem_manager.hf_manager else False
            
            result = {
                "github_connected": github_ok,
                "huggingface_connected": hf_ok,
                "reports_directory": str(ecosystem_manager.reports_dir)
            }
            success = github_ok
            message = f"Status check complete. GitHub: {'✅' if github_ok else '❌'}, HF: {'✅' if hf_ok else '❌'}"
            
        else:
            raise HTTPException(status_code=400, detail=f"Unknown operation: {operation}")
        
        return EcosystemResponse(
            operation=operation,
            success=success,
            data=result,
            message=message
        )
        
    except Exception as e:
        logger.error(f"❌ Error in ecosystem operation {operation}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error executing {operation}: {str(e)}"
        )

@app.post("/ecosystem/issue", response_model=Dict[str, Any])
async def create_ecosystem_issue(request: IssueRequest):
    """Create an issue in a repository"""
    if not ecosystem_manager:
        raise HTTPException(
            status_code=503,
            detail="Ecosystem manager not available"
        )
    
    try:
        success = ecosystem_manager.create_ecosystem_issue(
            request.repository,
            request.title,
            request.body,
            request.labels
        )
        
        if success:
            return {
                "success": True,
                "message": f"Issue created in {request.repository}",
                "title": request.title
            }
        else:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to create issue in {request.repository}"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error creating issue: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error creating issue: {str(e)}"
        )

@app.get("/ecosystem/repositories")
async def list_repositories():
    """List all repositories in the ecosystem"""
    if not ecosystem_manager:
        raise HTTPException(
            status_code=503,
            detail="Ecosystem manager not available"
        )
    
    try:
        summary = ecosystem_manager.github_manager.generate_ecosystem_summary()
        
        repositories = []
        for repo in summary.get("repositories", []):
            repositories.append({
                "name": repo.get("name"),
                "description": repo.get("description"),
                "language": repo.get("language"),
                "stars": repo.get("stars"),
                "forks": repo.get("forks"),
                "url": repo.get("url"),
                "updated_at": repo.get("updated_at")
            })
        
        return {
            "total_repositories": len(repositories),
            "repositories": repositories,
            "statistics": summary.get("statistics", {})
        }
        
    except Exception as e:
        logger.error(f"❌ Error listing repositories: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error listing repositories: {str(e)}"
        )

@app.get("/info")
async def get_info():
    """Get application information"""
    return {
        "name": "PANACEA ICONO",
        "version": "1.0.0",
        "description": "AI-Powered Healthcare Solutions & Ecosystem Manager",
        "features": [
            "OpenAI Integration",
            "Hugging Face Models",
            "Docker Containerization",
            "Heroku Deployment",
            "FastAPI Web Framework",
            "Health Monitoring",
            "GitHub Integration",
            "Package Management",
            "Security Auditing",
            "Ecosystem Automation",
            "Repository Management",
            "Issue Management"
        ],
        "endpoints": {
            "root": "/",
            "health": "/health",
            "docs": "/docs",
            "ai_process": "/ai/process",
            "ai_models": "/ai/models",
            "ecosystem_manage": "/ecosystem/manage",
            "ecosystem_issue": "/ecosystem/issue",
            "ecosystem_repositories": "/ecosystem/repositories",
            "info": "/info"
        }
    }

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
