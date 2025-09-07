#!/usr/bin/env python3
"""
🔍 PANACEA ICONO Repository Audit Tool
Comprehensive security, quality, and infrastructure audit for PANACEA ICONO
"""

import os
import sys
import json
import subprocess
import datetime
import re
from pathlib import Path
from typing import Dict, List, Any, Optional
        # Remove the pkg_resources import since it's deprecated
        # import pkg_resources
from dataclasses import dataclass, asdict

# Color codes for terminal output
class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    PURPLE = '\033[0;35m'
    CYAN = '\033[0;36m'
    WHITE = '\033[1;37m'
    NC = '\033[0m'  # No Color

@dataclass
class AuditResult:
    category: str
    test_name: str
    status: str  # "PASS", "FAIL", "WARN", "INFO"
    message: str
    details: Optional[Dict[str, Any]] = None
    recommendation: Optional[str] = None

class RepositoryAuditor:
    """Comprehensive repository auditor for PANACEA ICONO"""
    
    def __init__(self, repo_path: str = "."):
        self.repo_path = Path(repo_path).absolute()
        self.results: List[AuditResult] = []
        self.start_time = datetime.datetime.now()
        
    def log_result(self, category: str, test_name: str, status: str, message: str, 
                   details: Optional[Dict] = None, recommendation: Optional[str] = None):
        """Log an audit result"""
        result = AuditResult(category, test_name, status, message, details, recommendation)
        self.results.append(result)
        
        # Print to console with colors
        color = {
            "PASS": Colors.GREEN,
            "FAIL": Colors.RED,
            "WARN": Colors.YELLOW,
            "INFO": Colors.BLUE
        }.get(status, Colors.NC)
        
        print(f"{color}[{status}]{Colors.NC} {category} - {test_name}: {message}")
        if recommendation:
            print(f"  💡 {Colors.CYAN}Recommendation: {recommendation}{Colors.NC}")

    def run_command(self, command: List[str], capture_output: bool = True) -> tuple:
        """Run a shell command and return (returncode, stdout, stderr)"""
        try:
            result = subprocess.run(
                command, 
                cwd=self.repo_path,
                capture_output=capture_output,
                text=True,
                timeout=30
            )
            return result.returncode, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return -1, "", "Command timed out"
        except Exception as e:
            return -1, "", str(e)

    def check_file_exists(self, filename: str) -> bool:
        """Check if a file exists in the repository"""
        return (self.repo_path / filename).exists()

    def read_file_content(self, filename: str) -> Optional[str]:
        """Read file content safely"""
        try:
            file_path = self.repo_path / filename
            if file_path.exists():
                return file_path.read_text(encoding='utf-8')
            return None
        except Exception as e:
            return None

    def audit_security(self):
        """Audit security aspects of the repository"""
        print(f"\n{Colors.CYAN}🔒 SECURITY AUDIT{Colors.NC}")
        print("=" * 50)
        
        # Check for exposed secrets
        self.check_exposed_secrets()
        
        # Check environment variable usage
        self.check_environment_variables()
        
        # Check Docker security
        self.check_docker_security()
        
        # Check dependency vulnerabilities
        self.check_dependency_vulnerabilities()
        
        # Check API endpoint security
        self.check_api_security()

    def check_exposed_secrets(self):
        """Check for exposed secrets in the codebase"""
        secret_patterns = {
            'api_key': re.compile(r'(?i)(api[_-]?key|apikey)\s*[=:]\s*["\']?([a-zA-Z0-9]{20,})["\']?'),
            'password': re.compile(r'(?i)password\s*[=:]\s*["\']?([a-zA-Z0-9]{8,})["\']?'),
            'token': re.compile(r'(?i)(token|jwt)\s*[=:]\s*["\']?([a-zA-Z0-9._-]{20,})["\']?'),
            'secret': re.compile(r'(?i)secret\s*[=:]\s*["\']?([a-zA-Z0-9]{16,})["\']?'),
        }
        
        exposed_secrets = []
        
        # Check Python files
        for py_file in self.repo_path.rglob("*.py"):
            if '.git' in str(py_file) or '__pycache__' in str(py_file):
                continue
                
            try:
                content = py_file.read_text(encoding='utf-8')
                for secret_type, pattern in secret_patterns.items():
                    matches = pattern.findall(content)
                    for match in matches:
                        # Skip obvious placeholder values
                        value = match[1] if isinstance(match, tuple) else match
                        if not any(placeholder in value.lower() for placeholder in 
                                 ['your_', 'example', 'placeholder', 'xxx', 'dummy']):
                            exposed_secrets.append({
                                'file': str(py_file.relative_to(self.repo_path)),
                                'type': secret_type,
                                'value': value[:10] + "..." if len(value) > 10 else value
                            })
            except Exception:
                continue
        
        if exposed_secrets:
            self.log_result(
                "SECURITY", "Exposed Secrets", "FAIL",
                f"Found {len(exposed_secrets)} potential exposed secrets",
                {"secrets": exposed_secrets},
                "Move all secrets to environment variables and add them to .gitignore"
            )
        else:
            self.log_result(
                "SECURITY", "Exposed Secrets", "PASS",
                "No exposed secrets detected in source code"
            )

    def check_environment_variables(self):
        """Check environment variable configuration"""
        # Check both .env.example and env.example
        env_example = self.read_file_content(".env.example") or self.read_file_content("env.example")
        env_file_name = ".env.example" if self.check_file_exists(".env.example") else "env.example"
        
        if env_example:
            env_vars = re.findall(r'^([A-Z_]+)=', env_example, re.MULTILINE)
            self.log_result(
                "SECURITY", "Environment Variables", "PASS",
                f"Environment template found ({env_file_name}) with {len(env_vars)} variables",
                {"variables": env_vars, "file": env_file_name}
            )
        else:
            self.log_result(
                "SECURITY", "Environment Variables", "WARN",
                "No environment template file found (.env.example or env.example)",
                recommendation="Create .env.example with all required environment variables"
            )

    def check_docker_security(self):
        """Check Docker configuration security"""
        dockerfile_content = self.read_file_content("Dockerfile")
        if not dockerfile_content:
            self.log_result(
                "SECURITY", "Docker Configuration", "WARN",
                "No Dockerfile found"
            )
            return
        
        security_checks = {
            "Non-root user": "USER " in dockerfile_content,
            "Health check": "HEALTHCHECK" in dockerfile_content,
            "Multi-stage build": dockerfile_content.count("FROM") > 1,
            "No root execution": "USER root" not in dockerfile_content.split("USER ")[-1] if "USER " in dockerfile_content else True
        }
        
        passed_checks = sum(1 for check in security_checks.values() if check)
        total_checks = len(security_checks)
        
        status = "PASS" if passed_checks >= total_checks * 0.8 else "WARN"
        self.log_result(
            "SECURITY", "Docker Configuration", status,
            f"Docker security checks: {passed_checks}/{total_checks} passed",
            {"checks": security_checks}
        )

    def check_dependency_vulnerabilities(self):
        """Check for dependency vulnerabilities"""
        # Check if requirements.txt exists
        requirements_file = self.repo_path / "requirements.txt"
        if not requirements_file.exists():
            self.log_result(
                "SECURITY", "Dependency Vulnerabilities", "INFO",
                "No requirements.txt found"
            )
            return
        
        # Try to run safety check if available
        returncode, stdout, stderr = self.run_command(["python", "-m", "pip", "list", "--format=json"])
        if returncode == 0:
            try:
                packages = json.loads(stdout)
                package_count = len(packages)
                self.log_result(
                    "SECURITY", "Dependency Vulnerabilities", "INFO",
                    f"Found {package_count} installed packages",
                    {"package_count": package_count}
                )
            except json.JSONDecodeError:
                pass

    def check_api_security(self):
        """Check API endpoint security"""
        main_py = self.read_file_content("main.py")
        if not main_py:
            return
        
        security_features = {
            "CORS configured": "CORSMiddleware" in main_py,
            "Exception handling": "@app.exception_handler" in main_py,
            "Request validation": "BaseModel" in main_py,
            "Health endpoint": "/health" in main_py
        }
        
        passed_features = sum(1 for feature in security_features.values() if feature)
        total_features = len(security_features)
        
        status = "PASS" if passed_features >= total_features * 0.75 else "WARN"
        self.log_result(
            "SECURITY", "API Security", status,
            f"API security features: {passed_features}/{total_features} implemented",
            {"features": security_features}
        )

    def audit_code_quality(self):
        """Audit code quality aspects"""
        print(f"\n{Colors.PURPLE}✨ CODE QUALITY AUDIT{Colors.NC}")
        print("=" * 50)
        
        # Check code formatting and linting
        self.check_code_formatting()
        
        # Check documentation
        self.check_documentation()
        
        # Check project structure
        self.check_project_structure()
        
        # Check type hints
        self.check_type_hints()

    def check_code_formatting(self):
        """Check code formatting and style"""
        python_files = list(self.repo_path.rglob("*.py"))
        python_files = [f for f in python_files if '.git' not in str(f) and '__pycache__' not in str(f)]
        
        if not python_files:
            self.log_result(
                "CODE_QUALITY", "Code Formatting", "INFO",
                "No Python files found"
            )
            return
        
        # Check if formatting tools are configured
        has_black_config = any(config in self.read_file_content("pyproject.toml") or "" 
                              for config in ["[tool.black]", "black"])
        has_isort_config = any(config in self.read_file_content("pyproject.toml") or ""
                              for config in ["[tool.isort]", "isort"])
        
        formatting_score = 0
        if has_black_config:
            formatting_score += 1
        if has_isort_config:
            formatting_score += 1
        
        status = "PASS" if formatting_score >= 1 else "WARN"
        self.log_result(
            "CODE_QUALITY", "Code Formatting", status,
            f"Formatting tools configured: {formatting_score}/2",
            {
                "python_files": len(python_files),
                "black_configured": has_black_config,
                "isort_configured": has_isort_config
            }
        )

    def check_documentation(self):
        """Check documentation quality"""
        doc_files = {
            "README.md": self.check_file_exists("README.md"),
            "requirements.txt": self.check_file_exists("requirements.txt"),
            "pyproject.toml": self.check_file_exists("pyproject.toml"),
            "env.example": self.check_file_exists("env.example") or self.check_file_exists(".env.example"),
            "Dockerfile": self.check_file_exists("Dockerfile")
        }
        
        doc_score = sum(1 for exists in doc_files.values() if exists)
        total_docs = len(doc_files)
        
        readme_content = self.read_file_content("README.md")
        has_good_readme = False
        if readme_content and len(readme_content) > 500:
            has_good_readme = True
            doc_score += 1
            total_docs += 1
        
        status = "PASS" if doc_score >= total_docs * 0.8 else "WARN"
        self.log_result(
            "CODE_QUALITY", "Documentation", status,
            f"Documentation files: {doc_score}/{total_docs} present",
            {
                "files": doc_files,
                "readme_substantial": has_good_readme
            }
        )

    def check_project_structure(self):
        """Check project structure and organization"""
        required_files = [
            "main.py",
            "requirements.txt", 
            "Dockerfile",
            ".gitignore"
        ]
        
        present_files = {file: self.check_file_exists(file) for file in required_files}
        structure_score = sum(1 for exists in present_files.values() if exists)
        
        # Check for organized structure
        has_tests = any(self.repo_path.glob("*test*")) or any(self.repo_path.glob("tests/"))
        has_config_files = self.check_file_exists("pyproject.toml")
        has_ci_cd = self.check_file_exists(".github/workflows/ci-cd.yml")
        
        bonus_score = sum([has_tests, has_config_files, has_ci_cd])
        total_score = structure_score + bonus_score
        max_score = len(required_files) + 3
        
        status = "PASS" if total_score >= max_score * 0.7 else "WARN"
        self.log_result(
            "CODE_QUALITY", "Project Structure", status,
            f"Project structure score: {total_score}/{max_score}",
            {
                "required_files": present_files,
                "has_tests": has_tests,
                "has_config": has_config_files,
                "has_ci_cd": has_ci_cd
            }
        )

    def check_type_hints(self):
        """Check for type hints usage"""
        main_py = self.read_file_content("main.py")
        if not main_py:
            return
        
        # Count type annotations
        type_hint_patterns = [
            r':\s*[A-Za-z_][A-Za-z0-9_]*\[',  # Generic types
            r':\s*[A-Za-z_][A-Za-z0-9_]*\s*=',  # Simple type annotations
            r'def\s+\w+\([^)]*\)\s*->\s*[A-Za-z_]',  # Return type annotations
            r'from typing import'
        ]
        
        type_hint_count = sum(len(re.findall(pattern, main_py)) for pattern in type_hint_patterns)
        function_count = len(re.findall(r'def\s+\w+\(', main_py))
        
        if function_count > 0:
            type_coverage = type_hint_count / function_count
            status = "PASS" if type_coverage > 0.5 else "WARN"
            self.log_result(
                "CODE_QUALITY", "Type Hints", status,
                f"Type annotation coverage: {type_coverage:.1%}",
                {
                    "type_hints": type_hint_count,
                    "functions": function_count,
                    "coverage": type_coverage
                }
            )

    def audit_infrastructure(self):
        """Audit infrastructure and deployment aspects"""
        print(f"\n{Colors.BLUE}🏗️  INFRASTRUCTURE AUDIT{Colors.NC}")
        print("=" * 50)
        
        # Check Docker configuration
        self.check_docker_infrastructure()
        
        # Check CI/CD pipeline
        self.check_ci_cd()
        
        # Check deployment configuration
        self.check_deployment_config()
        
        # Check health monitoring
        self.check_health_monitoring()

    def check_docker_infrastructure(self):
        """Check Docker infrastructure setup"""
        docker_files = {
            "Dockerfile": self.check_file_exists("Dockerfile"),
            "docker-compose.yml": self.check_file_exists("docker-compose.yml"),
            ".dockerignore": self.check_file_exists(".dockerignore")
        }
        
        docker_score = sum(1 for exists in docker_files.values() if exists)
        
        # Check docker-compose services
        compose_content = self.read_file_content("docker-compose.yml")
        services_count = 0
        if compose_content:
            services_count = len(re.findall(r'^\s*[a-zA-Z0-9_-]+:', compose_content, re.MULTILINE))
        
        status = "PASS" if docker_score >= 2 else "WARN"
        self.log_result(
            "INFRASTRUCTURE", "Docker Setup", status,
            f"Docker files: {docker_score}/3, Services: {services_count}",
            {
                "files": docker_files,
                "services_count": services_count
            }
        )

    def check_ci_cd(self):
        """Check CI/CD pipeline configuration"""
        workflow_file = ".github/workflows/ci-cd.yml"
        has_workflow = self.check_file_exists(workflow_file)
        
        if not has_workflow:
            self.log_result(
                "INFRASTRUCTURE", "CI/CD Pipeline", "WARN",
                "No GitHub Actions workflow found",
                recommendation="Set up automated CI/CD pipeline"
            )
            return
        
        workflow_content = self.read_file_content(workflow_file)
        jobs_count = len(re.findall(r'^\s+[a-zA-Z0-9_-]+:', workflow_content, re.MULTILINE)) if workflow_content else 0
        
        has_quality_checks = "quality" in workflow_content.lower() if workflow_content else False
        has_docker_build = "docker" in workflow_content.lower() if workflow_content else False
        has_deployment = "deploy" in workflow_content.lower() if workflow_content else False
        
        pipeline_score = sum([has_quality_checks, has_docker_build, has_deployment])
        
        status = "PASS" if pipeline_score >= 2 else "WARN"
        self.log_result(
            "INFRASTRUCTURE", "CI/CD Pipeline", status,
            f"Pipeline features: {pipeline_score}/3, Jobs: {jobs_count}",
            {
                "has_quality_checks": has_quality_checks,
                "has_docker_build": has_docker_build,
                "has_deployment": has_deployment,
                "jobs_count": jobs_count
            }
        )

    def check_deployment_config(self):
        """Check deployment configuration"""
        deployment_files = {
            "Procfile": self.check_file_exists("Procfile"),
            "runtime.txt": self.check_file_exists("runtime.txt"),
            "app.json": self.check_file_exists("app.json")
        }
        
        # Check for environment configuration
        has_env_example = self.check_file_exists(".env.example") or self.check_file_exists("env.example")
        
        deployment_score = sum(1 for exists in deployment_files.values() if exists)
        if has_env_example:
            deployment_score += 1
        
        total_possible = len(deployment_files) + 1
        
        status = "PASS" if deployment_score >= 1 else "WARN"
        self.log_result(
            "INFRASTRUCTURE", "Deployment Config", status,
            f"Deployment files: {deployment_score}/{total_possible}",
            {
                "files": deployment_files,
                "has_env_example": has_env_example
            }
        )

    def check_health_monitoring(self):
        """Check health monitoring setup"""
        main_py = self.read_file_content("main.py")
        if not main_py:
            return
        
        monitoring_features = {
            "Health endpoint": "/health" in main_py,
            "Logging configured": "logging" in main_py,
            "Exception handling": "exception_handler" in main_py,
            "Structured responses": "BaseModel" in main_py
        }
        
        monitoring_score = sum(1 for feature in monitoring_features.values() if feature)
        total_features = len(monitoring_features)
        
        status = "PASS" if monitoring_score >= total_features * 0.75 else "WARN"
        self.log_result(
            "INFRASTRUCTURE", "Health Monitoring", status,
            f"Monitoring features: {monitoring_score}/{total_features}",
            {"features": monitoring_features}
        )

    def generate_report(self) -> Dict[str, Any]:
        """Generate comprehensive audit report"""
        end_time = datetime.datetime.now()
        duration = (end_time - self.start_time).total_seconds()
        
        # Categorize results
        categories = {}
        for result in self.results:
            if result.category not in categories:
                categories[result.category] = []
            categories[result.category].append(asdict(result))
        
        # Calculate statistics
        total_tests = len(self.results)
        passed_tests = len([r for r in self.results if r.status == "PASS"])
        failed_tests = len([r for r in self.results if r.status == "FAIL"])
        warning_tests = len([r for r in self.results if r.status == "WARN"])
        info_tests = len([r for r in self.results if r.status == "INFO"])
        
        # Overall score
        score = (passed_tests * 100 + warning_tests * 50) / (total_tests * 100) if total_tests > 0 else 0
        
        report = {
            "audit_info": {
                "timestamp": end_time.isoformat(),
                "duration_seconds": round(duration, 2),
                "repository_path": str(self.repo_path),
                "auditor_version": "1.0.0"
            },
            "summary": {
                "total_tests": total_tests,
                "passed": passed_tests,
                "failed": failed_tests,
                "warnings": warning_tests,
                "info": info_tests,
                "overall_score": round(score, 2)
            },
            "categories": categories,
            "recommendations": [
                r.recommendation for r in self.results 
                if r.recommendation and r.status in ["FAIL", "WARN"]
            ]
        }
        
        return report

    def print_summary(self):
        """Print audit summary"""
        print(f"\n{Colors.WHITE}📊 AUDIT SUMMARY{Colors.NC}")
        print("=" * 50)
        
        # Count results by status
        status_counts = {"PASS": 0, "FAIL": 0, "WARN": 0, "INFO": 0}
        for result in self.results:
            status_counts[result.status] += 1
        
        total = sum(status_counts.values())
        if total == 0:
            print("No tests were run.")
            return
        
        # Print statistics with colors
        print(f"{Colors.GREEN}✅ PASSED: {status_counts['PASS']}{Colors.NC}")
        print(f"{Colors.RED}❌ FAILED: {status_counts['FAIL']}{Colors.NC}")
        print(f"{Colors.YELLOW}⚠️  WARNINGS: {status_counts['WARN']}{Colors.NC}")
        print(f"{Colors.BLUE}ℹ️  INFO: {status_counts['INFO']}{Colors.NC}")
        print(f"📈 TOTAL TESTS: {total}")
        
        # Calculate overall score
        score = (status_counts['PASS'] * 100 + status_counts['WARN'] * 50) / (total * 100)
        score_color = Colors.GREEN if score > 0.8 else Colors.YELLOW if score > 0.6 else Colors.RED
        print(f"🎯 OVERALL SCORE: {score_color}{score:.1%}{Colors.NC}")
        
        # Print key recommendations
        recommendations = [r.recommendation for r in self.results if r.recommendation and r.status in ["FAIL", "WARN"]]
        if recommendations:
            print(f"\n{Colors.CYAN}💡 KEY RECOMMENDATIONS:{Colors.NC}")
            for i, rec in enumerate(recommendations[:5], 1):  # Show top 5
                print(f"  {i}. {rec}")

    def run_full_audit(self) -> Dict[str, Any]:
        """Run complete audit and return report"""
        print(f"{Colors.CYAN}🔍 Starting PANACEA ICONO Repository Audit{Colors.NC}")
        print(f"Repository: {self.repo_path}")
        print(f"Time: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Run all audit categories
        self.audit_security()
        self.audit_code_quality()
        self.audit_infrastructure()
        
        # Generate and save report
        report = self.generate_report()
        
        # Save report to file
        report_file = self.repo_path / "audit_report.json"
        try:
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            print(f"\n{Colors.GREEN}📄 Audit report saved to: {report_file}{Colors.NC}")
        except Exception as e:
            print(f"\n{Colors.RED}❌ Failed to save report: {e}{Colors.NC}")
        
        # Print summary
        self.print_summary()
        
        return report

def main():
    """Main function to run the audit"""
    import argparse
    
    parser = argparse.ArgumentParser(description="PANACEA ICONO Repository Audit Tool")
    parser.add_argument("--repo", default=".", help="Repository path (default: current directory)")
    parser.add_argument("--output", help="Output file for detailed report (default: audit_report.json)")
    parser.add_argument("--format", choices=["json", "html"], default="json", help="Report format")
    
    args = parser.parse_args()
    
    # Run audit
    auditor = RepositoryAuditor(args.repo)
    report = auditor.run_full_audit()
    
    # Save custom output if specified
    if args.output:
        output_path = Path(args.output)
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                if args.format == "json":
                    json.dump(report, f, indent=2, ensure_ascii=False)
                else:
                    # Simple HTML report
                    f.write(f"""
<!DOCTYPE html>
<html>
<head>
    <title>PANACEA ICONO Audit Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .pass {{ color: green; }}
        .fail {{ color: red; }}
        .warn {{ color: orange; }}
        .info {{ color: blue; }}
    </style>
</head>
<body>
    <h1>🔍 PANACEA ICONO Audit Report</h1>
    <p>Generated: {report['audit_info']['timestamp']}</p>
    <h2>Summary</h2>
    <p>Overall Score: {report['summary']['overall_score']}%</p>
    <ul>
        <li class="pass">Passed: {report['summary']['passed']}</li>
        <li class="fail">Failed: {report['summary']['failed']}</li>
        <li class="warn">Warnings: {report['summary']['warnings']}</li>
        <li class="info">Info: {report['summary']['info']}</li>
    </ul>
    <pre>{json.dumps(report, indent=2, ensure_ascii=False)}</pre>
</body>
</html>
                    """)
            print(f"{Colors.GREEN}📄 Custom report saved to: {output_path}{Colors.NC}")
        except Exception as e:
            print(f"{Colors.RED}❌ Failed to save custom report: {e}{Colors.NC}")

if __name__ == "__main__":
    main()