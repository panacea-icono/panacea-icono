#!/usr/bin/env python3
"""
🏥 PANACEA ICONO S.A. - Ecosistema de IA Integrado
Sistema unificado que integra bots, GPTs e IA para Panacea Icono S.A.
"""

import os
import logging
import asyncio
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
from dataclasses import dataclass
import json

# Importar sistemas individuales
from bots.telegram_bots_manager import PanaceaTelegramManager
from ai.panacea_gpt_system import PanaceaGPTSystem, GPTCategory
from ai.huggingface_medical_ai import PanaceaMedicalAI

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class AIEcosystemStatus:
    """Estado del ecosistema de IA"""
    timestamp: str
    telegram_bots: Dict[str, Any]
    gpt_system: Dict[str, Any]
    medical_ai: Dict[str, Any]
    overall_health: str
    total_components: int
    active_components: int

class PanaceaAIEcosystem:
    """Ecosistema integrado de IA para Panacea Icono S.A."""
    
    def __init__(self):
        self.telegram_manager = PanaceaTelegramManager()
        self.gpt_system = PanaceaGPTSystem()
        self.medical_ai = PanaceaMedicalAI()
        self.logger = logging.getLogger(__name__)
    
    async def get_ecosystem_status(self) -> AIEcosystemStatus:
        """Obtener estado completo del ecosistema de IA"""
        
        # Estado de bots de Telegram
        telegram_health = await self.telegram_manager.check_all_bots_health()
        telegram_stats = self.telegram_manager.get_bot_stats()
        
        # Estado del sistema GPT
        gpt_stats = self.gpt_system.get_gpt_stats()
        
        # Estado de IA médica
        medical_ai_stats = self.medical_ai.get_model_stats()
        
        # Calcular salud general
        total_components = (
            telegram_stats['total_bots'] + 
            gpt_stats['total_gpts'] + 
            medical_ai_stats['total_models']
        )
        
        active_components = (
            telegram_stats['active_bots'] + 
            gpt_stats['active_gpts'] + 
            medical_ai_stats['available_models']
        )
        
        health_percentage = (active_components / total_components) * 100 if total_components > 0 else 0
        
        if health_percentage >= 90:
            overall_health = "excellent"
        elif health_percentage >= 75:
            overall_health = "good"
        elif health_percentage >= 50:
            overall_health = "fair"
        else:
            overall_health = "poor"
        
        return AIEcosystemStatus(
            timestamp=datetime.now().isoformat(),
            telegram_bots={
                "health": telegram_health,
                "stats": telegram_stats
            },
            gpt_system=gpt_stats,
            medical_ai=medical_ai_stats,
            overall_health=overall_health,
            total_components=total_components,
            active_components=active_components
        )
    
    async def process_medical_query(self, query: str, user_id: str = None) -> Dict[str, Any]:
        """Procesar consulta médica usando el ecosistema completo"""
        
        try:
            # 1. Analizar la consulta con IA médica
            medical_analysis = await self.medical_ai.analyze_medical_text(query)
            
            # 2. Generar respuesta con GPT médico
            gpt_response = self.gpt_system.generate_gpt_prompt("panacea_medical", query)
            
            # 3. Determinar si necesita atención especializada
            needs_specialist = self._needs_specialist_attention(query)
            
            # 4. Preparar respuesta integrada
            response = {
                "timestamp": datetime.now().isoformat(),
                "query": query,
                "user_id": user_id,
                "medical_analysis": medical_analysis,
                "gpt_response": gpt_response,
                "needs_specialist": needs_specialist,
                "recommended_actions": self._get_recommended_actions(query, needs_specialist),
                "contact_info": {
                    "phone": "+591 69674560",
                    "email": "citas@panacea-icono.org",
                    "whatsapp": "+591 69674560"
                }
            }
            
            return response
            
        except Exception as e:
            self.logger.error(f"Error procesando consulta médica: {e}")
            return {
                "error": "Error procesando consulta médica",
                "timestamp": datetime.now().isoformat(),
                "contact_info": {
                    "phone": "+591 69674560",
                    "email": "citas@panacea-icono.org"
                }
            }
    
    def _needs_specialist_attention(self, query: str) -> bool:
        """Determinar si la consulta necesita atención especializada"""
        urgent_keywords = [
            "emergencia", "urgente", "dolor severo", "sangrado", "fiebre alta",
            "cirugía", "operación", "complicación", "reacción alérgica"
        ]
        
        query_lower = query.lower()
        return any(keyword in query_lower for keyword in urgent_keywords)
    
    def _get_recommended_actions(self, query: str, needs_specialist: bool) -> List[str]:
        """Obtener acciones recomendadas basadas en la consulta"""
        actions = []
        
        if needs_specialist:
            actions.extend([
                "Contactar inmediatamente al +591 69674560",
                "Agendar consulta presencial urgente",
                "Considerar visita a emergencias si es crítico"
            ])
        else:
            actions.extend([
                "Agendar consulta médica regular",
                "Contactar por WhatsApp para más información",
                "Revisar documentación médica disponible"
            ])
        
        return actions
    
    async def send_telegram_notification(self, bot_name: str, chat_id: str, message: str) -> Dict[str, Any]:
        """Enviar notificación a través de Telegram"""
        return await self.telegram_manager.send_message(bot_name, chat_id, message)
    
    async def get_ai_recommendations(self, category: str, input_data: str) -> Dict[str, Any]:
        """Obtener recomendaciones de IA según la categoría"""
        
        if category == "medical":
            return await self.medical_ai.analyze_medical_text(input_data)
        elif category == "surgical":
            return await self.medical_ai.analyze_plastic_surgery_case(input_data)
        elif category == "symptoms":
            return await self.medical_ai.classify_symptoms(input_data)
        elif category == "treatment":
            return await self.medical_ai.recommend_treatment("", input_data)
        else:
            return {"error": f"Categoría {category} no soportada"}
    
    def get_ecosystem_dashboard_data(self) -> Dict[str, Any]:
        """Obtener datos para el dashboard del ecosistema"""
        
        # Estadísticas de bots
        telegram_stats = self.telegram_manager.get_bot_stats()
        
        # Estadísticas de GPTs
        gpt_stats = self.gpt_system.get_gpt_stats()
        
        # Estadísticas de IA médica
        medical_ai_stats = self.medical_ai.get_model_stats()
        
        # Categorías de bots
        bot_categories = {}
        for bot in self.telegram_manager.bots.values():
            if bot.category not in bot_categories:
                bot_categories[bot.category] = 0
            bot_categories[bot.category] += 1
        
        return {
            "timestamp": datetime.now().isoformat(),
            "company": {
                "name": "Panacea Icono S.A.",
                "location": "Santa Cruz de la Sierra, Bolivia",
                "phone": "+591 69674560",
                "email": "repositorios.panacea@gmail.com"
            },
            "telegram_bots": {
                "total": telegram_stats['total_bots'],
                "active": telegram_stats['active_bots'],
                "categories": bot_categories,
                "error_rate": (telegram_stats['error_bots'] / telegram_stats['total_bots']) * 100 if telegram_stats['total_bots'] > 0 else 0
            },
            "gpt_system": {
                "total": gpt_stats['total_gpts'],
                "active": gpt_stats['active_gpts'],
                "categories": gpt_stats['categories'],
                "total_usage": gpt_stats['total_usage']
            },
            "medical_ai": {
                "total_models": medical_ai_stats['total_models'],
                "available": medical_ai_stats['available_models'],
                "categories": medical_ai_stats['categories'],
                "api_configured": medical_ai_stats['api_key_configured']
            },
            "overall_health": self._calculate_overall_health(telegram_stats, gpt_stats, medical_ai_stats)
        }
    
    def _calculate_overall_health(self, telegram_stats: Dict, gpt_stats: Dict, medical_ai_stats: Dict) -> str:
        """Calcular salud general del ecosistema"""
        
        total_components = (
            telegram_stats['total_bots'] + 
            gpt_stats['total_gpts'] + 
            medical_ai_stats['total_models']
        )
        
        active_components = (
            telegram_stats['active_bots'] + 
            gpt_stats['active_gpts'] + 
            medical_ai_stats['available_models']
        )
        
        if total_components == 0:
            return "unknown"
        
        health_percentage = (active_components / total_components) * 100
        
        if health_percentage >= 90:
            return "excellent"
        elif health_percentage >= 75:
            return "good"
        elif health_percentage >= 50:
            return "fair"
        else:
            return "poor"

# Instancia global del ecosistema
ai_ecosystem = PanaceaAIEcosystem()

async def main():
    """Función principal para testing"""
    print("🏥 PANACEA ICONO S.A. - Ecosistema de IA Integrado")
    print("=" * 60)
    
    # Obtener estado del ecosistema
    status = await ai_ecosystem.get_ecosystem_status()
    
    print(f"📊 Estado General: {status.overall_health.upper()}")
    print(f"🔢 Componentes Totales: {status.total_components}")
    print(f"✅ Componentes Activos: {status.active_components}")
    print(f"📅 Última Actualización: {status.timestamp}")
    
    print("\n🤖 Bots de Telegram:")
    print(f"  Total: {status.telegram_bots['stats']['total_bots']}")
    print(f"  Activos: {status.telegram_bots['stats']['active_bots']}")
    print(f"  Con Error: {status.telegram_bots['stats']['error_bots']}")
    
    print("\n🧠 Sistema GPT:")
    print(f"  Total: {status.gpt_system['total_gpts']}")
    print(f"  Activos: {status.gpt_system['active_gpts']}")
    print(f"  Uso Total: {status.gpt_system['total_usage']}")
    
    print("\n🔬 IA Médica:")
    print(f"  Modelos: {status.medical_ai['total_models']}")
    print(f"  Disponibles: {status.medical_ai['available_models']}")
    print(f"  API Configurada: {status.medical_ai['api_key_configured']}")
    
    # Ejemplo de consulta médica
    print("\n🔍 Ejemplo de Consulta Médica:")
    print("-" * 40)
    
    sample_query = "Tengo dolor en el pecho y dificultad para respirar"
    result = await ai_ecosystem.process_medical_query(sample_query, "user123")
    
    print(f"Consulta: {sample_query}")
    print(f"Necesita Especialista: {result.get('needs_specialist', 'N/A')}")
    print(f"Acciones Recomendadas: {result.get('recommended_actions', [])}")

if __name__ == "__main__":
    asyncio.run(main())
