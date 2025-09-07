#!/bin/bash

# 🛡️ PANACEA ICONO - Validation Script for Governance Rules
# Quick validation of branch rules and ecosystem connections
# Usage: ./validate-rules.sh [--branch|--connections|--security|--all]

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

# Configuration
GOVERNANCE_VERSION="1.0.0"
SCRIPT_NAME="validate-rules.sh"

# Function to show usage
show_usage() {
    echo -e "${CYAN}🛡️ PANACEA ICONO Governance Validation${NC}"
    echo "Usage: $SCRIPT_NAME [option]"
    echo ""
    echo "Options:"
    echo "  --branch       Validate branch naming and protection rules"
    echo "  --connections  Validate ecosystem service connections"
    echo "  --security     Validate security rules and secret scanning"
    echo "  --all          Run all validations (default)"
    echo "  --help         Show this help message"
    echo ""
}

# Function to validate branch rules
validate_branch_rules() {
    echo -e "${PURPLE}🌿 Validating Branch Rules...${NC}"
    
    local violations=0
    
    # Get current branch
    local current_branch=$(git branch --show-current 2>/dev/null || echo "unknown")
    echo -e "${BLUE}Current branch: $current_branch${NC}"
    
    # Define allowed patterns
    local allowed_patterns=(
        "^main$"
        "^develop$" 
        "^feature/[a-z0-9-]+$"
        "^bugfix/[a-z0-9-]+$"
        "^hotfix/[a-z0-9-]+$"
        "^release/v[0-9]+\.[0-9]+\.[0-9]+$"
        "^copilot/.*$"
    )
    
    # Check branch name
    local valid=false
    for pattern in "${allowed_patterns[@]}"; do
        if [[ $current_branch =~ $pattern ]]; then
            valid=true
            echo -e "${GREEN}✅ Branch name valid: matches pattern '$pattern'${NC}"
            break
        fi
    done
    
    if [ "$valid" = false ]; then
        echo -e "${RED}❌ Invalid branch name: $current_branch${NC}"
        echo -e "${YELLOW}💡 Allowed patterns:${NC}"
        printf '%s\n' "${allowed_patterns[@]}"
        ((violations++))
    fi
    
    # Check for prohibited commit messages in recent history
    echo -e "${BLUE}Checking recent commit messages...${NC}"
    local prohibited=("YOLO" "quick fix" "temp" "hack" "WIP" "TODO: remove")
    
    git log --oneline -10 | while read commit; do
        for word in "${prohibited[@]}"; do
            if [[ $commit =~ $word ]]; then
                echo -e "${YELLOW}⚠️ Found discouraged keyword '$word' in: $commit${NC}"
            fi
        done
    done
    
    # Check for required files
    local required_files=(".github/branch-protection-rules.md" ".github/workflows/rules-enforcement.yml")
    
    for file in "${required_files[@]}"; do
        if [ -f "$file" ]; then
            echo -e "${GREEN}✅ Required file found: $file${NC}"
        else
            echo -e "${RED}❌ Missing required file: $file${NC}"
            ((violations++))
        fi
    done
    
    if [ $violations -eq 0 ]; then
        echo -e "${GREEN}🌿 Branch rules validation: PASSED${NC}"
        return 0
    else
        echo -e "${RED}🌿 Branch rules validation: FAILED ($violations violations)${NC}"
        return 1
    fi
}

# Function to validate connections
validate_connections() {
    echo -e "${PURPLE}🔗 Validating Ecosystem Connections...${NC}"
    
    local connection_errors=0
    
    # GitHub connection
    if git remote get-url origin &> /dev/null; then
        local repo_url=$(git remote get-url origin)
        echo -e "${GREEN}✅ GitHub connection: OK${NC}"
        echo -e "   📚 Repository: $repo_url${NC}"
        
        # Test GitHub API
        if curl -s --max-time 5 https://api.github.com/user > /dev/null 2>&1; then
            echo -e "${GREEN}✅ GitHub API: Accessible${NC}"
        else
            echo -e "${YELLOW}⚠️ GitHub API: Limited access (may need authentication)${NC}"
        fi
    else
        echo -e "${RED}❌ GitHub connection: No remote origin${NC}"
        ((connection_errors++))
    fi
    
    # Docker configuration
    if [ -f "Dockerfile" ]; then
        echo -e "${GREEN}✅ Docker configuration: Dockerfile found${NC}"
        
        # Check Docker best practices
        if grep -q "^USER " Dockerfile; then
            echo -e "${GREEN}✅ Docker security: Non-root user configured${NC}"
        else
            echo -e "${YELLOW}⚠️ Docker security: No USER instruction found${NC}"
        fi
        
        if grep -q "^EXPOSE " Dockerfile; then
            local ports=$(grep "^EXPOSE " Dockerfile | awk '{print $2}')
            echo -e "${BLUE}📡 Docker ports exposed: $ports${NC}"
        fi
    else
        echo -e "${RED}❌ Docker configuration: No Dockerfile found${NC}"
        ((connection_errors++))
    fi
    
    # Heroku configuration
    if [ -n "${HEROKU_API_KEY:-}" ]; then
        echo -e "${GREEN}✅ Heroku: API key configured${NC}"
    else
        echo -e "${YELLOW}⚠️ Heroku: No API key (set HEROKU_API_KEY)${NC}"
    fi
    
    if [ -f "Procfile" ]; then
        echo -e "${GREEN}✅ Heroku: Procfile found${NC}"
        echo -e "   📝 Processes: $(cat Procfile | cut -d':' -f1 | tr '\n' ' ')${NC}"
    else
        echo -e "${YELLOW}⚠️ Heroku: No Procfile found${NC}"
    fi
    
    # Hugging Face configuration
    if [ -n "${HUGGINGFACE_API_KEY:-}" ]; then
        echo -e "${GREEN}✅ Hugging Face: API key configured${NC}"
    else
        echo -e "${YELLOW}⚠️ Hugging Face: No API key (set HUGGINGFACE_API_KEY)${NC}"
    fi
    
    if [ -f "huggingface_config.py" ]; then
        echo -e "${GREEN}✅ Hugging Face: Configuration file found${NC}"
    else
        echo -e "${YELLOW}⚠️ Hugging Face: No configuration file${NC}"
    fi
    
    # Test external connectivity
    echo -e "${BLUE}🌐 Testing external connectivity...${NC}"
    
    local services=("https://api.github.com" "https://heroku.com" "https://huggingface.co")
    
    for service in "${services[@]}"; do
        if curl -s --max-time 5 "$service" > /dev/null 2>&1; then
            echo -e "${GREEN}✅ $service: Accessible${NC}"
        else
            echo -e "${RED}❌ $service: Not accessible${NC}"
            ((connection_errors++))
        fi
    done
    
    if [ $connection_errors -eq 0 ]; then
        echo -e "${GREEN}🔗 Connection validation: PASSED${NC}"
        return 0
    else
        echo -e "${RED}🔗 Connection validation: FAILED ($connection_errors errors)${NC}"
        return 1
    fi
}

# Function to validate security
validate_security() {
    echo -e "${PURPLE}🔐 Validating Security Rules...${NC}"
    
    local security_issues=0
    
    # Check for secrets in code
    echo -e "${BLUE}🔍 Scanning for potential secrets...${NC}"
    
    local secret_patterns=(
        "api[_-]?key[\"'\s]*[:=][\"'\s]*[a-zA-Z0-9]+"
        "password[\"'\s]*[:=][\"'\s]*[a-zA-Z0-9]+"
        "secret[\"'\s]*[:=][\"'\s]*[a-zA-Z0-9]+"
        "token[\"'\s]*[:=][\"'\s]*[a-zA-Z0-9]+"
    )
    
    for pattern in "${secret_patterns[@]}"; do
        if grep -r -E "$pattern" . --exclude-dir=.git --exclude="*.md" --exclude="validate-rules.sh" --exclude="*rules*" >/dev/null 2>&1; then
            echo -e "${RED}❌ Potential secret found matching: $pattern${NC}"
            ((security_issues++))
        fi
    done
    
    if [ $security_issues -eq 0 ]; then
        echo -e "${GREEN}✅ No secrets found in source code${NC}"
    fi
    
    # Check .gitignore
    if [ -f ".gitignore" ]; then
        echo -e "${GREEN}✅ .gitignore file found${NC}"
        
        local required_ignores=(".env" "*.log" "__pycache__" "node_modules" "*.tmp")
        local missing_ignores=0
        
        for ignore in "${required_ignores[@]}"; do
            if grep -q "$ignore" .gitignore; then
                echo -e "${GREEN}  ✅ $ignore ignored${NC}"
            else
                echo -e "${YELLOW}  ⚠️ $ignore not in .gitignore${NC}"
                ((missing_ignores++))
            fi
        done
        
        if [ $missing_ignores -gt 0 ]; then
            echo -e "${YELLOW}⚠️ Consider adding missing patterns to .gitignore${NC}"
        fi
    else
        echo -e "${RED}❌ No .gitignore file found${NC}"
        ((security_issues++))
    fi
    
    # Check for security workflow
    if [ -f ".github/workflows/rules-enforcement.yml" ]; then
        echo -e "${GREEN}✅ Security workflow configured${NC}"
    else
        echo -e "${YELLOW}⚠️ No security enforcement workflow${NC}"
    fi
    
    if [ $security_issues -eq 0 ]; then
        echo -e "${GREEN}🔐 Security validation: PASSED${NC}"
        return 0
    else
        echo -e "${RED}🔐 Security validation: FAILED ($security_issues issues)${NC}"
        return 1
    fi
}

# Main function
main() {
    echo -e "${CYAN}🛡️ PANACEA ICONO Governance Validation${NC}"
    echo -e "${BLUE}Version: $GOVERNANCE_VERSION${NC}"
    echo "============================================="
    echo ""
    
    local option="${1:-all}"
    local total_errors=0
    
    case $option in
        --branch)
            validate_branch_rules || ((total_errors++))
            ;;
        --connections)
            validate_connections || ((total_errors++))
            ;;
        --security)
            validate_security || ((total_errors++))
            ;;
        --all)
            validate_branch_rules || ((total_errors++))
            echo ""
            validate_connections || ((total_errors++))
            echo ""
            validate_security || ((total_errors++))
            ;;
        --help)
            show_usage
            exit 0
            ;;
        *)
            echo -e "${RED}❌ Unknown option: $option${NC}"
            show_usage
            exit 1
            ;;
    esac
    
    echo ""
    echo "============================================="
    
    if [ $total_errors -eq 0 ]; then
        echo -e "${GREEN}🎉 All validations passed successfully!${NC}"
        exit 0
    else
        echo -e "${RED}❌ $total_errors validation(s) failed${NC}"
        echo -e "${YELLOW}💡 Review the issues above and fix before proceeding${NC}"
        exit 1
    fi
}

# Run main function with all arguments
main "$@"