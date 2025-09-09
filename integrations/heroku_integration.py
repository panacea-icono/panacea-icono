#!/usr/bin/env python3
"""
PANACEA ICONO S.A. - Integración con Heroku
Gestión y monitoreo de aplicaciones desplegadas en Heroku
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
class HerokuApp:
    """Información de una aplicación Heroku"""
    id: str
    name: str
    region: str
    stack: str
    state: str
    web_url: str
    created_at: str
    updated_at: str
    git_url: str
    repo_size: Optional[int] = None
    slug_size: Optional[int] = None

@dataclass
class HerokuDyno:
    """Información de un dyno de Heroku"""
    id: str
    name: str
    app_id: str
    state: str
    type: str
    size: str
    command: str
    created_at: str
    updated_at: str

class HerokuIntegration:
    """Integración con Heroku para el ecosistema Panacea"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.api_base = "https://api.heroku.com"
        self.token = os.getenv("HEROKU_API_TOKEN")
        self.session = None
        
        if not self.token:
            self.logger.warning("HEROKU_API_TOKEN no configurado")
    
    async def __aenter__(self):
        """Async context manager entry"""
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.heroku+json; version=3",
            "Content-Type": "application/json"
        }
        
        self.session = aiohttp.ClientSession(headers=headers)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
    
    async def get_apps(self) -> List[HerokuApp]:
        """Obtener todas las aplicaciones Heroku"""
        apps = []
        
        try:
            async with self.session.get(f"{self.api_base}/apps") as response:
                if response.status == 200:
                    data = await response.json()
                    for app_data in data:
                        app = HerokuApp(
                            id=app_data["id"],
                            name=app_data["name"],
                            region=app_data["region"]["name"],
                            stack=app_data["stack"]["name"],
                            state=app_data["state"],
                            web_url=app_data["web_url"],
                            created_at=app_data["created_at"],
                            updated_at=app_data["updated_at"],
                            git_url=app_data["git_url"],
                            repo_size=app_data.get("repo_size"),
                            slug_size=app_data.get("slug_size")
                        )
                        apps.append(app)
                else:
                    self.logger.error(f"Error obteniendo apps: HTTP {response.status}")
        except Exception as e:
            self.logger.error(f"Error en get_apps: {e}")
        
        return apps
    
    async def get_app_details(self, app_name: str) -> Optional[Dict[str, Any]]:
        """Obtener detalles específicos de una aplicación"""
        try:
            async with self.session.get(f"{self.api_base}/apps/{app_name}") as response:
                if response.status == 200:
                    return await response.json()
                else:
                    self.logger.error(f"Error obteniendo app {app_name}: HTTP {response.status}")
                    return None
        except Exception as e:
            self.logger.error(f"Error en get_app_details: {e}")
            return None
    
    async def get_app_dynos(self, app_name: str) -> List[HerokuDyno]:
        """Obtener dynos de una aplicación"""
        dynos = []
        
        try:
            async with self.session.get(f"{self.api_base}/apps/{app_name}/dynos") as response:
                if response.status == 200:
                    data = await response.json()
                    for dyno_data in data:
                        dyno = HerokuDyno(
                            id=dyno_data["id"],
                            name=dyno_data["name"],
                            app_id=dyno_data["app"]["id"],
                            state=dyno_data["state"],
                            type=dyno_data["type"],
                            size=dyno_data["size"],
                            command=dyno_data["command"],
                            created_at=dyno_data["created_at"],
                            updated_at=dyno_data["updated_at"]
                        )
                        dynos.append(dyno)
                else:
                    self.logger.error(f"Error obteniendo dynos de {app_name}: HTTP {response.status}")
        except Exception as e:
            self.logger.error(f"Error en get_app_dynos: {e}")
        
        return dynos
    
    async def get_app_logs(self, app_name: str, lines: int = 100) -> List[str]:
        """Obtener logs de una aplicación"""
        try:
            url = f"{self.api_base}/apps/{app_name}/log-sessions"
            payload = {"lines": lines}
            
            async with self.session.post(url, json=payload) as response:
                if response.status == 201:
                    data = await response.json()
                    log_url = data.get("logplex_url")
                    
                    if log_url:
                        # Obtener logs desde la URL de logplex
                        async with aiohttp.ClientSession() as log_session:
                            async with log_session.get(log_url) as log_response:
                                if log_response.status == 200:
                                    log_text = await log_response.text()
                                    return log_text.split('\n')
                
                self.logger.error(f"Error obteniendo logs de {app_name}: HTTP {response.status}")
                return []
        except Exception as e:
            self.logger.error(f"Error en get_app_logs: {e}")
            return []
    
    async def get_app_config(self, app_name: str) -> Dict[str, str]:
        """Obtener variables de configuración de una aplicación"""
        try:
            async with self.session.get(f"{self.api_base}/apps/{app_name}/config-vars") as response:
                if response.status == 200:
                    return await response.json()
                else:
                    self.logger.error(f"Error obteniendo config de {app_name}: HTTP {response.status}")
                    return {}
        except Exception as e:
            self.logger.error(f"Error en get_app_config: {e}")
            return {}
    
    async def restart_app(self, app_name: str) -> bool:
        """Reiniciar una aplicación"""
        try:
            async with self.session.post(f"{self.api_base}/apps/{app_name}/dynos", json={}) as response:
                if response.status == 201:
                    return True
                else:
                    self.logger.error(f"Error reiniciando {app_name}: HTTP {response.status}")
                    return False
        except Exception as e:
            self.logger.error(f"Error en restart_app: {e}")
            return False
    
    async def scale_dynos(self, app_name: str, dyno_type: str, quantity: int) -> bool:
        """Escalar dynos de una aplicación"""
        try:
            payload = {"quantity": quantity}
            async with self.session.patch(
                f"{self.api_base}/apps/{app_name}/formation/{dyno_type}",
                json=payload
            ) as response:
                if response.status == 200:
                    return True
                else:
                    self.logger.error(f"Error escalando {app_name}: HTTP {response.status}")
                    return False
        except Exception as e:
            self.logger.error(f"Error en scale_dynos: {e}")
            return False
    
    async def analyze_ecosystem_deployment(self) -> Dict[str, Any]:
        """Analizar el estado de despliegue del ecosistema en Heroku"""
        apps = await self.get_apps()
        
        if not apps:
            return {"error": "No se pudieron obtener aplicaciones"}
        
        # Categorizar aplicaciones por nombre
        categories = {
            "panacea": [],
            "fibonacci": [],
            "panas": [],
            "smart_contracts": [],
            "other": []
        }
        
        for app in apps:
            name_lower = app.name.lower()
            if "panacea" in name_lower:
                categories["panacea"].append(app)
            elif "fibonacci" in name_lower:
                categories["fibonacci"].append(app)
            elif "panas" in name_lower:
                categories["panas"].append(app)
            elif "smart" in name_lower or "contract" in name_lower:
                categories["smart_contracts"].append(app)
            else:
                categories["other"].append(app)
        
        # Calcular métricas
        total_apps = len(apps)
        running_apps = len([app for app in apps if app.state == "running"])
        sleeping_apps = len([app for app in apps if app.state == "sleeping"])
        crashed_apps = len([app for app in apps if app.state == "crashed"])
        
        # Obtener información detallada de cada app
        app_details = []
        for app in apps:
            details = await self.get_app_details(app.name)
            dynos = await self.get_app_dynos(app.name)
            
            app_info = {
                "name": app.name,
                "state": app.state,
                "region": app.region,
                "stack": app.stack,
                "web_url": app.web_url,
                "dynos": len(dynos),
                "running_dynos": len([d for d in dynos if d.state == "up"]),
                "created_at": app.created_at,
                "updated_at": app.updated_at
            }
            
            if details:
                app_info.update({
                    "repo_size": details.get("repo_size"),
                    "slug_size": details.get("slug_size"),
                    "buildpack": details.get("buildpack_provided_description")
                })
            
            app_details.append(app_info)
        
        return {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_applications": total_apps,
                "running_applications": running_apps,
                "sleeping_applications": sleeping_apps,
                "crashed_applications": crashed_apps
            },
            "categories": {
                name: {
                    "count": len(app_list),
                    "applications": [app.name for app in app_list]
                }
                for name, app_list in categories.items()
            },
            "applications": app_details
        }
    
    async def monitor_app_health(self, app_name: str) -> Dict[str, Any]:
        """Monitorear la salud de una aplicación específica"""
        details = await self.get_app_details(app_name)
        if not details:
            return {"error": f"No se pudo obtener detalles de {app_name}"}
        
        dynos = await self.get_app_dynos(app_name)
        config = await self.get_app_config(app_name)
        logs = await self.get_app_logs(app_name, 50)
        
        # Analizar logs para errores
        error_logs = [log for log in logs if "error" in log.lower() or "exception" in log.lower()]
        warning_logs = [log for log in logs if "warning" in log.lower() or "warn" in log.lower()]
        
        return {
            "application": app_name,
            "timestamp": datetime.now().isoformat(),
            "details": {
                "state": details.get("state", ""),
                "region": details.get("region", {}).get("name", ""),
                "stack": details.get("stack", {}).get("name", ""),
                "web_url": details.get("web_url", ""),
                "created_at": details.get("created_at", ""),
                "updated_at": details.get("updated_at", "")
            },
            "dynos": {
                "total": len(dynos),
                "running": len([d for d in dynos if d.state == "up"]),
                "crashed": len([d for d in dynos if d.state == "crashed"]),
                "sleeping": len([d for d in dynos if d.state == "sleeping"]),
                "details": [
                    {
                        "name": dyno.name,
                        "type": dyno.type,
                        "size": dyno.size,
                        "state": dyno.state,
                        "command": dyno.command
                    }
                    for dyno in dynos
                ]
            },
            "configuration": {
                "total_vars": len(config),
                "variables": list(config.keys())
            },
            "logs_analysis": {
                "total_logs": len(logs),
                "error_logs": len(error_logs),
                "warning_logs": len(warning_logs),
                "recent_errors": error_logs[-5:] if error_logs else [],
                "recent_warnings": warning_logs[-5:] if warning_logs else []
            }
        }

async def main():
    """Función principal para testing de la integración"""
    print("🚀 HEROKU INTEGRATION - PANACEA ECOSYSTEM")
    print("=" * 50)
    
    async with HerokuIntegration() as heroku:
        # Analizar despliegue del ecosistema
        print("\n📊 Análisis del Despliegue:")
        deployment = await heroku.analyze_ecosystem_deployment()
        
        if "error" not in deployment:
            summary = deployment["summary"]
            print(f"Total de Aplicaciones: {summary['total_applications']}")
            print(f"Aplicaciones Ejecutándose: {summary['running_applications']}")
            print(f"Aplicaciones Durmiendo: {summary['sleeping_applications']}")
            print(f"Aplicaciones Fallidas: {summary['crashed_applications']}")
            
            print("\n📁 Categorías:")
            for category, data in deployment["categories"].items():
                print(f"  {category.title()}: {data['count']} aplicaciones")
            
            print("\n🔥 Aplicaciones Activas:")
            for app in deployment["applications"][:5]:
                print(f"  {app['name']} - {app['state']} ({app['running_dynos']}/{app['dynos']} dynos)")
        else:
            print(f"Error: {deployment['error']}")
        
        # Monitorear aplicación específica (si existe)
        apps = await heroku.get_apps()
        if apps:
            print(f"\n🔍 Monitoreo de {apps[0].name}:")
            health = await heroku.monitor_app_health(apps[0].name)
            
            if "error" not in health:
                details = health["details"]
                dynos = health["dynos"]
                logs = health["logs_analysis"]
                
                print(f"Estado: {details['state']}")
                print(f"Región: {details['region']}")
                print(f"Stack: {details['stack']}")
                print(f"Dynos: {dynos['running']}/{dynos['total']} ejecutándose")
                print(f"Variables de Configuración: {health['configuration']['total_vars']}")
                print(f"Logs Recientes: {logs['total_logs']} (Errores: {logs['error_logs']}, Warnings: {logs['warning_logs']})")
            else:
                print(f"Error: {health['error']}")

if __name__ == "__main__":
    asyncio.run(main())
