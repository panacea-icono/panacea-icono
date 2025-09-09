# 🚀 GUÍA DE DESPLIEGUE - PANACEA ICONO S.A.

**Fecha**: 2025-09-09
**Versión**: v2025.09.09.0302
**Empresa**: Panacea Icono S.A.

## 📋 ÍNDICE DE DESPLIEGUE

### **Plataformas de Despliegue**
- [Heroku](#heroku)
- [Vercel](#vercel)
- [Docker](#docker)
- [GitHub Actions](#github-actions)

### **Entornos**
- [Desarrollo](#desarrollo)
- [Staging](#staging)
- [Producción](#producción)

---

## 🚀 HEROKU

### **Aplicaciones Desplegadas**

#### **API Central Panacea**
- **URL**: https://api-panacea-638dc550fab6.herokuapp.com
- **Stack**: heroku-22
- **Dynos**: 2 web dynos
- **Variables de entorno**: Configuradas
- **Base de datos**: PostgreSQL

#### **Simulador FIBONACCI**
- **URL**: https://fibonacci-b33f2f33a8ad.herokuapp.com
- **Stack**: heroku-22
- **Dynos**: 1 web dyno, 1 worker dyno
- **Variables de entorno**: Configuradas
- **Base de datos**: PostgreSQL

#### **Orquestador Telegram**
- **URL**: https://ton-telegram-orquestador-185e533131f8.herokuapp.com
- **Stack**: heroku-22
- **Dynos**: 1 web dyno
- **Variables de entorno**: Configuradas
- **Base de datos**: Redis

### **Configuración de Despliegue**

#### **Procfile**
```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
worker: python worker.py
```

#### **requirements.txt**
```
fastapi==0.104.1
uvicorn==0.24.0
httpx==0.25.0
python-dotenv==1.0.0
```

#### **Variables de Entorno**
```bash
# Base de datos
DATABASE_URL=postgresql://...
REDIS_URL=redis://...

# APIs externas
GITHUB_TOKEN=ghp_...
HEROKU_API_KEY=...
OPENAI_API_KEY=sk-...
HUGGINGFACE_API_KEY=hf_...

# Telegram
TELEGRAM_BOT_TOKENS=...
```

### **Comandos de Despliegue**

#### **Despliegue Manual**
```bash
# Login a Heroku
heroku login

# Crear aplicación
heroku create panacea-api

# Configurar variables de entorno
heroku config:set GITHUB_TOKEN=ghp_...

# Desplegar
git push heroku main
```

#### **Despliegue Automático**
```bash
# Configurar GitHub integration
heroku git:remote -a panacea-api

# Push para desplegar
git push heroku main
```

---

## ▲ VERCEL

### **Proyectos Desplegados**

#### **Landing Page**
- **URL**: https://panacea-icono.org
- **Framework**: Next.js 13.4
- **Build Command**: `npm run build`
- **Output Directory**: `.next`

#### **Dashboard**
- **URL**: https://dashboard.panacea-icono.org
- **Framework**: Next.js 13.4
- **Build Command**: `npm run build`
- **Output Directory**: `.next`

#### **Simulador Web**
- **URL**: https://simulator.panacea-icono.org
- **Framework**: Next.js 13.4
- **Build Command**: `npm run build`
- **Output Directory**: `.next`

### **Configuración de Despliegue**

#### **vercel.json**
```json
{
  "version": 2,
  "builds": [
    {
      "src": "package.json",
      "use": "@vercel/next"
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "/api/$1"
    }
  ],
  "env": {
    "GITHUB_TOKEN": "@github_token",
    "HEROKU_API_KEY": "@heroku_api_key"
  }
}
```

#### **package.json**
```json
{
  "scripts": {
    "build": "next build",
    "start": "next start",
    "dev": "next dev"
  },
  "dependencies": {
    "next": "13.4.0",
    "react": "18.2.0",
    "typescript": "5.1.0"
  }
}
```

### **Comandos de Despliegue**

#### **Despliegue Manual**
```bash
# Instalar Vercel CLI
npm i -g vercel

# Login
vercel login

# Desplegar
vercel

# Desplegar a producción
vercel --prod
```

#### **Despliegue Automático**
```bash
# Conectar con GitHub
vercel link

# Push para desplegar
git push origin main
```

---

## 🐳 DOCKER

### **Contenedores Configurados**

#### **API Central**
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### **Simulador FIBONACCI**
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["python", "fibonacci_simulator.py"]
```

### **Docker Compose**

#### **docker-compose.yml**
```yaml
version: '3.8'

services:
  api:
    build: ./api
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/panacea
    depends_on:
      - db
      - redis

  fibonacci:
    build: ./fibonacci
    ports:
      - "8001:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/panacea
    depends_on:
      - db

  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=panacea
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7
    ports:
      - "6379:6379"

volumes:
  postgres_data:
```

### **Comandos de Docker**

#### **Build y Run**
```bash
# Build de imágenes
docker-compose build

# Ejecutar servicios
docker-compose up -d

# Ver logs
docker-compose logs -f

# Parar servicios
docker-compose down
```

#### **Despliegue a Producción**
```bash
# Build para producción
docker-compose -f docker-compose.prod.yml build

# Ejecutar en producción
docker-compose -f docker-compose.prod.yml up -d
```

---

## ⚙️ GITHUB ACTIONS

### **Workflows Configurados**

#### **CI/CD Principal**
```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: pytest

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v4
      - name: Deploy to Heroku
        uses: akhileshns/heroku-deploy@v3.12.12
        with:
          heroku_api_key: ${{secrets.HEROKU_API_KEY}}
          heroku_app_name: "panacea-api"
          heroku_email: "repositorios.panacea@gmail.com"
```

#### **Coordinación del Ecosistema**
```yaml
name: Coordinate Ecosystem

on:
  schedule:
    - cron: '0 6 * * *'
  workflow_dispatch:

jobs:
  coordinate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Coordinate Ecosystem
        run: ./coordinate_ecosystem.sh
```

---

## 🔧 DESARROLLO

### **Configuración Local**

#### **Variables de Entorno**
```bash
# .env.local
DATABASE_URL=postgresql://localhost:5432/panacea_dev
REDIS_URL=redis://localhost:6379
GITHUB_TOKEN=ghp_...
HEROKU_API_KEY=...
OPENAI_API_KEY=sk-...
HUGGINGFACE_API_KEY=hf_...
TELEGRAM_BOT_TOKENS=...
```

#### **Comandos de Desarrollo**
```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar en desarrollo
uvicorn main:app --reload

# Ejecutar tests
pytest

# Linting
flake8 .
black .
```

---

## 🧪 STAGING

### **Configuración de Staging**

#### **URLs de Staging**
- **API**: https://panacea-api-staging.herokuapp.com
- **Dashboard**: https://staging.panacea-icono.org
- **Simulador**: https://staging-simulator.panacea-icono.org

#### **Variables de Entorno**
```bash
# Staging específico
ENVIRONMENT=staging
DEBUG=true
LOG_LEVEL=debug
```

---

## 🏭 PRODUCCIÓN

### **Configuración de Producción**

#### **URLs de Producción**
- **API**: https://api-panacea-638dc550fab6.herokuapp.com
- **Landing**: https://panacea-icono.org
- **Dashboard**: https://dashboard.panacea-icono.org
- **Simulador**: https://simulator.panacea-icono.org

#### **Variables de Entorno**
```bash
# Producción
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=info
```

### **Monitoreo de Producción**

#### **Health Checks**
```bash
# API Central
curl https://api-panacea-638dc550fab6.herokuapp.com/health

# Dashboard
curl https://panacea-icono.org/api/health

# Simulador
curl https://simulator.panacea-icono.org/health
```

#### **Logs**
```bash
# Heroku logs
heroku logs --tail -a panacea-api

# Docker logs
docker-compose logs -f api
```

---

## 📊 MONITOREO Y ALERTAS

### **Métricas Clave**
- **Uptime**: 99.9%
- **Response time**: <200ms
- **Error rate**: <0.1%
- **CPU usage**: <70%
- **Memory usage**: <80%

### **Alertas Configuradas**
- **Uptime < 99%**: Email + Slack
- **Response time > 500ms**: Email
- **Error rate > 1%**: Email + Slack
- **CPU > 90%**: Email
- **Memory > 95%**: Email + Slack

---

## 🔒 SEGURIDAD

### **Medidas de Seguridad**
- ✅ **HTTPS** en todas las aplicaciones
- ✅ **Variables de entorno** seguras
- ✅ **Secrets management** con GitHub Secrets
- ✅ **Access control** por roles
- ✅ **Audit logs** completos

### **Backup y Recovery**
- ✅ **Backup automático** de bases de datos
- ✅ **Versionado** de código
- ✅ **Rollback** automático en errores
- ✅ **Disaster recovery** plan

---

## 📚 DOCUMENTACIÓN ADICIONAL

- [Guía de Troubleshooting](troubleshooting.md)
- [Configuración de Monitoreo](monitoring.md)
- [Guía de Seguridad](security.md)
- [Procedimientos de Backup](backup.md)

---
*Documentación generada automáticamente el 2025-09-09*
*Sistema de Despliegue Panacea Icono S.A. v2025.09.09.0302*
