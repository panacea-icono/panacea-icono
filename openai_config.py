#!/usr/bin/env python3
"""
OpenAI Integration for PANACEA ICONO
Configuración y gestión de modelos de OpenAI para tareas de código
"""

import os
import logging
from typing import Dict, List, Optional, Any
import openai
from openai import OpenAI

logger = logging.getLogger(__name__)

class OpenAIManager:
    """Gestor de modelos de OpenAI para PANACEA ICONO - Enfoque en Codex/Code tasks"""
    
    def __init__(self, api_key: Optional[str] = None, organization: Optional[str] = None):
        """
        Inicializa el gestor de OpenAI
        
        Args:
            api_key: API key de OpenAI
            organization: Organization ID de OpenAI
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        self.organization = organization or os.getenv('OPENAI_ORGANIZATION')
        
        if not self.api_key:
            logger.warning("⚠️ OPENAI_API_KEY no configurada - funcionalidad limitada")
            self.client = None
        else:
            try:
                self.client = OpenAI(
                    api_key=self.api_key,
                    organization=self.organization
                )
                logger.info("✅ Cliente OpenAI inicializado correctamente")
            except Exception as e:
                logger.error(f"❌ Error inicializando cliente OpenAI: {e}")
                self.client = None
        
        # Modelos recomendados para tareas de código
        self.code_models = {
            "chat": "gpt-4o-mini",  # Más económico para chat
            "code_generation": "gpt-4o",  # Mejor para generación de código
            "code_explanation": "gpt-4o-mini",  # Eficiente para explicaciones
            "code_completion": "gpt-4o-mini",  # Rápido para completado
            "code_review": "gpt-4o",  # Mejor para análisis profundo
        }
        
        # Templates de prompts para diferentes tareas
        self.prompt_templates = {
            "code_generation": """Eres un experto programador. Genera código limpio y bien documentado para la siguiente tarea:

Tarea: {task}
Lenguaje: {language}
Requisitos adicionales: {requirements}

Proporciona el código con comentarios explicativos cuando sea necesario.""",
            
            "code_explanation": """Eres un experto programador. Explica el siguiente código de manera clara y educativa:

Código:
```{language}
{code}
```

Proporciona una explicación detallada de lo que hace el código, cómo funciona y cualquier concepto importante.""",
            
            "code_completion": """Eres un experto programador. Completa el siguiente código de manera lógica y consistente:

Código incompleto:
```{language}
{partial_code}
```

Contexto: {context}

Completa el código manteniendo el estilo y la lógica existente.""",
            
            "code_review": """Eres un experto en revisión de código. Analiza el siguiente código y proporciona feedback constructivo:

Código:
```{language}
{code}
```

Evalúa:
- Calidad del código
- Posibles mejoras
- Problemas de seguridad
- Optimizaciones
- Mejores prácticas

Proporciona sugerencias específicas y constructivas."""
        }
    
    def verify_connection(self) -> bool:
        """
        Verifica la conexión con OpenAI
        
        Returns:
            True si la conexión es exitosa
        """
        if not self.client:
            return False
            
        try:
            # Intenta hacer una llamada simple para verificar la conexión
            response = self.client.models.list()
            return True
        except Exception as e:
            logger.error(f"❌ Error de conexión con OpenAI: {e}")
            return False
    
    def get_available_models(self) -> List[str]:
        """
        Obtiene la lista de modelos disponibles
        
        Returns:
            Lista de nombres de modelos
        """
        if not self.client:
            return []
        
        try:
            models = self.client.models.list()
            return [model.id for model in models.data if "gpt" in model.id.lower()]
        except Exception as e:
            logger.error(f"❌ Error obteniendo modelos: {e}")
            return []
    
    def generate_code(self, task: str, language: str = "python", 
                     requirements: str = "", model: str = None) -> Optional[str]:
        """
        Genera código basado en una tarea específica
        
        Args:
            task: Descripción de la tarea
            language: Lenguaje de programación
            requirements: Requisitos adicionales
            model: Modelo a usar (opcional)
            
        Returns:
            Código generado o None si hay error
        """
        if not self.client:
            logger.error("❌ Cliente OpenAI no disponible")
            return None
        
        model_name = model or self.code_models["code_generation"]
        prompt = self.prompt_templates["code_generation"].format(
            task=task,
            language=language,
            requirements=requirements
        )
        
        try:
            logger.info(f"🔧 Generando código para: {task}")
            response = self.client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": "Eres un experto programador que genera código limpio, eficiente y bien documentado."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.3
            )
            
            result = response.choices[0].message.content
            logger.info("✅ Código generado exitosamente")
            return result
            
        except Exception as e:
            logger.error(f"❌ Error generando código: {e}")
            return None
    
    def explain_code(self, code: str, language: str = "python", 
                    model: str = None) -> Optional[str]:
        """
        Explica código existente
        
        Args:
            code: Código a explicar
            language: Lenguaje de programación
            model: Modelo a usar (opcional)
            
        Returns:
            Explicación del código o None si hay error
        """
        if not self.client:
            logger.error("❌ Cliente OpenAI no disponible")
            return None
        
        model_name = model or self.code_models["code_explanation"]
        prompt = self.prompt_templates["code_explanation"].format(
            code=code,
            language=language
        )
        
        try:
            logger.info("🔍 Explicando código...")
            response = self.client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": "Eres un experto programador que explica código de manera clara y educativa."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1500,
                temperature=0.2
            )
            
            result = response.choices[0].message.content
            logger.info("✅ Explicación generada exitosamente")
            return result
            
        except Exception as e:
            logger.error(f"❌ Error explicando código: {e}")
            return None
    
    def complete_code(self, partial_code: str, context: str = "", 
                     language: str = "python", model: str = None) -> Optional[str]:
        """
        Completa código parcial
        
        Args:
            partial_code: Código parcial
            context: Contexto adicional
            language: Lenguaje de programación
            model: Modelo a usar (opcional)
            
        Returns:
            Código completado o None si hay error
        """
        if not self.client:
            logger.error("❌ Cliente OpenAI no disponible")
            return None
        
        model_name = model or self.code_models["code_completion"]
        prompt = self.prompt_templates["code_completion"].format(
            partial_code=partial_code,
            context=context,
            language=language
        )
        
        try:
            logger.info("🔧 Completando código...")
            response = self.client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": "Eres un experto programador que completa código de manera lógica y consistente."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.3
            )
            
            result = response.choices[0].message.content
            logger.info("✅ Código completado exitosamente")
            return result
            
        except Exception as e:
            logger.error(f"❌ Error completando código: {e}")
            return None
    
    def review_code(self, code: str, language: str = "python", 
                   model: str = None) -> Optional[str]:
        """
        Revisa código y proporciona feedback
        
        Args:
            code: Código a revisar
            language: Lenguaje de programación
            model: Modelo a usar (opcional)
            
        Returns:
            Review del código o None si hay error
        """
        if not self.client:
            logger.error("❌ Cliente OpenAI no disponible")
            return None
        
        model_name = model or self.code_models["code_review"]
        prompt = self.prompt_templates["code_review"].format(
            code=code,
            language=language
        )
        
        try:
            logger.info("📝 Revisando código...")
            response = self.client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": "Eres un experto en revisión de código que proporciona feedback constructivo y específico."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.2
            )
            
            result = response.choices[0].message.content
            logger.info("✅ Review completado exitosamente")
            return result
            
        except Exception as e:
            logger.error(f"❌ Error revisando código: {e}")
            return None
    
    def chat_about_code(self, message: str, conversation_history: List[Dict] = None,
                       model: str = None) -> Optional[str]:
        """
        Chat conversacional sobre código
        
        Args:
            message: Mensaje del usuario
            conversation_history: Historial de conversación
            model: Modelo a usar (opcional)
            
        Returns:
            Respuesta del chat o None si hay error
        """
        if not self.client:
            logger.error("❌ Cliente OpenAI no disponible")
            return None
        
        model_name = model or self.code_models["chat"]
        
        # Construir mensajes de conversación
        messages = [
            {"role": "system", "content": "Eres un experto programador y mentor de código. Ayudas a los desarrolladores con dudas sobre programación, debugging, mejores prácticas y arquitectura de software. Responde de manera clara, práctica y con ejemplos cuando sea útil."}
        ]
        
        # Agregar historial si existe
        if conversation_history:
            messages.extend(conversation_history)
        
        messages.append({"role": "user", "content": message})
        
        try:
            logger.info("💬 Procesando chat sobre código...")
            response = self.client.chat.completions.create(
                model=model_name,
                messages=messages,
                max_tokens=1500,
                temperature=0.4
            )
            
            result = response.choices[0].message.content
            logger.info("✅ Respuesta de chat generada exitosamente")
            return result
            
        except Exception as e:
            logger.error(f"❌ Error en chat: {e}")
            return None

def main():
    """Función principal para probar la integración"""
    print("🤖 Iniciando integración con OpenAI...")
    
    # Crear instancia del gestor
    openai_manager = OpenAIManager()
    
    # Verificar conexión
    if openai_manager.verify_connection():
        print("✅ Conexión con OpenAI establecida")
        
        # Obtener modelos disponibles
        models = openai_manager.get_available_models()
        if models:
            print(f"📚 Modelos disponibles: {len(models)}")
            for model in models[:5]:  # Mostrar solo los primeros 5
                print(f"  - {model}")
        
        # Probar generación de código
        print("\n🧪 Probando generación de código...")
        code_result = openai_manager.generate_code(
            task="Crear una función que calcule el factorial de un número",
            language="python"
        )
        if code_result:
            print("✅ Código generado exitosamente")
            print(f"📄 Resultado: {code_result[:200]}...")
        
    else:
        print("❌ No se pudo establecer conexión con OpenAI")
        print("💡 Verifica tu API key y conexión a internet")

if __name__ == "__main__":
    main()