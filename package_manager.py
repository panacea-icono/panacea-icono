#!/usr/bin/env python3
"""
📦 Package Manager for PANACEA ICONO
Handles NPM packages, audits, and dependency management
"""

import os
import json
import subprocess
import logging
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path
import requests

logger = logging.getLogger(__name__)

class PackageManager:
    """Manages package operations for the PANACEA ICONO ecosystem"""
    
    def __init__(self, base_path: Optional[str] = None):
        self.base_path = Path(base_path) if base_path else Path.cwd()
        self.package_files = ["package.json", "pyproject.toml", "requirements.txt", "Cargo.toml", "go.mod"]
    
    def find_package_files(self, directory: Path) -> Dict[str, List[Path]]:
        """Find all package files in a directory and subdirectories"""
        found_files = {
            "package.json": [],
            "pyproject.toml": [],
            "requirements.txt": [],
            "Cargo.toml": [],
            "go.mod": [],
            "composer.json": [],
            "pom.xml": []
        }
        
        try:
            for root, dirs, files in os.walk(directory):
                # Skip common directories that shouldn't contain root package files
                dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', '__pycache__', '.venv', 'venv', 'target', 'vendor']]
                
                root_path = Path(root)
                for file in files:
                    if file in found_files:
                        found_files[file].append(root_path / file)
            
            return found_files
            
        except Exception as e:
            logger.error(f"❌ Error finding package files: {e}")
            return found_files
    
    def read_package_json(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """Read and parse a package.json file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"❌ Error reading {file_path}: {e}")
            return None
    
    def write_package_json(self, file_path: Path, content: Dict[str, Any]) -> bool:
        """Write content to a package.json file"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(content, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            logger.error(f"❌ Error writing {file_path}: {e}")
            return False
    
    def run_npm_audit(self, directory: Path) -> Dict[str, Any]:
        """Run npm audit in a directory"""
        try:
            result = subprocess.run(
                ["npm", "audit", "--json"],
                cwd=directory,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0 or result.stdout:
                try:
                    audit_data = json.loads(result.stdout)
                    return {
                        "success": True,
                        "data": audit_data,
                        "vulnerabilities": audit_data.get("vulnerabilities", {}),
                        "summary": audit_data.get("metadata", {}).get("vulnerabilities", {})
                    }
                except json.JSONDecodeError:
                    return {"success": False, "error": "Invalid JSON response from npm audit"}
            else:
                return {"success": False, "error": result.stderr}
                
        except subprocess.TimeoutExpired:
            return {"success": False, "error": "npm audit timed out"}
        except FileNotFoundError:
            return {"success": False, "error": "npm not found"}
        except Exception as e:
            logger.error(f"❌ Error running npm audit: {e}")
            return {"success": False, "error": str(e)}
    
    def run_npm_update(self, directory: Path) -> Dict[str, Any]:
        """Run npm update in a directory"""
        try:
            result = subprocess.run(
                ["npm", "update"],
                cwd=directory,
                capture_output=True,
                text=True,
                timeout=180
            )
            
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr
            }
            
        except subprocess.TimeoutExpired:
            return {"success": False, "error": "npm update timed out"}
        except FileNotFoundError:
            return {"success": False, "error": "npm not found"}
        except Exception as e:
            logger.error(f"❌ Error running npm update: {e}")
            return {"success": False, "error": str(e)}
    
    def run_pip_audit(self, directory: Path) -> Dict[str, Any]:
        """Run pip audit (using pip-audit if available)"""
        try:
            # First try pip-audit
            result = subprocess.run(
                ["pip-audit", "--format=json"],
                cwd=directory,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                try:
                    audit_data = json.loads(result.stdout)
                    return {
                        "success": True,
                        "data": audit_data,
                        "vulnerabilities_count": len(audit_data)
                    }
                except json.JSONDecodeError:
                    return {"success": False, "error": "Invalid JSON response from pip-audit"}
            else:
                # Fallback to safety check
                return self.run_safety_check(directory)
                
        except FileNotFoundError:
            # Try safety as fallback
            return self.run_safety_check(directory)
        except Exception as e:
            logger.error(f"❌ Error running pip audit: {e}")
            return {"success": False, "error": str(e)}
    
    def run_safety_check(self, directory: Path) -> Dict[str, Any]:
        """Run safety check for Python dependencies"""
        try:
            result = subprocess.run(
                ["safety", "check", "--json"],
                cwd=directory,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.stdout:
                try:
                    safety_data = json.loads(result.stdout)
                    return {
                        "success": True,
                        "data": safety_data,
                        "vulnerabilities_count": len(safety_data)
                    }
                except json.JSONDecodeError:
                    return {"success": False, "error": "Invalid JSON response from safety"}
            else:
                return {"success": True, "data": [], "vulnerabilities_count": 0}
                
        except FileNotFoundError:
            return {"success": False, "error": "safety not found"}
        except Exception as e:
            logger.error(f"❌ Error running safety check: {e}")
            return {"success": False, "error": str(e)}
    
    def check_outdated_packages(self, directory: Path, package_type: str) -> Dict[str, Any]:
        """Check for outdated packages"""
        try:
            if package_type == "npm":
                result = subprocess.run(
                    ["npm", "outdated", "--json"],
                    cwd=directory,
                    capture_output=True,
                    text=True,
                    timeout=60
                )
                
                if result.stdout:
                    try:
                        outdated_data = json.loads(result.stdout)
                        return {"success": True, "data": outdated_data}
                    except json.JSONDecodeError:
                        return {"success": False, "error": "Invalid JSON response"}
                else:
                    return {"success": True, "data": {}}
                    
            elif package_type == "pip":
                result = subprocess.run(
                    ["pip", "list", "--outdated", "--format=json"],
                    cwd=directory,
                    capture_output=True,
                    text=True,
                    timeout=60
                )
                
                if result.returncode == 0 and result.stdout:
                    try:
                        outdated_data = json.loads(result.stdout)
                        return {"success": True, "data": outdated_data}
                    except json.JSONDecodeError:
                        return {"success": False, "error": "Invalid JSON response"}
                else:
                    return {"success": True, "data": []}
            
            return {"success": False, "error": f"Unsupported package type: {package_type}"}
            
        except Exception as e:
            logger.error(f"❌ Error checking outdated packages: {e}")
            return {"success": False, "error": str(e)}
    
    def create_package_json(self, directory: Path, name: str, description: str = "") -> bool:
        """Create a new package.json file"""
        try:
            package_content = {
                "name": name,
                "version": "1.0.0",
                "description": description or f"Package for {name}",
                "main": "index.js",
                "scripts": {
                    "test": "echo \"Error: no test specified\" && exit 1",
                    "start": "node index.js",
                    "dev": "nodemon index.js"
                },
                "keywords": ["panacea-icono", "ecosystem"],
                "author": "PANACEA ICONO Team",
                "license": "MIT",
                "dependencies": {},
                "devDependencies": {}
            }
            
            package_file = directory / "package.json"
            return self.write_package_json(package_file, package_content)
            
        except Exception as e:
            logger.error(f"❌ Error creating package.json: {e}")
            return False
    
    def update_package_scripts(self, directory: Path, scripts: Dict[str, str]) -> bool:
        """Update scripts in package.json"""
        try:
            package_file = directory / "package.json"
            if not package_file.exists():
                logger.error(f"❌ package.json not found in {directory}")
                return False
            
            package_data = self.read_package_json(package_file)
            if not package_data:
                return False
            
            if "scripts" not in package_data:
                package_data["scripts"] = {}
            
            package_data["scripts"].update(scripts)
            
            return self.write_package_json(package_file, package_data)
            
        except Exception as e:
            logger.error(f"❌ Error updating package scripts: {e}")
            return False
    
    def analyze_repository_packages(self, repo_path: Path) -> Dict[str, Any]:
        """Analyze all packages in a repository"""
        try:
            analysis = {
                "repository": str(repo_path),
                "package_files": {},
                "audits": {},
                "outdated": {},
                "summary": {
                    "total_files": 0,
                    "vulnerabilities": 0,
                    "outdated_packages": 0,
                    "package_types": []
                },
                "analyzed_at": "2025-09-07T18:30:00Z"
            }
            
            # Find all package files
            found_files = self.find_package_files(repo_path)
            
            for package_type, files in found_files.items():
                if files:
                    analysis["package_files"][package_type] = [str(f) for f in files]
                    analysis["summary"]["total_files"] += len(files)
                    analysis["summary"]["package_types"].append(package_type)
                    
                    # Run appropriate audits
                    for file_path in files:
                        file_dir = file_path.parent
                        
                        if package_type == "package.json":
                            # NPM audit
                            audit_result = self.run_npm_audit(file_dir)
                            if audit_result["success"]:
                                analysis["audits"][str(file_path)] = audit_result
                                vuln_summary = audit_result.get("summary", {})
                                analysis["summary"]["vulnerabilities"] += sum(vuln_summary.values()) if isinstance(vuln_summary, dict) else 0
                            
                            # Check outdated NPM packages
                            outdated_result = self.check_outdated_packages(file_dir, "npm")
                            if outdated_result["success"]:
                                analysis["outdated"][str(file_path)] = outdated_result
                                analysis["summary"]["outdated_packages"] += len(outdated_result.get("data", {}))
                        
                        elif package_type in ["requirements.txt", "pyproject.toml"]:
                            # Python security audit
                            audit_result = self.run_pip_audit(file_dir)
                            if audit_result["success"]:
                                analysis["audits"][str(file_path)] = audit_result
                                analysis["summary"]["vulnerabilities"] += audit_result.get("vulnerabilities_count", 0)
                            
                            # Check outdated Python packages
                            outdated_result = self.check_outdated_packages(file_dir, "pip")
                            if outdated_result["success"]:
                                analysis["outdated"][str(file_path)] = outdated_result
                                analysis["summary"]["outdated_packages"] += len(outdated_result.get("data", []))
            
            logger.info(f"📦 Analyzed {analysis['summary']['total_files']} package files")
            return analysis
            
        except Exception as e:
            logger.error(f"❌ Error analyzing repository packages: {e}")
            return {"error": str(e)}


def main():
    """Test the package manager"""
    logging.basicConfig(level=logging.INFO)
    
    # Create package manager
    package_manager = PackageManager()
    
    # Analyze current directory
    analysis = package_manager.analyze_repository_packages(Path.cwd())
    
    print(f"📦 Package Analysis Summary:")
    print(f"   Total package files: {analysis.get('summary', {}).get('total_files', 0)}")
    print(f"   Package types: {', '.join(analysis.get('summary', {}).get('package_types', []))}")
    print(f"   Vulnerabilities found: {analysis.get('summary', {}).get('vulnerabilities', 0)}")
    print(f"   Outdated packages: {analysis.get('summary', {}).get('outdated_packages', 0)}")


if __name__ == "__main__":
    main()