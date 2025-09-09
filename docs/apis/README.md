# 🔌 APIs DEL ECOSISTEMA PANACEA ICONO S.A.

**Fecha**: 2025-09-09
**Versión**: v2025.09.09.0302
**Empresa**: Panacea Icono S.A.

## 📋 ÍNDICE DE APIs

### **APIs Principales**
- [API Central Panacea](#api-central-panacea)
- [API de Smart Contracts](#api-de-smart-contracts)
- [API de Telegram](#api-de-telegram)
- [API de Auditoría](#api-de-auditoría)
- [API de FIBONACCI](#api-de-fibonacci)

### **APIs de Integración**
- [GitHub Integration API](#github-integration-api)
- [Heroku Integration API](#heroku-integration-api)
- [Hugging Face API](#hugging-face-api)
- [Vercel Integration API](#vercel-integration-api)

---

## 🏠 API CENTRAL PANACEA

### **Base URL**
```
https://api-panacea-638dc550fab6.herokuapp.com
```

### **Endpoints Principales**

#### **Dashboard del Ecosistema**
```http
GET /dashboard
```
**Descripción**: Dashboard principal del ecosistema
**Respuesta**: HTML del dashboard con métricas en tiempo real

#### **Estado del Ecosistema**
```http
GET /ecosystem/status
```
**Descripción**: Estado general del ecosistema
**Respuesta**:
```json
{
  "timestamp": "2025-09-09T03:02:00Z",
  "status": "healthy",
  "services": {
    "github": "active",
    "heroku": "active",
    "telegram": "active",
    "huggingface": "active"
  }
}
```

#### **Análisis de GitHub**
```http
GET /github/analysis
```
**Descripción**: Análisis completo de repositorios GitHub
**Respuesta**: Análisis detallado de repositorios, commits, y actividad

#### **Estado de Heroku**
```http
GET /heroku/deployment
```
**Descripción**: Estado de aplicaciones Heroku
**Respuesta**: Estado de dynos, logs, y métricas de rendimiento

---

## ⚡ API DE SMART CONTRACTS

### **Base URL**
```
https://smart-contracts-api.panacea-icono.org
```

### **Endpoints de Contratos**

#### **Información de Contratos**
```http
GET /contracts
```
**Descripción**: Lista todos los contratos disponibles
**Respuesta**:
```json
{
  "contracts": [
    {
      "name": "PanasToken",
      "type": "token",
      "address": "0x...",
      "status": "active"
    }
  ]
}
```

#### **Deploy de Contrato**
```http
POST /contracts/deploy
```
**Descripción**: Despliega un nuevo contrato
**Body**:
```json
{
  "contract_type": "token",
  "parameters": {
    "name": "PanasToken",
    "symbol": "PANAS"
  }
}
```

---

## 📱 API DE TELEGRAM

### **Base URL**
```
https://telegram-webhook.panacea-icono.org
```

### **Endpoints de Bots**

#### **Estado de Bots**
```http
GET /bots/status
```
**Descripción**: Estado de todos los bots de Telegram
**Respuesta**:
```json
{
  "total_bots": 29,
  "active_bots": 28,
  "bots": [
    {
      "name": "ALINA",
      "username": "ALINA_KUCHITV_BOT",
      "status": "active"
    }
  ]
}
```

#### **Enviar Mensaje**
```http
POST /bots/send
```
**Descripción**: Envía mensaje desde un bot específico
**Body**:
```json
{
  "bot_username": "ALINA_KUCHITV_BOT",
  "chat_id": "123456789",
  "message": "Hola, soy ALINA"
}
```

---

## 🤖 API DE AUDITORÍA

### **Base URL**
```
https://auditor-api.panacea-icono.org
```

### **Endpoints de Auditoría**

#### **Iniciar Auditoría**
```http
POST /audit/start
```
**Descripción**: Inicia auditoría completa del ecosistema
**Body**:
```json
{
  "scope": "full",
  "include_github": true,
  "include_heroku": true,
  "include_telegram": true
}
```

#### **Estado de Auditoría**
```http
GET /audit/status/{audit_id}
```
**Descripción**: Estado de una auditoría específica
**Respuesta**:
```json
{
  "audit_id": "audit_123",
  "status": "completed",
  "progress": 100,
  "results": {
    "github": "passed",
    "heroku": "passed",
    "telegram": "warning"
  }
}
```

---

## 🧬 API DE FIBONACCI

### **Base URL**
```
https://fibonacci-simulator.panacea-icono.org
```

### **Endpoints del Simulador**

#### **Simulación Médica**
```http
POST /simulate
```
**Descripción**: Ejecuta simulación médica
**Body**:
```json
{
  "patient_data": {
    "age": 35,
    "gender": "female",
    "medical_history": ["diabetes"]
  },
  "procedure": "liposuction",
  "risk_factors": ["obesity"]
}
```

#### **Resultados de Simulación**
```http
GET /simulation/{simulation_id}
```
**Descripción**: Obtiene resultados de simulación
**Respuesta**:
```json
{
  "simulation_id": "sim_123",
  "status": "completed",
  "risk_score": 0.15,
  "recommendations": [
    "Proceder con precaución",
    "Monitoreo post-operatorio intensivo"
  ]
}
```

---

## 🔗 GITHUB INTEGRATION API

### **Endpoints de Integración**

#### **Repositorios de la Organización**
```http
GET /github/repos
```
**Descripción**: Lista repositorios de la organización
**Respuesta**: Lista de repositorios con métricas

#### **Actividad de Repositorio**
```http
GET /github/repos/{owner}/{repo}/activity
```
**Descripción**: Actividad reciente de un repositorio
**Respuesta**: Commits, issues, y pull requests recientes

---

## 🚀 HEROKU INTEGRATION API

### **Endpoints de Heroku**

#### **Aplicaciones Heroku**
```http
GET /heroku/apps
```
**Descripción**: Lista aplicaciones Heroku
**Respuesta**: Estado de aplicaciones y dynos

#### **Logs de Aplicación**
```http
GET /heroku/apps/{app_name}/logs
```
**Descripción**: Logs de una aplicación específica
**Respuesta**: Logs recientes de la aplicación

---

## 🤗 HUGGING FACE API

### **Endpoints de IA**

#### **Modelos Disponibles**
```http
GET /huggingface/models
```
**Descripción**: Lista modelos de IA disponibles
**Respuesta**: Modelos y sus capacidades

#### **Inferencia de Modelo**
```http
POST /huggingface/infer
```
**Descripción**: Ejecuta inferencia con un modelo
**Body**:
```json
{
  "model": "panacea-medical-bert",
  "input": "Paciente con dolor de cabeza",
  "parameters": {
    "max_length": 100
  }
}
```

---

## ▲ VERCEL INTEGRATION API

### **Endpoints de Vercel**

#### **Proyectos Vercel**
```http
GET /vercel/projects
```
**Descripción**: Lista proyectos de Vercel
**Respuesta**: Proyectos y sus deployments

#### **Deployments**
```http
GET /vercel/projects/{project_id}/deployments
```
**Descripción**: Deployments de un proyecto
**Respuesta**: Historial de deployments

---

## 🔐 AUTENTICACIÓN

### **API Keys**
Todas las APIs requieren autenticación mediante API key:

```http
Authorization: Bearer YOUR_API_KEY
```

### **Rate Limiting**
- **Límite**: 1000 requests/hora por API key
- **Headers**: `X-RateLimit-Limit`, `X-RateLimit-Remaining`

---

## 📊 MONITOREO Y MÉTRICAS

### **Health Checks**
```http
GET /health
```
**Descripción**: Estado de salud de todas las APIs
**Respuesta**: Estado de cada servicio

### **Métricas**
```http
GET /metrics
```
**Descripción**: Métricas de rendimiento
**Respuesta**: Métricas en formato Prometheus

---

## 📚 DOCUMENTACIÓN ADICIONAL

- [Guía de Integración](integration-guide.md)
- [Ejemplos de Uso](examples.md)
- [Códigos de Error](error-codes.md)
- [Changelog](changelog.md)

---
*Documentación generada automáticamente el 2025-09-09*
*Sistema de APIs Panacea Icono S.A. v2025.09.09.0302*
