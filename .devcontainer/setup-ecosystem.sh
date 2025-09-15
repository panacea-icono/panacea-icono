#!/bin/bash

# 🚀 PANACEA ICONO Ecosystem Setup Script for Codespaces
# Sets up the integrated development environment with key repositories

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}🏥 PANACEA ICONO Ecosystem Development Setup${NC}"
echo "=============================================="

# Environment variables
ECOSYSTEM_DIR="${PANACEA_ECOSYSTEM_DIR:-/workspaces/ecosystem}"
MAIN_REPO="${PANACEA_MAIN_REPO:-/workspaces/panacea-icono}"

# Key repositories to clone for integrated development
declare -A KEY_REPOS=(
    ["Ton-telegram"]="https://github.com/panacea-icono/Ton-telegram.git"
    ["Dr_dela_TV"]="https://github.com/panacea-icono/Dr_dela_TV.git"
    ["Super-code-tasker"]="https://github.com/https-panacea-icono-org/Super-code-tasker.git"
    ["PANACEA-API-CENTRAL-CODEX"]="https://github.com/panacea-icono/PANACEA-API-CENTRAL-CODEX.git"
    ["gpt-local"]="https://github.com/panacea-icono/gpt-local.git"
    ["nextjs-with-supabase"]="https://github.com/panacea-icono/nextjs-with-supabase.git"
    ["MEDIOS-REDES"]="https://github.com/panacea-icono/MEDIOS-REDES.git"
    ["dr-de-la-tvr"]="https://github.com/panacea-icono/dr-de-la-tvr.git"
)

# Function to setup Python environment
setup_python_env() {
    echo -e "${YELLOW}🐍 Setting up Python environment...${NC}"
    
    cd "$MAIN_REPO"
    
    # Install dependencies
    if [ -f requirements.txt ]; then
        echo "📦 Installing Python dependencies..."
        pip install --user -r requirements.txt || echo "⚠️  Some packages may have failed to install"
    fi
    
    # Install development dependencies
    pip install --user black isort flake8 mypy pytest pytest-asyncio
    
    echo -e "${GREEN}✅ Python environment setup complete${NC}"
}

# Function to setup Node.js environment
setup_node_env() {
    echo -e "${YELLOW}📦 Setting up Node.js environment...${NC}"
    
    # Install global packages commonly used in the ecosystem
    npm install -g typescript ts-node prettier eslint @vercel/cli
    
    echo -e "${GREEN}✅ Node.js environment setup complete${NC}"
}

# Function to clone key repositories
clone_key_repos() {
    echo -e "${YELLOW}📚 Cloning key ecosystem repositories...${NC}"
    
    mkdir -p "$ECOSYSTEM_DIR"
    cd "$ECOSYSTEM_DIR"
    
    for repo_name in "${!KEY_REPOS[@]}"; do
        repo_url="${KEY_REPOS[$repo_name]}"
        
        if [ ! -d "$repo_name" ]; then
            echo -e "${BLUE}🔄 Cloning $repo_name...${NC}"
            git clone "$repo_url" "$repo_name" --depth 1 || {
                echo -e "${RED}❌ Failed to clone $repo_name${NC}"
                continue
            }
            echo -e "${GREEN}✅ $repo_name cloned successfully${NC}"
        else
            echo -e "${GREEN}✅ $repo_name already exists${NC}"
        fi
    done
    
    echo -e "${GREEN}✅ Key repositories setup complete${NC}"
}

# Function to setup workspace configuration
setup_workspace() {
    echo -e "${YELLOW}🔧 Setting up workspace configuration...${NC}"
    
    # Create workspace settings if not exists
    if [ ! -f "$MAIN_REPO/.vscode/settings.json" ]; then
        mkdir -p "$MAIN_REPO/.vscode"
        cat > "$MAIN_REPO/.vscode/settings.json" << 'EOF'
{
    "python.defaultInterpreterPath": "/usr/local/bin/python",
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.formatting.provider": "black",
    "editor.formatOnSave": true,
    "terminal.integrated.cwd": "/workspaces/panacea-icono",
    "files.exclude": {
        "**/__pycache__": true,
        "**/.pytest_cache": true,
        "**/node_modules": true,
        "**/.git": false
    }
}
EOF
    fi
    
    echo -e "${GREEN}✅ Workspace configuration complete${NC}"
}

# Function to create ecosystem navigation script
create_navigation_script() {
    echo -e "${YELLOW}🧭 Creating ecosystem navigation script...${NC}"
    
    cat > "$MAIN_REPO/navigate-ecosystem.sh" << 'EOF'
#!/bin/bash

# PANACEA ICONO Ecosystem Navigation Helper

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

ECOSYSTEM_DIR="${PANACEA_ECOSYSTEM_DIR:-/workspaces/ecosystem}"
MAIN_REPO="${PANACEA_MAIN_REPO:-/workspaces/panacea-icono}"

show_help() {
    echo -e "${CYAN}🏥 PANACEA ICONO Ecosystem Navigation${NC}"
    echo "====================================="
    echo ""
    echo "Available commands:"
    echo "  list              - List all cloned repositories"
    echo "  goto <repo>       - Navigate to a repository"
    echo "  status            - Show git status of all repos"
    echo "  pull-all          - Pull latest changes for all repos"
    echo "  sync              - Run ecosystem sync script"
    echo "  repos             - Show repository information"
    echo ""
}

list_repos() {
    echo -e "${CYAN}📚 Available Repositories:${NC}"
    echo "=========================="
    echo -e "${YELLOW}Main Repository:${NC}"
    echo "  • panacea-icono (current: $MAIN_REPO)"
    echo ""
    echo -e "${YELLOW}Ecosystem Repositories:${NC}"
    if [ -d "$ECOSYSTEM_DIR" ]; then
        for dir in "$ECOSYSTEM_DIR"/*; do
            if [ -d "$dir" ]; then
                repo_name=$(basename "$dir")
                echo "  • $repo_name ($dir)"
            fi
        done
    else
        echo "  No ecosystem repositories found. Run setup first."
    fi
}

goto_repo() {
    local repo="$1"
    if [ -z "$repo" ]; then
        echo "Usage: $0 goto <repository-name>"
        return 1
    fi
    
    if [ "$repo" = "panacea-icono" ] || [ "$repo" = "main" ]; then
        cd "$MAIN_REPO"
        echo -e "${GREEN}📂 Switched to main repository: $(pwd)${NC}"
    elif [ -d "$ECOSYSTEM_DIR/$repo" ]; then
        cd "$ECOSYSTEM_DIR/$repo"
        echo -e "${GREEN}📂 Switched to $repo: $(pwd)${NC}"
    else
        echo -e "${RED}❌ Repository '$repo' not found${NC}"
        return 1
    fi
}

show_status() {
    echo -e "${CYAN}📊 Repository Status:${NC}"
    echo "===================="
    
    echo -e "${YELLOW}Main Repository (panacea-icono):${NC}"
    cd "$MAIN_REPO"
    git status --porcelain | wc -l | xargs echo "  Changes:"
    
    if [ -d "$ECOSYSTEM_DIR" ]; then
        echo -e "${YELLOW}Ecosystem Repositories:${NC}"
        for dir in "$ECOSYSTEM_DIR"/*; do
            if [ -d "$dir/.git" ]; then
                repo_name=$(basename "$dir")
                cd "$dir"
                changes=$(git status --porcelain | wc -l)
                echo "  $repo_name: $changes changes"
            fi
        done
    fi
}

pull_all() {
    echo -e "${CYAN}🔄 Pulling latest changes...${NC}"
    echo "============================"
    
    echo -e "${YELLOW}Updating main repository...${NC}"
    cd "$MAIN_REPO"
    git pull origin main || echo "Failed to pull main repo"
    
    if [ -d "$ECOSYSTEM_DIR" ]; then
        echo -e "${YELLOW}Updating ecosystem repositories...${NC}"
        for dir in "$ECOSYSTEM_DIR"/*; do
            if [ -d "$dir/.git" ]; then
                repo_name=$(basename "$dir")
                echo "Pulling $repo_name..."
                cd "$dir"
                git pull || echo "Failed to pull $repo_name"
            fi
        done
    fi
}

run_sync() {
    echo -e "${CYAN}🔄 Running ecosystem sync...${NC}"
    cd "$MAIN_REPO"
    if [ -f sync_ecosystem.sh ]; then
        ./sync_ecosystem.sh
    else
        echo "Sync script not found"
    fi
}

case "$1" in
    "list")
        list_repos
        ;;
    "goto")
        goto_repo "$2"
        ;;
    "status")
        show_status
        ;;
    "pull-all")
        pull_all
        ;;
    "sync")
        run_sync
        ;;
    "repos")
        echo -e "${CYAN}🏢 PANACEA ICONO Ecosystem${NC}"
        echo "Hub: https://github.com/panacea-icono/Ton-telegram"
        echo "Docs: https://github.com/panacea-icono/Ton-telegram/tree/main/docs"
        echo "Website: https://panacea-icono.org"
        ;;
    *)
        show_help
        ;;
esac
EOF
    
    chmod +x "$MAIN_REPO/navigate-ecosystem.sh"
    
    echo -e "${GREEN}✅ Navigation script created${NC}"
    echo -e "${BLUE}💡 Use './navigate-ecosystem.sh' to navigate the ecosystem${NC}"
}

# Main setup process
main() {
    echo -e "${PURPLE}🚀 Starting ecosystem setup...${NC}"
    echo ""
    
    setup_python_env
    setup_node_env
    clone_key_repos
    setup_workspace
    create_navigation_script
    
    echo ""
    echo -e "${GREEN}🎉 PANACEA ICONO Ecosystem setup complete!${NC}"
    echo ""
    echo -e "${CYAN}Quick Start:${NC}"
    echo "  • Main repo: $MAIN_REPO"
    echo "  • Ecosystem: $ECOSYSTEM_DIR"
    echo "  • Navigation: ./navigate-ecosystem.sh"
    echo "  • Sync: ./sync_ecosystem.sh"
    echo ""
    echo -e "${BLUE}💡 Pro tip: Use 'source navigate-ecosystem.sh' for inline commands${NC}"
}

# Run main function
main "$@"