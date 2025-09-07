#!/bin/bash

# 🚀 PANACEA ICONO Ecosystem Synchronization Script
# Sincroniza Docker, Heroku, Hugging Face y GitHub
# Developed by: drtv

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
APP_NAME="panacea-icono-ai"
HEROKU_APP_URL="https://panacea-icono-ai-78b4eb86c23b.herokuapp.com"
GITHUB_REPO="panacea-icono/panacea-icono"
DOCKER_IMAGE="drtv/panacea-icono"
DOCKER_USERNAME="drtv"

echo -e "${CYAN}🏥 PANACEA ICONO Ecosystem Synchronization${NC}"
echo "=================================================="
echo -e "${BLUE}🐳 Docker User: ${DOCKER_USERNAME}${NC}"
echo -e "${BLUE}🚀 Heroku App: ${APP_NAME}${NC}"
echo -e "${BLUE}📚 GitHub Repo: ${GITHUB_REPO}${NC}"
echo ""

# Función para mostrar estado
show_status() {
    echo -e "${BLUE}📊 Estado actual:${NC}"
    echo "  🐳 Docker: $1"
    echo "  🚀 Heroku: $2"
    echo "  🤖 Hugging Face: $3"
    echo "  📚 GitHub: $4"
    echo ""
}

# Función para verificar Docker
check_docker() {
    echo -e "${YELLOW}🔍 Verificando Docker...${NC}"
    
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}❌ Docker no está instalado${NC}"
        return 1
    fi
    
    if ! docker info &> /dev/null; then
        echo -e "${RED}❌ Docker no está ejecutándose${NC}"
        return 1
    fi
    
    # Verificar login de Docker Hub
    if ! docker info | grep -q "Username"; then
        echo -e "${YELLOW}⚠️ No hay sesión activa en Docker Hub${NC}"
        echo -e "${BLUE}💡 Ejecuta: docker login${NC}"
    else
        echo -e "${GREEN}✅ Docker está funcionando y autenticado${NC}"
    fi
    
    return 0
}

# Función para verificar Heroku
check_heroku() {
    echo -e "${YELLOW}🔍 Verificando Heroku...${NC}"
    
    if ! command -v heroku &> /dev/null; then
        echo -e "${RED}❌ Heroku CLI no está instalado${NC}"
        return 1
    fi
    
    # Verificar autenticación
    if ! heroku auth:whoami &> /dev/null; then
        echo -e "${RED}❌ No autenticado en Heroku${NC}"
        return 1
    fi
    
    # Verificar app
    if ! heroku apps:info --app $APP_NAME &> /dev/null; then
        echo -e "${RED}❌ App $APP_NAME no encontrada${NC}"
        return 1
    fi
    
    echo -e "${GREEN}✅ Heroku está configurado${NC}"
    return 0
}

# Función para verificar Hugging Face
check_huggingface() {
    echo -e "${YELLOW}🔍 Verificando Hugging Face...${NC}"
    
    # Verificar variables de entorno
    if [ -z "$HUGGINGFACE_API_KEY" ]; then
        echo -e "${RED}❌ HUGGINGFACE_API_KEY no configurada${NC}"
        return 1
    fi
    
    if [ -z "$HUGGINGFACE_EMAIL" ]; then
        echo -e "${RED}❌ HUGGINGFACE_EMAIL no configurada${NC}"
        return 1
    fi
    
    echo -e "${GREEN}✅ Hugging Face está configurado${NC}"
    return 0
}

# Función para verificar GitHub
check_github() {
    echo -e "${YELLOW}🔍 Verificando GitHub...${NC}"
    
    if ! command -v git &> /dev/null; then
        echo -e "${RED}❌ Git no está instalado${NC}"
        return 1
    fi
    
    # Verificar remoto
    if ! git remote get-url origin &> /dev/null; then
        echo -e "${RED}❌ No hay remoto origin configurado${NC}"
        return 1
    fi
    
    echo -e "${GREEN}✅ GitHub está configurado${NC}"
    return 0
}

# Función para construir Docker
build_docker() {
    echo -e "${YELLOW}🐳 Construyendo imagen Docker...${NC}"
    
    if docker build -t $DOCKER_IMAGE .; then
        echo -e "${GREEN}✅ Imagen Docker construida exitosamente${NC}"
        return 0
    else
        echo -e "${RED}❌ Error al construir imagen Docker${NC}"
        return 1
    fi
}

# Función para probar Docker
test_docker() {
    echo -e "${YELLOW}🧪 Probando imagen Docker...${NC}"
    
    # Crear contenedor temporal para pruebas
    if docker run --rm -d --name test-panacea $DOCKER_IMAGE; then
        echo -e "${GREEN}✅ Contenedor Docker iniciado exitosamente${NC}"
        
        # Esperar un momento y verificar logs
        sleep 5
        if docker logs test-panacea &> /dev/null; then
            echo -e "${GREEN}✅ Contenedor está funcionando${NC}"
        fi
        
        # Limpiar contenedor de prueba
        docker stop test-panacea &> /dev/null
        docker rm test-panacea &> /dev/null
        
        return 0
    else
        echo -e "${RED}❌ Error al probar contenedor Docker${NC}"
        return 1
    fi
}

# Función para hacer push a Docker Hub
push_docker() {
    echo -e "${YELLOW}📤 Haciendo push a Docker Hub...${NC}"
    
    # Verificar si hay sesión activa
    if ! docker info | grep -q "Username"; then
        echo -e "${RED}❌ No hay sesión activa en Docker Hub${NC}"
        echo -e "${BLUE}💡 Ejecuta: docker login${NC}"
        return 1
    fi
    
    # Hacer push
    if docker push $DOCKER_IMAGE; then
        echo -e "${GREEN}✅ Imagen subida a Docker Hub exitosamente${NC}"
        echo -e "${BLUE}🌐 Disponible en: https://hub.docker.com/r/${DOCKER_USERNAME}/panacea-icono${NC}"
        return 0
    else
        echo -e "${RED}❌ Error al subir imagen a Docker Hub${NC}"
        return 1
    fi
}

# Función para desplegar en Heroku
deploy_heroku() {
    echo -e "${YELLOW}🚀 Desplegando en Heroku...${NC}"
    
    # Verificar si ya hay remoto de Heroku
    if ! git remote get-url heroku &> /dev/null; then
        echo "🔗 Agregando remoto de Heroku..."
        heroku git:remote -a $APP_NAME
    fi
    
    # Desplegar
    if git push heroku main; then
        echo -e "${GREEN}✅ Despliegue en Heroku exitoso${NC}"
        
        # Verificar estado
        echo "🔍 Verificando estado de la app..."
        heroku ps --app $APP_NAME
        
        # Abrir en navegador
        echo "🌐 Abriendo app en navegador..."
        heroku open --app $APP_NAME
        
        return 0
    else
        echo -e "${RED}❌ Error en despliegue de Heroku${NC}"
        return 1
    fi
}

# Función para sincronizar con Hugging Face
sync_huggingface() {
    echo -e "${YELLOW}🤖 Sincronizando con Hugging Face...${NC}"
    
    # Ejecutar script de Python
    if python3 huggingface_config.py; then
        echo -e "${GREEN}✅ Sincronización con Hugging Face exitosa${NC}"
        return 0
    else
        echo -e "${RED}❌ Error en sincronización con Hugging Face${NC}"
        return 1
    fi
}

# Función para ejecutar gestión del ecosistema
run_ecosystem_management() {
    echo -e "${YELLOW}🌍 Ejecutando gestión del ecosistema...${NC}"
    
    # Ejecutar el ecosistema manager de Python
    if python3 ecosystem_manager.py sync; then
        echo -e "${GREEN}✅ Gestión del ecosistema exitosa${NC}"
        return 0
    else
        echo -e "${RED}❌ Error en gestión del ecosistema${NC}"
        return 1
    fi
}

# Función para actualizar README automáticamente
update_readme() {
    echo -e "${YELLOW}📝 Actualizando README automáticamente...${NC}"
    
    if python3 ecosystem_manager.py readme; then
        echo -e "${GREEN}✅ README actualizado exitosamente${NC}"
        return 0
    else
        echo -e "${RED}❌ Error actualizando README${NC}"
        return 1
    fi
}

# Función para auditar paquetes
audit_packages() {
    echo -e "${YELLOW}🔍 Auditando paquetes y dependencias...${NC}"
    
    if python3 ecosystem_manager.py audit; then
        echo -e "${GREEN}✅ Auditoría de paquetes completada${NC}"
        return 0
    else
        echo -e "${RED}❌ Error en auditoría de paquetes${NC}"
        return 1
    fi
}

# Función para sincronizar con GitHub
sync_github() {
    echo -e "${YELLOW}📚 Sincronizando con GitHub...${NC}"
    
    # Primero ejecutar la gestión del ecosistema
    if run_ecosystem_management; then
        echo -e "${GREEN}✅ Gestión del ecosistema completada${NC}"
    fi
    
    # Verificar cambios
    if git status --porcelain | grep -q .; then
        echo "📝 Hay cambios pendientes, haciendo commit..."
        
        git add .
        git commit -m "🔄 Sync: Actualización automática del ecosistema $(date +'%Y-%m-%d %H:%M:%S')
        
        - 🐳 Docker build y test (drtv)
        - 🚀 Heroku deployment
        - 🤖 Hugging Face integration
        - 📚 GitHub synchronization
        - 🌍 Ecosystem management update
        - 📦 Package audits and updates
        - 📝 README automation"
        
        if git push origin main; then
            echo -e "${GREEN}✅ Push a GitHub exitoso${NC}"
            return 0
        else
            echo -e "${RED}❌ Error en push a GitHub${NC}"
            return 1
        fi
    else
        echo -e "${GREEN}✅ No hay cambios pendientes en GitHub${NC}"
        return 0
    fi
}

# Función para mostrar resumen
show_summary() {
    echo ""
    echo -e "${CYAN}🎯 Resumen de la Sincronización:${NC}"
    echo "=========================================="
    
    # Estado de Docker
    if docker images | grep -q $DOCKER_IMAGE; then
        echo -e "  🐳 Docker: ${GREEN}✅ Imagen construida${NC}"
        echo -e "     Usuario: ${DOCKER_USERNAME}"
        echo -e "     Imagen: ${DOCKER_IMAGE}"
    else
        echo -e "  🐳 Docker: ${RED}❌ Imagen no construida${NC}"
    fi
    
    # Estado de Heroku
    if heroku apps:info --app $APP_NAME &> /dev/null; then
        echo -e "  🚀 Heroku: ${GREEN}✅ App configurada${NC}"
        echo -e "     URL: $HEROKU_APP_URL"
    else
        echo -e "  🚀 Heroku: ${RED}❌ App no configurada${NC}"
    fi
    
    # Estado de Hugging Face
    if [ -n "$HUGGINGFACE_API_KEY" ]; then
        echo -e "  🤖 Hugging Face: ${GREEN}✅ API Key configurada${NC}"
    else
        echo -e "  🤖 Hugging Face: ${RED}❌ API Key no configurada${NC}"
    fi
    
    # Estado de GitHub
    if git remote get-url origin &> /dev/null; then
        echo -e "  📚 GitHub: ${GREEN}✅ Repositorio configurado${NC}"
        echo -e "     Repo: $GITHUB_REPO"
    else
        echo -e "  📚 GitHub: ${RED}❌ Repositorio no configurado${NC}"
    fi
}

# Función principal
main() {
    echo -e "${PURPLE}🚀 Iniciando sincronización completa del ecosistema...${NC}"
    echo ""
    
    # Verificaciones iniciales
    docker_status="❌"
    heroku_status="❌"
    huggingface_status="❌"
    github_status="❌"
    
    if check_docker; then
        docker_status="✅"
    fi
    
    if check_heroku; then
        heroku_status="✅"
    fi
    
    if check_huggingface; then
        huggingface_status="✅"
    fi
    
    if check_github; then
        github_status="✅"
    fi
    
    show_status "$docker_status" "$heroku_status" "$huggingface_status" "$github_status"
    
    # Sincronización
    echo -e "${PURPLE}🔄 Iniciando sincronización...${NC}"
    echo ""
    
    # Docker
    if [ "$docker_status" = "✅" ]; then
        if build_docker && test_docker; then
            echo -e "${GREEN}✅ Docker sincronizado${NC}"
            
            # Intentar hacer push a Docker Hub
            echo -e "${BLUE}💡 ¿Quieres hacer push a Docker Hub? (y/n)${NC}"
            read -r response
            if [[ "$response" =~ ^[Yy]$ ]]; then
                push_docker
            fi
        else
            echo -e "${RED}❌ Error en sincronización de Docker${NC}"
        fi
    fi
    
    # Heroku
    if [ "$heroku_status" = "✅" ]; then
        if deploy_heroku; then
            echo -e "${GREEN}✅ Heroku sincronizado${NC}"
        else
            echo -e "${RED}❌ Error en sincronización de Heroku${NC}"
        fi
    fi
    
    # Hugging Face
    if [ "$huggingface_status" = "✅" ]; then
        if sync_huggingface; then
            echo -e "${GREEN}✅ Hugging Face sincronizado${NC}"
        else
            echo -e "${RED}❌ Error en sincronización de Hugging Face${NC}"
        fi
    fi
    
    # Ecosystem Management
    if [ "$github_status" = "✅" ]; then
        echo -e "${PURPLE}🌍 Ejecutando gestión completa del ecosistema...${NC}"
        
        # Auditoría de paquetes
        if audit_packages; then
            echo -e "${GREEN}✅ Auditoría de paquetes completada${NC}"
        else
            echo -e "${YELLOW}⚠️ Advertencias en auditoría de paquetes${NC}"
        fi
        
        # Actualizar README
        if update_readme; then
            echo -e "${GREEN}✅ README actualizado${NC}"
        else
            echo -e "${YELLOW}⚠️ README no actualizado${NC}"
        fi
        
        # Sincronización final con GitHub
        if sync_github; then
            echo -e "${GREEN}✅ GitHub sincronizado con gestión del ecosistema${NC}"
        else
            echo -e "${RED}❌ Error en sincronización de GitHub${NC}"
        fi
    fi
    
    echo ""
    show_summary
    
    echo -e "${CYAN}🎉 Sincronización del ecosistema completada!${NC}"
    echo -e "${BLUE}🐳 Docker Hub: https://hub.docker.com/r/${DOCKER_USERNAME}${NC}"
}

# Ejecutar función principal
main "$@"
