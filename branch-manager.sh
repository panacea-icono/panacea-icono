#!/bin/bash

# 🌿 Branch Management Utility for PANACEA ICONO
# Helps manage branch creation, validation, and cleanup according to governance rules

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

SCRIPT_NAME="branch-manager.sh"

# Function to show usage
show_usage() {
    echo -e "${CYAN}🌿 PANACEA ICONO Branch Management Utility${NC}"
    echo "Usage: $SCRIPT_NAME <command> [options]"
    echo ""
    echo "Commands:"
    echo "  create <type> <name>    Create a new branch with proper naming"
    echo "  validate                Validate current branch name"
    echo "  cleanup                 Delete merged feature branches"
    echo "  list                    List branches with their status"
    echo "  protect <branch>        Show protection rules for branch"
    echo "  help                    Show this help message"
    echo ""
    echo "Branch types for 'create':"
    echo "  feature                 Create feature/name branch"
    echo "  bugfix                  Create bugfix/name branch"
    echo "  hotfix                  Create hotfix/name branch"
    echo "  release                 Create release/vX.X.X branch"
    echo ""
    echo "Examples:"
    echo "  $SCRIPT_NAME create feature user-authentication"
    echo "  $SCRIPT_NAME create bugfix login-error"
    echo "  $SCRIPT_NAME create hotfix security-patch"
    echo "  $SCRIPT_NAME create release v1.2.3"
    echo "  $SCRIPT_NAME validate"
    echo "  $SCRIPT_NAME cleanup"
    echo ""
}

# Function to validate branch name format
validate_branch_name() {
    local branch_name="$1"
    
    # Define allowed patterns
    local patterns=(
        "^main$"
        "^develop$"
        "^feature/[a-z0-9-]+$"
        "^bugfix/[a-z0-9-]+$"
        "^hotfix/[a-z0-9-]+$"
        "^release/v[0-9]+\.[0-9]+\.[0-9]+$"
        "^copilot/.*$"
    )
    
    for pattern in "${patterns[@]}"; do
        if [[ $branch_name =~ $pattern ]]; then
            return 0
        fi
    done
    
    return 1
}

# Function to create a new branch
create_branch() {
    local branch_type="$1"
    local branch_name="$2"
    
    if [ -z "$branch_type" ] || [ -z "$branch_name" ]; then
        echo -e "${RED}❌ Error: Branch type and name are required${NC}"
        echo -e "${YELLOW}Usage: $SCRIPT_NAME create <type> <name>${NC}"
        return 1
    fi
    
    # Sanitize branch name (lowercase, replace spaces with dashes)
    branch_name=$(echo "$branch_name" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | sed 's/[^a-z0-9-]//g')
    
    local full_branch_name
    local source_branch="develop"
    
    case $branch_type in
        feature)
            full_branch_name="feature/$branch_name"
            ;;
        bugfix)
            full_branch_name="bugfix/$branch_name"
            ;;
        hotfix)
            full_branch_name="hotfix/$branch_name"
            source_branch="main"
            ;;
        release)
            if [[ ! $branch_name =~ ^v[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
                echo -e "${RED}❌ Error: Release version must be in format vX.X.X${NC}"
                return 1
            fi
            full_branch_name="release/$branch_name"
            ;;
        *)
            echo -e "${RED}❌ Error: Invalid branch type '$branch_type'${NC}"
            echo -e "${YELLOW}Valid types: feature, bugfix, hotfix, release${NC}"
            return 1
            ;;
    esac
    
    # Validate the constructed branch name
    if ! validate_branch_name "$full_branch_name"; then
        echo -e "${RED}❌ Error: Generated branch name '$full_branch_name' is invalid${NC}"
        return 1
    fi
    
    # Check if branch already exists
    if git show-ref --verify --quiet refs/heads/$full_branch_name; then
        echo -e "${RED}❌ Error: Branch '$full_branch_name' already exists${NC}"
        return 1
    fi
    
    # Check if we're on the correct source branch
    local current_branch=$(git branch --show-current)
    if [ "$current_branch" != "$source_branch" ]; then
        echo -e "${YELLOW}⚠️ Warning: Currently on '$current_branch', but '$branch_type' should be created from '$source_branch'${NC}"
        echo -e "${BLUE}Switching to '$source_branch'...${NC}"
        git checkout "$source_branch"
        git pull origin "$source_branch"
    fi
    
    # Create and checkout the new branch
    echo -e "${BLUE}🌿 Creating branch: $full_branch_name${NC}"
    git checkout -b "$full_branch_name"
    
    echo -e "${GREEN}✅ Successfully created and switched to branch: $full_branch_name${NC}"
    echo -e "${YELLOW}💡 Next steps:${NC}"
    echo -e "   1. Make your changes"
    echo -e "   2. Commit with proper message format"
    echo -e "   3. Push: git push -u origin $full_branch_name"
    echo -e "   4. Create Pull Request to $source_branch"
    
    return 0
}

# Function to validate current branch
validate_current_branch() {
    local current_branch=$(git branch --show-current 2>/dev/null || echo "")
    
    if [ -z "$current_branch" ]; then
        echo -e "${RED}❌ Error: Unable to determine current branch${NC}"
        return 1
    fi
    
    echo -e "${BLUE}🌿 Validating current branch: $current_branch${NC}"
    
    if validate_branch_name "$current_branch"; then
        echo -e "${GREEN}✅ Branch name is valid${NC}"
        
        # Show branch type and recommendations
        case $current_branch in
            main)
                echo -e "${YELLOW}📋 Main branch - Protected, no direct pushes${NC}"
                ;;
            develop)
                echo -e "${YELLOW}📋 Development branch - Merge features here${NC}"
                ;;
            feature/*)
                echo -e "${BLUE}📋 Feature branch - Merge to develop when ready${NC}"
                ;;
            bugfix/*)
                echo -e "${BLUE}📋 Bugfix branch - Merge to develop when ready${NC}"
                ;;
            hotfix/*)
                echo -e "${RED}📋 Hotfix branch - Critical fix, merge to main and develop${NC}"
                ;;
            release/*)
                echo -e "${PURPLE}📋 Release branch - Prepare for production${NC}"
                ;;
        esac
        
        return 0
    else
        echo -e "${RED}❌ Branch name is invalid${NC}"
        echo -e "${YELLOW}💡 Valid patterns:${NC}"
        echo -e "   • main (protected)"
        echo -e "   • develop (protected)"
        echo -e "   • feature/your-feature-name"
        echo -e "   • bugfix/your-bug-description"
        echo -e "   • hotfix/your-hotfix-name"
        echo -e "   • release/vX.X.X"
        return 1
    fi
}

# Function to list branches with status
list_branches() {
    echo -e "${CYAN}🌿 Branch Status Overview${NC}"
    echo "================================"
    
    # Current branch
    local current_branch=$(git branch --show-current)
    echo -e "${PURPLE}Current: $current_branch${NC}"
    echo ""
    
    # Local branches
    echo -e "${BLUE}Local Branches:${NC}"
    git branch --format="%(refname:short)" | while read branch; do
        if validate_branch_name "$branch"; then
            echo -e "  ${GREEN}✅${NC} $branch"
        else
            echo -e "  ${RED}❌${NC} $branch (invalid name)"
        fi
    done
    
    echo ""
    
    # Remote branches
    echo -e "${BLUE}Remote Branches:${NC}"
    git branch -r --format="%(refname:lstrip=3)" | grep -v "HEAD" | head -10 | while read branch; do
        if validate_branch_name "$branch"; then
            echo -e "  ${GREEN}✅${NC} origin/$branch"
        else
            echo -e "  ${RED}❌${NC} origin/$branch (invalid name)"
        fi
    done
    
    # Show merged branches that can be cleaned up
    echo ""
    echo -e "${YELLOW}Merged branches (candidates for cleanup):${NC}"
    git branch --merged develop | grep -E "^\s*(feature/|bugfix/)" | head -5 | while read branch; do
        branch=$(echo "$branch" | xargs)
        echo -e "  ${YELLOW}🧹${NC} $branch"
    done
}

# Function to cleanup merged branches
cleanup_branches() {
    echo -e "${CYAN}🧹 Cleaning up merged branches...${NC}"
    
    # Switch to develop if we're on a feature branch
    local current_branch=$(git branch --show-current)
    if [[ $current_branch =~ ^(feature|bugfix)/ ]]; then
        echo -e "${BLUE}Switching to develop branch...${NC}"
        git checkout develop
        git pull origin develop
    fi
    
    # Find merged feature and bugfix branches
    local merged_branches=$(git branch --merged develop | grep -E "^\s*(feature/|bugfix/)" | sed 's/^[* ] //')
    
    if [ -z "$merged_branches" ]; then
        echo -e "${GREEN}✅ No merged feature/bugfix branches to clean up${NC}"
        return 0
    fi
    
    echo -e "${YELLOW}Found merged branches:${NC}"
    echo "$merged_branches" | while read branch; do
        echo -e "  • $branch"
    done
    
    echo ""
    echo -e "${YELLOW}⚠️ This will delete the branches above. Continue? (y/N)${NC}"
    read -r response
    
    if [[ "$response" =~ ^[Yy]$ ]]; then
        echo "$merged_branches" | while read branch; do
            if [ ! -z "$branch" ]; then
                echo -e "${BLUE}Deleting: $branch${NC}"
                git branch -d "$branch" 2>/dev/null || echo -e "${YELLOW}  ⚠️ Could not delete $branch${NC}"
            fi
        done
        echo -e "${GREEN}✅ Branch cleanup completed${NC}"
    else
        echo -e "${BLUE}Branch cleanup cancelled${NC}"
    fi
}

# Function to show protection rules for a branch
show_protection_rules() {
    local branch="${1:-$(git branch --show-current)}"
    
    echo -e "${CYAN}🛡️ Protection Rules for Branch: $branch${NC}"
    echo "=============================================="
    
    case $branch in
        main)
            echo -e "${RED}🔒 HIGHLY PROTECTED${NC}"
            echo "• Requires 2+ reviews"
            echo "• Requires status checks to pass"
            echo "• No direct pushes allowed"
            echo "• No force pushes allowed"
            echo "• No deletions allowed"
            echo "• Auto-deploys to production"
            ;;
        develop)
            echo -e "${YELLOW}🔒 PROTECTED${NC}"
            echo "• Requires 1+ review"
            echo "• Requires status checks to pass"
            echo "• Limited force pushes (admins only)"
            echo "• No deletions allowed"
            echo "• Auto-deploys to staging"
            ;;
        feature/*)
            echo -e "${BLUE}🔓 STANDARD PROTECTION${NC}"
            echo "• CI checks required"
            echo "• Can be deleted after merge"
            echo "• Should merge to develop"
            echo "• Regular pushes allowed"
            ;;
        hotfix/*)
            echo -e "${RED}🚨 HOTFIX PROTECTION${NC}"
            echo "• Expedited review process"
            echo "• Must merge to both main and develop"
            echo "• Creates version tag automatically"
            echo "• Triggers immediate deployment"
            ;;
        release/*)
            echo -e "${PURPLE}📦 RELEASE PROTECTION${NC}"
            echo "• No new features allowed"
            echo "• Only bugfixes permitted"
            echo "• Must merge to main and develop"
            echo "• Creates release tag"
            ;;
        *)
            echo -e "${YELLOW}⚠️ NON-STANDARD BRANCH${NC}"
            echo "• May not follow governance rules"
            echo "• Consider renaming to standard format"
            echo "• Limited CI/CD support"
            ;;
    esac
    
    echo ""
    echo -e "${BLUE}📋 See .github/branch-protection-rules.md for full details${NC}"
}

# Main function
main() {
    local command="${1:-help}"
    
    case $command in
        create)
            create_branch "$2" "$3"
            ;;
        validate)
            validate_current_branch
            ;;
        cleanup)
            cleanup_branches
            ;;
        list)
            list_branches
            ;;
        protect)
            show_protection_rules "$2"
            ;;
        help|--help)
            show_usage
            ;;
        *)
            echo -e "${RED}❌ Unknown command: $command${NC}"
            show_usage
            exit 1
            ;;
    esac
}

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo -e "${RED}❌ Error: Not in a git repository${NC}"
    exit 1
fi

# Run main function with all arguments
main "$@"