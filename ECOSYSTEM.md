# 🌍 Ecosystem Management

This repository now includes comprehensive ecosystem management tools to handle all panacea-icono repositories from a central hub.

## ✨ Features

### GitHub Integration
- 📊 Repository listing and statistics
- 🐛 Issue creation and management across all repos
- 🍴 Fork management and synchronization
- 📈 Automated reporting and analytics

### Package Management
- 📦 Multi-language package detection (NPM, Python, Rust, Go)
- 🔍 Security vulnerability scanning
- 📋 Outdated package detection
- ⚡ Automated package updates

### Ecosystem Operations
- 🔄 Full ecosystem synchronization
- 📝 Automated README updates with live data
- 🛡️ Security auditing across all repositories
- 📊 Comprehensive ecosystem reporting

## 🚀 Quick Start

### Using the CLI Tool
```bash
# Show ecosystem status
./ecosystem_cli.sh status

# Generate comprehensive report
./ecosystem_cli.sh report

# Run full synchronization
./ecosystem_cli.sh sync

# Update README with latest data
./ecosystem_cli.sh readme

# Run security audit
./ecosystem_cli.sh audit

# List all repositories
./ecosystem_cli.sh repos

# Create an issue in a repository
./ecosystem_cli.sh issue repo-name "Issue title" "Issue description"
```

### Using Python Directly
```bash
# Generate ecosystem report
python3 ecosystem_manager.py report

# Run full synchronization
python3 ecosystem_manager.py sync

# Update README
python3 ecosystem_manager.py readme

# Check ecosystem status
python3 ecosystem_manager.py status
```

### Using the Web API
The FastAPI application now includes ecosystem management endpoints:

- `POST /ecosystem/manage` - Execute ecosystem operations
- `POST /ecosystem/issue` - Create issues in repositories
- `GET /ecosystem/repositories` - List all repositories

## ⚙️ Configuration

Copy the template configuration:
```bash
cp ecosystem_config.json.template ecosystem_config.json
```

Edit the configuration to set your preferences:
```json
{
  "github_org": "panacea-icono",
  "github_token": "your-github-token",
  "default_labels": ["enhancement", "ecosystem", "automation"],
  "audit_enabled": true,
  "auto_update_readme": true
}
```

## 🔧 Environment Variables

Set the following environment variables for full functionality:

```bash
export GITHUB_TOKEN="your-github-token"
export HUGGINGFACE_API_KEY="your-hf-token"
export HUGGINGFACE_EMAIL="your-email@example.com"
```

## 📊 Ecosystem Components

### Core Modules
- `ecosystem_manager.py` - Main orchestrator for all operations
- `github_integration.py` - GitHub API integration
- `package_manager.py` - Package management and auditing
- `ecosystem_cli.sh` - Command-line interface

### Enhanced Scripts
- `sync_ecosystem.sh` - Enhanced with ecosystem management
- `main.py` - FastAPI app with ecosystem endpoints

## 🔄 Automated Operations

The ecosystem manager can automatically:
- Update README with current repository data
- Generate daily/weekly reports
- Audit packages for security vulnerabilities
- Synchronize forks with upstream
- Create issues for maintenance tasks
- Commit and push changes

## 📈 Reports and Monitoring

Reports are automatically saved to the `reports/` directory:
- `ecosystem_report_YYYYMMDD_HHMMSS.json` - Comprehensive reports
- `ecosystem_sync_YYYYMMDD_HHMMSS.json` - Synchronization results
- `ecosystem.log` - Detailed operation logs

## 🛡️ Security Features

- Package vulnerability scanning
- Dependency audit across all languages
- Security alert generation
- Automated security reporting
- Safe update recommendations

## 🔌 Integration

The ecosystem manager integrates with:
- GitHub API for repository management
- NPM for JavaScript package auditing
- pip/safety for Python security scanning
- Hugging Face for AI model management
- Docker for containerization
- Heroku for deployment

This makes panacea-icono a true central hub for managing the entire ecosystem of repositories and services.