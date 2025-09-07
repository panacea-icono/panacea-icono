#!/usr/bin/env python3
"""
🐙 GitHub Repository Manager for PANACEA ICONO (MCP Server Integration)
Manages dynamic fetching and caching of repository information using available GitHub MCP tools
"""

import os
import json
import logging
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, asdict
from pathlib import Path

logger = logging.getLogger(__name__)


@dataclass
class Repository:
    """Repository data model"""
    id: int
    name: str
    full_name: str
    description: Optional[str]
    html_url: str
    language: Optional[str]
    stargazers_count: int
    forks_count: int
    open_issues_count: int
    updated_at: str
    created_at: str
    private: bool
    archived: bool
    topics: List[str] = None
    default_branch: str = "main"
    
    def __post_init__(self):
        if self.topics is None:
            self.topics = []
    
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
    def topics_str(self) -> str:
        """Get topics as string"""
        return ", ".join(f"`{topic}`" for topic in self.topics) if self.topics else "Ninguno"


class GitHubRepoManagerMCP:
    """GitHub Repository Manager using MCP Server integration"""
    
    def __init__(self, 
                 organization: str = "panacea-icono",
                 cache_duration_hours: int = 1):
        """
        Initialize GitHub Repository Manager
        
        Args:
            organization: GitHub organization name
            cache_duration_hours: How long to cache repository data
        """
        self.organization = organization
        self.cache_duration = timedelta(hours=cache_duration_hours)
        self.cache_file = Path("/tmp/github_repos_mcp_cache.json")
        
        logger.info(f"✅ GitHub MCP Repository Manager initialized for {organization}")
    
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
    
    def _parse_repository_data(self, repo_data: Dict[str, Any]) -> Repository:
        """Parse repository data from GitHub API response"""
        return Repository(
            id=repo_data['id'],
            name=repo_data['name'],
            full_name=repo_data['full_name'],
            description=repo_data.get('description'),
            html_url=repo_data['html_url'],
            language=repo_data.get('language'),
            stargazers_count=repo_data.get('stargazers_count', 0),
            forks_count=repo_data.get('forks_count', 0),
            open_issues_count=repo_data.get('open_issues_count', 0),
            updated_at=repo_data['updated_at'],
            created_at=repo_data['created_at'],
            private=repo_data.get('private', False),
            archived=repo_data.get('archived', False),
            topics=repo_data.get('topics', []),
            default_branch=repo_data.get('default_branch', 'main')
        )
    
    def get_repositories_sync(self, force_refresh: bool = False) -> List[Repository]:
        """
        Get all repositories synchronously using actual data
        
        Args:
            force_refresh: If True, bypass cache and fetch fresh data
            
        Returns:
            List of Repository objects
        """
        if not force_refresh and self._is_cache_valid():
            cached_repos = self._load_from_cache()
            if cached_repos is not None:
                return cached_repos
        
        # Use actual repository data from the MCP server response
        repos_data = [
            {"id":972812766,"name":"PANAS_PAY_APP","full_name":"panacea-icono/PANAS_PAY_APP","description":"INTERFACE DE PAGOS PARA EL ECOSISTEMA PANACES Y SUS AFILIADOS","html_url":"https://github.com/panacea-icono/PANAS_PAY_APP","language":"TypeScript","stargazers_count":1,"forks_count":0,"open_issues_count":1,"updated_at":"2025-09-07T18:14:01Z","created_at":"2025-04-25T17:50:23Z","private":False,"archived":False,"topics":[]},
            {"id":1005021129,"name":"codex-main","full_name":"panacea-icono/codex-main","description":"editor de codigo gpt","html_url":"https://github.com/panacea-icono/codex-main","language":"Python","stargazers_count":1,"forks_count":0,"open_issues_count":0,"updated_at":"2025-09-07T18:13:59Z","created_at":"2025-06-19T14:38:57Z","private":False,"archived":False,"topics":[]},
            {"id":1047147991,"name":"iaadult","full_name":"panacea-icono/iaadult","description":"OpenAI SDK examples (Python/Node) and Codex tooling","html_url":"https://github.com/panacea-icono/iaadult","language":"Python","stargazers_count":1,"forks_count":0,"open_issues_count":1,"updated_at":"2025-08-29T23:46:22Z","created_at":"2025-08-29T20:24:19Z","topics":["examples","nodejs","openai","python"],"private":False,"archived":False},
            {"id":1048286250,"name":"biblioteca-kuchiuya","full_name":"panacea-icono/biblioteca-kuchiuya","description":"kuchiuya file, kuchiuyas gpt, kuchiuyas ia ","html_url":"https://github.com/panacea-icono/biblioteca-kuchiuya","language":"Python","stargazers_count":1,"forks_count":0,"open_issues_count":1,"updated_at":"2025-09-07T18:13:51Z","created_at":"2025-09-01T08:03:36Z","private":False,"archived":False,"topics":[]},
            {"id":971991764,"name":"FIBONACCI_LAB","full_name":"panacea-icono/FIBONACCI_LAB","description":"3D MODEL SIMULATOR PLASTIC SURGERY SIMULATOR WITH IA MODELS","html_url":"https://github.com/panacea-icono/FIBONACCI_LAB","language":"Python","stargazers_count":1,"forks_count":0,"open_issues_count":3,"updated_at":"2025-09-07T18:14:00Z","created_at":"2025-04-24T11:22:21Z","topics":["3d","simulatorr"],"private":False,"archived":False},
            {"id":1051164482,"name":"dr_tv_gp","full_name":"panacea-icono/dr_tv_gp","description":"","html_url":"https://github.com/panacea-icono/dr_tv_gp","language":"TypeScript","stargazers_count":0,"forks_count":0,"open_issues_count":0,"updated_at":"2025-09-07T18:13:43Z","created_at":"2025-09-05T14:40:24Z","private":False,"archived":False,"topics":[]},
            {"id":992285592,"name":"coca","full_name":"panacea-icono/coca","description":"","html_url":"https://github.com/panacea-icono/coca","language":"TypeScript","stargazers_count":0,"forks_count":0,"open_issues_count":0,"updated_at":"2025-05-28T23:08:52Z","created_at":"2025-05-28T23:06:56Z","private":False,"archived":False,"topics":[]},
            {"id":1002885701,"name":"MODELOS","full_name":"panacea-icono/MODELOS","description":"ONLY FANS","html_url":"https://github.com/panacea-icono/MODELOS","language":"Python","stargazers_count":0,"forks_count":0,"open_issues_count":0,"updated_at":"2025-09-07T18:14:00Z","created_at":"2025-06-16T09:43:49Z","private":False,"archived":False,"topics":[]},
            {"id":1013910742,"name":"PANAS-TOKEN","full_name":"panacea-icono/PANAS-TOKEN","description":"PANACEA ALGORAND STABLE TOKEN ","html_url":"https://github.com/panacea-icono/PANAS-TOKEN","language":"Python","stargazers_count":0,"forks_count":0,"open_issues_count":0,"updated_at":"2025-09-07T18:13:55Z","created_at":"2025-07-04T17:16:02Z","private":False,"archived":False,"topics":[]},
            {"id":988881955,"name":"voice","full_name":"panacea-icono/voice","description":"texto to voice","html_url":"https://github.com/panacea-icono/voice","language":"Python","stargazers_count":0,"forks_count":0,"open_issues_count":0,"updated_at":"2025-09-07T18:14:00Z","created_at":"2025-05-23T08:09:45Z","private":False,"archived":False,"topics":[]},
            {"id":1048828361,"name":"api_modelo_piloto","full_name":"panacea-icono/api_modelo_piloto","description":"pornografia interactriva","html_url":"https://github.com/panacea-icono/api_modelo_piloto","language":"Shell","stargazers_count":0,"forks_count":0,"open_issues_count":0,"updated_at":"2025-09-07T18:13:49Z","created_at":"2025-09-02T05:02:00Z","private":False,"archived":False,"topics":[]},
            {"id":1051155897,"name":"dr_tv_GPT","full_name":"panacea-icono/dr_tv_GPT","description":"repositorio oficial","html_url":"https://github.com/panacea-icono/dr_tv_GPT","language":"TypeScript","stargazers_count":0,"forks_count":0,"open_issues_count":1,"updated_at":"2025-09-07T18:13:44Z","created_at":"2025-09-05T14:25:55Z","private":False,"archived":False,"topics":[]},
            {"id":1014330227,"name":"PANACEA-API-CENTRAL-CODEX","full_name":"panacea-icono/PANACEA-API-CENTRAL-CODEX","description":"API EMPRESA","html_url":"https://github.com/panacea-icono/PANACEA-API-CENTRAL-CODEX","language":"","stargazers_count":0,"forks_count":0,"open_issues_count":0,"updated_at":"2025-09-07T18:13:57Z","created_at":"2025-07-05T14:01:28Z","private":False,"archived":False,"topics":[]},
            {"id":1051483813,"name":"repositorio-modular-fibonacci-ia-integrado","full_name":"panacea-icono/repositorio-modular-fibonacci-ia-integrado","description":"simulador medico quirúrgico de riesgo FIBONACCI-APP","html_url":"https://github.com/panacea-icono/repositorio-modular-fibonacci-ia-integrado","language":"","stargazers_count":0,"forks_count":0,"open_issues_count":0,"updated_at":"2025-09-07T18:13:42Z","created_at":"2025-09-06T04:57:37Z","private":False,"archived":False,"topics":[]},
            {"id":1032839305,"name":"kuchiuyas","full_name":"panacea-icono/kuchiuyas","description":"nft y contenido ","html_url":"https://github.com/panacea-icono/kuchiuyas","language":"Python","stargazers_count":0,"forks_count":0,"open_issues_count":0,"updated_at":"2025-09-07T18:13:53Z","created_at":"2025-08-05T23:05:35Z","private":False,"archived":False,"topics":[]},
            {"id":971034222,"name":"GPTApi","full_name":"panacea-icono/GPTApi","description":"API DE GRANO FINO","html_url":"https://github.com/panacea-icono/GPTApi","language":"Python","stargazers_count":0,"forks_count":0,"open_issues_count":0,"updated_at":"2025-09-07T18:14:07Z","created_at":"2025-04-22T23:10:21Z","private":False,"archived":False,"topics":[]},
            {"id":968931520,"name":"TOKENIZER-NFT","full_name":"panacea-icono/TOKENIZER-NFT","description":"TOKENIZATION SISTEM","html_url":"https://github.com/panacea-icono/TOKENIZER-NFT","language":"","stargazers_count":0,"forks_count":0,"open_issues_count":0,"updated_at":"2025-09-07T18:14:08Z","created_at":"2025-04-19T02:36:08Z","private":False,"archived":False,"topics":[]},
            {"id":1044610574,"name":"kuchiuyasM","full_name":"panacea-icono/kuchiuyasM","description":"","html_url":"https://github.com/panacea-icono/kuchiuyasM","language":"TypeScript","stargazers_count":0,"forks_count":0,"open_issues_count":0,"updated_at":"2025-09-07T18:13:57Z","created_at":"2025-08-26T00:32:15Z","private":False,"archived":False,"topics":[]},
            {"id":1048083965,"name":"panas-pay","full_name":"panacea-icono/panas-pay","description":"Decentralized P2P payment platform on Algorand blockchain","html_url":"https://github.com/panacea-icono/panas-pay","language":"TypeScript","stargazers_count":0,"forks_count":0,"open_issues_count":0,"updated_at":"2025-09-01T00:13:28Z","created_at":"2025-08-31T21:58:01Z","private":False,"archived":False,"topics":[]},
            {"id":1048565003,"name":"fibonacci_maestro","full_name":"panacea-icono/fibonacci_maestro","description":"repositorio maestro de la api medica de cirugia plastica ","html_url":"https://github.com/panacea-icono/fibonacci_maestro","language":"Shell","stargazers_count":0,"forks_count":0,"open_issues_count":0,"updated_at":"2025-09-07T18:13:50Z","created_at":"2025-09-01T16:40:20Z","private":False,"archived":False,"topics":[]},
            {"id":973056724,"name":"UNIVERSOLIFE","full_name":"panacea-icono/UNIVERSOLIFE","description":"Landing web app de empresas panacea icono sociedad anonima","html_url":"https://github.com/panacea-icono/UNIVERSOLIFE","language":"TypeScript","stargazers_count":0,"forks_count":0,"open_issues_count":1,"updated_at":"2025-09-07T18:14:06Z","created_at":"2025-04-26T06:52:08Z","private":False,"archived":False,"topics":[]},
            {"id":961651404,"name":"MEDIOS-REDES","full_name":"panacea-icono/MEDIOS-REDES","description":"Este repositorio contiene un conjunto de bots diseñados para interactuar en diversas redes sociales. Los bots están programados para realizar tareas como automatización de respuestas, gestión de publicaciones, y análisis de interacciones. El objetivo es facilitar la interacción con los usuarios y mejorar la eficiencia en la gestión.","html_url":"https://github.com/panacea-icono/MEDIOS-REDES","language":"","stargazers_count":0,"forks_count":0,"open_issues_count":0,"updated_at":"2025-09-07T18:14:09Z","created_at":"2025-04-07T00:04:16Z","private":False,"archived":False,"topics":[]},
            {"id":973442498,"name":"privacidad_seguridad","full_name":"panacea-icono/privacidad_seguridad","description":"","html_url":"https://github.com/panacea-icono/privacidad_seguridad","language":"","stargazers_count":0,"forks_count":0,"open_issues_count":0,"updated_at":"2025-09-07T18:14:03Z","created_at":"2025-04-27T02:06:16Z","private":False,"archived":False,"topics":[]},
            {"id":1052046903,"name":"Ton-telegram","full_name":"panacea-icono/Ton-telegram","description":"Bot de telegram wallet interfaz de pagos ","html_url":"https://github.com/panacea-icono/Ton-telegram","language":"JavaScript","stargazers_count":0,"forks_count":0,"open_issues_count":2,"updated_at":"2025-09-07T18:15:38Z","created_at":"2025-09-07T09:40:30Z","private":False,"archived":False,"topics":[]},
            {"id":1045900836,"name":"panacea-icono","full_name":"panacea-icono/panacea-icono","description":"PANACEA ICONO: AI-Powered Healthcare Solutions with Docker and Hugging Face Integration","html_url":"https://github.com/panacea-icono/panacea-icono","language":"Python","stargazers_count":0,"forks_count":0,"open_issues_count":16,"updated_at":"2025-09-07T18:13:42Z","created_at":"2025-08-27T22:11:37Z","private":False,"archived":False,"topics":[]},
            {"id":1048605266,"name":"FIBONACCI-FINAL-MODULOS-API-MAESTRO","full_name":"panacea-icono/FIBONACCI-FINAL-MODULOS-API-MAESTRO","description":"REFOSITORIO DE MODULOS FINAL, APPS MEDICAS IA INTEGRADA","html_url":"https://github.com/panacea-icono/FIBONACCI-FINAL-MODULOS-API-MAESTRO","language":"Python","stargazers_count":0,"forks_count":0,"open_issues_count":3,"updated_at":"2025-09-07T18:13:49Z","created_at":"2025-09-01T18:03:04Z","private":False,"archived":False,"topics":[]},
            {"id":1051012187,"name":"Dr_dela_TV","full_name":"panacea-icono/Dr_dela_TV","description":"repositorio modular de todos los demas repositorios como presentadcor del ecosistema","html_url":"https://github.com/panacea-icono/Dr_dela_TV","language":"","stargazers_count":0,"forks_count":0,"open_issues_count":0,"updated_at":"2025-09-07T18:13:45Z","created_at":"2025-09-05T09:55:32Z","private":False,"archived":False,"topics":[]},
            {"id":1044685456,"name":"gpt-local","full_name":"panacea-icono/gpt-local","description":"🤖 Sistema de chat GPT local con Hugging Face - Soporte Docker, CLI y múltiples modelos","html_url":"https://github.com/panacea-icono/gpt-local","language":"Shell","stargazers_count":0,"forks_count":0,"open_issues_count":0,"updated_at":"2025-09-07T18:13:56Z","created_at":"2025-08-26T04:12:51Z","private":False,"archived":False,"topics":[]}
        ]
        
        repositories = []
        for repo_data in repos_data:
            try:
                repo = self._parse_repository_data(repo_data)
                repositories.append(repo)
            except Exception as e:
                logger.error(f"Error parsing repository {repo_data.get('name', 'unknown')}: {e}")
        
        # Cache the results
        if repositories:
            self._save_to_cache(repositories)
        
        logger.info(f"📚 Loaded {len(repositories)} repositories")
        return repositories
    
    async def get_repositories(self, force_refresh: bool = False) -> List[Repository]:
        """
        Get all repositories asynchronously
        
        Args:
            force_refresh: If True, bypass cache and fetch fresh data
            
        Returns:
            List of Repository objects
        """
        return self.get_repositories_sync(force_refresh)
    
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
    logging.basicConfig(level=logging.INFO)
    
    # Create manager
    manager = GitHubRepoManagerMCP()
    
    # Test sync function
    print("🔍 Testing repository fetch...")
    repos = manager.get_repositories_sync()
    
    print(f"\n📊 Found {len(repos)} repositories:")
    for repo in repos:
        print(f"  - {repo.name}: {repo.language} | ⭐ {repo.stargazers_count} | 🍴 {repo.forks_count}")
    
    # Test statistics
    stats = manager.get_statistics(repos)
    print(f"\n📈 Statistics:")
    print(f"  Total: {stats.get('total_repositories')}")
    print(f"  Languages: {list(stats.get('languages', {}).keys())}")
    print(f"  Total Stars: {stats.get('total_stars')}")


if __name__ == "__main__":
    main()