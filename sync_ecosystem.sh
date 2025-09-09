#!/bin/bash

# 🔄 SCRIPT DE SINCRONIZACIÓN ECOSISTEMA PANACEA ICONO S.A.
# Fecha: 2025-09-09
# Propósito: Sincronizar y coordinar todos los repositorios del ecosistema

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
LOG_FILE="logs/sync_ecosystem_$(date '+%Y%m%d_%H%M%S').log"

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

# Función para sincronizar repositorio
sync_repo() {
    local repo_path="$1"
    local repo_name="$2"
    local commit_message="$3"
    local push_enabled="${4:-true}"
    
    info "Sincronizando $repo_name..."
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
    fi
    
    # Verificar estado del repositorio
    if git status --porcelain | grep -q .; then
        info "Hay cambios pendientes en $repo_name"
        git add .
        git commit -m "$commit_message" || {
            warning "No se pudo hacer commit en $repo_name"
            return 1
        }
        success "Commit realizado en $repo_name"
        
        # Push si está habilitado y hay remoto
        if [ "$push_enabled" = true ]; then
            if git remote -v | grep -q origin; then
                info "Haciendo push de $repo_name..."
                git push origin main || git push origin master || {
                    warning "No se pudo hacer push de $repo_name"
                    return 1
                }
                success "Push realizado en $repo_name"
            else
                warning "$repo_name no tiene remoto configurado, saltando push"
            fi
        else
            info "Push deshabilitado para $repo_name"
        fi
    else
        info "No hay cambios pendientes en $repo_name"
    fi
    
    success "✅ $repo_name sincronizado correctamente"
    return 0
}

# Función para verificar estado del ecosistema
check_ecosystem_status() {
    info "Verificando estado del ecosistema..."
    
    local repos=(
        "/Users/kuchimac/Desktop/panacea-icono:Landing Page:Hub central del ecosistema"
        "/Users/kuchimac/Desktop/smart contracts:Smart Contracts:Contratos inteligentes del ecosistema"
        "/Users/kuchimac/Desktop/variables :Variables:Variables maestro del ecosistema"
        "/Users/kuchimac/Desktop/auditor:Auditor:Bot auditor del ecosistema"
    )
    
    for repo_info in "${repos[@]}"; do
        IFS=':' read -r path name description <<< "$repo_info"
        if [ -d "$path" ]; then
            success "✅ $name: $description"
        else
            warning "⚠️  $name: No encontrado en $path"
        fi
    done
}

# Función principal
main() {
    echo -e "${PURPLE}🔄 SINCRONIZACIÓN ECOSISTEMA PANACEA ICONO S.A.${NC}"
    echo "=================================================="
    echo -e "${CYAN}Fecha: $TIMESTAMP${NC}"
    echo ""
    
    # Verificar estado inicial
    check_ecosystem_status
    echo ""
    
    # Sincronizar repositorios principales
    info "Iniciando sincronización de repositorios..."
    echo ""
    
    # 1. Landing Page (Hub Central)
    sync_repo \
        "/Users/kuchimac/Desktop/panacea-icono" \
        "Landing Page" \
        "feat: Actualización del hub central del ecosistema Panacea Icono S.A. - $TIMESTAMP" \
        true
    
    echo ""
    
    # 2. Smart Contracts
    sync_repo \
        "/Users/kuchimac/Desktop/smart contracts" \
        "Smart Contracts" \
        "feat: Actualización de contratos inteligentes del ecosistema Panacea Icono S.A. - $TIMESTAMP" \
        true
    
    echo ""
    
    # 3. Variables (Local - sin push)
    sync_repo \
        "/Users/kuchimac/Desktop/variables " \
        "Variables" \
        "feat: Actualización de variables maestro del ecosistema Panacea Icono S.A. - $TIMESTAMP" \
        false
    
    echo ""
    
    # 4. Auditor (Local - sin push)
    sync_repo \
        "/Users/kuchimac/Desktop/auditor" \
        "Auditor" \
        "feat: Actualización del bot auditor del ecosistema Panacea Icono S.A. - $TIMESTAMP" \
        false
    
    echo ""
    
    # Resumen final
    success "🎉 Sincronización del ecosistema completada"
    info "Log guardado en: $LOG_FILE"
    
    # Mostrar resumen de commits
    echo ""
    echo -e "${CYAN}📊 RESUMEN DE COMMITS:${NC}"
    echo "========================"
    
    local repos=(
        "/Users/kuchimac/Desktop/panacea-icono:Landing Page"
        "/Users/kuchimac/Desktop/smart contracts:Smart Contracts"
        "/Users/kuchimac/Desktop/variables :Variables"
        "/Users/kuchimac/Desktop/auditor:Auditor"
    )
    
    for repo_info in "${repos[@]}"; do
        IFS=':' read -r path name <<< "$repo_info"
        if [ -d "$path/.git" ]; then
            cd "$path"
            local commit_count=$(git rev-list --count HEAD 2>/dev/null || echo "0")
            local last_commit=$(git log -1 --format="%h - %s (%cr)" 2>/dev/null || echo "Sin commits")
            echo -e "${GREEN}$name:${NC} $commit_count commits - Último: $last_commit"
        fi
    done
    
    echo ""
    echo -e "${PURPLE}✨ Ecosistema Panacea Icono S.A. sincronizado exitosamente${NC}"
}

# Ejecutar función principal
main "$@"