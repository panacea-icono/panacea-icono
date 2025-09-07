#!/usr/bin/env python3
"""
Medical Data Models for PANACEA ICONO EMD (Emergency Medical Data) System
Defines Pydantic models for healthcare data validation
"""

from datetime import datetime
from enum import Enum
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, validator, EmailStr
import re


class SeverityLevel(str, Enum):
    """Medical severity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class EmergencyType(str, Enum):
    """Types of medical emergencies"""
    CARDIAC = "cardiac"
    RESPIRATORY = "respiratory"
    TRAUMA = "trauma"
    NEUROLOGICAL = "neurological"
    PSYCHIATRIC = "psychiatric"
    POISONING = "poisoning"
    ALLERGIC = "allergic"
    OTHER = "other"


class PatientGender(str, Enum):
    """Patient gender options"""
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
    PREFER_NOT_TO_SAY = "prefer_not_to_say"


class Patient(BaseModel):
    """Patient data model with validation rules"""
    patient_id: Optional[str] = Field(None, description="Unique patient identifier")
    first_name: str = Field(..., min_length=2, max_length=50, description="Patient first name")
    last_name: str = Field(..., min_length=2, max_length=50, description="Patient last name")
    date_of_birth: str = Field(..., description="Date of birth (YYYY-MM-DD)")
    gender: PatientGender = Field(..., description="Patient gender")
    email: Optional[EmailStr] = Field(None, description="Patient email")
    phone: str = Field(..., description="Patient phone number")
    emergency_contact: Optional[str] = Field(None, description="Emergency contact information")
    medical_conditions: Optional[List[str]] = Field(default=[], description="Known medical conditions")
    medications: Optional[List[str]] = Field(default=[], description="Current medications")
    allergies: Optional[List[str]] = Field(default=[], description="Known allergies")
    
    @validator('date_of_birth')
    def validate_date_of_birth(cls, v):
        """Validate date of birth format and range"""
        try:
            birth_date = datetime.strptime(v, '%Y-%m-%d')
            if birth_date > datetime.now():
                raise ValueError('Date of birth cannot be in the future')
            if birth_date.year < 1900:
                raise ValueError('Date of birth must be after 1900')
            return v
        except ValueError as e:
            raise ValueError(f'Invalid date of birth format. Use YYYY-MM-DD: {e}')
    
    @validator('phone')
    def validate_phone(cls, v):
        """Validate phone number format"""
        # Remove all non-digit characters
        phone_digits = re.sub(r'\D', '', v)
        if len(phone_digits) < 10 or len(phone_digits) > 15:
            raise ValueError('Phone number must be between 10-15 digits')
        return v
    
    @validator('first_name', 'last_name')
    def validate_names(cls, v):
        """Validate name fields"""
        if not re.match(r'^[a-zA-ZÀ-ÿ\s-]+$', v):
            raise ValueError('Names can only contain letters, spaces, and hyphens')
        return v.strip().title()


class EmergencyData(BaseModel):
    """Emergency medical data model"""
    emergency_id: Optional[str] = Field(None, description="Unique emergency identifier")
    patient_id: str = Field(..., description="Patient identifier")
    emergency_type: EmergencyType = Field(..., description="Type of emergency")
    severity: SeverityLevel = Field(..., description="Severity level")
    symptoms: List[str] = Field(..., min_items=1, description="List of symptoms")
    vital_signs: Optional[Dict[str, float]] = Field(None, description="Vital signs measurements")
    location: Optional[str] = Field(None, description="Emergency location")
    timestamp: datetime = Field(default_factory=datetime.now, description="Emergency timestamp")
    notes: Optional[str] = Field(None, max_length=1000, description="Additional notes")
    attending_physician: Optional[str] = Field(None, description="Attending physician")
    
    @validator('symptoms')
    def validate_symptoms(cls, v):
        """Validate symptoms list"""
        if not v:
            raise ValueError('At least one symptom must be provided')
        # Clean and validate each symptom
        cleaned_symptoms = []
        for symptom in v:
            if not symptom or len(symptom.strip()) < 3:
                raise ValueError('Each symptom must be at least 3 characters long')
            cleaned_symptoms.append(symptom.strip().lower())
        return cleaned_symptoms
    
    @validator('vital_signs')
    def validate_vital_signs(cls, v):
        """Validate vital signs values"""
        if v:
            valid_ranges = {
                'heart_rate': (30, 200),
                'blood_pressure_systolic': (70, 250),
                'blood_pressure_diastolic': (40, 150),
                'temperature': (35.0, 42.0),  # Celsius
                'respiratory_rate': (8, 50),
                'oxygen_saturation': (70, 100)
            }
            
            for sign, value in v.items():
                if sign in valid_ranges:
                    min_val, max_val = valid_ranges[sign]
                    if not (min_val <= value <= max_val):
                        raise ValueError(f'{sign} value {value} is outside normal range ({min_val}-{max_val})')
        return v


class MedicalAIRequest(BaseModel):
    """Request model for AI medical analysis"""
    patient_id: Optional[str] = Field(None, description="Patient identifier")
    symptoms: List[str] = Field(..., min_items=1, description="List of symptoms")
    vital_signs: Optional[Dict[str, float]] = Field(None, description="Vital signs")
    medical_history: Optional[List[str]] = Field(default=[], description="Medical history")
    current_medications: Optional[List[str]] = Field(default=[], description="Current medications")
    analysis_type: str = Field(default="diagnosis", description="Type of analysis (diagnosis, risk_assessment)")
    
    @validator('analysis_type')
    def validate_analysis_type(cls, v):
        """Validate analysis type"""
        valid_types = ['diagnosis', 'risk_assessment', 'treatment_recommendation', 'symptom_analysis']
        if v not in valid_types:
            raise ValueError(f'Analysis type must be one of: {", ".join(valid_types)}')
        return v


class MedicalAIResponse(BaseModel):
    """Response model for AI medical analysis"""
    analysis_type: str = Field(..., description="Type of analysis performed")
    confidence: float = Field(..., description="AI confidence score (0-1)")
    recommendations: List[str] = Field(..., description="AI recommendations")
    risk_factors: Optional[List[str]] = Field(None, description="Identified risk factors")
    suggested_actions: List[str] = Field(..., description="Suggested medical actions")
    timestamp: datetime = Field(default_factory=datetime.now, description="Analysis timestamp")
    warnings: Optional[List[str]] = Field(None, description="Important warnings or alerts")


class ValidationResponse(BaseModel):
    """Response model for data validation"""
    is_valid: bool = Field(..., description="Whether the data is valid")
    validation_errors: List[str] = Field(default=[], description="List of validation errors")
    warnings: List[str] = Field(default=[], description="List of warnings")
    validated_data: Optional[Dict[str, Any]] = Field(None, description="Validated and cleaned data")


class EMDResponse(BaseModel):
    """Standard response model for EMD endpoints"""
    success: bool = Field(..., description="Operation success status")
    message: str = Field(..., description="Response message")
    data: Optional[Dict[str, Any]] = Field(None, description="Response data")
    timestamp: datetime = Field(default_factory=datetime.now, description="Response timestamp")
    request_id: Optional[str] = Field(None, description="Request tracking ID")