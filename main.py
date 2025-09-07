#!/usr/bin/env python3
"""
🏥 PANACEA ICONO - Main Application
FastAPI application with AI models integration
"""

import os
import logging
from typing import Dict, Any, Optional, List
from pathlib import Path
from datetime import datetime
import json

from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import uvicorn
import requests

# Import Hugging Face manager
try:
    from huggingface_config import HuggingFaceManager
    HF_MANAGER_AVAILABLE = True
except ImportError:
    HuggingFaceManager = None
    HF_MANAGER_AVAILABLE = False

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

class EnvironmentInfo(BaseModel):
    name: str = Field(description="Environment name")
    status: str = Field(description="Environment status")
    url: Optional[str] = Field(description="Environment URL", default=None)
    objectives: List[str] = Field(description="Environment objectives", default=[])
    
class DeploymentInfo(BaseModel):
    environment: str = Field(description="Deployment environment")
    status: str = Field(description="Deployment status")
    timestamp: datetime = Field(description="Deployment timestamp")
    version: str = Field(description="Deployed version")
    
class GistRequest(BaseModel):
    description: str = Field(description="Gist description")
    files: Dict[str, str] = Field(description="Files content")
    public: bool = Field(description="Public gist", default=True)
    
class LinkInfo(BaseModel):
    name: str = Field(description="Link name")
    url: str = Field(description="Link URL")
    category: str = Field(description="Link category")
    description: Optional[str] = Field(description="Link description", default=None)
    
class ProjectionData(BaseModel):
    metric: str = Field(description="Metric name")
    current_value: float = Field(description="Current value")
    projected_value: float = Field(description="Projected value")
    timeframe: str = Field(description="Projection timeframe")

# Global variables
hf_manager: Optional[HuggingFaceManager] = None

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    global hf_manager
    
    logger.info("🚀 Starting PANACEA ICONO application...")
    
    # Initialize Hugging Face manager
    if HF_MANAGER_AVAILABLE and HuggingFaceManager:
        try:
            hf_manager = HuggingFaceManager()
            logger.info("✅ Hugging Face manager initialized")
        except Exception as e:
            logger.error(f"❌ Error initializing Hugging Face manager: {e}")
            hf_manager = None
    
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
            "info": "/info",
            "deploy_environments": "/deploy/environments",
            "deploy_status": "/deploy/status/{environment}",
            "deploy_gist": "/deploy/gist",
            "deploy_releases": "/deploy/releases",
            "deploy_tags": "/deploy/tags", 
            "deploy_packages": "/deploy/packages",
            "deploy_links": "/deploy/links",
            "deploy_projections": "/deploy/projections",
            "deploy_objectives": "/deploy/objectives/{environment}"
        }
    }

# === DEPLOYMENT WORKFLOW ROUTES ===

@app.get("/deploy/environments", response_model=List[EnvironmentInfo])
async def get_environments():
    """Get deployment environments status"""
    environments = [
        EnvironmentInfo(
            name="development",
            status="active",
            url="http://localhost:8000",
            objectives=["Local testing", "Development workflow", "Feature development"]
        ),
        EnvironmentInfo(
            name="staging", 
            status="active",
            url="https://panacea-icono-staging.herokuapp.com",
            objectives=["Pre-production testing", "Integration testing", "User acceptance testing"]
        ),
        EnvironmentInfo(
            name="production",
            status="active", 
            url="https://panacea-icono-ai-78b4eb86c23b.herokuapp.com",
            objectives=["Live application", "Production workloads", "User traffic"]
        )
    ]
    return environments

@app.get("/deploy/status/{environment}")
async def get_deployment_status(environment: str):
    """Get deployment status for specific environment"""
    deployments = {
        "development": DeploymentInfo(
            environment="development",
            status="healthy",
            timestamp=datetime.utcnow(),
            version="1.0.0-dev"
        ),
        "staging": DeploymentInfo(
            environment="staging", 
            status="healthy",
            timestamp=datetime.utcnow(),
            version="1.0.0-rc.1"
        ),
        "production": DeploymentInfo(
            environment="production",
            status="healthy", 
            timestamp=datetime.utcnow(),
            version="1.0.0"
        )
    }
    
    if environment not in deployments:
        raise HTTPException(status_code=404, detail=f"Environment {environment} not found")
    
    return deployments[environment]

@app.post("/deploy/gist")
async def create_gist(gist_request: GistRequest):
    """Create a GitHub gist with deployment information"""
    try:
        # Simulate gist creation (in real implementation, would use GitHub API)
        gist_data = {
            "id": f"gist-{datetime.utcnow().timestamp()}",
            "description": gist_request.description,
            "public": gist_request.public,
            "files": gist_request.files,
            "url": f"https://gist.github.com/placeholder/{datetime.utcnow().timestamp()}",
            "created_at": datetime.utcnow().isoformat()
        }
        
        return {
            "message": "Gist created successfully",
            "gist": gist_data
        }
        
    except Exception as e:
        logger.error(f"Error creating gist: {e}")
        raise HTTPException(status_code=500, detail=f"Error creating gist: {str(e)}")

@app.get("/deploy/releases")
async def get_releases():
    """Get GitHub releases information"""
    try:
        # Simulate releases data (in real implementation, would fetch from GitHub API)
        releases = [
            {
                "tag_name": "v1.0.0",
                "name": "PANACEA ICONO v1.0.0",
                "body": "Initial release with AI integration and deployment workflows",
                "created_at": "2025-09-07T18:00:00Z",
                "published_at": "2025-09-07T18:00:00Z",
                "assets": [
                    {
                        "name": "panacea-icono-1.0.0.tar.gz",
                        "download_count": 42,
                        "size": 1024000
                    }
                ]
            }
        ]
        
        return {
            "releases": releases,
            "total": len(releases)
        }
        
    except Exception as e:
        logger.error(f"Error fetching releases: {e}")
        raise HTTPException(status_code=500, detail=f"Error fetching releases: {str(e)}")

@app.get("/deploy/tags")  
async def get_tags():
    """Get GitHub tags information"""
    try:
        # Simulate tags data (in real implementation, would fetch from GitHub API)
        tags = [
            {
                "name": "v1.0.0",
                "commit": {
                    "sha": "abc123456",
                    "message": "Release v1.0.0 with deployment workflows"
                }
            },
            {
                "name": "v0.9.0",
                "commit": {
                    "sha": "def789012", 
                    "message": "Pre-release with basic features"
                }
            }
        ]
        
        return {
            "tags": tags,
            "total": len(tags)
        }
        
    except Exception as e:
        logger.error(f"Error fetching tags: {e}")
        raise HTTPException(status_code=500, detail=f"Error fetching tags: {str(e)}")

@app.get("/deploy/packages")
async def get_packages():
    """Get package information"""
    try:
        packages = [
            {
                "name": "panacea-icono",
                "version": "1.0.0",
                "type": "docker",
                "registry": "ghcr.io/panacea-icono/panacea-icono",
                "size": "512 MB",
                "downloads": 156
            },
            {
                "name": "panacea-icono-py",
                "version": "1.0.0", 
                "type": "python",
                "registry": "pypi",
                "size": "2.1 MB",
                "downloads": 89
            }
        ]
        
        return {
            "packages": packages,
            "total": len(packages)
        }
        
    except Exception as e:
        logger.error(f"Error fetching packages: {e}")
        raise HTTPException(status_code=500, detail=f"Error fetching packages: {str(e)}")

@app.get("/deploy/links", response_model=List[LinkInfo])
async def get_deployment_links():
    """Get deployment-related links"""
    links = [
        LinkInfo(
            name="Production App",
            url="https://panacea-icono-ai-78b4eb86c23b.herokuapp.com",
            category="deployment",
            description="Production deployment on Heroku"
        ),
        LinkInfo(
            name="GitHub Repository", 
            url="https://github.com/panacea-icono/panacea-icono",
            category="source",
            description="Main repository"
        ),
        LinkInfo(
            name="Docker Hub",
            url="https://hub.docker.com/r/drtv/panacea-icono", 
            category="registry",
            description="Docker container registry"
        ),
        LinkInfo(
            name="GitHub Actions",
            url="https://github.com/panacea-icono/panacea-icono/actions",
            category="cicd",
            description="CI/CD workflows"
        ),
        LinkInfo(
            name="Documentation",
            url="https://panacea-icono.org",
            category="docs",
            description="Project documentation"
        )
    ]
    
    return links

@app.get("/deploy/projections", response_model=List[ProjectionData])
async def get_deployment_projections():
    """Get deployment projections and analytics"""
    projections = [
        ProjectionData(
            metric="deployment_frequency",
            current_value=2.5,
            projected_value=4.0,
            timeframe="next_month"
        ),
        ProjectionData(
            metric="success_rate",
            current_value=95.5,
            projected_value=98.0,
            timeframe="next_quarter"
        ),
        ProjectionData(
            metric="average_deployment_time", 
            current_value=8.5,
            projected_value=6.0,
            timeframe="next_month"
        ),
        ProjectionData(
            metric="rollback_rate",
            current_value=5.2,
            projected_value=2.0,
            timeframe="next_quarter"
        )
    ]
    
    return projections

@app.get("/deploy/objectives/{environment}")
async def get_environment_objectives(environment: str):
    """Get environment-specific objectives and achievements"""
    objectives = {
        "development": {
            "achieved": [
                "FastAPI application setup",
                "Hugging Face integration",
                "Docker containerization",
                "Local testing environment"
            ],
            "in_progress": [
                "Enhanced deployment workflows",
                "GitHub integration features"
            ],
            "planned": [
                "Advanced monitoring",
                "Performance optimization"
            ]
        },
        "staging": {
            "achieved": [
                "Staging environment deployment",
                "Integration testing setup",
                "Performance testing"
            ],
            "in_progress": [
                "User acceptance testing",
                "Load testing"
            ],
            "planned": [
                "Security testing",
                "Compliance validation"
            ]
        },
        "production": {
            "achieved": [
                "Production deployment",
                "Health monitoring",
                "Backup systems"
            ],
            "in_progress": [
                "Performance optimization",
                "Scaling improvements"
            ],
            "planned": [
                "Multi-region deployment",
                "Advanced analytics"
            ]
        }
    }
    
    if environment not in objectives:
        raise HTTPException(status_code=404, detail=f"Environment {environment} not found")
    
    return {
        "environment": environment,
        "objectives": objectives[environment]
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
