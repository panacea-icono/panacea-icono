#!/usr/bin/env python3
"""
🏥 PANACEA ICONO S.A. - Aplicación Principal Integrada
FastAPI application con integración completa del ecosistema
"""

import os
import logging
import asyncio
from typing import Dict, Any, Optional, List
from pathlib import Path
from datetime import datetime

from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
import uvicorn

# Importar módulos del ecosistema
from modules.panacea_connector import PanaceaConnector
from integrations.github_integration import GitHubIntegration
from integrations.heroku_integration import HerokuIntegration

# Importar sistemas de IA
from ai.panacea_ai_ecosystem import ai_ecosystem
from ai.panacea_gpt_system import panacea_gpt_system
from ai.huggingface_medical_ai import medical_ai
from bots.telegram_bots_manager import telegram_manager

# Import Hugging Face manager
try:
    from huggingface_config import HuggingFaceManager
    HF_MANAGER_AVAILABLE = True
except ImportError:
    HuggingFaceManager = None
    HF_MANAGER_AVAILABLE = False

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="🏥 PANACEA ICONO S.A. - ECOSYSTEM HUB",
    description="Hub central del ecosistema Panacea Icono S.A. - Medicina Estética, Cirugía Plástica, IA y Web3",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    contact={
        "name": "Panacea Icono S.A.",
        "url": "https://panacea-icono.org",
        "email": "repositorios.panacea@gmail.com",
    },
    license_info={
        "name": "Proprietary",
        "url": "https://panacea-icono.org/legal",
    }
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/assets", StaticFiles(directory="public/assets"), name="assets")

# Pydantic models
class EcosystemStatus(BaseModel):
    timestamp: str
    overall_status: str
    total_modules: int
    status_counts: Dict[str, int]
    modules: Dict[str, Any]

class WorkflowRequest(BaseModel):
    workflow_name: str
    parameters: Optional[Dict[str, Any]] = None

class CommandRequest(BaseModel):
    module_name: str
    command: str
    data: Optional[Dict[str, Any]] = None

class GitHubAnalysis(BaseModel):
    timestamp: str
    summary: Dict[str, Any]
    categories: Dict[str, Any]
    most_active: List[Dict[str, Any]]
    most_popular: List[Dict[str, Any]]

class HerokuDeployment(BaseModel):
    timestamp: str
    summary: Dict[str, Any]
    categories: Dict[str, Any]
    applications: List[Dict[str, Any]]

# Global variables for managers
panacea_connector = None
github_integration = None
heroku_integration = None
hf_manager = None

@app.on_event("startup")
async def startup_event():
    """Inicializar integraciones al arrancar la aplicación"""
    global panacea_connector, github_integration, heroku_integration, hf_manager
    
    logger.info("🚀 Iniciando PANACEA ICONO S.A. Ecosystem Hub...")
    
    # Inicializar conector principal
    panacea_connector = PanaceaConnector()
    
    # Inicializar integraciones
    github_integration = GitHubIntegration()
    heroku_integration = HerokuIntegration()
    
    # Inicializar Hugging Face si está disponible
    if HF_MANAGER_AVAILABLE:
        hf_manager = HuggingFaceManager()
        logger.info("✅ Hugging Face Manager inicializado")
    
    logger.info("✅ Ecosystem Hub iniciado correctamente")

@app.on_event("shutdown")
async def shutdown_event():
    """Limpiar recursos al cerrar la aplicación"""
    global panacea_connector, github_integration, heroku_integration
    
    logger.info("🛑 Cerrando PANACEA ICONO S.A. Ecosystem Hub...")
    
    if panacea_connector:
        await panacea_connector.__aexit__(None, None, None)
    if github_integration:
        await github_integration.__aexit__(None, None, None)
    if heroku_integration:
        await heroku_integration.__aexit__(None, None, None)
    
    logger.info("✅ Ecosystem Hub cerrado correctamente")

# Root endpoint
@app.get("/", response_class=HTMLResponse)
async def root():
    """Página principal del ecosistema"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>🏥 PANACEA ICONO S.A. - Ecosystem Hub</title>
        <link rel="icon" type="image/svg+xml" href="/assets/icon-favicon.svg">
        <meta charset="utf-8">
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
            .container { max-width: 1200px; margin: 0 auto; background: white; padding: 40px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            h1 { color: #2c3e50; text-align: center; }
            .modules { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin: 30px 0; }
            .module { background: #ecf0f1; padding: 20px; border-radius: 8px; border-left: 4px solid #3498db; }
            .module h3 { color: #2c3e50; margin-top: 0; }
            .status { display: inline-block; padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: bold; }
            .status.healthy { background: #d5f4e6; color: #27ae60; }
            .status.degraded { background: #fef9e7; color: #f39c12; }
            .status.error { background: #fadbd8; color: #e74c3c; }
            .links { text-align: center; margin: 30px 0; }
            .links a { display: inline-block; margin: 10px; padding: 10px 20px; background: #3498db; color: white; text-decoration: none; border-radius: 5px; }
            .links a:hover { background: #2980b9; }
        </style>
    </head>
    <body>
        <div class="container">
            <div style="text-align: center; margin-bottom: 30px;">
                <img src="/assets/logo-panacea.svg" alt="Panacea Icono S.A. Logo" style="width: 100px; height: 100px; margin-bottom: 20px;">
            </div>
            <h1>🏥 PANACEA ICONO S.A.</h1>
            <h2>Ecosystem Hub - Centro de Control del Ecosistema</h2>
            <p><strong>📍 Ubicación:</strong> Santa Cruz de la Sierra, Bolivia</p>
            <p><strong>📞 Contacto:</strong> +591 69674560 | repositorios.panacea@gmail.com</p>
            <p><strong>🏥 Especialidad:</strong> Medicina Estética, Cirugía Plástica, IA y Web3</p>
            
            <div class="modules">
                <div class="module">
                    <h3>🔗 Conector Principal</h3>
                    <p>Gestión centralizada de todos los módulos del ecosistema</p>
                    <span class="status healthy">ACTIVO</span>
                </div>
                
                <div class="module">
                    <h3>📄 Smart Contracts</h3>
                    <p>Contratos inteligentes para el ecosistema PANAS</p>
                    <span class="status healthy">ACTIVO</span>
                </div>
                
                <div class="module">
                    <h3>🤖 Variables (GPT Auditor)</h3>
                    <p>Sistema de auditoría con IA para todo el ecosistema</p>
                    <span class="status healthy">ACTIVO</span>
                </div>
                
                <div class="module">
                    <h3>🔍 Auditor del Ecosistema</h3>
                    <p>Monitoreo y auditoría de despliegues y roadmap</p>
                    <span class="status healthy">ACTIVO</span>
                </div>
                
                <div class="module">
                    <h3>🐙 GitHub Integration</h3>
                    <p>Gestión y monitoreo de repositorios</p>
                    <span class="status healthy">ACTIVO</span>
                </div>
                
                <div class="module">
                    <h3>🚀 Heroku Integration</h3>
                    <p>Gestión y monitoreo de aplicaciones desplegadas</p>
                    <span class="status healthy">ACTIVO</span>
                </div>
            </div>
            
            <div class="links">
                <a href="/docs">📚 API Documentation</a>
                <a href="/ecosystem/status">📊 Estado del Ecosistema</a>
                <a href="/github/analysis">🐙 Análisis GitHub</a>
                <a href="/heroku/deployment">🚀 Estado Heroku</a>
                <a href="/workflows">⚙️ Workflows</a>
            </div>
        </div>
    </body>
    </html>
    """

# Health check
@app.get("/health")
async def health_check():
    """Verificar salud de la aplicación"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "2.0.0",
        "ecosystem": "PANACEA ICONO S.A."
    }

# Ecosystem status
@app.get("/ecosystem/status", response_model=EcosystemStatus)
async def get_ecosystem_status():
    """Obtener estado completo del ecosistema"""
    try:
        async with PanaceaConnector() as connector:
            status = await connector.get_ecosystem_status()
            return EcosystemStatus(**status)
    except Exception as e:
        logger.error(f"Error obteniendo estado del ecosistema: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# GitHub analysis
@app.get("/github/analysis", response_model=GitHubAnalysis)
async def get_github_analysis():
    """Obtener análisis completo de GitHub"""
    try:
        async with GitHubIntegration() as github:
            analysis = await github.analyze_ecosystem_health()
            return GitHubAnalysis(**analysis)
    except Exception as e:
        logger.error(f"Error en análisis de GitHub: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Heroku deployment status
@app.get("/heroku/deployment", response_model=HerokuDeployment)
async def get_heroku_deployment():
    """Obtener estado de despliegue en Heroku"""
    try:
        async with HerokuIntegration() as heroku:
            deployment = await heroku.analyze_ecosystem_deployment()
            return HerokuDeployment(**deployment)
    except Exception as e:
        logger.error(f"Error en análisis de Heroku: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Execute workflow
@app.post("/workflows/execute")
async def execute_workflow(request: WorkflowRequest, background_tasks: BackgroundTasks):
    """Ejecutar un workflow del ecosistema"""
    try:
        async with PanaceaConnector() as connector:
            result = await connector.orchestrate_workflow(
                request.workflow_name,
                request.parameters
            )
            return result
    except Exception as e:
        logger.error(f"Error ejecutando workflow {request.workflow_name}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Send command to module
@app.post("/modules/command")
async def send_module_command(request: CommandRequest):
    """Enviar comando a un módulo específico"""
    try:
        async with PanaceaConnector() as connector:
            result = await connector.send_command(
                request.module_name,
                request.command,
                request.data
            )
            return result
    except Exception as e:
        logger.error(f"Error enviando comando a {request.module_name}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Monitor specific repository
@app.get("/github/repo/{repo_name}")
async def monitor_repository(repo_name: str):
    """Monitorear un repositorio específico"""
    try:
        async with GitHubIntegration() as github:
            result = await github.monitor_repo_changes(repo_name)
            return result
    except Exception as e:
        logger.error(f"Error monitoreando repositorio {repo_name}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Monitor specific Heroku app
@app.get("/heroku/app/{app_name}")
async def monitor_heroku_app(app_name: str):
    """Monitorear una aplicación Heroku específica"""
    try:
        async with HerokuIntegration() as heroku:
            result = await heroku.monitor_app_health(app_name)
            return result
    except Exception as e:
        logger.error(f"Error monitoreando app Heroku {app_name}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Available workflows
@app.get("/workflows")
async def list_workflows():
    """Listar workflows disponibles"""
    workflows = {
        "audit_ecosystem": {
            "name": "Auditoría del Ecosistema",
            "description": "Ejecutar auditoría completa de todo el ecosistema",
            "steps": ["Variables", "Smart Contracts", "Auditor", "Reporte"]
        },
        "deploy_update": {
            "name": "Despliegue de Actualización",
            "description": "Desplegar actualización con validaciones de seguridad",
            "steps": ["Validar Contratos", "Verificar Seguridad", "Notificar", "Monitorear"]
        },
        "medical_analysis": {
            "name": "Análisis Médico",
            "description": "Análisis médico con IA usando datos de Fibonacci",
            "steps": ["Cargar Datos", "Análisis IA", "Validar", "Generar Reporte"]
        }
    }
    return workflows

# Webhook placeholder (p. ej., Telegram/externo)
@app.post("/webhook/{source}")
async def webhook_handler(source: str, request: Request):
    """Webhook genérico de entrada. Guarda evento y responde 200.
    Solo esqueleto; validación/firmas se agregan luego.
    """
    try:
        payload = await request.json()
    except Exception:
        payload = {"raw": (await request.body()).decode(errors="ignore")}

    logger.info(f"📥 Webhook recibido de {source}: {str(payload)[:500]}")
    return {"status": "received", "source": source, "timestamp": datetime.now().isoformat()}

# ===== ENDPOINTS DE IA Y BOTS =====

@app.get("/ai/ecosystem/status")
async def get_ai_ecosystem_status():
    """Obtener estado completo del ecosistema de IA"""
    try:
        status = await ai_ecosystem.get_ecosystem_status()
        return {
            "status": "success",
            "data": {
                "timestamp": status.timestamp,
                "overall_health": status.overall_health,
                "total_components": status.total_components,
                "active_components": status.active_components,
                "telegram_bots": status.telegram_bots,
                "gpt_system": status.gpt_system,
                "medical_ai": status.medical_ai
            }
        }
    except Exception as e:
        logger.error(f"Error obteniendo estado del ecosistema de IA: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ai/medical/query")
async def process_medical_query(query: str, user_id: str = None):
    """Procesar consulta médica usando el ecosistema de IA"""
    try:
        result = await ai_ecosystem.process_medical_query(query, user_id)
        return {"status": "success", "data": result}
    except Exception as e:
        logger.error(f"Error procesando consulta médica: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/ai/gpts")
async def list_available_gpts():
    """Listar GPTs disponibles"""
    try:
        gpts = panacea_gpt_system.list_available_gpts()
        return {"status": "success", "data": gpts}
    except Exception as e:
        logger.error(f"Error listando GPTs: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/ai/models")
async def list_medical_models():
    """Listar modelos de IA médica disponibles"""
    try:
        models = medical_ai.list_available_models()
        return {"status": "success", "data": models}
    except Exception as e:
        logger.error(f"Error listando modelos médicos: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/bots/telegram/status")
async def get_telegram_bots_status():
    """Obtener estado de todos los bots de Telegram"""
    try:
        health_results = await telegram_manager.check_all_bots_health()
        stats = telegram_manager.get_bot_stats()
        return {
            "status": "success",
            "data": {
                "health_results": health_results,
                "stats": stats
            }
        }
    except Exception as e:
        logger.error(f"Error obteniendo estado de bots de Telegram: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/bots/telegram/send")
async def send_telegram_message(bot_name: str, chat_id: str, message: str):
    """Enviar mensaje a través de un bot de Telegram específico"""
    try:
        result = await telegram_manager.send_message(bot_name, chat_id, message)
        return {"status": "success", "data": result}
    except Exception as e:
        logger.error(f"Error enviando mensaje de Telegram: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/ai/dashboard")
async def get_ai_dashboard():
    """Obtener datos para el dashboard de IA"""
    try:
        dashboard_data = ai_ecosystem.get_ecosystem_dashboard_data()
        return {"status": "success", "data": dashboard_data}
    except Exception as e:
        logger.error(f"Error obteniendo datos del dashboard de IA: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Hugging Face models (if available)
@app.get("/huggingface/models")
async def get_hf_models():
    """Obtener modelos de Hugging Face disponibles"""
    if not HF_MANAGER_AVAILABLE or not hf_manager:
        raise HTTPException(status_code=503, detail="Hugging Face Manager no disponible")
    
    try:
        models = hf_manager.list_models()
        return {"models": models}
    except Exception as e:
        logger.error(f"Error obteniendo modelos HF: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Dashboard data
@app.get("/dashboard")
async def get_dashboard_data():
    """Obtener datos para el dashboard principal"""
    try:
        # Obtener datos de todos los servicios en paralelo
        tasks = []
        
        # Estado del ecosistema
        tasks.append(("ecosystem", get_ecosystem_status()))
        
        # Análisis de GitHub
        tasks.append(("github", get_github_analysis()))
        
        # Estado de Heroku
        tasks.append(("heroku", get_heroku_deployment()))
        
        # Ejecutar en paralelo
        results = {}
        for name, task in tasks:
            try:
                if asyncio.iscoroutine(task):
                    results[name] = await task
                else:
                    results[name] = task
            except Exception as e:
                results[name] = {"error": str(e)}
        
        return {
            "timestamp": datetime.now().isoformat(),
            "data": results
        }
    except Exception as e:
        logger.error(f"Error obteniendo datos del dashboard: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # Configurar variables de entorno
    os.environ.setdefault("SMART_CONTRACTS_URL", "http://localhost:8001")
    os.environ.setdefault("VARIABLES_URL", "http://localhost:8002")
    os.environ.setdefault("AUDITOR_URL", "http://localhost:8003")
    os.environ.setdefault("FIBONACCI_URL", "http://localhost:8004")
    
    # Ejecutar aplicación
    uvicorn.run(
        "main_integrated:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
