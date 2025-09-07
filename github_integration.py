#!/usr/bin/env python3
"""
🐙 GitHub Integration for PANACEA ICONO
Manages GitHub operations: issues, forks, repositories, etc.
"""

import os
import json
import logging
from typing import Dict, List, Optional, Any
import requests
from datetime import datetime

logger = logging.getLogger(__name__)

class GitHubManager:
    """Manages GitHub API operations for the PANACEA ICONO ecosystem"""
    
    def __init__(self, token: Optional[str] = None, org: str = "panacea-icono"):
        self.token = token or os.getenv("GITHUB_TOKEN")
        self.org = org
        self.base_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {self.token}" if self.token else None,
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "panacea-icono-ecosystem-manager"
        }
        
        if not self.token:
            logger.warning("⚠️ No GitHub token provided. Some operations may be limited.")
    
    def test_connection(self) -> bool:
        """Test GitHub API connection"""
        try:
            response = requests.get(f"{self.base_url}/user", headers=self.headers, timeout=10)
            return response.status_code == 200
        except Exception as e:
            logger.error(f"❌ GitHub connection failed: {e}")
            return False
    
    def list_organization_repos(self) -> List[Dict[str, Any]]:
        """List all repositories in the organization"""
        try:
            repos = []
            page = 1
            per_page = 100
            
            while True:
                response = requests.get(
                    f"{self.base_url}/orgs/{self.org}/repos",
                    headers=self.headers,
                    params={"page": page, "per_page": per_page, "sort": "updated"},
                    timeout=30
                )
                
                if response.status_code != 200:
                    logger.error(f"❌ Failed to fetch repos: {response.status_code}")
                    break
                
                batch = response.json()
                if not batch:
                    break
                    
                repos.extend(batch)
                page += 1
                
                # Limit to prevent infinite loops
                if len(repos) > 1000:
                    break
            
            logger.info(f"📚 Found {len(repos)} repositories")
            return repos
            
        except Exception as e:
            logger.error(f"❌ Error listing repos: {e}")
            return []
    
    def get_repository_info(self, repo_name: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a specific repository"""
        try:
            response = requests.get(
                f"{self.base_url}/repos/{self.org}/{repo_name}",
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"❌ Failed to get repo info for {repo_name}: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"❌ Error getting repo info: {e}")
            return None
    
    def create_issue(self, repo_name: str, title: str, body: str, labels: Optional[List[str]] = None) -> Optional[Dict[str, Any]]:
        """Create an issue in a repository"""
        try:
            data = {
                "title": title,
                "body": body,
                "labels": labels or []
            }
            
            response = requests.post(
                f"{self.base_url}/repos/{self.org}/{repo_name}/issues",
                headers=self.headers,
                json=data,
                timeout=10
            )
            
            if response.status_code == 201:
                issue = response.json()
                logger.info(f"✅ Created issue #{issue['number']} in {repo_name}")
                return issue
            else:
                logger.error(f"❌ Failed to create issue: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"❌ Error creating issue: {e}")
            return None
    
    def list_issues(self, repo_name: str, state: str = "open") -> List[Dict[str, Any]]:
        """List issues in a repository"""
        try:
            response = requests.get(
                f"{self.base_url}/repos/{self.org}/{repo_name}/issues",
                headers=self.headers,
                params={"state": state, "per_page": 100},
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"❌ Failed to list issues: {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"❌ Error listing issues: {e}")
            return []
    
    def get_forks(self, repo_name: str) -> List[Dict[str, Any]]:
        """Get forks of a repository"""
        try:
            response = requests.get(
                f"{self.base_url}/repos/{self.org}/{repo_name}/forks",
                headers=self.headers,
                params={"per_page": 100},
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"❌ Failed to get forks: {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"❌ Error getting forks: {e}")
            return []
    
    def update_fork(self, repo_name: str) -> bool:
        """Update a fork to sync with upstream"""
        try:
            # This would typically require the GitHub CLI or more complex API calls
            # For now, we'll log the action
            logger.info(f"🔄 Updating fork: {repo_name}")
            
            # In a real implementation, you would:
            # 1. Get the upstream repository
            # 2. Create a sync request
            # 3. Handle the merge conflicts if any
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Error updating fork: {e}")
            return False
    
    def get_repository_languages(self, repo_name: str) -> Dict[str, int]:
        """Get programming languages used in a repository"""
        try:
            response = requests.get(
                f"{self.base_url}/repos/{self.org}/{repo_name}/languages",
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"❌ Failed to get languages: {response.status_code}")
                return {}
                
        except Exception as e:
            logger.error(f"❌ Error getting languages: {e}")
            return {}
    
    def get_repository_topics(self, repo_name: str) -> List[str]:
        """Get topics/tags for a repository"""
        try:
            headers_with_topics = self.headers.copy()
            headers_with_topics["Accept"] = "application/vnd.github.mercy-preview+json"
            
            response = requests.get(
                f"{self.base_url}/repos/{self.org}/{repo_name}/topics",
                headers=headers_with_topics,
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json().get("names", [])
            else:
                logger.error(f"❌ Failed to get topics: {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"❌ Error getting topics: {e}")
            return []
    
    def generate_ecosystem_summary(self) -> Dict[str, Any]:
        """Generate a comprehensive summary of the ecosystem"""
        try:
            repos = self.list_organization_repos()
            
            summary = {
                "total_repos": len(repos),
                "repositories": [],
                "statistics": {
                    "total_stars": 0,
                    "total_forks": 0,
                    "total_watchers": 0,
                    "languages": {},
                    "licenses": {},
                    "updated_recently": 0  # Updated in last 30 days
                },
                "generated_at": datetime.utcnow().isoformat()
            }
            
            recent_cutoff = datetime.utcnow().timestamp() - (30 * 24 * 60 * 60)  # 30 days ago
            
            for repo in repos:
                if not repo:
                    continue
                    
                repo_info = {
                    "name": repo.get("name", ""),
                    "description": repo.get("description", "Sin descripción"),
                    "url": repo.get("html_url", ""),
                    "language": repo.get("language", "Sin especificar"),
                    "stars": repo.get("stargazers_count", 0),
                    "forks": repo.get("forks_count", 0),
                    "watchers": repo.get("watchers_count", 0),
                    "updated_at": repo.get("updated_at", ""),
                    "license": repo.get("license", {}).get("name", "Sin licencia") if repo.get("license") else "Sin licencia",
                    "topics": self.get_repository_topics(repo.get("name", ""))
                }
                
                summary["repositories"].append(repo_info)
                
                # Update statistics
                summary["statistics"]["total_stars"] += repo_info["stars"]
                summary["statistics"]["total_forks"] += repo_info["forks"]
                summary["statistics"]["total_watchers"] += repo_info["watchers"]
                
                # Language statistics
                lang = repo_info["language"]
                if lang != "Sin especificar":
                    summary["statistics"]["languages"][lang] = summary["statistics"]["languages"].get(lang, 0) + 1
                
                # License statistics
                license_name = repo_info["license"]
                summary["statistics"]["licenses"][license_name] = summary["statistics"]["licenses"].get(license_name, 0) + 1
                
                # Recently updated
                try:
                    updated_timestamp = datetime.fromisoformat(repo.get("updated_at", "").replace("Z", "+00:00")).timestamp()
                    if updated_timestamp > recent_cutoff:
                        summary["statistics"]["updated_recently"] += 1
                except:
                    pass
            
            # Sort repositories by update date
            summary["repositories"].sort(key=lambda x: x["updated_at"], reverse=True)
            
            logger.info(f"📊 Generated ecosystem summary with {len(repos)} repositories")
            return summary
            
        except Exception as e:
            logger.error(f"❌ Error generating ecosystem summary: {e}")
            return {"error": str(e)}


def main():
    """Test the GitHub integration"""
    logging.basicConfig(level=logging.INFO)
    
    # Create manager
    github_manager = GitHubManager()
    
    # Test connection
    if github_manager.test_connection():
        print("✅ GitHub connection successful")
        
        # Generate ecosystem summary
        summary = github_manager.generate_ecosystem_summary()
        print(f"📊 Found {summary.get('total_repos', 0)} repositories")
        print(f"⭐ Total stars: {summary.get('statistics', {}).get('total_stars', 0)}")
        print(f"🍴 Total forks: {summary.get('statistics', {}).get('total_forks', 0)}")
        
    else:
        print("❌ GitHub connection failed")


if __name__ == "__main__":
    main()