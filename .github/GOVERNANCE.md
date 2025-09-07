# 🛡️ Governance & Rules Guide

## 📋 Overview

This document provides a comprehensive guide to the governance rules, branch protection policies, and ecosystem connection management for the PANACEA ICONO organization.

## 🌿 Branch Management

### Protected Branches

| Branch | Protection Level | Required Reviews | Auto-Deploy |
|--------|-----------------|------------------|-------------|
| `main` | High | 2+ | Production |
| `develop` | Medium | 1+ | Staging |
| `feature/*` | Low | CI only | None |
| `hotfix/*` | High | 1+ | Production |

### Naming Conventions

```bash
# ✅ Valid branch names
main
develop
feature/user-authentication
feature/ticket-123-payment-system
bugfix/login-error-fix
bugfix/issue-456-database-connection
hotfix/security-patch-v1.2.3
release/v2.0.0
copilot/fix-123abc-description

# ❌ Invalid branch names
test
temp
quick-fix
user_branch
Feature/NewLogin
```

### Branch Rules Enforcement

The repository automatically enforces branch rules through:

1. **GitHub Actions Workflow**: `.github/workflows/rules-enforcement.yml`
2. **Sync Script Validation**: Enhanced `sync_ecosystem.sh`
3. **Pre-commit Hooks**: (Optional) Local validation

## 🔗 Ecosystem Connections

### Service Integration Rules

#### 🐳 Docker Hub
- **Registry**: GitHub Container Registry (`ghcr.io`)
- **Auto-build**: On push to `main`/`develop`
- **Security**: Vulnerability scanning required
- **Retention**: 30 days for development images

#### 🚀 Heroku
- **Environments**: `prod`, `staging`, `dev`
- **Auto-deploy**: `main` → prod, `develop` → staging
- **Health checks**: Required before and after deployment
- **Rollback**: Automatic on health check failure

#### 🤖 Hugging Face
- **Organization**: `panacea-icono`
- **Model versioning**: Semantic versioning required
- **Documentation**: Model cards mandatory
- **Evaluation**: Automated model testing

#### 📚 GitHub
- **Branch protection**: Automated configuration
- **Secret scanning**: Enabled across all repos
- **Security advisories**: Auto-generated
- **Dependency updates**: Dependabot enabled

### Connection Health Monitoring

```bash
# Check all connections
./sync_ecosystem.sh --health-check

# Validate governance rules
./sync_ecosystem.sh --validate-governance

# Emergency disconnect
./sync_ecosystem.sh --emergency-mode
```

## 🔐 Security Rules

### Secret Management
- ❌ No hardcoded secrets in source code
- ✅ Use GitHub Secrets for sensitive data
- ✅ Environment-specific configuration
- ✅ Auto-rotation every 90 days

### Required Secrets
```yaml
# Production secrets
HEROKU_API_KEY: "Heroku deployment"
HUGGINGFACE_API_KEY: "AI models access"
DOCKER_REGISTRY_TOKEN: "Container registry"
DATABASE_URL: "Database connection"

# Optional secrets
OPENAI_API_KEY: "AI services"
TELEGRAM_BOT_TOKEN: "Bot integration"
MONITORING_WEBHOOK: "Alerts and notifications"
```

### Security Scanning
- **Static Analysis**: CodeQL on every PR
- **Dependency Check**: Dependabot alerts
- **Container Scanning**: Trivy for Docker images
- **Secret Scanning**: GitHub secret detection

## 📊 Compliance & Monitoring

### Automated Checks

1. **Branch Name Validation**
   - Regex pattern matching
   - Prohibited keywords detection
   - Convention enforcement

2. **Code Quality Gates**
   - Linting (pylint, black, isort)
   - Type checking (mypy)
   - Security analysis (bandit)

3. **Connection Validation**
   - Service availability checks
   - Authentication verification
   - Configuration validation

### Metrics & KPIs

| Metric | Target | Current |
|--------|--------|---------|
| Rule Compliance | 100% | ✅ |
| Security Score | >95% | ✅ |
| Connection Uptime | >99.9% | ✅ |
| Failed Deployments | <1% | ✅ |

## 🚨 Violation Handling

### Automatic Actions
- **Branch Rule Violation**: Block merge until fixed
- **Security Alert**: Immediate notification + PR block
- **Connection Failure**: Fallback to backup service
- **Quality Gate Failure**: Prevent deployment

### Manual Intervention
```bash
# Override in emergency (admin only)
git push --force-with-lease origin main

# Temporary rule bypass (with justification)
git commit -m "emergency: bypass rules - incident #123"

# Restore compliance
./sync_ecosystem.sh --restore-compliance
```

## 📋 Checklist for New Repositories

When creating a new repository in the ecosystem:

- [ ] Apply branch protection rules
- [ ] Configure required status checks
- [ ] Set up CI/CD workflows
- [ ] Add security scanning
- [ ] Configure secret scanning
- [ ] Enable dependency alerts
- [ ] Create connection documentation
- [ ] Test governance compliance
- [ ] Add to ecosystem sync script
- [ ] Document in main README

## 🔄 Rule Updates

### Process for Changing Rules
1. Create issue with rule change proposal
2. Discuss in team review meeting
3. Create PR with rule modifications
4. Test changes in staging environment
5. Get approval from 2+ maintainers
6. Deploy and monitor impact
7. Update documentation

### Version History
- `v1.0.0` (2025-09-07): Initial governance rules
- Future versions will be documented here

## 🆘 Emergency Procedures

### Service Outage
```bash
# Check service status
./sync_ecosystem.sh --status-check

# Switch to backup services
./sync_ecosystem.sh --emergency-mode --activate-backup

# Notify team
./sync_ecosystem.sh --notify-emergency "Service outage detected"
```

### Security Incident
```bash
# Immediate lockdown
./sync_ecosystem.sh --security-lockdown

# Revoke compromised access
./sync_ecosystem.sh --revoke-access --user "compromised-user"

# Generate incident report
./sync_ecosystem.sh --incident-report --severity "high"
```

## 📞 Support & Contacts

- **Technical Issues**: Create issue in relevant repository
- **Security Concerns**: security@iconosa.com
- **Rule Questions**: Team lead or maintainers
- **Emergency**: Follow incident response procedures

---

*This guide is living documentation and should be updated as the ecosystem evolves.*