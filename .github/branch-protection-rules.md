# 🛡️ Reglas de Protección de Ramas - PANACEA ICONO

## 📋 Configuración de Ramas Protegidas

### 🔒 Rama Principal (`main`)

**Reglas de Protección:**
- ✅ Requerir revisiones de pull request antes de mergear
- ✅ Número mínimo de revisiones requeridas: **2**
- ✅ Descartar revisiones obsoletas cuando se envíen nuevos commits
- ✅ Requerir revisión de propietarios del código
- ✅ Requerir que las verificaciones de estado pasen antes de mergear
- ✅ Requerir que las ramas estén actualizadas antes de mergear
- ✅ Requerir conversación resuelta antes de mergear
- ❌ Permitir push forzado: **PROHIBIDO**
- ❌ Permitir eliminaciones: **PROHIBIDO**

**Verificaciones de Estado Requeridas:**
- `🔍 Code Quality & Security`
- `🐳 Docker Build & Test`
- `🧪 Security Scans`
- `📊 Dependency Check`

### 🚀 Rama de Desarrollo (`develop`)

**Reglas de Protección:**
- ✅ Requerir revisiones de pull request antes de mergear
- ✅ Número mínimo de revisiones requeridas: **1**
- ✅ Requerir que las verificaciones de estado pasen antes de mergear
- ✅ Requerir que las ramas estén actualizadas antes de mergear
- ❌ Permitir push forzado: **RESTRINGIDO** (solo administradores)
- ❌ Permitir eliminaciones: **PROHIBIDO**

**Verificaciones de Estado Requeridas:**
- `🔍 Code Quality & Security`
- `🐳 Docker Build & Test`

### 🔧 Ramas de Características (`feature/*`)

**Convenciones de Nomenclatura:**
- `feature/nombre-de-funcionalidad`
- `feature/ticket-123-descripcion`
- `feature/modulo-nueva-caracteristica`

**Reglas:**
- ✅ Crear desde `develop`
- ✅ Mergear hacia `develop`
- ✅ Eliminar después del merge
- ✅ Requerir CI passing antes del merge

### 🐛 Ramas de Corrección (`bugfix/*`)

**Convenciones de Nomenclatura:**
- `bugfix/descripcion-del-error`
- `bugfix/issue-456-solucion`
- `bugfix/modulo-error-especifico`

**Reglas:**
- ✅ Crear desde `develop` o `main` (según urgencia)
- ✅ Mergear hacia `develop` y `main` (si es hotfix)
- ✅ Eliminar después del merge

### 🚨 Ramas de Hotfix (`hotfix/*`)

**Convenciones de Nomenclatura:**
- `hotfix/version-patch`
- `hotfix/security-fix`
- `hotfix/critico-descripcion`

**Reglas:**
- ✅ Crear desde `main`
- ✅ Mergear hacia `main` y `develop`
- ✅ Crear tag de versión automáticamente
- ✅ Despliegue automático a producción

### 🔄 Ramas de Release (`release/*`)

**Convenciones de Nomenclatura:**
- `release/v1.0.0`
- `release/v2023.12.01`

**Reglas:**
- ✅ Crear desde `develop`
- ✅ Mergear hacia `main` y `develop`
- ✅ Crear tag de versión
- ✅ No permitir features nuevas, solo bugfixes

## 🔗 Reglas de Merge

### Estrategias de Merge Permitidas

1. **Merge Commit** (Preferido para releases)
2. **Squash and Merge** (Preferido para features)
3. **Rebase and Merge** (Solo para hotfixes)

### Formato de Commits

```
tipo(ámbito): descripción breve

Descripción detallada del cambio (opcional)

- Cambio específico 1
- Cambio específico 2

Fixes #123
Co-authored-by: Nombre <email>
```

**Tipos de commit permitidos:**
- `feat`: Nueva funcionalidad
- `fix`: Corrección de error
- `docs`: Cambios en documentación
- `style`: Cambios de formato
- `refactor`: Refactorización de código
- `test`: Añadir o modificar tests
- `chore`: Tareas de mantenimiento
- `security`: Correcciones de seguridad
- `perf`: Mejoras de rendimiento

## 🚫 Restricciones

### Ramas Prohibidas
- No crear ramas directamente desde `main` (excepto hotfixes)
- No usar nombres genéricos como `test`, `temp`, `fix`
- No usar espacios o caracteres especiales en nombres de ramas

### Acciones Prohibidas
- Push directo a `main` sin PR
- Merge sin revisión
- Eliminación de ramas principales
- Push forzado en ramas protegidas

## 👥 Permisos por Rol

### 🔑 Administradores
- Pueden crear y eliminar ramas protegidas
- Pueden hacer override de reglas en emergencias
- Acceso a configuración de repositorio

### 🧑‍💻 Desarrolladores
- Pueden crear ramas feature/bugfix
- Pueden hacer PR a develop
- Requieren aprobación para merge a main

### 👀 Colaboradores
- Pueden crear forks
- Pueden proponer cambios via PR
- Acceso de solo lectura a ramas principales

## 📊 Monitoreo y Cumplimiento

### Métricas a Monitorear
- Tiempo de vida de ramas
- Número de commits por rama
- Frecuencia de merges
- Violaciones de reglas

### Alertas Automáticas
- PR sin revisión después de 24h
- Ramas stale (más de 30 días)
- Vulnerabilidades de seguridad
- Fallos en CI/CD

---

*Última actualización: $(date)*
*Aplicable a todo el ecosistema panacea-icono*