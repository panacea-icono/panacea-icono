# 🌐 Reglas de Conexiones del Ecosistema - PANACEA ICONO

## 📋 Configuración de Conexiones de Servicios

### 🐳 Docker Hub Connection Rules

**Configuración Requerida:**
- Registry: `ghcr.io` (GitHub Container Registry)
- Imagen principal: `ghcr.io/panacea-icono/panacea-icono`
- Tags automáticos: `latest`, `develop`, `v{version}`

**Reglas de Imagen:**
- ✅ Build automático en cada push a `main` y `develop`
- ✅ Escaneo de vulnerabilidades antes del push
- ✅ Firma de imágenes con cosign
- ✅ Multi-arquitectura (amd64, arm64)
- ❌ No permitir imágenes sin escanear
- ❌ No permitir tags manuales en producción

**Conexiones Requeridas:**
```yaml
docker:
  registry: "ghcr.io"
  username: "${{ github.actor }}"
  token: "${{ secrets.GITHUB_TOKEN }}"
  image_name: "${{ github.repository }}"
  scan_enabled: true
  auto_cleanup: true
  retention_days: 30
```

### 🚀 Heroku Connection Rules

**Configuración de Apps:**
- Producción: `panacea-icono-prod`
- Staging: `panacea-icono-staging`
- Desarrollo: `panacea-icono-dev`

**Variables de Entorno Requeridas:**
```bash
HEROKU_API_KEY=<secret>
HEROKU_APP_NAME=<app-name>
HEROKU_EMAIL=<email>
DATABASE_URL=<postgres-url>
REDIS_URL=<redis-url>
```

**Reglas de Despliegue:**
- ✅ Despliegue automático desde `main` → producción
- ✅ Despliegue automático desde `develop` → staging
- ✅ Health checks antes y después del despliegue
- ✅ Rollback automático en caso de fallo
- ❌ No despliegues manuales en producción
- ❌ No bypass de health checks

### 🤖 Hugging Face Connection Rules

**Configuración de Hub:**
- Organización: `panacea-icono`
- Modelos principales: `medical-bert`, `healthcare-gpt`, `diagnostic-ai`
- Datasets: `medical-data`, `patient-records`, `diagnostic-images`

**Variables de Entorno Requeridas:**
```bash
HUGGINGFACE_API_KEY=<secret>
HUGGINGFACE_EMAIL=<email>
HUGGINGFACE_USERNAME=<username>
HF_HUB_CACHE=/app/.cache/huggingface
```

**Reglas de Modelos:**
- ✅ Versionado semántico de modelos
- ✅ Metadatos completos (license, description, tags)
- ✅ Evaluación automática de modelos
- ✅ Documentación del modelo (README, model card)
- ❌ No modelos sin licencia definida
- ❌ No modelos sin evaluación

### 📚 GitHub Connection Rules

**Configuración de Repositorios:**
- Organización principal: `panacea-icono`
- Repositorios: 50+ (ver lista en README)
- Branch principal: `main`
- Branch desarrollo: `develop`

**Tokens y Permisos:**
```yaml
github:
  token: "${{ secrets.GITHUB_TOKEN }}"
  permissions:
    contents: write
    packages: write
    actions: write
    security-events: write
    pull-requests: write
```

**Reglas de Sincronización:**
- ✅ Sync automático de metadatos
- ✅ Propagación de releases coordinados
- ✅ Auditorías automáticas de repositorios
- ✅ Backup de configuraciones críticas
- ❌ No cambios manuales en metadatos sin PR

## 🔗 Conexiones Inter-Repositorios

### 🎯 Hub Central: Ton-telegram
**Rol:** Orchestrador principal del ecosistema
**Conexiones:**
- Coordina releases entre repositorios
- Gestiona sincronización de READMEs
- Ejecuta auditorías automáticas
- Maneja secrets compartidos

### 📊 Repositorios de Aplicaciones

#### 1. PANAS_PAY_APP (TypeScript)
**Conexiones:**
- Backend: `main.py` APIs
- Blockchain: TON Network
- Payments: Telegram Bot API
- Database: PostgreSQL/Redis

#### 2. dr_tv_GPT (TypeScript)
**Conexiones:**
- AI Models: Hugging Face Hub
- Media: Docker containers
- API: FastAPI endpoints
- Storage: Cloud services

#### 3. macuquina_proyecto (Python)
**Conexiones:**
- Blockchain: Algorand
- Smart Contracts: PyTeal
- NFT Storage: IPFS
- Database: MongoDB

### 🔧 Utilidades y Herramientas

#### codex-github (Shell)
**Conexiones:**
- GitHub API
- Repository metadata
- Automation scripts
- CI/CD pipelines

#### REDES (TypeScript)
**Conexiones:**
- Network protocols
- API gateways
- Service mesh
- Load balancers

## 🛡️ Reglas de Seguridad

### 🔐 Secrets Management
```yaml
secrets:
  required:
    - GITHUB_TOKEN
    - HEROKU_API_KEY
    - HUGGINGFACE_API_KEY
    - DOCKER_REGISTRY_TOKEN
  optional:
    - OPENAI_API_KEY
    - TELEGRAM_BOT_TOKEN
    - DATABASE_ENCRYPTION_KEY
  
  rules:
    - No secrets en código fuente
    - Rotación automática cada 90 días
    - Audit log de accesos
    - Encrypted at rest y in transit
```

### 🚨 Monitoring y Alertas
```yaml
monitoring:
  health_checks:
    interval: 30s
    timeout: 10s
    retries: 3
  
  alerts:
    - connection_failure
    - unauthorized_access
    - resource_exhaustion
    - security_vulnerability
  
  dashboards:
    - Service status
    - Performance metrics
    - Security events
    - Cost tracking
```

## 📈 Métricas de Conexión

### 🎯 KPIs Principales
- **Uptime**: > 99.9% para servicios críticos
- **Response Time**: < 200ms para APIs
- **Error Rate**: < 0.1% para transacciones
- **Security Score**: > 95% en auditorías

### 📊 Reportes Automáticos
- Reporte semanal de estado de conexiones
- Análisis mensual de rendimiento
- Auditoría trimestral de seguridad
- Review anual de arquitectura

## 🔄 Proceso de Cambios

### 📝 Solicitudes de Cambio
1. Crear issue con template de conexión
2. Proponer cambios en PR
3. Review de arquitectura
4. Testing en staging
5. Aprobación y deploy

### ✅ Checklist Pre-Deploy
- [ ] Conexiones probadas en staging
- [ ] Secrets actualizados
- [ ] Monitoring configurado
- [ ] Rollback plan definido
- [ ] Team notificado

---

## 🚀 Scripts de Validación

### Connection Health Check
```bash
#!/bin/bash
# Validar todas las conexiones del ecosistema
./sync_ecosystem.sh --health-check --all-services
```

### Emergency Disconnect
```bash
#!/bin/bash
# Desconectar servicios en caso de emergencia
./sync_ecosystem.sh --emergency-mode --disconnect-all
```

---

*Última actualización: $(date)*
*Para cambios en estas reglas, crear PR en Ton-telegram repository*