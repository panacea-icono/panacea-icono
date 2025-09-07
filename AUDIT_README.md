# 🔍 PANACEA ICONO Audit Tool

Comprehensive security, quality, and infrastructure auditing tool for the PANACEA ICONO repository.

## Features

### Security Auditing
- ✅ **Secret Detection**: Scans for exposed API keys, passwords, tokens, and secrets
- ✅ **Environment Variables**: Validates environment configuration and templates
- ✅ **Docker Security**: Checks container security best practices
- ✅ **Dependency Vulnerabilities**: Analyzes installed packages for security issues
- ✅ **API Security**: Validates FastAPI security features

### Code Quality Assessment
- ✅ **Code Formatting**: Checks Black, isort configuration
- ✅ **Documentation**: Validates README, requirements, and project documentation
- ✅ **Project Structure**: Analyzes file organization and best practices
- ✅ **Type Hints**: Measures type annotation coverage

### Infrastructure Analysis
- ✅ **Docker Setup**: Validates Docker, docker-compose, and .dockerignore
- ✅ **CI/CD Pipeline**: Analyzes GitHub Actions workflows
- ✅ **Deployment Configuration**: Checks Heroku and cloud deployment files
- ✅ **Health Monitoring**: Validates monitoring and logging setup

## Usage

### Basic Audit
```bash
python audit.py
```

### Custom Options
```bash
# Specify repository path
python audit.py --repo /path/to/repo

# Custom output file
python audit.py --output my_audit.json

# HTML report
python audit.py --output report.html --format html
```

### Command Line Options
- `--repo`: Repository path (default: current directory)
- `--output`: Custom output file name
- `--format`: Report format (`json` or `html`)

## Report Interpretation

### Overall Score Calculation
- **PASS**: 100 points per test
- **WARN**: 50 points per test  
- **FAIL**: 0 points per test
- **INFO**: Does not affect score

### Score Ranges
- 🟢 **90-100%**: Excellent - Production ready
- 🟡 **70-89%**: Good - Minor improvements needed
- 🟠 **50-69%**: Fair - Several issues to address
- 🔴 **<50%**: Poor - Significant security/quality issues

### Status Indicators
- ✅ **PASS**: Test passed successfully
- ❌ **FAIL**: Critical issue found
- ⚠️ **WARN**: Potential issue or improvement needed
- ℹ️ **INFO**: Informational message

## Output Files

### JSON Report (`audit_report.json`)
Structured data containing:
- Audit metadata (timestamp, duration, version)
- Summary statistics
- Detailed test results by category
- Actionable recommendations

### HTML Report (when using `--format html`)
Web-friendly report with:
- Visual indicators and styling
- Expandable sections
- Summary dashboard
- Detailed findings

## Integration

### CI/CD Pipeline
Add to GitHub Actions:
```yaml
- name: 🔍 Security & Quality Audit
  run: |
    python audit.py --output audit_results.json
    # Fail build if score < 80%
    python -c "
    import json
    with open('audit_results.json') as f:
        report = json.load(f)
    if report['summary']['overall_score'] < 0.8:
        exit(1)
    "
```

### Pre-commit Hook
```bash
#!/bin/sh
python audit.py --repo . --output /tmp/audit.json
```

## Customization

### Adding Custom Checks
Extend the `RepositoryAuditor` class:
```python
def audit_custom_requirements(self):
    # Your custom audit logic here
    self.log_result(
        "CUSTOM", "My Check", "PASS", 
        "Custom validation passed"
    )
```

### Configuration
Modify checks by editing the audit script:
- Adjust security patterns
- Add file type checks
- Customize scoring weights

## Troubleshooting

### Common Issues
1. **Permission errors**: Ensure audit.py is executable (`chmod +x audit.py`)
2. **Missing dependencies**: Install required packages from requirements.txt
3. **Path issues**: Use absolute paths for custom repository locations

### Debug Mode
Add debug output:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Healthcare Compliance Notes

This tool performs basic security and quality checks suitable for healthcare applications:

- Secrets management validation
- Environment variable security
- Container security best practices
- API security configurations
- Dependency vulnerability scanning

For full HIPAA/GDPR compliance, additional specialized auditing tools may be required.

## Contributing

To improve the audit tool:
1. Add new test categories in the appropriate audit methods
2. Enhance pattern matching for security scans
3. Improve reporting formats and visualizations
4. Add integration with external security tools

## Version History

- **v1.0.0**: Initial release with comprehensive security, quality, and infrastructure auditing
  - 13 core audit tests
  - JSON and HTML reporting
  - CLI interface
  - Integration support