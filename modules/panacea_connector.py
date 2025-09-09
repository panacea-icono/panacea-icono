#!/usr/bin/env python3
"""
PANACEA ICONO S.A. - Conector Base del Ecosistema
Conector central para la comunicación entre todos los módulos del ecosistema
"""

import asyncio
import aiohttp
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
import json
import os

@dataclass
class ModuleConfig:
    """Configuración de un módulo del ecosistema"""
    name: str
    url: str
    api_key: str
    status: str = "unknown"
    last_check: Optional[datetime] = None

class PanaceaConnector:
    """Conector base para todos los módulos del ecosistema Panacea"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.modules = {}
        self.session = None
        self._load_config()
    
    def _load_config(self):
        """Cargar configuración de módulos desde variables de entorno"""
        self.modules = {
            "smart_contracts": ModuleConfig(
                name="Smart Contracts",
                url=os.getenv("SMART_CONTRACTS_URL", "http://localhost:8001"),
                api_key=os.getenv("SMART_CONTRACTS_API_KEY", "")
            ),
            "variables": ModuleConfig(
                name="Variables (GPT Auditor)",
                url=os.getenv("VARIABLES_URL", "http://localhost:8002"),
                api_key=os.getenv("VARIABLES_API_KEY", "")
            ),
            "auditor": ModuleConfig(
                name="Ecosystem Auditor",
                url=os.getenv("AUDITOR_URL", "http://localhost:8003"),
                api_key=os.getenv("AUDITOR_API_KEY", "")
            ),
            "fibonacci": ModuleConfig(
                name="Fibonacci Medical APIs",
                url=os.getenv("FIBONACCI_URL", "http://localhost:8004"),
                api_key=os.getenv("FIBONACCI_API_KEY", "")
            )
        }
    
    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
    
    async def check_module_health(self, module_name: str) -> Dict[str, Any]:
        """Verificar salud de un módulo específico"""
        if module_name not in self.modules:
            return {"error": f"Módulo {module_name} no encontrado"}
        
        module = self.modules[module_name]
        try:
            async with self.session.get(f"{module.url}/health") as response:
                if response.status == 200:
                    module.status = "healthy"
                    data = await response.json()
                    module.last_check = datetime.now()
                    return {
                        "module": module_name,
                        "status": "healthy",
                        "data": data,
                        "timestamp": module.last_check.isoformat()
                    }
                else:
                    module.status = "unhealthy"
                    return {
                        "module": module_name,
                        "status": "unhealthy",
                        "error": f"HTTP {response.status}",
                        "timestamp": datetime.now().isoformat()
                    }
        except Exception as e:
            module.status = "error"
            return {
                "module": module_name,
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    async def check_all_modules(self) -> Dict[str, Any]:
        """Verificar salud de todos los módulos"""
        results = {}
        tasks = []
        
        for module_name in self.modules:
            task = asyncio.create_task(self.check_module_health(module_name))
            tasks.append((module_name, task))
        
        for module_name, task in tasks:
            try:
                result = await task
                results[module_name] = result
            except Exception as e:
                results[module_name] = {
                    "module": module_name,
                    "status": "error",
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                }
        
        return results
    
    async def send_command(self, module_name: str, command: str, data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Enviar comando a un módulo específico"""
        if module_name not in self.modules:
            return {"error": f"Módulo {module_name} no encontrado"}
        
        module = self.modules[module_name]
        payload = {
            "command": command,
            "data": data or {},
            "timestamp": datetime.now().isoformat()
        }
        
        try:
            headers = {"Authorization": f"Bearer {module.api_key}"} if module.api_key else {}
            async with self.session.post(
                f"{module.url}/api/command",
                json=payload,
                headers=headers
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    return {
                        "error": f"HTTP {response.status}",
                        "details": await response.text()
                    }
        except Exception as e:
            return {"error": str(e)}
    
    async def get_ecosystem_status(self) -> Dict[str, Any]:
        """Obtener estado completo del ecosistema"""
        health_check = await self.check_all_modules()
        
        # Contar módulos por estado
        status_counts = {}
        for result in health_check.values():
            status = result.get("status", "unknown")
            status_counts[status] = status_counts.get(status, 0) + 1
        
        return {
            "timestamp": datetime.now().isoformat(),
            "total_modules": len(self.modules),
            "status_counts": status_counts,
            "modules": health_check,
            "overall_status": "healthy" if status_counts.get("error", 0) == 0 else "degraded"
        }
    
    async def orchestrate_workflow(self, workflow_name: str, parameters: Dict[str, Any] = None) -> Dict[str, Any]:
        """Orquestar un workflow entre múltiples módulos"""
        workflows = {
            "audit_ecosystem": {
                "steps": [
                    ("variables", "start_audit", {"scope": "full"}),
                    ("smart_contracts", "audit_contracts", {}),
                    ("auditor", "analyze_results", {}),
                    ("variables", "generate_report", {})
                ]
            },
            "deploy_update": {
                "steps": [
                    ("smart_contracts", "validate_contracts", {}),
                    ("auditor", "security_check", {}),
                    ("variables", "deploy_notification", {}),
                    ("auditor", "monitor_deployment", {})
                ]
            },
            "medical_analysis": {
                "steps": [
                    ("fibonacci", "load_medical_data", {}),
                    ("variables", "ai_analysis", {}),
                    ("auditor", "validate_results", {}),
                    ("variables", "generate_medical_report", {})
                ]
            }
        }
        
        if workflow_name not in workflows:
            return {"error": f"Workflow {workflow_name} no encontrado"}
        
        workflow = workflows[workflow_name]
        results = []
        
        for module_name, command, data in workflow["steps"]:
            # Mergear parámetros del workflow con datos del paso
            step_data = {**(data or {}), **(parameters or {})}
            result = await self.send_command(module_name, command, step_data)
            results.append({
                "module": module_name,
                "command": command,
                "result": result
            })
            
            # Si hay error, detener el workflow
            if "error" in result:
                return {
                    "workflow": workflow_name,
                    "status": "failed",
                    "step": len(results),
                    "results": results
                }
        
        return {
            "workflow": workflow_name,
            "status": "completed",
            "steps": len(results),
            "results": results
        }

async def main():
    """Función principal para testing del conector"""
    print("🔗 PANACEA ECOSYSTEM CONNECTOR")
    print("=" * 40)
    
    async with PanaceaConnector() as connector:
        # Verificar estado del ecosistema
        print("\n📊 Estado del Ecosistema:")
        status = await connector.get_ecosystem_status()
        print(f"Estado General: {status['overall_status']}")
        print(f"Módulos Totales: {status['total_modules']}")
        
        for module, result in status['modules'].items():
            print(f"  {module}: {result['status']}")
        
        # Ejecutar workflow de auditoría
        print("\n🔍 Ejecutando Auditoría del Ecosistema:")
        audit_result = await connector.orchestrate_workflow("audit_ecosystem")
        print(f"Workflow: {audit_result['status']}")
        print(f"Pasos ejecutados: {audit_result.get('steps', 0)}")

if __name__ == "__main__":
    asyncio.run(main())
