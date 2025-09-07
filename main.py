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

# Import Hugging Face manager
try:
    from huggingface_config import HuggingFaceManager
    HF_MANAGER_AVAILABLE = True
except ImportError:
    HuggingFaceManager = None
    HF_MANAGER_AVAILABLE = False

# Import OpenAI manager
try:
    from openai_config import OpenAIManager
    OPENAI_MANAGER_AVAILABLE = True
except ImportError:
    OpenAIManager = None
    OPENAI_MANAGER_AVAILABLE = False

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

# OpenAI Code-related models
class CodeGenerationRequest(BaseModel):
    task: str = Field(description="Task description for code generation", min_length=1)
    language: str = Field(description="Programming language", default="python")
    requirements: str = Field(description="Additional requirements", default="")
    model: Optional[str] = Field(description="OpenAI model to use", default=None)

class CodeExplanationRequest(BaseModel):
    code: str = Field(description="Code to explain", min_length=1)
    language: str = Field(description="Programming language", default="python")
    model: Optional[str] = Field(description="OpenAI model to use", default=None)

class CodeCompletionRequest(BaseModel):
    partial_code: str = Field(description="Partial code to complete", min_length=1)
    context: str = Field(description="Additional context", default="")
    language: str = Field(description="Programming language", default="python")
    model: Optional[str] = Field(description="OpenAI model to use", default=None)

class CodeReviewRequest(BaseModel):
    code: str = Field(description="Code to review", min_length=1)
    language: str = Field(description="Programming language", default="python")
    model: Optional[str] = Field(description="OpenAI model to use", default=None)

class CodeChatRequest(BaseModel):
    message: str = Field(description="Chat message about code", min_length=1)
    conversation_history: Optional[List[Dict[str, str]]] = Field(description="Previous conversation", default=None)
    model: Optional[str] = Field(description="OpenAI model to use", default=None)

class CodeResponse(BaseModel):
    result: str = Field(description="Generated result")
    task: str = Field(description="Task performed")
    model: str = Field(description="Model used")
    language: str = Field(description="Programming language")

# Global variables
hf_manager: Optional[HuggingFaceManager] = None
openai_manager: Optional[OpenAIManager] = None

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    global hf_manager, openai_manager
    
    logger.info("🚀 Starting PANACEA ICONO application...")
    
    # Initialize Hugging Face manager
    if HF_MANAGER_AVAILABLE and HuggingFaceManager:
        try:
            hf_manager = HuggingFaceManager()
            logger.info("✅ Hugging Face manager initialized")
        except Exception as e:
            logger.error(f"❌ Error initializing Hugging Face manager: {e}")
            hf_manager = None
    
    # Initialize OpenAI manager
    if OPENAI_MANAGER_AVAILABLE and OpenAIManager:
        try:
            openai_manager = OpenAIManager()
            logger.info("✅ OpenAI manager initialized")
        except Exception as e:
            logger.error(f"❌ Error initializing OpenAI manager: {e}")
            openai_manager = None
    
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
        "openai": "healthy" if openai_manager else "unavailable",
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
    
    # Test OpenAI connection if available
    if openai_manager:
        try:
            if openai_manager.verify_connection():
                services["openai"] = "healthy"
            else:
                services["openai"] = "unhealthy"
        except Exception as e:
            logger.error(f"Error checking OpenAI health: {e}")
            services["openai"] = "error"
    
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

# OpenAI Code endpoints
@app.post("/ai/code/generate", response_model=CodeResponse)
async def generate_code(request: CodeGenerationRequest):
    """Generate code using OpenAI"""
    if not openai_manager:
        raise HTTPException(
            status_code=503,
            detail="OpenAI service not available"
        )
    
    try:
        result = openai_manager.generate_code(
            task=request.task,
            language=request.language,
            requirements=request.requirements,
            model=request.model
        )
        
        if not result:
            raise HTTPException(
                status_code=500,
                detail="Failed to generate code"
            )
        
        return CodeResponse(
            result=result,
            task="code_generation",
            model=request.model or openai_manager.code_models["code_generation"],
            language=request.language
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating code: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error generating code: {str(e)}"
        )

@app.post("/ai/code/explain", response_model=CodeResponse)
async def explain_code(request: CodeExplanationRequest):
    """Explain code using OpenAI"""
    if not openai_manager:
        raise HTTPException(
            status_code=503,
            detail="OpenAI service not available"
        )
    
    try:
        result = openai_manager.explain_code(
            code=request.code,
            language=request.language,
            model=request.model
        )
        
        if not result:
            raise HTTPException(
                status_code=500,
                detail="Failed to explain code"
            )
        
        return CodeResponse(
            result=result,
            task="code_explanation",
            model=request.model or openai_manager.code_models["code_explanation"],
            language=request.language
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error explaining code: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error explaining code: {str(e)}"
        )

@app.post("/ai/code/complete", response_model=CodeResponse)
async def complete_code(request: CodeCompletionRequest):
    """Complete code using OpenAI"""
    if not openai_manager:
        raise HTTPException(
            status_code=503,
            detail="OpenAI service not available"
        )
    
    try:
        result = openai_manager.complete_code(
            partial_code=request.partial_code,
            context=request.context,
            language=request.language,
            model=request.model
        )
        
        if not result:
            raise HTTPException(
                status_code=500,
                detail="Failed to complete code"
            )
        
        return CodeResponse(
            result=result,
            task="code_completion",
            model=request.model or openai_manager.code_models["code_completion"],
            language=request.language
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error completing code: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error completing code: {str(e)}"
        )

@app.post("/ai/code/review", response_model=CodeResponse)
async def review_code(request: CodeReviewRequest):
    """Review code using OpenAI"""
    if not openai_manager:
        raise HTTPException(
            status_code=503,
            detail="OpenAI service not available"
        )
    
    try:
        result = openai_manager.review_code(
            code=request.code,
            language=request.language,
            model=request.model
        )
        
        if not result:
            raise HTTPException(
                status_code=500,
                detail="Failed to review code"
            )
        
        return CodeResponse(
            result=result,
            task="code_review",
            model=request.model or openai_manager.code_models["code_review"],
            language=request.language
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error reviewing code: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error reviewing code: {str(e)}"
        )

@app.post("/ai/code/chat", response_model=CodeResponse)
async def chat_about_code(request: CodeChatRequest):
    """Chat about code using OpenAI"""
    if not openai_manager:
        raise HTTPException(
            status_code=503,
            detail="OpenAI service not available"
        )
    
    try:
        result = openai_manager.chat_about_code(
            message=request.message,
            conversation_history=request.conversation_history,
            model=request.model
        )
        
        if not result:
            raise HTTPException(
                status_code=500,
                detail="Failed to process chat"
            )
        
        return CodeResponse(
            result=result,
            task="code_chat",
            model=request.model or openai_manager.code_models["chat"],
            language="text"  # Chat is language-agnostic
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing code chat: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing code chat: {str(e)}"
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
            "OpenAI Codex Chat GPT",
            "Code Generation",
            "Code Explanation",
            "Code Completion",
            "Code Review",
            "Code Chat",
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
            "code_generate": "/ai/code/generate",
            "code_explain": "/ai/code/explain",
            "code_complete": "/ai/code/complete",
            "code_review": "/ai/code/review",
            "code_chat": "/ai/code/chat",
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
