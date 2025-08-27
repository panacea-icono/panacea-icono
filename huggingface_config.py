#!/usr/bin/env python3
"""
Hugging Face Integration for PANACEA ICONO
Configuración y gestión de modelos de Hugging Face
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Optional
import requests
from transformers import pipeline, AutoTokenizer, AutoModel
import torch

class HuggingFaceManager:
    """Gestor de modelos de Hugging Face para PANACEA ICONO"""
    
    def __init__(self, api_key: Optional[str] = None, email: Optional[str] = None):
        """
        Inicializa el gestor de Hugging Face
        
        Args:
            api_key: API key de Hugging Face
            email: Email de la cuenta de Hugging Face
        """
        self.api_key = api_key or os.getenv('HUGGINGFACE_API_KEY')
        self.email = email or os.getenv('HUGGINGFACE_EMAIL')
        self.base_url = "https://huggingface.co/api"
        self.headers = {"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}
        
        # Directorios para cache y modelos
        self.cache_dir = Path("./models/huggingface")
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Modelos predefinidos
        self.default_models = {
            "text-classification": "distilbert-base-uncased-finetuned-sst-2-english",
            "sentiment-analysis": "cardiffnlp/twitter-roberta-base-sentiment-latest",
            "text-generation": "gpt2",
            "translation": "Helsinki-NLP/opus-mt-es-en",
            "summarization": "facebook/bart-large-cnn",
            "question-answering": "deepset/roberta-base-squad2",
            "token-classification": "dbmdz/bert-large-cased-finetuned-conll03-english"
        }
    
    def verify_connection(self) -> bool:
        """
        Verifica la conexión con Hugging Face
        
        Returns:
            True si la conexión es exitosa
        """
        try:
            response = requests.get(f"{self.base_url}/models", headers=self.headers, timeout=10)
            return response.status_code == 200
        except Exception as e:
            print(f"❌ Error de conexión: {e}")
            return False
    
    def get_user_info(self) -> Optional[Dict]:
        """
        Obtiene información del usuario de Hugging Face
        
        Returns:
            Información del usuario o None si hay error
        """
        try:
            response = requests.get(f"{self.base_url}/whoami", headers=self.headers, timeout=10)
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"❌ Error al obtener información del usuario: {e}")
            return None
    
    def list_user_models(self) -> List[Dict]:
        """
        Lista los modelos del usuario
        
        Returns:
            Lista de modelos del usuario
        """
        try:
            if not self.email:
                return []
            
            response = requests.get(
                f"{self.base_url}/models", 
                headers=self.headers, 
                params={"author": self.email},
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            return []
        except Exception as e:
            print(f"❌ Error al listar modelos: {e}")
            return []
    
    def download_model(self, model_name: str, task: str = None) -> bool:
        """
        Descarga un modelo de Hugging Face
        
        Args:
            model_name: Nombre del modelo
            task: Tipo de tarea (opcional)
            
        Returns:
            True si la descarga fue exitosa
        """
        try:
            print(f"📥 Descargando modelo: {model_name}")
            
            if task:
                # Crear pipeline con tarea específica
                model = pipeline(task, model=model_name, cache_dir=self.cache_dir)
                print(f"✅ Modelo descargado: {model_name}")
                return True
            else:
                # Descargar tokenizer y modelo
                tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir=self.cache_dir)
                model = AutoModel.from_pretrained(model_name, cache_dir=self.cache_dir)
                print(f"✅ Modelo descargado: {model_name}")
                return True
                
        except Exception as e:
            print(f"❌ Error al descargar modelo {model_name}: {e}")
            return False
    
    def create_pipeline(self, task: str, model_name: str = None) -> Optional[object]:
        """
        Crea un pipeline de Hugging Face
        
        Args:
            task: Tipo de tarea
            model_name: Nombre del modelo (opcional)
            
        Returns:
            Pipeline de Hugging Face o None si hay error
        """
        try:
            if not model_name:
                model_name = self.default_models.get(task, "gpt2")
            
            print(f"🔧 Creando pipeline para {task} con modelo {model_name}")
            pipeline_obj = pipeline(task, model=model_name, cache_dir=self.cache_dir)
            print(f"✅ Pipeline creado exitosamente")
            return pipeline_obj
            
        except Exception as e:
            print(f"❌ Error al crear pipeline: {e}")
            return None
    
    def test_models(self) -> Dict[str, bool]:
        """
        Prueba todos los modelos predefinidos
        
        Returns:
            Diccionario con el estado de cada modelo
        """
        results = {}
        
        for task, model_name in self.default_models.items():
            print(f"🧪 Probando {task} con {model_name}")
            try:
                pipeline_obj = self.create_pipeline(task, model_name)
                results[task] = pipeline_obj is not None
            except Exception as e:
                print(f"❌ Error en {task}: {e}")
                results[task] = False
        
        return results
    
    def get_model_info(self, model_name: str) -> Optional[Dict]:
        """
        Obtiene información de un modelo específico
        
        Args:
            model_name: Nombre del modelo
            
        Returns:
            Información del modelo o None si hay error
        """
        try:
            response = requests.get(f"{self.base_url}/models/{model_name}", headers=self.headers, timeout=10)
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"❌ Error al obtener información del modelo: {e}")
            return None

def main():
    """Función principal para probar la integración"""
    print("🤗 Iniciando integración con Hugging Face...")
    
    # Crear instancia del gestor
    hf_manager = HuggingFaceManager()
    
    # Verificar conexión
    if hf_manager.verify_connection():
        print("✅ Conexión con Hugging Face establecida")
        
        # Obtener información del usuario
        user_info = hf_manager.get_user_info()
        if user_info:
            print(f"👤 Usuario: {user_info.get('name', 'N/A')}")
        
        # Listar modelos del usuario
        user_models = hf_manager.list_user_models()
        if user_models:
            print(f"📚 Modelos del usuario: {len(user_models)}")
            for model in user_models[:3]:  # Mostrar solo los primeros 3
                print(f"  - {model.get('name', 'N/A')}")
        
        # Probar modelos predefinidos
        print("\n🧪 Probando modelos predefinidos...")
        test_results = hf_manager.test_models()
        
        print("\n📊 Resultados de las pruebas:")
        for task, success in test_results.items():
            status = "✅" if success else "❌"
            print(f"  {status} {task}")
        
    else:
        print("❌ No se pudo establecer conexión con Hugging Face")
        print("💡 Verifica tu API key y conexión a internet")

if __name__ == "__main__":
    main()
