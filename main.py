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
import uuid

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

# Import EMD models and validation
try:
    from models import (
        Patient, EmergencyData, MedicalAIRequest, MedicalAIResponse,
        ValidationResponse, EMDResponse, SeverityLevel, EmergencyType
    )
    from validation_rules import MedicalValidator
    EMD_AVAILABLE = True
except ImportError:
    EMD_AVAILABLE = False

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
medical_validator: Optional[Any] = None

# In-memory storage for demo purposes (use database in production)
patients_db: Dict[str, Dict] = {}
emergencies_db: Dict[str, Dict] = {}

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    global hf_manager, medical_validator
    
    logger.info("🚀 Starting PANACEA ICONO application...")
    
    # Initialize Hugging Face manager
    if HF_MANAGER_AVAILABLE and HuggingFaceManager:
        try:
            hf_manager = HuggingFaceManager()
            logger.info("✅ Hugging Face manager initialized")
        except Exception as e:
            logger.error(f"❌ Error initializing Hugging Face manager: {e}")
            hf_manager = None
    
    # Initialize Medical Validator
    if EMD_AVAILABLE:
        try:
            medical_validator = MedicalValidator()
            logger.info("✅ Medical validator initialized")
        except Exception as e:
            logger.error(f"❌ Error initializing medical validator: {e}")
            medical_validator = None
    
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
        "emd": "healthy" if medical_validator else "unavailable",
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
            "Health Monitoring",
            "Emergency Medical Data (EMD) System",
            "Medical AI Analysis",
            "Patient Data Management"
        ],
        "endpoints": {
            "root": "/",
            "health": "/health",
            "docs": "/docs",
            "ai_process": "/ai/process",
            "ai_models": "/ai/models",
            "info": "/info",
            "emd_patients": "/emd/patients/",
            "emd_emergency": "/emd/emergency/",
            "emd_ai": "/emd/ai/",
            "emd_validate": "/emd/validate/"
        }
    }


# ========================================
# EMD (Emergency Medical Data) Endpoints
# ========================================

@app.post("/emd/patients/", response_model=EMDResponse)
async def register_patient(patient: Patient):
    """Register a new patient in the EMD system"""
    if not EMD_AVAILABLE or not medical_validator:
        raise HTTPException(
            status_code=503,
            detail="EMD system not available"
        )
    
    try:
        # Generate patient ID if not provided
        if not patient.patient_id:
            patient.patient_id = f"PAT_{uuid.uuid4().hex[:8].upper()}"
        
        # Validate patient data
        is_valid, errors, warnings = medical_validator.validate_patient_data(patient)
        
        if not is_valid:
            raise HTTPException(
                status_code=400,
                detail=f"Patient data validation failed: {'; '.join(errors)}"
            )
        
        # Store patient (in production, use database)
        patients_db[patient.patient_id] = patient.dict()
        
        response_data = {
            "patient_id": patient.patient_id,
            "validation_warnings": warnings
        }
        
        return EMDResponse(
            success=True,
            message=f"Patient {patient.patient_id} registered successfully",
            data=response_data
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error registering patient: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error registering patient: {str(e)}"
        )


@app.get("/emd/patients/{patient_id}", response_model=EMDResponse)
async def get_patient(patient_id: str):
    """Get patient information by ID"""
    if not EMD_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="EMD system not available"
        )
    
    if patient_id not in patients_db:
        raise HTTPException(
            status_code=404,
            detail=f"Patient {patient_id} not found"
        )
    
    return EMDResponse(
        success=True,
        message=f"Patient {patient_id} retrieved successfully",
        data=patients_db[patient_id]
    )


@app.put("/emd/patients/{patient_id}", response_model=EMDResponse)
async def update_patient(patient_id: str, patient: Patient):
    """Update patient information"""
    if not EMD_AVAILABLE or not medical_validator:
        raise HTTPException(
            status_code=503,
            detail="EMD system not available"
        )
    
    if patient_id not in patients_db:
        raise HTTPException(
            status_code=404,
            detail=f"Patient {patient_id} not found"
        )
    
    try:
        # Ensure patient ID matches
        patient.patient_id = patient_id
        
        # Validate patient data
        is_valid, errors, warnings = medical_validator.validate_patient_data(patient)
        
        if not is_valid:
            raise HTTPException(
                status_code=400,
                detail=f"Patient data validation failed: {'; '.join(errors)}"
            )
        
        # Update patient (in production, use database)
        patients_db[patient_id] = patient.dict()
        
        response_data = {
            "patient_id": patient_id,
            "validation_warnings": warnings
        }
        
        return EMDResponse(
            success=True,
            message=f"Patient {patient_id} updated successfully",
            data=response_data
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating patient: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error updating patient: {str(e)}"
        )


@app.post("/emd/emergency/", response_model=EMDResponse)
async def submit_emergency(emergency: EmergencyData):
    """Submit emergency medical data"""
    if not EMD_AVAILABLE or not medical_validator:
        raise HTTPException(
            status_code=503,
            detail="EMD system not available"
        )
    
    try:
        # Generate emergency ID if not provided
        if not emergency.emergency_id:
            emergency.emergency_id = f"EMG_{uuid.uuid4().hex[:8].upper()}"
        
        # Validate patient exists
        if emergency.patient_id not in patients_db:
            raise HTTPException(
                status_code=404,
                detail=f"Patient {emergency.patient_id} not found"
            )
        
        # Validate emergency data
        is_valid, errors, warnings = medical_validator.validate_emergency_data(emergency)
        
        if not is_valid:
            raise HTTPException(
                status_code=400,
                detail=f"Emergency data validation failed: {'; '.join(errors)}"
            )
        
        # Calculate triage priority
        patient_data = patients_db[emergency.patient_id]
        try:
            birth_date = datetime.strptime(patient_data['date_of_birth'], '%Y-%m-%d')
            patient_age = (datetime.now() - birth_date).days // 365
        except:
            patient_age = 30  # Default age if calculation fails
            
        triage_priority, triage_reason = medical_validator.calculate_triage_priority(
            emergency, patient_age
        )
        
        # Store emergency (in production, use database)
        emergency_dict = emergency.dict()
        emergency_dict['triage_priority'] = triage_priority
        emergency_dict['triage_reason'] = triage_reason
        emergencies_db[emergency.emergency_id] = emergency_dict
        
        response_data = {
            "emergency_id": emergency.emergency_id,
            "triage_priority": triage_priority,
            "triage_reason": triage_reason,
            "validation_warnings": warnings
        }
        
        return EMDResponse(
            success=True,
            message=f"Emergency {emergency.emergency_id} submitted successfully",
            data=response_data
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error submitting emergency: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error submitting emergency: {str(e)}"
        )


@app.get("/emd/emergency/{emergency_id}", response_model=EMDResponse)
async def get_emergency(emergency_id: str):
    """Get emergency record by ID"""
    if not EMD_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="EMD system not available"
        )
    
    if emergency_id not in emergencies_db:
        raise HTTPException(
            status_code=404,
            detail=f"Emergency {emergency_id} not found"
        )
    
    return EMDResponse(
        success=True,
        message=f"Emergency {emergency_id} retrieved successfully",
        data=emergencies_db[emergency_id]
    )


@app.post("/emd/ai/diagnose", response_model=MedicalAIResponse)
async def ai_medical_diagnosis(request: MedicalAIRequest):
    """Perform AI-powered medical diagnosis"""
    if not EMD_AVAILABLE or not medical_validator:
        raise HTTPException(
            status_code=503,
            detail="EMD system not available"
        )
    
    if not hf_manager:
        raise HTTPException(
            status_code=503,
            detail="AI system not available"
        )
    
    try:
        # Validate AI request
        is_valid, errors, warnings = medical_validator.validate_ai_request(request)
        
        if not is_valid:
            raise HTTPException(
                status_code=400,
                detail=f"AI request validation failed: {'; '.join(errors)}"
            )
        
        # Prepare symptoms text for AI analysis
        symptoms_text = "; ".join(request.symptoms)
        if request.medical_history:
            symptoms_text += f". Medical history: {'; '.join(request.medical_history)}"
        
        # Use Hugging Face for text analysis (medical classification)
        try:
            pipeline_obj = hf_manager.create_pipeline("text-classification")
            if pipeline_obj:
                ai_result = pipeline_obj(symptoms_text)
                confidence = ai_result[0].get('score', 0.5) if ai_result else 0.5
            else:
                confidence = 0.5
        except:
            confidence = 0.5
        
        # Generate medical recommendations based on symptoms
        recommendations = []
        suggested_actions = []
        risk_factors = []
        
        symptoms_lower = [s.lower() for s in request.symptoms]
        symptoms_text_lower = ' '.join(symptoms_lower)
        
        # Basic symptom-based recommendations
        if any(word in symptoms_text_lower for word in ['chest pain', 'heart', 'cardiac']):
            recommendations.extend([
                "Consider cardiac evaluation",
                "Monitor vital signs closely",
                "Obtain ECG if available"
            ])
            suggested_actions.extend([
                "Immediate medical attention recommended",
                "Consider emergency transport"
            ])
            risk_factors.append("Potential cardiac event")
            
        elif any(word in symptoms_text_lower for word in ['shortness of breath', 'difficulty breathing']):
            recommendations.extend([
                "Assess respiratory function",
                "Check oxygen saturation",
                "Consider pulmonary evaluation"
            ])
            suggested_actions.extend([
                "Provide oxygen support if needed",
                "Position patient for optimal breathing"
            ])
            risk_factors.append("Respiratory compromise")
            
        else:
            recommendations.extend([
                "Complete medical evaluation recommended",
                "Monitor patient condition",
                "Document symptoms and progression"
            ])
            suggested_actions.extend([
                "Seek appropriate medical care",
                "Follow up with healthcare provider"
            ])
        
        # Add warnings from validation
        warnings_list = warnings if warnings else []
        
        return MedicalAIResponse(
            analysis_type=request.analysis_type,
            confidence=confidence,
            recommendations=recommendations,
            risk_factors=risk_factors,
            suggested_actions=suggested_actions,
            warnings=warnings_list
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in AI diagnosis: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error in AI diagnosis: {str(e)}"
        )


@app.post("/emd/ai/risk-assessment", response_model=MedicalAIResponse)
async def ai_risk_assessment(request: MedicalAIRequest):
    """Perform AI-powered medical risk assessment"""
    if not EMD_AVAILABLE or not medical_validator:
        raise HTTPException(
            status_code=503,
            detail="EMD system not available"
        )
    
    try:
        # Set analysis type for risk assessment
        request.analysis_type = "risk_assessment"
        
        # Validate AI request
        is_valid, errors, warnings = medical_validator.validate_ai_request(request)
        
        if not is_valid:
            raise HTTPException(
                status_code=400,
                detail=f"Risk assessment request validation failed: {'; '.join(errors)}"
            )
        
        # Calculate risk factors
        risk_factors = []
        recommendations = []
        suggested_actions = []
        
        # Age-based risk (if patient_id provided)
        if request.patient_id and request.patient_id in patients_db:
            patient_data = patients_db[request.patient_id]
            try:
                birth_date = datetime.strptime(patient_data['date_of_birth'], '%Y-%m-%d')
                age = (datetime.now() - birth_date).days // 365
                if age >= 65:
                    risk_factors.append("Advanced age (>=65)")
                    recommendations.append("Age-appropriate monitoring protocols")
            except:
                pass
        
        # Vital signs risk assessment
        if request.vital_signs:
            vs = request.vital_signs
            if vs.get('blood_pressure_systolic', 120) >= 140:
                risk_factors.append("Hypertension")
                recommendations.append("Blood pressure management")
            if vs.get('heart_rate', 70) >= 100:
                risk_factors.append("Tachycardia")
                recommendations.append("Cardiac monitoring")
            if vs.get('oxygen_saturation', 100) < 95:
                risk_factors.append("Hypoxemia")
                recommendations.append("Oxygen support evaluation")
        
        # Medical history risk assessment
        if request.medical_history:
            high_risk_conditions = ['diabetes', 'heart disease', 'copd', 'kidney disease']
            for condition in request.medical_history:
                condition_lower = condition.lower()
                for risk_condition in high_risk_conditions:
                    if risk_condition in condition_lower:
                        risk_factors.append(f"History of {condition}")
                        recommendations.append(f"Monitor for {risk_condition} complications")
        
        # Determine overall risk level and confidence
        risk_score = len(risk_factors)
        if risk_score >= 3:
            confidence = 0.8
            suggested_actions.extend([
                "High-risk patient - close monitoring required",
                "Consider hospital admission",
                "Immediate physician evaluation"
            ])
        elif risk_score >= 2:
            confidence = 0.7
            suggested_actions.extend([
                "Moderate risk - enhanced monitoring",
                "Follow up within 24 hours",
                "Consider outpatient management"
            ])
        else:
            confidence = 0.6
            suggested_actions.extend([
                "Standard care protocols",
                "Routine follow-up appropriate",
                "Patient education and discharge planning"
            ])
        
        if not risk_factors:
            risk_factors = ["Low risk based on available data"]
            recommendations.append("Standard preventive care measures")
        
        return MedicalAIResponse(
            analysis_type="risk_assessment",
            confidence=confidence,
            recommendations=recommendations,
            risk_factors=risk_factors,
            suggested_actions=suggested_actions,
            warnings=warnings
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in risk assessment: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error in risk assessment: {str(e)}"
        )


@app.post("/emd/validate/", response_model=ValidationResponse)
async def validate_medical_data(data: Dict[str, Any]):
    """Validate medical data against EMD rules"""
    if not EMD_AVAILABLE or not medical_validator:
        raise HTTPException(
            status_code=503,
            detail="EMD system not available"
        )
    
    try:
        validation_errors = []
        warnings = []
        validated_data = {}
        
        # Determine data type and validate accordingly
        if 'patient_id' in data and 'first_name' in data:
            # Patient data
            try:
                patient = Patient(**data)
                is_valid, errors, warns = medical_validator.validate_patient_data(patient)
                validation_errors.extend(errors)
                warnings.extend(warns)
                validated_data = patient.dict()
            except Exception as e:
                validation_errors.append(f"Patient data structure error: {str(e)}")
                
        elif 'emergency_id' in data or 'emergency_type' in data:
            # Emergency data
            try:
                emergency = EmergencyData(**data)
                is_valid, errors, warns = medical_validator.validate_emergency_data(emergency)
                validation_errors.extend(errors)
                warnings.extend(warns)
                validated_data = emergency.dict()
            except Exception as e:
                validation_errors.append(f"Emergency data structure error: {str(e)}")
                
        elif 'symptoms' in data:
            # AI request data
            try:
                ai_request = MedicalAIRequest(**data)
                is_valid, errors, warns = medical_validator.validate_ai_request(ai_request)
                validation_errors.extend(errors)
                warnings.extend(warns)
                validated_data = ai_request.dict()
            except Exception as e:
                validation_errors.append(f"AI request data structure error: {str(e)}")
                
        else:
            validation_errors.append("Unknown data type - cannot determine validation rules")
        
        return ValidationResponse(
            is_valid=len(validation_errors) == 0,
            validation_errors=validation_errors,
            warnings=warnings,
            validated_data=validated_data if len(validation_errors) == 0 else None
        )
        
    except Exception as e:
        logger.error(f"Error validating medical data: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error validating medical data: {str(e)}"
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
