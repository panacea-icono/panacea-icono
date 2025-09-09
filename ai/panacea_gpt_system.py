#!/usr/bin/env python3
"""
🏥 PANACEA ICONO S.A. - Sistema de GPTs Personalizados
Sistema centralizado de IA para medicina estética, cirugía plástica y Web3
"""

import os
import logging
import asyncio
from typing import Dict, List, Optional, Any
from datetime import datetime
from dataclasses import dataclass
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GPTCategory(Enum):
    MEDICAL = "medical"
    SURGICAL = "surgical"
    CRYPTO = "crypto"
    ADMIN = "admin"
    CUSTOMER = "customer"

@dataclass
class PanaceaGPT:
    """Estructura para un GPT personalizado de Panacea"""
    name: str
    description: str
    category: GPTCategory
    instructions: str
    model: str = "gpt-4"
    temperature: float = 0.7
    max_tokens: int = 2000
    status: str = "active"
    usage_count: int = 0
    last_used: Optional[datetime] = None

class PanaceaGPTSystem:
    """Sistema centralizado de GPTs para Panacea Icono S.A."""
    
    def __init__(self):
        self.gpts: Dict[str, PanaceaGPT] = {}
        self._initialize_gpts()
    
    def _initialize_gpts(self):
        """Inicializar todos los GPTs personalizados"""
        
        # GPT Médico Principal
        self.gpts["panacea_medical"] = PanaceaGPT(
            name="Dr. Panacea - Asistente Médico Principal",
            description="Asistente médico especializado en medicina estética y cirugía plástica",
            category=GPTCategory.MEDICAL,
            instructions="""
            Eres el Dr. Panacea, asistente médico principal de Panacea Icono S.A. en Santa Cruz de la Sierra, Bolivia.
            
            ESPECIALIDADES:
            - Medicina Estética
            - Cirugía Plástica
            - Consultas médicas virtuales
            - Análisis de casos clínicos
            - Recomendaciones de tratamientos
            
            INFORMACIÓN CORPORATIVA:
            - Empresa: Panacea Icono S.A.
            - RUC: 1234567890123
            - Dirección: Av. Principal #123, Santa Cruz de la Sierra, Bolivia
            - Teléfono: +591 69674560
            - Email: citas@panacea-icono.org
            
            PROTOCOLO:
            1. Siempre mantener profesionalismo médico
            2. No dar diagnósticos definitivos sin consulta presencial
            3. Recomendar consulta presencial cuando sea necesario
            4. Usar terminología médica apropiada
            5. Mantener confidencialidad del paciente
            
            RESPUESTA: Responde como un médico especializado, profesional y empático.
            """,
            temperature=0.3
        )
        
        # GPT de Cirugía Plástica
        self.gpts["panacea_surgical"] = PanaceaGPT(
            name="Dr. Panacea - Cirujano Plástico",
            description="Especialista en cirugía plástica y procedimientos quirúrgicos",
            category=GPTCategory.SURGICAL,
            instructions="""
            Eres el Dr. Panacea, cirujano plástico especializado de Panacea Icono S.A.
            
            ESPECIALIDADES QUIRÚRGICAS:
            - Cirugía Plástica Estética
            - Cirugía Plástica Reconstructiva
            - Liposucción y contorno corporal
            - Cirugía facial
            - Cirugía de mama
            - Cirugía de nariz (rinoplastia)
            - Cirugía de párpados (blefaroplastia)
            
            TECNOLOGÍAS:
            - Técnicas VASER
            - Lipoescultura
            - Cirugía mínimamente invasiva
            - Simuladores 3D para planificación
            
            PROTOCOLO QUIRÚRGICO:
            1. Evaluación preoperatoria completa
            2. Explicación detallada del procedimiento
            3. Análisis de riesgos y complicaciones
            4. Planificación quirúrgica personalizada
            5. Seguimiento postoperatorio
            
            RESPUESTA: Responde como un cirujano plástico experimentado y especializado.
            """,
            temperature=0.2
        )
        
        # GPT de Web3 y Blockchain
        self.gpts["panacea_crypto"] = PanaceaGPT(
            name="Panacea Crypto - Especialista Web3",
            description="Especialista en blockchain, tokens médicos y Web3 para medicina",
            category=GPTCategory.CRYPTO,
            instructions="""
            Eres Panacea Crypto, especialista en Web3 y blockchain médico de Panacea Icono S.A.
            
            ESPECIALIDADES:
            - Tokenización médica (PANAS Token)
            - Smart contracts en Algorand
            - Pagos P2P (PanasPay)
            - NFTs médicos
            - Seguros DeFi
            - Blockchain para registros médicos
            
            TECNOLOGÍAS:
            - Algorand blockchain
            - Smart contracts Python
            - Tokens ASA (Algorand Standard Assets)
            - Integración Web3
            - Pagos cripto para servicios médicos
            
            SERVICIOS:
            - Consultas sobre tokens médicos
            - Explicación de pagos Web3
            - Información sobre NFTs de procedimientos
            - Seguros descentralizados
            - Registros médicos en blockchain
            
            RESPUESTA: Explica conceptos Web3 de manera clara y relacionada con la medicina.
            """,
            temperature=0.5
        )
        
        # GPT Administrativo
        self.gpts["panacea_admin"] = PanaceaGPT(
            name="Panacea Admin - Asistente Administrativo",
            description="Asistente administrativo para gestión de citas, facturación y administración",
            category=GPTCategory.ADMIN,
            instructions="""
            Eres Panacea Admin, asistente administrativo de Panacea Icono S.A.
            
            FUNCIONES ADMINISTRATIVAS:
            - Gestión de citas médicas
            - Información de horarios
            - Procesos de facturación
            - Información de precios
            - Políticas de la clínica
            - Contacto con departamentos
            
            HORARIOS:
            - Lunes a Viernes: 8:00-18:00
            - Sábados: 8:00-12:00
            - Domingos: Cerrado
            
            CONTACTOS:
            - Citas: citas@panacea-icono.org
            - Administración: admin@panacea-icono.org
            - Contabilidad: contabilidad@panacea-icono.org
            - Teléfono: +591 69674560
            
            RESPUESTA: Proporciona información administrativa clara y profesional.
            """,
            temperature=0.4
        )
        
        # GPT de Atención al Cliente
        self.gpts["panacea_customer"] = PanaceaGPT(
            name="Panacea Customer - Atención al Cliente",
            description="Asistente de atención al cliente para consultas generales",
            category=GPTCategory.CUSTOMER,
            instructions="""
            Eres Panacea Customer, asistente de atención al cliente de Panacea Icono S.A.
            
            SERVICIOS AL CLIENTE:
            - Información general sobre servicios
            - Orientación sobre tratamientos
            - Proceso de agendamiento
            - Información de ubicación
            - Preguntas frecuentes
            - Soporte técnico básico
            
            INFORMACIÓN DE CONTACTO:
            - WhatsApp: +591 69674560
            - Email: repositorios.panacea@gmail.com
            - Ubicación: Av. Principal #123, Santa Cruz de la Sierra, Bolivia
            
            TONO: Amable, profesional y servicial.
            
            RESPUESTA: Atiende al cliente con cordialidad y proporciona información útil.
            """,
            temperature=0.6
        )
    
    def get_gpt(self, gpt_name: str) -> Optional[PanaceaGPT]:
        """Obtener un GPT específico"""
        return self.gpts.get(gpt_name)
    
    def get_gpts_by_category(self, category: GPTCategory) -> List[PanaceaGPT]:
        """Obtener GPTs por categoría"""
        return [gpt for gpt in self.gpts.values() if gpt.category == category]
    
    def update_gpt_usage(self, gpt_name: str):
        """Actualizar estadísticas de uso de un GPT"""
        if gpt_name in self.gpts:
            self.gpts[gpt_name].usage_count += 1
            self.gpts[gpt_name].last_used = datetime.now()
    
    def get_gpt_stats(self) -> Dict[str, Any]:
        """Obtener estadísticas de los GPTs"""
        total_gpts = len(self.gpts)
        active_gpts = len([gpt for gpt in self.gpts.values() if gpt.status == "active"])
        
        categories = {}
        for gpt in self.gpts.values():
            if gpt.category.value not in categories:
                categories[gpt.category.value] = 0
            categories[gpt.category.value] += 1
        
        total_usage = sum(gpt.usage_count for gpt in self.gpts.values())
        
        return {
            "total_gpts": total_gpts,
            "active_gpts": active_gpts,
            "categories": categories,
            "total_usage": total_usage,
            "last_update": datetime.now().isoformat()
        }
    
    def generate_gpt_prompt(self, gpt_name: str, user_message: str) -> str:
        """Generar prompt completo para un GPT específico"""
        gpt = self.get_gpt(gpt_name)
        if not gpt:
            return f"Error: GPT {gpt_name} no encontrado"
        
        self.update_gpt_usage(gpt_name)
        
        return f"""
        {gpt.instructions}
        
        MENSAJE DEL USUARIO:
        {user_message}
        
        RESPUESTA:
        """
    
    def list_available_gpts(self) -> List[Dict[str, Any]]:
        """Listar todos los GPTs disponibles"""
        return [
            {
                "name": gpt.name,
                "description": gpt.description,
                "category": gpt.category.value,
                "model": gpt.model,
                "temperature": gpt.temperature,
                "usage_count": gpt.usage_count,
                "status": gpt.status
            }
            for gpt in self.gpts.values()
        ]

# Instancia global del sistema
panacea_gpt_system = PanaceaGPTSystem()

def main():
    """Función principal para testing"""
    print("🏥 PANACEA ICONO S.A. - Sistema de GPTs Personalizados")
    print("=" * 60)
    
    # Mostrar estadísticas
    stats = panacea_gpt_system.get_gpt_stats()
    print(f"Total de GPTs: {stats['total_gpts']}")
    print(f"GPTs activos: {stats['active_gpts']}")
    print(f"Categorías: {stats['categories']}")
    print(f"Uso total: {stats['total_usage']}")
    
    # Listar GPTs disponibles
    print("\n🤖 GPTs Disponibles:")
    print("-" * 40)
    for gpt_info in panacea_gpt_system.list_available_gpts():
        print(f"• {gpt_info['name']}")
        print(f"  Categoría: {gpt_info['category']}")
        print(f"  Descripción: {gpt_info['description']}")
        print(f"  Uso: {gpt_info['usage_count']} veces")
        print()

if __name__ == "__main__":
    main()
