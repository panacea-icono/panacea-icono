#!/usr/bin/env python3
"""
🐙 GitHub Repository Manager for PANACEA ICONO
Manages dynamic fetching and caching of repository information
"""

import os
import json
import logging
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, asdict
from pathlib import Path

import aiohttp
import requests
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


@dataclass
class Repository:
    """Repository data model"""
    id: int
    name: str
    full_name: str
    description: Optional[str]
    html_url: str
    clone_url: str
    ssh_url: str
    language: Optional[str]
    size: int
    stargazers_count: int
    watchers_count: int
    forks_count: int
    open_issues_count: int
    default_branch: str
    created_at: str
    updated_at: str
    pushed_at: str
    license: Optional[Dict[str, Any]]
    topics: List[str]
    visibility: str
    private: bool
    archived: bool
    disabled: bool
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)
    
    @property
    def last_updated_formatted(self) -> str:
        """Format last update date"""
        try:
            dt = datetime.fromisoformat(self.updated_at.replace('Z', '+00:00'))
            return dt.strftime('%d/%m/%Y')
        except:
            return self.updated_at
    
    @property
    def license_name(self) -> str:
        """Get license name"""
        if self.license and 'name' in self.license:
            return self.license['name']
        return "Sin licencia"
    
    @property
    def topics_str(self) -> str:
        """Get topics as string"""
        return ", ".join(f"`{topic}`" for topic in self.topics) if self.topics else "Ninguno"


class GitHubRepoManager:
    """GitHub Repository Manager"""
    
    def __init__(self, 
                 github_token: Optional[str] = None,
                 organization: str = "panacea-icono",
                 cache_duration_hours: int = 1):
        """
        Initialize GitHub Repository Manager
        
        Args:
            github_token: GitHub personal access token
            organization: GitHub organization name
            cache_duration_hours: How long to cache repository data
        """
        self.github_token = github_token or os.getenv("GITHUB_TOKEN")
        self.organization = organization
        self.cache_duration = timedelta(hours=cache_duration_hours)
        self.base_url = "https://api.github.com"
        self.cache_file = Path("/tmp/github_repos_cache.json")
        
        # Setup headers
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "PANACEA-ICONO-App/1.0"
        }
        if self.github_token:
            self.headers["Authorization"] = f"token {self.github_token}"
            logger.info("✅ GitHub token configured")
        else:
            logger.warning("⚠️ No GitHub token provided - rate limits will apply")
    
    def _is_cache_valid(self) -> bool:
        """Check if cache is still valid"""
        if not self.cache_file.exists():
            return False
        
        try:
            with open(self.cache_file, 'r') as f:
                cache_data = json.load(f)
            
            cache_time = datetime.fromisoformat(cache_data.get('cached_at', ''))
            return datetime.now() - cache_time < self.cache_duration
        except Exception as e:
            logger.error(f"Error checking cache validity: {e}")
            return False
    
    def _load_from_cache(self) -> Optional[List[Repository]]:
        """Load repositories from cache"""
        try:
            with open(self.cache_file, 'r') as f:
                cache_data = json.load(f)
            
            repos = []
            for repo_data in cache_data.get('repositories', []):
                repos.append(Repository(**repo_data))
            
            logger.info(f"📦 Loaded {len(repos)} repositories from cache")
            return repos
        except Exception as e:
            logger.error(f"Error loading from cache: {e}")
            return None
    
    def _save_to_cache(self, repositories: List[Repository]):
        """Save repositories to cache"""
        try:
            cache_data = {
                'cached_at': datetime.now().isoformat(),
                'organization': self.organization,
                'repositories': [repo.to_dict() for repo in repositories]
            }
            
            # Ensure cache directory exists
            self.cache_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.cache_file, 'w') as f:
                json.dump(cache_data, f, indent=2)
            
            logger.info(f"💾 Cached {len(repositories)} repositories")
        except Exception as e:
            logger.error(f"Error saving to cache: {e}")
    
    async def _fetch_repositories_async(self) -> List[Repository]:
        """Fetch repositories asynchronously"""
        url = f"{self.base_url}/orgs/{self.organization}/repos"
        all_repos = []
        page = 1
        per_page = 100
        
        async with aiohttp.ClientSession(headers=self.headers) as session:
            while True:
                params = {
                    'page': page,
                    'per_page': per_page,
                    'sort': 'updated',
                    'direction': 'desc'
                }
                
                logger.info(f"🔄 Fetching page {page} of repositories...")
                
                try:
                    async with session.get(url, params=params) as response:
                        if response.status == 200:
                            repos_data = await response.json()
                            
                            if not repos_data:
                                break
                            
                            for repo_data in repos_data:
                                try:
                                    repo = Repository(
                                        id=repo_data['id'],
                                        name=repo_data['name'],
                                        full_name=repo_data['full_name'],
                                        description=repo_data.get('description'),
                                        html_url=repo_data['html_url'],
                                        clone_url=repo_data['clone_url'],
                                        ssh_url=repo_data['ssh_url'],
                                        language=repo_data.get('language'),
                                        size=repo_data['size'],
                                        stargazers_count=repo_data['stargazers_count'],
                                        watchers_count=repo_data['watchers_count'],
                                        forks_count=repo_data['forks_count'],
                                        open_issues_count=repo_data['open_issues_count'],
                                        default_branch=repo_data['default_branch'],
                                        created_at=repo_data['created_at'],
                                        updated_at=repo_data['updated_at'],
                                        pushed_at=repo_data['pushed_at'],
                                        license=repo_data.get('license'),
                                        topics=repo_data.get('topics', []),
                                        visibility=repo_data['visibility'],
                                        private=repo_data['private'],
                                        archived=repo_data['archived'],
                                        disabled=repo_data['disabled']
                                    )
                                    all_repos.append(repo)
                                except Exception as e:
                                    logger.error(f"Error parsing repository {repo_data.get('name', 'unknown')}: {e}")
                            
                            if len(repos_data) < per_page:
                                break
                            
                            page += 1
                        else:
                            logger.error(f"GitHub API error: {response.status} - {await response.text()}")
                            break
                            
                except Exception as e:
                    logger.error(f"Error fetching repositories: {e}")
                    break
        
        logger.info(f"📚 Fetched {len(all_repos)} repositories from GitHub API")
        return all_repos
    
    def _fetch_repositories_sync(self) -> List[Repository]:
        """Fetch repositories synchronously"""
        url = f"{self.base_url}/orgs/{self.organization}/repos"
        all_repos = []
        page = 1
        per_page = 100
        
        while True:
            params = {
                'page': page,
                'per_page': per_page,
                'sort': 'updated', 
                'direction': 'desc'
            }
            
            logger.info(f"🔄 Fetching page {page} of repositories...")
            
            try:
                response = requests.get(url, headers=self.headers, params=params, timeout=30)
                
                if response.status_code == 200:
                    repos_data = response.json()
                    
                    if not repos_data:
                        break
                    
                    for repo_data in repos_data:
                        try:
                            repo = Repository(
                                id=repo_data['id'],
                                name=repo_data['name'],
                                full_name=repo_data['full_name'],
                                description=repo_data.get('description'),
                                html_url=repo_data['html_url'],
                                clone_url=repo_data['clone_url'],
                                ssh_url=repo_data['ssh_url'],
                                language=repo_data.get('language'),
                                size=repo_data['size'],
                                stargazers_count=repo_data['stargazers_count'],
                                watchers_count=repo_data['watchers_count'],
                                forks_count=repo_data['forks_count'],
                                open_issues_count=repo_data['open_issues_count'],
                                default_branch=repo_data['default_branch'],
                                created_at=repo_data['created_at'],
                                updated_at=repo_data['updated_at'],
                                pushed_at=repo_data['pushed_at'],
                                license=repo_data.get('license'),
                                topics=repo_data.get('topics', []),
                                visibility=repo_data['visibility'],
                                private=repo_data['private'],
                                archived=repo_data['archived'],
                                disabled=repo_data['disabled']
                            )
                            all_repos.append(repo)
                        except Exception as e:
                            logger.error(f"Error parsing repository {repo_data.get('name', 'unknown')}: {e}")
                    
                    if len(repos_data) < per_page:
                        break
                    
                    page += 1
                else:
                    logger.error(f"GitHub API error: {response.status_code} - {response.text}")
                    break
                    
            except Exception as e:
                logger.error(f"Error fetching repositories: {e}")
                break
        
        logger.info(f"📚 Fetched {len(all_repos)} repositories from GitHub API")
        return all_repos
    
    async def get_repositories(self, force_refresh: bool = False) -> List[Repository]:
        """
        Get all repositories for the organization
        
        Args:
            force_refresh: If True, bypass cache and fetch fresh data
            
        Returns:
            List of Repository objects
        """
        if not force_refresh and self._is_cache_valid():
            cached_repos = self._load_from_cache()
            if cached_repos is not None:
                return cached_repos
        
        # Fetch fresh data
        try:
            repos = await self._fetch_repositories_async()
        except Exception as e:
            logger.error(f"Error in async fetch, falling back to sync: {e}")
            repos = self._fetch_repositories_sync()
        
        # Cache the results
        if repos:
            self._save_to_cache(repos)
        
        return repos
    
    def get_repositories_sync(self, force_refresh: bool = False) -> List[Repository]:
        """
        Get all repositories synchronously
        
        Args:
            force_refresh: If True, bypass cache and fetch fresh data
            
        Returns:
            List of Repository objects
        """
        if not force_refresh and self._is_cache_valid():
            cached_repos = self._load_from_cache()
            if cached_repos is not None:
                return cached_repos
        
        # Fetch fresh data
        repos = self._fetch_repositories_sync()
        
        # Cache the results
        if repos:
            self._save_to_cache(repos)
        
        return repos
    
    async def get_repository(self, repo_name: str) -> Optional[Repository]:
        """Get a specific repository by name"""
        repos = await self.get_repositories()
        for repo in repos:
            if repo.name == repo_name:
                return repo
        return None
    
    def filter_repositories(self, 
                          repositories: List[Repository],
                          language: Optional[str] = None,
                          min_stars: Optional[int] = None,
                          max_stars: Optional[int] = None,
                          is_archived: Optional[bool] = None,
                          has_topics: Optional[bool] = None,
                          search_term: Optional[str] = None) -> List[Repository]:
        """
        Filter repositories based on criteria
        
        Args:
            repositories: List of repositories to filter
            language: Filter by programming language
            min_stars: Minimum number of stars
            max_stars: Maximum number of stars
            is_archived: Filter by archived status
            has_topics: Filter by presence of topics
            search_term: Search in name and description
            
        Returns:
            Filtered list of repositories
        """
        filtered = repositories
        
        if language:
            filtered = [r for r in filtered if r.language and r.language.lower() == language.lower()]
        
        if min_stars is not None:
            filtered = [r for r in filtered if r.stargazers_count >= min_stars]
        
        if max_stars is not None:
            filtered = [r for r in filtered if r.stargazers_count <= max_stars]
        
        if is_archived is not None:
            filtered = [r for r in filtered if r.archived == is_archived]
        
        if has_topics is not None:
            if has_topics:
                filtered = [r for r in filtered if r.topics]
            else:
                filtered = [r for r in filtered if not r.topics]
        
        if search_term:
            search_lower = search_term.lower()
            filtered = [r for r in filtered 
                       if search_lower in r.name.lower() or
                          (r.description and search_lower in r.description.lower())]
        
        return filtered
    
    def get_statistics(self, repositories: List[Repository]) -> Dict[str, Any]:
        """Get statistics about repositories"""
        total_repos = len(repositories)
        if total_repos == 0:
            return {}
        
        # Language statistics
        languages = {}
        for repo in repositories:
            if repo.language:
                languages[repo.language] = languages.get(repo.language, 0) + 1
        
        # Sort languages by frequency
        sorted_languages = dict(sorted(languages.items(), key=lambda x: x[1], reverse=True))
        
        # Topic statistics
        topics = {}
        for repo in repositories:
            for topic in repo.topics:
                topics[topic] = topics.get(topic, 0) + 1
        
        # Sort topics by frequency
        sorted_topics = dict(sorted(topics.items(), key=lambda x: x[1], reverse=True))
        
        # General statistics
        total_stars = sum(repo.stargazers_count for repo in repositories)
        total_forks = sum(repo.forks_count for repo in repositories)
        public_repos = len([r for r in repositories if not r.private])
        private_repos = len([r for r in repositories if r.private])
        archived_repos = len([r for r in repositories if r.archived])
        
        return {
            "total_repositories": total_repos,
            "public_repositories": public_repos,
            "private_repositories": private_repos,
            "archived_repositories": archived_repos,
            "total_stars": total_stars,
            "total_forks": total_forks,
            "languages": sorted_languages,
            "top_languages": list(sorted_languages.keys())[:10],
            "topics": sorted_topics,
            "popular_topics": list(sorted_topics.keys())[:10],
            "average_stars": round(total_stars / total_repos, 1) if total_repos > 0 else 0,
            "average_forks": round(total_forks / total_repos, 1) if total_repos > 0 else 0
        }


def main():
    """Test the GitHub Repository Manager"""
    import asyncio
    
    logging.basicConfig(level=logging.INFO)
    
    # Create manager
    manager = GitHubRepoManager()
    
    # Test sync function
    print("🔍 Testing sync repository fetch...")
    repos = manager.get_repositories_sync()
    
    print(f"\n📊 Found {len(repos)} repositories:")
    for repo in repos[:5]:  # Show first 5
        print(f"  - {repo.name}: {repo.language} | ⭐ {repo.stargazers_count} | 🍴 {repo.forks_count}")
    
    # Test statistics
    stats = manager.get_statistics(repos)
    print(f"\n📈 Statistics:")
    print(f"  Total: {stats.get('total_repositories')}")
    print(f"  Languages: {list(stats.get('languages', {}).keys())[:5]}")
    print(f"  Total Stars: {stats.get('total_stars')}")


if __name__ == "__main__":
    main()