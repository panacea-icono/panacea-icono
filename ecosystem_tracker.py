#!/usr/bin/env python3
"""
Ecosystem Tracker for PANACEA ICONO
Tracks forks and updates across all repositories in the ecosystem
"""

import os
import json
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import time
import re

class EcosystemTracker:
    """Tracks forks and updates across the PANACEA ICONO ecosystem"""
    
    def __init__(self, github_token: Optional[str] = None):
        """
        Initialize the ecosystem tracker
        
        Args:
            github_token: GitHub personal access token
        """
        self.github_token = github_token or os.getenv('GITHUB_TOKEN')
        self.base_url = "https://api.github.com"
        self.headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28"
        }
        
        if self.github_token:
            self.headers["Authorization"] = f"Bearer {self.github_token}"
        
        # Organizations to track
        self.organizations = [
            "panacea-icono",
            "https-panacea-icono-org"
        ]
        
        # Rate limiting
        self.rate_limit_remaining = 5000
        self.rate_limit_reset = time.time()
        
    def _make_request(self, url: str, params: Dict = None) -> Optional[Dict]:
        """
        Make a request to GitHub API with rate limiting
        
        Args:
            url: API endpoint URL
            params: Query parameters
            
        Returns:
            Response data or None if error
        """
        try:
            # Check rate limiting
            if self.rate_limit_remaining <= 10 and time.time() < self.rate_limit_reset:
                sleep_time = self.rate_limit_reset - time.time() + 1
                print(f"⏳ Rate limit approaching, sleeping for {sleep_time:.0f} seconds...")
                time.sleep(sleep_time)
            
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            
            # Update rate limit info
            self.rate_limit_remaining = int(response.headers.get('x-ratelimit-remaining', 5000))
            self.rate_limit_reset = int(response.headers.get('x-ratelimit-reset', time.time() + 3600))
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                print(f"⚠️ Repository not found: {url}")
                return None
            elif response.status_code == 403:
                print(f"⚠️ Rate limited or access denied: {url}")
                return None
            else:
                print(f"❌ Error {response.status_code}: {url}")
                return None
                
        except Exception as e:
            print(f"❌ Request error: {e}")
            return None
    
    def get_organization_repos(self, org: str) -> List[Dict]:
        """
        Get all repositories from an organization
        
        Args:
            org: Organization name
            
        Returns:
            List of repository information
        """
        repos = []
        page = 1
        per_page = 100
        
        while True:
            url = f"{self.base_url}/orgs/{org}/repos"
            params = {
                "page": page,
                "per_page": per_page,
                "sort": "updated",
                "direction": "desc"
            }
            
            data = self._make_request(url, params)
            if not data:
                break
                
            if len(data) == 0:
                break
                
            repos.extend(data)
            page += 1
            
            # Prevent infinite loops
            if len(data) < per_page:
                break
        
        return repos
    
    def get_repository_forks(self, owner: str, repo: str) -> List[Dict]:
        """
        Get forks for a specific repository
        
        Args:
            owner: Repository owner
            repo: Repository name
            
        Returns:
            List of fork information
        """
        url = f"{self.base_url}/repos/{owner}/{repo}/forks"
        params = {
            "sort": "newest",
            "per_page": 30
        }
        
        data = self._make_request(url, params)
        return data or []
    
    def get_repository_commits(self, owner: str, repo: str, since_days: int = 7) -> List[Dict]:
        """
        Get recent commits for a repository
        
        Args:
            owner: Repository owner
            repo: Repository name
            since_days: Number of days to look back
            
        Returns:
            List of recent commits
        """
        since_date = (datetime.now() - timedelta(days=since_days)).isoformat()
        
        url = f"{self.base_url}/repos/{owner}/{repo}/commits"
        params = {
            "since": since_date,
            "per_page": 10
        }
        
        data = self._make_request(url, params)
        return data or []
    
    def get_repository_releases(self, owner: str, repo: str) -> List[Dict]:
        """
        Get releases for a repository
        
        Args:
            owner: Repository owner
            repo: Repository name
            
        Returns:
            List of releases
        """
        url = f"{self.base_url}/repos/{owner}/{repo}/releases"
        params = {"per_page": 5}
        
        data = self._make_request(url, params)
        return data or []
    
    def extract_repo_info_from_readme(self, readme_path: str = "README.md") -> List[Tuple[str, str, Dict]]:
        """
        Extract repository information from README.md
        
        Args:
            readme_path: Path to README file
            
        Returns:
            List of (owner, repo, metadata) tuples
        """
        repos = []
        
        try:
            with open(readme_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse repository sections
            sections = re.findall(
                r'### \d+\. \[([^\]]+)\]\(([^)]+)\)(.*?)(?=### \d+\.|$)', 
                content, 
                re.DOTALL
            )
            
            for name, url, metadata_text in sections:
                # Extract owner and repo from URL
                github_match = re.search(r'https://github\.com/([^/\s]+)/([^/\s\)]+)', url)
                if github_match:
                    owner, repo = github_match.groups()
                    
                    # Parse metadata
                    metadata = {
                        'name': name,
                        'url': url,
                        'description': '',
                        'language': '',
                        'stars': 0,
                        'forks': 0,
                        'watchers': 0,
                        'last_update': '',
                        'license': ''
                    }
                    
                    # Extract description
                    desc_match = re.search(r'- \*\*Descripción\*\*: (.+)', metadata_text)
                    if desc_match:
                        metadata['description'] = desc_match.group(1)
                    
                    # Extract language
                    lang_match = re.search(r'- \*\*Lenguaje\*\*: (.+)', metadata_text)
                    if lang_match:
                        metadata['language'] = lang_match.group(1)
                    
                    # Extract stats
                    stats_match = re.search(r'⭐ (\d+)[^🍴]+🍴 (\d+)[^👀]+👀 (\d+)', metadata_text)
                    if stats_match:
                        metadata['stars'] = int(stats_match.group(1))
                        metadata['forks'] = int(stats_match.group(2))
                        metadata['watchers'] = int(stats_match.group(3))
                    
                    # Extract last update
                    date_match = re.search(r'- \*\*Última actualización\*\*: (.+)', metadata_text)
                    if date_match:
                        metadata['last_update'] = date_match.group(1)
                    
                    # Extract license
                    license_match = re.search(r'- \*\*Licencia\*\*: (.+)', metadata_text)
                    if license_match:
                        metadata['license'] = license_match.group(1)
                    
                    repos.append((owner, repo, metadata))
            
            return repos
            
        except Exception as e:
            print(f"❌ Error reading README: {e}")
            return []
    
    def track_ecosystem_activity(self, days_back: int = 7) -> Dict:
        """
        Track activity across the entire ecosystem
        
        Args:
            days_back: Number of days to look back for activity
            
        Returns:
            Dictionary with ecosystem activity data
        """
        print("🔍 Tracking ecosystem activity...")
        
        # Get repositories from README
        repos_from_readme = self.extract_repo_info_from_readme()
        print(f"📚 Found {len(repos_from_readme)} repositories in README")
        
        # Initialize ecosystem data
        ecosystem_data = {
            "last_updated": datetime.now().isoformat(),
            "repositories": {},
            "recent_activity": [],
            "fork_summary": {"total_forks": 0, "repositories_with_forks": 0},
            "activity_summary": {"total_commits": 0, "total_releases": 0, "total_repositories": len(repos_from_readme)}
        }
        
        # Process repositories from README (works without GitHub token)
        for i, (owner, repo, metadata) in enumerate(repos_from_readme, 1):
            print(f"📊 Processing {i}/{len(repos_from_readme)}: {owner}/{repo}")
            
            repo_key = f"{owner}/{repo}"
            
            # Store basic repository data from README
            ecosystem_data["repositories"][repo_key] = {
                "name": repo,
                "owner": owner,
                "full_name": repo_key,
                "description": metadata.get("description", ""),
                "stars": metadata.get("stars", 0),
                "forks_count": metadata.get("forks", 0),
                "watchers": metadata.get("watchers", 0),
                "last_updated": metadata.get("last_update", ""),
                "language": metadata.get("language", ""),
                "license": metadata.get("license", ""),
                "url": metadata.get("url", f"https://github.com/{owner}/{repo}"),
                "forks": [],  # Will be populated if GitHub API is available
                "recent_commits": [],
                "recent_releases": []
            }
            
            # Update summaries from README data
            ecosystem_data["fork_summary"]["total_forks"] += metadata.get("forks", 0)
            if metadata.get("forks", 0) > 0:
                ecosystem_data["fork_summary"]["repositories_with_forks"] += 1
            
            # Try to get additional data from GitHub API if token is available
            if self.github_token:
                try:
                    # Get basic repository info
                    repo_url = f"{self.base_url}/repos/{owner}/{repo}"
                    repo_info = self._make_request(repo_url)
                    
                    if repo_info:
                        # Update with fresh data from GitHub
                        ecosystem_data["repositories"][repo_key].update({
                            "stars": repo_info.get("stargazers_count", metadata.get("stars", 0)),
                            "forks_count": repo_info.get("forks_count", metadata.get("forks", 0)),
                            "watchers": repo_info.get("watchers_count", metadata.get("watchers", 0)),
                            "last_updated": repo_info.get("updated_at", metadata.get("last_update", "")),
                            "language": repo_info.get("language", metadata.get("language", "")),
                        })
                        
                        # Get forks
                        forks = self.get_repository_forks(owner, repo)
                        ecosystem_data["repositories"][repo_key]["forks"] = [
                            {
                                "owner": fork["owner"]["login"],
                                "created_at": fork["created_at"],
                                "updated_at": fork["updated_at"]
                            } for fork in forks
                        ]
                        
                        # Get recent commits
                        commits = self.get_repository_commits(owner, repo, days_back)
                        ecosystem_data["repositories"][repo_key]["recent_commits"] = [
                            {
                                "sha": commit["sha"][:8],
                                "message": commit["commit"]["message"].split('\n')[0][:100],
                                "author": commit["commit"]["author"]["name"],
                                "date": commit["commit"]["author"]["date"]
                            } for commit in commits
                        ]
                        
                        # Get releases
                        releases = self.get_repository_releases(owner, repo)
                        ecosystem_data["repositories"][repo_key]["recent_releases"] = [
                            {
                                "name": release["name"] or release["tag_name"],
                                "tag": release["tag_name"],
                                "published_at": release["published_at"],
                                "prerelease": release["prerelease"]
                            } for release in releases
                        ]
                        
                        # Update activity counters
                        ecosystem_data["activity_summary"]["total_commits"] += len(commits)
                        ecosystem_data["activity_summary"]["total_releases"] += len(releases)
                        
                        # Add to recent activity
                        for commit in commits[:2]:  # Top 2 recent commits per repo
                            ecosystem_data["recent_activity"].append({
                                "type": "commit",
                                "repository": repo_key,
                                "title": commit["commit"]["message"].split('\n')[0][:80],
                                "author": commit["commit"]["author"]["name"],
                                "date": commit["commit"]["author"]["date"],
                                "url": f"https://github.com/{owner}/{repo}/commit/{commit['sha']}"
                            })
                        
                        for release in releases[:1]:  # Most recent release per repo
                            ecosystem_data["recent_activity"].append({
                                "type": "release",
                                "repository": repo_key,
                                "title": release["name"] or release["tag_name"],
                                "date": release["published_at"],
                                "url": release["html_url"]
                            })
                        
                        # Small delay to be respectful to GitHub API
                        time.sleep(0.2)
                        
                except Exception as e:
                    print(f"⚠️ Could not fetch GitHub data for {repo_key}: {e}")
                    # Continue with README data
            else:
                # Add basic activity entry from README metadata
                if metadata.get("last_update"):
                    ecosystem_data["recent_activity"].append({
                        "type": "repository",
                        "repository": repo_key,
                        "title": f"Repository: {metadata.get('description', repo)[:60]}",
                        "date": f"{metadata.get('last_update')}T00:00:00Z",  # Approximate ISO format
                        "url": metadata.get("url", f"https://github.com/{owner}/{repo}")
                    })
        
        # Sort recent activity by date
        ecosystem_data["recent_activity"].sort(
            key=lambda x: x["date"], 
            reverse=True
        )
        
        # Keep only recent items
        ecosystem_data["recent_activity"] = ecosystem_data["recent_activity"][:50]
        
        # Recalculate fork summary from actual data
        total_forks = sum(len(repo_data.get("forks", [])) or repo_data.get("forks_count", 0) 
                         for repo_data in ecosystem_data["repositories"].values())
        ecosystem_data["fork_summary"]["total_forks"] = total_forks
        
        repositories_with_forks = sum(1 for repo_data in ecosystem_data["repositories"].values() 
                                    if (len(repo_data.get("forks", [])) > 0 or repo_data.get("forks_count", 0) > 0))
        ecosystem_data["fork_summary"]["repositories_with_forks"] = repositories_with_forks
        
        return ecosystem_data
    
    def save_data(self, data: Dict, filename: str = "ecosystem_data.json"):
        """
        Save ecosystem data to a JSON file
        
        Args:
            data: Ecosystem data dictionary
            filename: Output filename
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"✅ Data saved to {filename}")
        except Exception as e:
            print(f"❌ Error saving data: {e}")
    
    def load_data(self, filename: str = "ecosystem_data.json") -> Dict:
        """
        Load ecosystem data from a JSON file
        
        Args:
            filename: Input filename
            
        Returns:
            Ecosystem data dictionary
        """
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            print(f"✅ Data loaded from {filename}")
            return data
        except FileNotFoundError:
            print(f"⚠️ File {filename} not found, returning empty data")
            return {}
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            return {}

def main():
    """Main function to demonstrate ecosystem tracking"""
    print("🔍 Starting ecosystem tracking...")
    
    tracker = EcosystemTracker()
    
    # Track ecosystem activity
    data = tracker.track_ecosystem_activity(days_back=14)
    
    # Save data
    tracker.save_data(data)
    
    # Print summary
    print("\n📊 Ecosystem Summary:")
    print(f"  📚 Total repositories: {len(data['repositories'])}")
    print(f"  🍴 Total forks: {data['fork_summary']['total_forks']}")
    print(f"  📈 Repositories with forks: {data['fork_summary']['repositories_with_forks']}")
    print(f"  📝 Recent commits: {data['activity_summary']['total_commits']}")
    print(f"  🏷️ Recent releases: {data['activity_summary']['total_releases']}")
    print(f"  🎯 Recent activity items: {len(data['recent_activity'])}")
    
    print("\n🎯 Recent Activity (Top 10):")
    for item in data['recent_activity'][:10]:
        emoji = "📝" if item['type'] == 'commit' else "🏷️" if item['type'] == 'release' else "📚"
        
        # Handle different date formats
        try:
            if item['date'].endswith('Z'):
                date = datetime.fromisoformat(item['date'].replace('Z', '+00:00')).strftime("%Y-%m-%d %H:%M")
            elif 'T' in item['date']:
                date = datetime.fromisoformat(item['date']).strftime("%Y-%m-%d %H:%M")
            else:
                # Handle simple date format like "9/6/2025"
                date = item['date']
        except:
            date = item['date']
            
        print(f"  {emoji} {item['repository']}: {item['title']} ({date})")

if __name__ == "__main__":
    main()