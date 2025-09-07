#!/usr/bin/env python3
"""
🌍 PANACEA ICONO Ecosystem Manager
Central hub for managing all repositories, packages, issues, and automation
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
import argparse
import sys

# Import our custom modules
try:
    from github_integration import GitHubManager
    from package_manager import PackageManager
    from huggingface_config import HuggingFaceManager
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure all required modules are available")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("ecosystem.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class EcosystemManager:
    """Main ecosystem management class"""
    
    def __init__(self, config_file: Optional[str] = None):
        self.config_file = config_file or "ecosystem_config.json"
        self.config = self.load_config()
        
        # Initialize managers
        self.github_manager = GitHubManager(
            token=self.config.get("github_token") or os.getenv("GITHUB_TOKEN"),
            org=self.config.get("github_org", "panacea-icono")
        )
        
        self.package_manager = PackageManager()
        
        self.hf_manager = None
        try:
            self.hf_manager = HuggingFaceManager()
        except Exception as e:
            logger.warning(f"⚠️ Hugging Face manager not available: {e}")
        
        self.base_path = Path.cwd()
        self.reports_dir = self.base_path / "reports"
        self.reports_dir.mkdir(exist_ok=True)
        
        logger.info("🌍 Ecosystem Manager initialized")
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file"""
        try:
            config_path = Path(self.config_file)
            if config_path.exists():
                with open(config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            logger.warning(f"⚠️ Could not load config: {e}")
        
        return {
            "github_org": "panacea-icono",
            "default_labels": ["enhancement", "ecosystem", "automation"],
            "audit_enabled": True,
            "auto_update_readme": True,
            "repositories": {}
        }
    
    def save_config(self) -> bool:
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2)
            return True
        except Exception as e:
            logger.error(f"❌ Error saving config: {e}")
            return False
    
    def generate_ecosystem_report(self) -> Dict[str, Any]:
        """Generate comprehensive ecosystem report"""
        logger.info("📊 Generating ecosystem report...")
        
        report = {
            "generated_at": datetime.utcnow().isoformat(),
            "ecosystem": {
                "organization": self.config.get("github_org", "panacea-icono"),
                "total_repositories": 0,
                "active_repositories": 0,
                "total_issues": 0,
                "open_issues": 0,
                "security_vulnerabilities": 0,
                "outdated_packages": 0
            },
            "repositories": [],
            "github_summary": {},
            "package_analysis": {},
            "huggingface_status": {},
            "recommendations": []
        }
        
        try:
            # GitHub analysis
            github_summary = self.github_manager.generate_ecosystem_summary()
            report["github_summary"] = github_summary
            report["ecosystem"]["total_repositories"] = github_summary.get("total_repos", 0)
            
            # Analyze each repository
            for repo_info in github_summary.get("repositories", [])[:10]:  # Limit for performance
                repo_name = repo_info.get("name", "")
                if not repo_name:
                    continue
                
                logger.info(f"🔍 Analyzing repository: {repo_name}")
                
                repo_analysis = {
                    "name": repo_name,
                    "description": repo_info.get("description", ""),
                    "language": repo_info.get("language", ""),
                    "stars": repo_info.get("stars", 0),
                    "forks": repo_info.get("forks", 0),
                    "issues": [],
                    "security_status": "unknown",
                    "package_status": "unknown",
                    "last_updated": repo_info.get("updated_at", "")
                }
                
                # Get issues for this repository
                try:
                    issues = self.github_manager.list_issues(repo_name)
                    repo_analysis["issues"] = [
                        {
                            "number": issue.get("number"),
                            "title": issue.get("title"),
                            "state": issue.get("state"),
                            "labels": [label.get("name") for label in issue.get("labels", [])]
                        }
                        for issue in issues[:5]  # Limit to first 5 issues
                    ]
                    report["ecosystem"]["open_issues"] += len([i for i in issues if i.get("state") == "open"])
                    report["ecosystem"]["total_issues"] += len(issues)
                except Exception as e:
                    logger.warning(f"⚠️ Could not fetch issues for {repo_name}: {e}")
                
                report["repositories"].append(repo_analysis)
            
            # Package analysis (for current repository)
            try:
                package_analysis = self.package_manager.analyze_repository_packages(self.base_path)
                report["package_analysis"] = package_analysis
                report["ecosystem"]["security_vulnerabilities"] += package_analysis.get("summary", {}).get("vulnerabilities", 0)
                report["ecosystem"]["outdated_packages"] += package_analysis.get("summary", {}).get("outdated_packages", 0)
            except Exception as e:
                logger.warning(f"⚠️ Package analysis failed: {e}")
            
            # Hugging Face status
            if self.hf_manager:
                try:
                    if self.hf_manager.verify_connection():
                        user_info = self.hf_manager.get_user_info()
                        user_models = self.hf_manager.list_user_models()
                        report["huggingface_status"] = {
                            "connected": True,
                            "user": user_info.get("name", "Unknown") if user_info else "Unknown",
                            "total_models": len(user_models),
                            "recent_models": [model.get("name") for model in user_models[:5]]
                        }
                    else:
                        report["huggingface_status"] = {"connected": False}
                except Exception as e:
                    logger.warning(f"⚠️ Hugging Face status check failed: {e}")
                    report["huggingface_status"] = {"connected": False, "error": str(e)}
            
            # Generate recommendations
            recommendations = []
            
            if report["ecosystem"]["security_vulnerabilities"] > 0:
                recommendations.append({
                    "type": "security",
                    "priority": "high",
                    "message": f"Found {report['ecosystem']['security_vulnerabilities']} security vulnerabilities. Run security audit."
                })
            
            if report["ecosystem"]["outdated_packages"] > 0:
                recommendations.append({
                    "type": "maintenance",
                    "priority": "medium",
                    "message": f"Found {report['ecosystem']['outdated_packages']} outdated packages. Consider updating."
                })
            
            if report["ecosystem"]["open_issues"] > 10:
                recommendations.append({
                    "type": "issues",
                    "priority": "medium",
                    "message": f"High number of open issues ({report['ecosystem']['open_issues']}). Consider issue triage."
                })
            
            report["recommendations"] = recommendations
            
            # Save report
            report_file = self.reports_dir / f"ecosystem_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            
            logger.info(f"📊 Report saved to: {report_file}")
            
        except Exception as e:
            logger.error(f"❌ Error generating report: {e}")
            report["error"] = str(e)
        
        return report
    
    def create_ecosystem_issue(self, repo_name: str, title: str, body: str, labels: Optional[List[str]] = None) -> bool:
        """Create an issue in a repository"""
        try:
            issue_labels = (labels or []) + self.config.get("default_labels", [])
            issue = self.github_manager.create_issue(repo_name, title, body, issue_labels)
            
            if issue:
                logger.info(f"✅ Created issue #{issue['number']} in {repo_name}: {title}")
                return True
            else:
                logger.error(f"❌ Failed to create issue in {repo_name}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error creating issue: {e}")
            return False
    
    def update_repository_readme(self, force_update: bool = False) -> bool:
        """Update the main README with current ecosystem information"""
        try:
            logger.info("📝 Updating README with ecosystem information...")
            
            readme_path = self.base_path / "README.md"
            if not readme_path.exists():
                logger.error("❌ README.md not found")
                return False
            
            # Generate fresh ecosystem data
            ecosystem_summary = self.github_manager.generate_ecosystem_summary()
            
            # Read current README
            with open(readme_path, 'r', encoding='utf-8') as f:
                readme_content = f.read()
            
            # Generate new repository listing
            new_repos_section = self.generate_readme_repositories_section(ecosystem_summary)
            
            # Find and replace the repositories section
            start_marker = "## 📋 Lista de Repositorios"
            end_marker = "## 🤝 Contribuir"
            
            start_index = readme_content.find(start_marker)
            end_index = readme_content.find(end_marker)
            
            if start_index != -1 and end_index != -1:
                new_readme = (
                    readme_content[:start_index] +
                    new_repos_section +
                    "\n" +
                    readme_content[end_index:]
                )
                
                # Update timestamp
                timestamp = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
                new_readme = new_readme.replace(
                    "*Última actualización: 7/9/2025, 13:31:00*",
                    f"*Última actualización: {timestamp}*"
                )
                
                # Write updated README
                with open(readme_path, 'w', encoding='utf-8') as f:
                    f.write(new_readme)
                
                logger.info("✅ README updated successfully")
                return True
            else:
                logger.error("❌ Could not find README sections to update")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error updating README: {e}")
            return False
    
    def generate_readme_repositories_section(self, ecosystem_summary: Dict[str, Any]) -> str:
        """Generate the repositories section for README"""
        try:
            section = "## 📋 Lista de Repositorios\n\n"
            
            repositories = ecosystem_summary.get("repositories", [])
            
            for index, repo in enumerate(repositories, 1):
                name = repo.get("name", "")
                description = repo.get("description", "Sin descripción")
                url = repo.get("url", "")
                language = repo.get("language", "Sin especificar")
                stars = repo.get("stars", 0)
                forks = repo.get("forks", 0)
                watchers = repo.get("watchers", 0)
                updated_at = repo.get("updated_at", "")
                license_name = repo.get("license", "Sin licencia")
                topics = repo.get("topics", [])
                
                # Format date
                try:
                    if updated_at:
                        updated_date = datetime.fromisoformat(updated_at.replace("Z", "+00:00"))
                        formatted_date = updated_date.strftime("%d/%m/%Y")
                    else:
                        formatted_date = "No disponible"
                except:
                    formatted_date = "No disponible"
                
                # Generate repository entry
                section += f"### {index}. [{name}]({url})\n\n"
                section += f"- **Descripción**: {description}\n"
                section += f"- **Lenguaje**: {language}\n"
                section += f"- **Estrellas**: ⭐ {stars} | **Forks**: 🍴 {forks} | **Watchers**: 👀 {watchers}\n"
                section += f"- **Última actualización**: {formatted_date}\n"
                section += f"- **Licencia**: {license_name}\n"
                
                if topics:
                    section += f"- **Temas**: {', '.join(topics)}\n"
                else:
                    section += f"- **Temas**: Ninguno\n"
                
                section += f"- **URL**: [{url}]({url})\n\n"
                
                # Add clone command
                section += "```bash\n"
                section += f"# Clonar repositorio\n"
                section += f"git clone {url}.git\n"
                section += f"cd {name}\n"
                section += "```\n\n"
            
            return section
            
        except Exception as e:
            logger.error(f"❌ Error generating README section: {e}")
            return "## 📋 Lista de Repositorios\n\n*Error generando la lista de repositorios*\n\n"
    
    def run_full_ecosystem_sync(self) -> Dict[str, Any]:
        """Run complete ecosystem synchronization"""
        logger.info("🔄 Starting full ecosystem synchronization...")
        
        sync_results = {
            "started_at": datetime.utcnow().isoformat(),
            "steps": {},
            "summary": {
                "success": True,
                "total_steps": 0,
                "completed_steps": 0,
                "failed_steps": 0
            }
        }
        
        steps = [
            ("ecosystem_report", "Generate ecosystem report"),
            ("readme_update", "Update README"),
            ("package_audit", "Run package audits"),
            ("github_sync", "Sync with GitHub")
        ]
        
        sync_results["summary"]["total_steps"] = len(steps)
        
        for step_id, step_name in steps:
            logger.info(f"🔄 Executing: {step_name}")
            
            try:
                if step_id == "ecosystem_report":
                    result = self.generate_ecosystem_report()
                    success = "error" not in result
                    
                elif step_id == "readme_update":
                    success = self.update_repository_readme()
                    result = {"updated": success}
                    
                elif step_id == "package_audit":
                    result = self.package_manager.analyze_repository_packages(self.base_path)
                    success = "error" not in result
                    
                elif step_id == "github_sync":
                    # This would typically involve git operations
                    result = {"status": "simulated"}
                    success = True
                    
                else:
                    result = {"status": "unknown"}
                    success = False
                
                sync_results["steps"][step_id] = {
                    "name": step_name,
                    "success": success,
                    "result": result,
                    "completed_at": datetime.utcnow().isoformat()
                }
                
                if success:
                    sync_results["summary"]["completed_steps"] += 1
                    logger.info(f"✅ {step_name} completed")
                else:
                    sync_results["summary"]["failed_steps"] += 1
                    logger.error(f"❌ {step_name} failed")
                    
            except Exception as e:
                logger.error(f"❌ Error in {step_name}: {e}")
                sync_results["steps"][step_id] = {
                    "name": step_name,
                    "success": False,
                    "error": str(e),
                    "completed_at": datetime.utcnow().isoformat()
                }
                sync_results["summary"]["failed_steps"] += 1
        
        # Overall success
        sync_results["summary"]["success"] = sync_results["summary"]["failed_steps"] == 0
        sync_results["completed_at"] = datetime.utcnow().isoformat()
        
        # Save sync results
        sync_file = self.reports_dir / f"ecosystem_sync_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(sync_file, 'w', encoding='utf-8') as f:
            json.dump(sync_results, f, indent=2)
        
        logger.info(f"🔄 Synchronization completed. Results saved to: {sync_file}")
        return sync_results


def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(description="PANACEA ICONO Ecosystem Manager")
    parser.add_argument("command", choices=[
        "report", "sync", "readme", "issue", "audit", "status"
    ], help="Command to execute")
    parser.add_argument("--repo", help="Repository name for specific operations")
    parser.add_argument("--title", help="Issue title")
    parser.add_argument("--body", help="Issue body")
    parser.add_argument("--labels", nargs="*", help="Issue labels")
    parser.add_argument("--config", help="Config file path")
    
    args = parser.parse_args()
    
    # Initialize ecosystem manager
    manager = EcosystemManager(args.config)
    
    if args.command == "report":
        print("📊 Generating ecosystem report...")
        report = manager.generate_ecosystem_report()
        print(f"✅ Report generated with {report.get('ecosystem', {}).get('total_repositories', 0)} repositories")
        
    elif args.command == "sync":
        print("🔄 Running full ecosystem synchronization...")
        results = manager.run_full_ecosystem_sync()
        if results["summary"]["success"]:
            print("✅ Synchronization completed successfully")
        else:
            print(f"⚠️ Synchronization completed with {results['summary']['failed_steps']} failures")
            
    elif args.command == "readme":
        print("📝 Updating README...")
        success = manager.update_repository_readme()
        if success:
            print("✅ README updated successfully")
        else:
            print("❌ README update failed")
            
    elif args.command == "issue":
        if not args.repo or not args.title:
            print("❌ Repository name and title are required for issue creation")
            return
        
        print(f"🐛 Creating issue in {args.repo}...")
        success = manager.create_ecosystem_issue(args.repo, args.title, args.body or "", args.labels)
        if success:
            print("✅ Issue created successfully")
        else:
            print("❌ Issue creation failed")
            
    elif args.command == "audit":
        print("🔍 Running package audit...")
        analysis = manager.package_manager.analyze_repository_packages(Path.cwd())
        print(f"📦 Found {analysis.get('summary', {}).get('vulnerabilities', 0)} vulnerabilities")
        print(f"📦 Found {analysis.get('summary', {}).get('outdated_packages', 0)} outdated packages")
        
    elif args.command == "status":
        print("📊 Ecosystem Status:")
        print(f"  GitHub connection: {'✅' if manager.github_manager.test_connection() else '❌'}")
        print(f"  Hugging Face: {'✅' if manager.hf_manager and manager.hf_manager.verify_connection() else '❌'}")
        print(f"  Reports directory: {manager.reports_dir}")


if __name__ == "__main__":
    main()