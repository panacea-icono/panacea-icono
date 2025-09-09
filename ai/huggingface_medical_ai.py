#!/usr/bin/env python3
"""
🏥 PANACEA ICONO S.A. - Sistema de IA Médica con Hugging Face
Integración con modelos de IA especializados en medicina
"""

import os
import logging
import asyncio
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
from dataclasses import dataclass
import httpx
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class MedicalModel:
    """Estructura para un modelo médico de Hugging Face"""
    name: str
    model_id: str
    description: str
    category: str
    task: str
    status: str = "available"
    last_used: Optional[datetime] = None
    usage_count: int = 0

class PanaceaMedicalAI:
    """Sistema de IA médica integrado con Hugging Face para Panacea Icono S.A."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("HUGGINGFACE_API_KEY")
        self.base_url = "https://api-inference.huggingface.co/models"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        self.models: Dict[str, MedicalModel] = {}
        self._initialize_medical_models()
    
    def _initialize_medical_models(self):
        """Inicializar modelos médicos especializados"""
        
        # Modelos de análisis de imágenes médicas
        self.models["medical_image_analysis"] = MedicalModel(
            name="Análisis de Imágenes Médicas",
            model_id="microsoft/DialoGPT-medium",
            description="Análisis de imágenes médicas y diagnósticos por imagen",
            category="medical_imaging",
            task="image-classification"
        )
        
        # Modelo de procesamiento de lenguaje médico
        self.models["medical_nlp"] = MedicalModel(
            name="Procesamiento de Lenguaje Médico",
            model_id="microsoft/BioGPT",
            description="Procesamiento de texto médico y análisis de historias clínicas",
            category="natural_language_processing",
            task="text-generation"
        )
        
        # Modelo de clasificación de síntomas
        self.models["symptom_classifier"] = MedicalModel(
            name="Clasificador de Síntomas",
            model_id="microsoft/DialoGPT-medium",
            description="Clasificación y análisis de síntomas médicos",
            category="symptom_analysis",
            task="text-classification"
        )
        
        # Modelo de recomendaciones de tratamientos
        self.models["treatment_recommender"] = MedicalModel(
            name="Recomendador de Tratamientos",
            model_id="microsoft/BioGPT",
            description="Recomendaciones de tratamientos basadas en síntomas",
            category="treatment_recommendation",
            task="text-generation"
        )
        
        # Modelo de análisis de cirugía plástica
        self.models["plastic_surgery_analyzer"] = MedicalModel(
            name="Analizador de Cirugía Plástica",
            model_id="microsoft/DialoGPT-medium",
            description="Análisis especializado en procedimientos de cirugía plástica",
            category="plastic_surgery",
            task="text-generation"
        )
    
    async def query_model(self, model_name: str, input_data: Union[str, Dict], **kwargs) -> Dict[str, Any]:
        """Consultar un modelo específico"""
        if model_name not in self.models:
            return {"error": f"Modelo {model_name} no encontrado"}
        
        model = self.models[model_name]
        
        try:
            async with httpx.AsyncClient() as client:
                # Preparar datos según el tipo de tarea
                if model.task == "text-generation":
                    payload = {
                        "inputs": input_data,
                        "parameters": {
                            "max_length": kwargs.get("max_length", 200),
                            "temperature": kwargs.get("temperature", 0.7),
                            "do_sample": kwargs.get("do_sample", True)
                        }
                    }
                elif model.task == "text-classification":
                    payload = {"inputs": input_data}
                elif model.task == "image-classification":
                    payload = {"inputs": input_data}
                else:
                    payload = {"inputs": input_data}
                
                response = await client.post(
                    f"{self.base_url}/{model.model_id}",
                    headers=self.headers,
                    json=payload,
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    result = response.json()
                    model.usage_count += 1
                    model.last_used = datetime.now()
                    return {
                        "status": "success",
                        "model": model_name,
                        "result": result,
                        "timestamp": datetime.now().isoformat()
                    }
                else:
                    return {
                        "status": "error",
                        "model": model_name,
                        "error": f"HTTP {response.status_code}: {response.text}",
                        "timestamp": datetime.now().isoformat()
                    }
        
        except Exception as e:
            return {
                "status": "error",
                "model": model_name,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    async def analyze_medical_text(self, text: str) -> Dict[str, Any]:
        """Analizar texto médico usando NLP"""
        return await self.query_model(
            "medical_nlp",
            f"Analiza el siguiente texto médico: {text}",
            max_length=300,
            temperature=0.3
        )
    
    async def classify_symptoms(self, symptoms: str) -> Dict[str, Any]:
        """Clasificar síntomas médicos"""
        return await self.query_model(
            "symptom_classifier",
            f"Clasifica estos síntomas: {symptoms}",
            max_length=200,
            temperature=0.2
        )
    
    async def recommend_treatment(self, condition: str, symptoms: str) -> Dict[str, Any]:
        """Recomendar tratamiento basado en condición y síntomas"""
        prompt = f"""
        Condición: {condition}
        Síntomas: {symptoms}
        
        Recomienda un tratamiento apropiado para Panacea Icono S.A.:
        """
        return await self.query_model(
            "treatment_recommender",
            prompt,
            max_length=400,
            temperature=0.4
        )
    
    async def analyze_plastic_surgery_case(self, case_description: str) -> Dict[str, Any]:
        """Analizar caso de cirugía plástica"""
        prompt = f"""
        Analiza este caso de cirugía plástica para Panacea Icono S.A.:
        
        Descripción del caso: {case_description}
        
        Proporciona:
        1. Evaluación del caso
        2. Procedimientos recomendados
        3. Consideraciones especiales
        4. Riesgos potenciales
        """
        return await self.query_model(
            "plastic_surgery_analyzer",
            prompt,
            max_length=500,
            temperature=0.3
        )
    
    def get_model_stats(self) -> Dict[str, Any]:
        """Obtener estadísticas de los modelos"""
        total_models = len(self.models)
        available_models = len([model for model in self.models.values() if model.status == "available"])
        
        categories = {}
        for model in self.models.values():
            if model.category not in categories:
                categories[model.category] = 0
            categories[model.category] += 1
        
        total_usage = sum(model.usage_count for model in self.models.values())
        
        return {
            "total_models": total_models,
            "available_models": available_models,
            "categories": categories,
            "total_usage": total_usage,
            "api_key_configured": bool(self.api_key),
            "last_update": datetime.now().isoformat()
        }
    
    def list_available_models(self) -> List[Dict[str, Any]]:
        """Listar modelos disponibles"""
        return [
            {
                "name": model.name,
                "model_id": model.model_id,
                "description": model.description,
                "category": model.category,
                "task": model.task,
                "status": model.status,
                "usage_count": model.usage_count
            }
            for model in self.models.values()
        ]

# Instancia global del sistema de IA médica
medical_ai = PanaceaMedicalAI()

async def main():
    """Función principal para testing"""
    print("🏥 PANACEA ICONO S.A. - Sistema de IA Médica con Hugging Face")
    print("=" * 70)
    
    # Mostrar estadísticas
    stats = medical_ai.get_model_stats()
    print(f"Total de modelos: {stats['total_models']}")
    print(f"Modelos disponibles: {stats['available_models']}")
    print(f"Categorías: {stats['categories']}")
    print(f"Uso total: {stats['total_usage']}")
    print(f"API Key configurada: {stats['api_key_configured']}")
    
    # Listar modelos disponibles
    print("\n🤖 Modelos de IA Médica Disponibles:")
    print("-" * 50)
    for model_info in medical_ai.list_available_models():
        print(f"• {model_info['name']}")
        print(f"  ID: {model_info['model_id']}")
        print(f"  Categoría: {model_info['category']}")
        print(f"  Tarea: {model_info['task']}")
        print(f"  Uso: {model_info['usage_count']} veces")
        print()
    
    # Ejemplo de uso
    if stats['api_key_configured']:
        print("🔍 Ejemplo de análisis médico:")
        print("-" * 30)
        
        # Analizar texto médico de ejemplo
        sample_text = "Paciente de 35 años con dolor abdominal en cuadrante inferior derecho, fiebre de 38.5°C, náuseas y vómitos."
        result = await medical_ai.analyze_medical_text(sample_text)
        print(f"Resultado: {result}")

if __name__ == "__main__":
    asyncio.run(main())
