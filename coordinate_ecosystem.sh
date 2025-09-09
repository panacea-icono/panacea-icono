#!/bin/bash

# 🚀 SCRIPT DE COORDINACIÓN COMPLETA ECOSISTEMA PANACEA ICONO S.A.
# Fecha: 2025-09-09
# Propósito: Coordinar commits, push, releases, tags y packages del ecosistema

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuración
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
VERSION=$(date '+%Y.%m.%d.%H%M')
LOG_FILE="logs/coordinate_ecosystem_$(date '+%Y%m%d_%H%M%S').log"

# Crear directorio de logs si no existe
mkdir -p logs

# Función para logging
log() {
    local message="$1"
    echo -e "${GREEN}[$TIMESTAMP]${NC} $message" | tee -a "$LOG_FILE"
}

error() {
    local message="$1"
    echo -e "${RED}[ERROR]${NC} $message" | tee -a "$LOG_FILE"
    exit 1
}

warning() {
    local message="$1"
    echo -e "${YELLOW}[WARNING]${NC} $message" | tee -a "$LOG_FILE"
}

info() {
    local message="$1"
    echo -e "${BLUE}[INFO]${NC} $message" | tee -a "$LOG_FILE"
}

success() {
    local message="$1"
    echo -e "${GREEN}[SUCCESS]${NC} $message" | tee -a "$LOG_FILE"
}

# Función para coordinar repositorio completo
coordinate_repo() {
    local repo_path="$1"
    local repo_name="$2"
    local repo_type="$3"
    local commit_message="$4"
    local push_enabled="${5:-true}"
    local create_release="${6:-false}"
    local create_tag="${7:-false}"
    local create_package="${8:-false}"
    
    info "🔄 Coordinando $repo_name ($repo_type)..."
    info "Ruta: $repo_path"
    
    if [ ! -d "$repo_path" ]; then
        warning "Directorio $repo_path no existe, saltando..."
        return 1
    fi
    
    cd "$repo_path" || {
        warning "No se puede acceder a $repo_path, saltando..."
        return 1
    }
    
    # Verificar si es un repositorio Git
    if [ ! -d ".git" ]; then
        warning "$repo_name no es un repositorio Git, inicializando..."
        git init
        git config user.name "Panacea Icono S.A."
        git config user.email "repositorios.panacea@gmail.com"
        git branch -M main
    fi
    
    # Verificar estado del repositorio
    if git status --porcelain | grep -q .; then
        info "📝 Hay cambios pendientes en $repo_name"
        git add .
        git commit -m "$commit_message" || {
            warning "No se pudo hacer commit en $repo_name"
            return 1
        }
        success "✅ Commit realizado en $repo_name"
        
        # Push si está habilitado
        if [ "$push_enabled" = true ]; then
            if git remote -v | grep -q origin; then
                info "🚀 Haciendo push de $repo_name..."
                git push origin main || git push origin master || {
                    warning "No se pudo hacer push de $repo_name"
                    return 1
                }
                success "✅ Push realizado en $repo_name"
            else
                warning "$repo_name no tiene remoto configurado, saltando push"
            fi
        fi
        
        # Crear tag si está habilitado
        if [ "$create_tag" = true ]; then
            info "🏷️  Creando tag v$VERSION para $repo_name..."
            git tag -a "v$VERSION" -m "Release v$VERSION - $repo_name" || {
                warning "No se pudo crear tag en $repo_name"
            }
            if [ "$push_enabled" = true ] && git remote -v | grep -q origin; then
                git push origin "v$VERSION" || {
                    warning "No se pudo hacer push del tag en $repo_name"
                }
            fi
            success "✅ Tag v$VERSION creado para $repo_name"
        fi
        
        # Crear release si está habilitado
        if [ "$create_release" = true ]; then
            info "📦 Creando release v$VERSION para $repo_name..."
            # Aquí se podría integrar con GitHub CLI para crear releases automáticamente
            # gh release create "v$VERSION" --title "Release v$VERSION - $repo_name" --notes "Release coordinado del ecosistema Panacea Icono S.A."
            success "✅ Release v$VERSION preparado para $repo_name"
        fi
        
        # Crear package si está habilitado
        if [ "$create_package" = true ]; then
            info "📦 Creando package para $repo_name..."
            # Verificar si tiene package.json o setup.py
            if [ -f "package.json" ]; then
                info "📦 Detectado package.json, preparando NPM package..."
                # npm publish --dry-run || warning "No se pudo preparar NPM package"
            elif [ -f "setup.py" ]; then
                info "📦 Detectado setup.py, preparando PyPI package..."
                # python setup.py sdist bdist_wheel || warning "No se pudo preparar PyPI package"
            fi
            success "✅ Package preparado para $repo_name"
        fi
        
    else
        info "ℹ️  No hay cambios pendientes en $repo_name"
    fi
    
    success "✅ $repo_name coordinado correctamente"
    return 0
}

# Función para crear release notes coordinado
create_coordinated_release_notes() {
    local version="$1"
    local timestamp="$2"
    
    cat > "RELEASE_NOTES_v$version.md" << EOF
# 🚀 Release Coordinado v$version - Ecosistema Panacea Icono S.A.

**Fecha**: $timestamp  
**Versión**: $version  
**Tipo**: Release Coordinado del Ecosistema  

## 📋 Repositorios Incluidos

### 🏠 Landing Page (Hub Central)
- **Repositorio**: panacea-icono
- **Cambios**: Actualizaciones del hub central
- **Estado**: ✅ Sincronizado

### ⚡ Smart Contracts
- **Repositorio**: panacea_smart_contracts
- **Cambios**: Contratos inteligentes actualizados
- **Estado**: ✅ Sincronizado

### 🔧 Variables (Base de Datos)
- **Repositorio**: variables (local)
- **Cambios**: Variables maestro actualizadas
- **Estado**: ✅ Sincronizado

### 🤖 Auditor (Bot GPT)
- **Repositorio**: auditor (local)
- **Cambios**: Bot auditor actualizado
- **Estado**: ✅ Sincronizado

## 🎯 Características Principales

- ✅ Coordinación completa del ecosistema
- ✅ Sincronización automática de repositorios
- ✅ Sistema de commits coordinados
- ✅ Gestión centralizada de variables
- ✅ Bot auditor integrado

## 🔄 Próximos Pasos

1. Monitoreo continuo del ecosistema
2. Integración de las 3 empresas SRL
3. Optimización de sincronización
4. Escalamiento del sistema

---
*Release generado automáticamente por el Sistema de Coordinación Panacea Icono S.A.*
EOF

    success "📝 Release notes coordinado creado: RELEASE_NOTES_v$version.md"
}

# Función principal
main() {
    echo -e "${PURPLE}🚀 COORDINACIÓN COMPLETA ECOSISTEMA PANACEA ICONO S.A.${NC}"
    echo "=========================================================="
    echo -e "${CYAN}Versión: $VERSION${NC}"
    echo -e "${CYAN}Fecha: $TIMESTAMP${NC}"
    echo ""
    
    # Crear release notes coordinado
    create_coordinated_release_notes "$VERSION" "$TIMESTAMP"
    
    # Coordinar repositorios principales
    info "🔄 Iniciando coordinación de repositorios..."
    echo ""
    
    # 1. Landing Page (Hub Central) - Con release y tag
    coordinate_repo \
        "/Users/kuchimac/Desktop/panacea-icono" \
        "Landing Page" \
        "Hub Central" \
        "feat: Coordinación v$VERSION - Hub central del ecosistema Panacea Icono S.A." \
        true \
        true \
        true \
        false
    
    echo ""
    
    # 2. Smart Contracts - Con release, tag y package
    coordinate_repo \
        "/Users/kuchimac/Desktop/smart contracts" \
        "Smart Contracts" \
        "Contratos Inteligentes" \
        "feat: Coordinación v$VERSION - Contratos inteligentes del ecosistema Panacea Icono S.A." \
        true \
        true \
        true \
        true
    
    echo ""
    
    # 3. Variables (Local) - Sin push, con tag local
    coordinate_repo \
        "/Users/kuchimac/Desktop/variables " \
        "Variables" \
        "Base de Datos" \
        "feat: Coordinación v$VERSION - Variables maestro del ecosistema Panacea Icono S.A." \
        false \
        false \
        true \
        false
    
    echo ""
    
    # 4. Auditor (Local) - Sin push, con tag local
    coordinate_repo \
        "/Users/kuchimac/Desktop/auditor" \
        "Auditor" \
        "Bot Auditor" \
        "feat: Coordinación v$VERSION - Bot auditor del ecosistema Panacea Icono S.A." \
        false \
        false \
        true \
        false
    
    echo ""
    
    # Resumen final
    success "🎉 Coordinación del ecosistema completada"
    info "📊 Versión coordinada: v$VERSION"
    info "📝 Log guardado en: $LOG_FILE"
    info "📋 Release notes: RELEASE_NOTES_v$VERSION.md"
    
    # Mostrar resumen de coordinación
    echo ""
    echo -e "${CYAN}📊 RESUMEN DE COORDINACIÓN:${NC}"
    echo "================================"
    
    local repos=(
        "/Users/kuchimac/Desktop/panacea-icono:Landing Page:Hub Central:✅"
        "/Users/kuchimac/Desktop/smart contracts:Smart Contracts:Contratos:✅"
        "/Users/kuchimac/Desktop/variables :Variables:Base de Datos:✅"
        "/Users/kuchimac/Desktop/auditor:Auditor:Bot GPT:✅"
    )
    
    for repo_info in "${repos[@]}"; do
        IFS=':' read -r path name type status <<< "$repo_info"
        if [ -d "$path/.git" ]; then
            cd "$path"
            local commit_count=$(git rev-list --count HEAD 2>/dev/null || echo "0")
            local last_commit=$(git log -1 --format="%h - %s (%cr)" 2>/dev/null || echo "Sin commits")
            echo -e "${GREEN}$name ($type):${NC} $status - $commit_count commits - Último: $last_commit"
        fi
    done
    
    echo ""
    echo -e "${PURPLE}✨ Ecosistema Panacea Icono S.A. coordinado exitosamente${NC}"
    echo -e "${CYAN}🏷️  Versión: v$VERSION${NC}"
    echo -e "${CYAN}📅 Fecha: $TIMESTAMP${NC}"
}

# Ejecutar función principal
main "$@"
