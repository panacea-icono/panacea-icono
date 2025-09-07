#!/bin/bash

# 🌍 PANACEA ICONO Ecosystem CLI
# Simple command-line interface for ecosystem management

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

# Display header
echo -e "${CYAN}🌍 PANACEA ICONO Ecosystem CLI${NC}"
echo "======================================"

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3 is required but not installed${NC}"
    exit 1
fi

# Function to show help
show_help() {
    echo -e "${BLUE}Available commands:${NC}"
    echo "  status    - Show ecosystem status"
    echo "  report    - Generate ecosystem report"
    echo "  sync      - Run full ecosystem synchronization"
    echo "  readme    - Update README with current data"
    echo "  audit     - Run package security audit"
    echo "  issue     - Create issue in repository"
    echo "  repos     - List all repositories"
    echo "  help      - Show this help message"
    echo ""
    echo -e "${BLUE}Examples:${NC}"
    echo "  $0 status"
    echo "  $0 sync"
    echo "  $0 issue my-repo 'Bug title' 'Bug description'"
    echo "  $0 audit"
}

# Function to show status
show_status() {
    echo -e "${YELLOW}📊 Checking ecosystem status...${NC}"
    python3 ecosystem_manager.py status
}

# Function to generate report
generate_report() {
    echo -e "${YELLOW}📊 Generating ecosystem report...${NC}"
    python3 ecosystem_manager.py report
}

# Function to run sync
run_sync() {
    echo -e "${YELLOW}🔄 Running full ecosystem synchronization...${NC}"
    python3 ecosystem_manager.py sync
}

# Function to update README
update_readme() {
    echo -e "${YELLOW}📝 Updating README...${NC}"
    python3 ecosystem_manager.py readme
}

# Function to run audit
run_audit() {
    echo -e "${YELLOW}🔍 Running security audit...${NC}"
    python3 ecosystem_manager.py audit
}

# Function to create issue
create_issue() {
    if [ $# -lt 3 ]; then
        echo -e "${RED}❌ Usage: $0 issue <repository> <title> [body]${NC}"
        exit 1
    fi
    
    local repo="$1"
    local title="$2"
    local body="${3:-}"
    
    echo -e "${YELLOW}🐛 Creating issue in ${repo}...${NC}"
    python3 ecosystem_manager.py issue --repo "$repo" --title "$title" --body "$body"
}

# Function to list repositories
list_repos() {
    echo -e "${YELLOW}📚 Listing repositories...${NC}"
    python3 -c "
from github_integration import GitHubManager
import json

manager = GitHubManager()
summary = manager.generate_ecosystem_summary()

print(f'📊 Total repositories: {summary.get(\"total_repos\", 0)}')
print(f'⭐ Total stars: {summary.get(\"statistics\", {}).get(\"total_stars\", 0)}')
print(f'🍴 Total forks: {summary.get(\"statistics\", {}).get(\"total_forks\", 0)}')
print()

for i, repo in enumerate(summary.get('repositories', [])[:10], 1):
    name = repo.get('name', '')
    desc = repo.get('description', 'No description')[:50]
    lang = repo.get('language', 'N/A')
    stars = repo.get('stars', 0)
    print(f'{i:2d}. {name} ({lang}) - ⭐{stars}')
    if desc and desc != 'No description':
        print(f'    {desc}...')
    print()
"
}

# Main command handling
case "${1:-help}" in
    "status")
        show_status
        ;;
    "report")
        generate_report
        ;;
    "sync")
        run_sync
        ;;
    "readme")
        update_readme
        ;;
    "audit")
        run_audit
        ;;
    "issue")
        shift
        create_issue "$@"
        ;;
    "repos")
        list_repos
        ;;
    "help"|"--help"|"-h")
        show_help
        ;;
    *)
        echo -e "${RED}❌ Unknown command: $1${NC}"
        echo ""
        show_help
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}✅ Command completed${NC}"