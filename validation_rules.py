#!/usr/bin/env python3
"""
Medical Validation Rules for PANACEA ICONO EMD System
Implements comprehensive validation rules for healthcare data
"""

from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Any
import re
from models import Patient, EmergencyData, MedicalAIRequest, SeverityLevel, EmergencyType


class MedicalValidator:
    """Medical data validation engine with healthcare-specific rules"""
    
    def __init__(self):
        """Initialize the medical validator with rules"""
        self.critical_symptoms = {
            'chest_pain', 'shortness_of_breath', 'severe_headache', 'loss_of_consciousness',
            'difficulty_breathing', 'heart_attack', 'stroke', 'seizure', 'severe_bleeding',
            'anaphylaxis', 'cardiac_arrest', 'respiratory_failure'
        }
        
        self.high_priority_conditions = {
            'diabetes', 'hypertension', 'heart_disease', 'asthma', 'copd', 'epilepsy',
            'kidney_disease', 'liver_disease', 'cancer', 'immunocompromised'
        }
        
        self.drug_interactions = {
            'warfarin': ['aspirin', 'ibuprofen', 'naproxen'],
            'insulin': ['alcohol', 'sulfonylureas'],
            'digoxin': ['amiodarone', 'verapamil', 'quinidine']
        }
    
    def validate_patient_data(self, patient: Patient) -> Tuple[bool, List[str], List[str]]:
        """
        Validate patient data with medical rules
        
        Returns:
            Tuple of (is_valid, errors, warnings)
        """
        errors = []
        warnings = []
        
        # Age validation
        try:
            birth_date = datetime.strptime(patient.date_of_birth, '%Y-%m-%d')
            age = (datetime.now() - birth_date).days // 365
            
            if age < 0:
                errors.append("Patient cannot have a future birth date")
            elif age > 150:
                warnings.append("Patient age seems unusually high, please verify")
            elif age < 1:
                warnings.append("Infant patient - additional care protocols may apply")
            elif age >= 65:
                warnings.append("Elderly patient - consider age-related risk factors")
                
        except ValueError:
            errors.append("Invalid date of birth format")
        
        # Medical conditions validation
        if patient.medical_conditions:
            for condition in patient.medical_conditions:
                condition_lower = condition.lower().strip()
                if condition_lower in self.high_priority_conditions:
                    warnings.append(f"High-priority medical condition detected: {condition}")
        
        # Medication interactions validation
        if patient.medications and len(patient.medications) > 1:
            medication_warnings = self._check_drug_interactions(patient.medications)
            warnings.extend(medication_warnings)
        
        # Allergy validation
        if patient.allergies:
            for allergy in patient.allergies:
                if any(med.lower() in allergy.lower() for med in patient.medications or []):
                    errors.append(f"Potential allergy-medication conflict: {allergy}")
        
        # Emergency contact validation
        if not patient.emergency_contact and age >= 65:
            warnings.append("Elderly patient without emergency contact - recommend adding one")
        
        is_valid = len(errors) == 0
        return is_valid, errors, warnings
    
    def validate_emergency_data(self, emergency: EmergencyData) -> Tuple[bool, List[str], List[str]]:
        """
        Validate emergency data with medical rules
        
        Returns:
            Tuple of (is_valid, errors, warnings)
        """
        errors = []
        warnings = []
        
        # Critical symptom detection
        critical_detected = False
        for symptom in emergency.symptoms:
            symptom_lower = symptom.lower().strip()
            if any(crit_symptom in symptom_lower for crit_symptom in self.critical_symptoms):
                critical_detected = True
                warnings.append(f"CRITICAL SYMPTOM DETECTED: {symptom}")
        
        # Severity vs symptoms consistency
        if critical_detected and emergency.severity != SeverityLevel.CRITICAL:
            warnings.append("Critical symptoms detected but severity not marked as CRITICAL")
        
        # Vital signs validation
        if emergency.vital_signs:
            vital_warnings = self._validate_vital_signs_medical_rules(emergency.vital_signs)
            warnings.extend(vital_warnings)
        
        # Time-sensitive emergency types
        time_sensitive_types = {EmergencyType.CARDIAC, EmergencyType.NEUROLOGICAL}
        if emergency.emergency_type in time_sensitive_types:
            time_diff = datetime.now() - emergency.timestamp
            if time_diff > timedelta(hours=1):
                warnings.append(f"Time-sensitive emergency ({emergency.emergency_type}) reported over 1 hour ago")
        
        # Emergency type vs symptoms consistency
        type_symptom_check = self._validate_emergency_type_symptoms(
            emergency.emergency_type, emergency.symptoms
        )
        if type_symptom_check:
            warnings.append(type_symptom_check)
        
        is_valid = len(errors) == 0
        return is_valid, errors, warnings
    
    def validate_ai_request(self, request: MedicalAIRequest) -> Tuple[bool, List[str], List[str]]:
        """
        Validate AI medical analysis request
        
        Returns:
            Tuple of (is_valid, errors, warnings)
        """
        errors = []
        warnings = []
        
        # Symptom quality validation
        if len(request.symptoms) == 1 and len(request.symptoms[0]) < 10:
            warnings.append("Single, very brief symptom description - consider providing more detail")
        
        # Medical history vs medications consistency
        if request.medical_history and request.current_medications:
            history_lower = [h.lower() for h in request.medical_history]
            med_warnings = []
            
            for med in request.current_medications:
                med_lower = med.lower()
                # Check if medication matches medical history
                if 'diabetes' in history_lower and 'insulin' not in med_lower and 'metformin' not in med_lower:
                    med_warnings.append("Diabetes in history but no diabetes medications listed")
                elif 'hypertension' in history_lower and not any(bp_med in med_lower 
                    for bp_med in ['lisinopril', 'amlodipine', 'losartan', 'hydrochlorothiazide']):
                    med_warnings.append("Hypertension in history but no blood pressure medications listed")
            
            warnings.extend(med_warnings)
        
        # Vital signs completeness for different analysis types
        if request.analysis_type == 'risk_assessment' and not request.vital_signs:
            warnings.append("Risk assessment requested but no vital signs provided")
        
        is_valid = len(errors) == 0
        return is_valid, errors, warnings
    
    def _check_drug_interactions(self, medications: List[str]) -> List[str]:
        """Check for potential drug interactions"""
        warnings = []
        med_lower = [med.lower().strip() for med in medications]
        
        for med in med_lower:
            if med in self.drug_interactions:
                for interacting_drug in self.drug_interactions[med]:
                    if interacting_drug in med_lower:
                        warnings.append(
                            f"Potential drug interaction: {med} and {interacting_drug}"
                        )
        
        return warnings
    
    def _validate_vital_signs_medical_rules(self, vital_signs: Dict[str, float]) -> List[str]:
        """Validate vital signs with medical rules"""
        warnings = []
        
        # Critical vital signs thresholds
        critical_ranges = {
            'heart_rate': [(30, 50, "Bradycardia"), (100, 200, "Tachycardia")],
            'blood_pressure_systolic': [(90, 120, "Hypotension"), (140, 250, "Hypertension")],
            'temperature': [(35.0, 36.0, "Hypothermia"), (38.5, 42.0, "Hyperthermia")],
            'oxygen_saturation': [(70, 90, "Hypoxemia")]
        }
        
        for sign, value in vital_signs.items():
            if sign in critical_ranges:
                for min_val, max_val, condition in critical_ranges[sign]:
                    if min_val <= value < max_val:
                        warnings.append(f"{condition} detected: {sign} = {value}")
        
        # Vital signs combinations
        if 'heart_rate' in vital_signs and 'blood_pressure_systolic' in vital_signs:
            hr = vital_signs['heart_rate']
            bp_sys = vital_signs['blood_pressure_systolic']
            
            if hr > 100 and bp_sys < 90:
                warnings.append("Tachycardia with hypotension - possible shock")
            elif hr < 60 and bp_sys > 160:
                warnings.append("Bradycardia with hypertension - possible increased intracranial pressure")
        
        return warnings
    
    def _validate_emergency_type_symptoms(self, emergency_type: EmergencyType, symptoms: List[str]) -> Optional[str]:
        """Validate consistency between emergency type and symptoms"""
        symptoms_lower = [s.lower() for s in symptoms]
        symptoms_text = ' '.join(symptoms_lower)
        
        expected_keywords = {
            EmergencyType.CARDIAC: ['chest', 'heart', 'cardiac', 'palpitation', 'angina'],
            EmergencyType.RESPIRATORY: ['breath', 'lung', 'asthma', 'copd', 'oxygen'],
            EmergencyType.NEUROLOGICAL: ['head', 'brain', 'seizure', 'stroke', 'neurological'],
            EmergencyType.TRAUMA: ['injury', 'trauma', 'fracture', 'wound', 'accident']
        }
        
        if emergency_type in expected_keywords:
            keywords = expected_keywords[emergency_type]
            if not any(keyword in symptoms_text for keyword in keywords):
                return f"Emergency type '{emergency_type}' may not match reported symptoms"
        
        return None
    
    def calculate_triage_priority(self, emergency: EmergencyData, patient_age: int) -> Tuple[int, str]:
        """
        Calculate triage priority (1=highest, 5=lowest)
        
        Returns:
            Tuple of (priority_level, reason)
        """
        priority = 3  # Default priority
        reasons = []
        
        # Critical symptoms = Priority 1
        for symptom in emergency.symptoms:
            symptom_lower = symptom.lower()
            if any(crit in symptom_lower for crit in self.critical_symptoms):
                priority = 1
                reasons.append("Critical symptoms present")
                break
        
        # Severity-based priority
        if emergency.severity == SeverityLevel.CRITICAL:
            priority = min(priority, 1)
            reasons.append("Critical severity")
        elif emergency.severity == SeverityLevel.HIGH:
            priority = min(priority, 2)
            reasons.append("High severity")
        
        # Age-based priority adjustments
        if patient_age >= 65:
            priority = min(priority, 2)
            reasons.append("Elderly patient")
        elif patient_age < 2:
            priority = min(priority, 2)
            reasons.append("Infant patient")
        
        # Vital signs priority
        if emergency.vital_signs:
            vs = emergency.vital_signs
            if (vs.get('oxygen_saturation', 100) < 90 or 
                vs.get('heart_rate', 70) > 120 or 
                vs.get('blood_pressure_systolic', 120) < 90):
                priority = min(priority, 2)
                reasons.append("Abnormal vital signs")
        
        reason_text = "; ".join(reasons) if reasons else "Standard triage assessment"
        return priority, reason_text