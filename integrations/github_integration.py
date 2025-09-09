#!/usr/bin/env python3
"""
PANACEA ICONO S.A. - Integración con GitHub
Gestión y monitoreo de repositorios del ecosistema Panacea
"""

import asyncio
import aiohttp
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
import json
import os

@dataclass
class RepositoryInfo:
    """Información de un repositorio"""
    name: str
    full_name: str
    description: str
    language: str
    stars: int
    forks: int
    watchers: int
    last_updated: str
    url: str
    private: bool
    archived: bool

class GitHubIntegration:
    """Integración con GitHub para el ecosistema Panacea"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.api_base = "https://api.github.com"
        self.token = os.getenv("GITHUB_TOKEN")
        self.organization = "panacea-icono"
        self.session = None
        
        if not self.token:
            self.logger.warning("GITHUB_TOKEN no configurado")
    
    async def __aenter__(self):
        """Async context manager entry"""
        headers = {}
        if self.token:
            headers["Authorization"] = f"token {self.token}"
        
        self.session = aiohttp.ClientSession(headers=headers)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
    
    async def get_organization_repos(self) -> List[RepositoryInfo]:
        """Obtener todos los repositorios de la organización"""
        repos = []
        page = 1
        per_page = 100
        
        while True:
            url = f"{self.api_base}/orgs/{self.organization}/repos"
            params = {
                "page": page,
                "per_page": per_page,
                "sort": "updated",
                "direction": "desc"
            }
            
            try:
                async with self.session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        if not data:  # No hay más páginas
                            break
                        
                        for repo_data in data:
                            repo = RepositoryInfo(
                                name=repo_data["name"],
                                full_name=repo_data["full_name"],
                                description=repo_data.get("description", ""),
                                language=repo_data.get("language", ""),
                                stars=repo_data["stargazers_count"],
                                forks=repo_data["forks_count"],
                                watchers=repo_data["watchers_count"],
                                last_updated=repo_data["updated_at"],
                                url=repo_data["html_url"],
                                private=repo_data["private"],
                                archived=repo_data["archived"]
                            )
                            repos.append(repo)
                        
                        page += 1
                    else:
                        self.logger.error(f"Error obteniendo repos: HTTP {response.status}")
                        break
            except Exception as e:
                self.logger.error(f"Error en get_organization_repos: {e}")
                break
        
        return repos
    
    async def get_repo_details(self, repo_name: str) -> Optional[Dict[str, Any]]:
        """Obtener detalles específicos de un repositorio"""
        url = f"{self.api_base}/repos/{self.organization}/{repo_name}"
        
        try:
            async with self.session.get(url) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    self.logger.error(f"Error obteniendo repo {repo_name}: HTTP {response.status}")
                    return None
        except Exception as e:
            self.logger.error(f"Error en get_repo_details: {e}")
            return None
    
    async def get_repo_commits(self, repo_name: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Obtener commits recientes de un repositorio"""
        url = f"{self.api_base}/repos/{self.organization}/{repo_name}/commits"
        params = {"per_page": limit}
        
        try:
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    self.logger.error(f"Error obteniendo commits de {repo_name}: HTTP {response.status}")
                    return []
        except Exception as e:
            self.logger.error(f"Error en get_repo_commits: {e}")
            return []
    
    async def get_repo_issues(self, repo_name: str, state: str = "open") -> List[Dict[str, Any]]:
        """Obtener issues de un repositorio"""
        url = f"{self.api_base}/repos/{self.organization}/{repo_name}/issues"
        params = {"state": state, "per_page": 100}
        
        try:
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    self.logger.error(f"Error obteniendo issues de {repo_name}: HTTP {response.status}")
                    return []
        except Exception as e:
            self.logger.error(f"Error en get_repo_issues: {e}")
            return []
    
    async def get_repo_pull_requests(self, repo_name: str, state: str = "open") -> List[Dict[str, Any]]:
        """Obtener pull requests de un repositorio"""
        url = f"{self.api_base}/repos/{self.organization}/{repo_name}/pulls"
        params = {"state": state, "per_page": 100}
        
        try:
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    self.logger.error(f"Error obteniendo PRs de {repo_name}: HTTP {response.status}")
                    return []
        except Exception as e:
            self.logger.error(f"Error en get_repo_pull_requests: {e}")
            return []
    
    async def get_repo_releases(self, repo_name: str) -> List[Dict[str, Any]]:
        """Obtener releases de un repositorio"""
        url = f"{self.api_base}/repos/{self.organization}/{repo_name}/releases"
        
        try:
            async with self.session.get(url) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    self.logger.error(f"Error obteniendo releases de {repo_name}: HTTP {response.status}")
                    return []
        except Exception as e:
            self.logger.error(f"Error en get_repo_releases: {e}")
            return []
    
    async def analyze_ecosystem_health(self) -> Dict[str, Any]:
        """Analizar la salud general del ecosistema en GitHub"""
        repos = await self.get_organization_repos()
        
        if not repos:
            return {"error": "No se pudieron obtener repositorios"}
        
        # Categorizar repositorios
        categories = {
            "panacea": [],
            "fibonacci": [],
            "panas": [],
            "other": []
        }
        
        for repo in repos:
            name_lower = repo.name.lower()
            if "panacea" in name_lower:
                categories["panacea"].append(repo)
            elif "fibonacci" in name_lower:
                categories["fibonacci"].append(repo)
            elif "panas" in name_lower:
                categories["panas"].append(repo)
            else:
                categories["other"].append(repo)
        
        # Calcular métricas
        total_repos = len(repos)
        public_repos = len([r for r in repos if not r.private])
        private_repos = len([r for r in repos if r.private])
        archived_repos = len([r for r in repos if r.archived])
        
        total_stars = sum(r.stars for r in repos)
        total_forks = sum(r.forks for r in repos)
        total_watchers = sum(r.watchers for r in repos)
        
        # Repositorios más activos (por última actualización)
        active_repos = sorted(repos, key=lambda x: x.last_updated, reverse=True)[:10]
        
        # Repositorios más populares (por estrellas)
        popular_repos = sorted(repos, key=lambda x: x.stars, reverse=True)[:10]
        
        return {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_repositories": total_repos,
                "public_repositories": public_repos,
                "private_repositories": private_repos,
                "archived_repositories": archived_repos,
                "total_stars": total_stars,
                "total_forks": total_forks,
                "total_watchers": total_watchers
            },
            "categories": {
                name: {
                    "count": len(repo_list),
                    "repositories": [repo.name for repo in repo_list]
                }
                for name, repo_list in categories.items()
            },
            "most_active": [
                {
                    "name": repo.name,
                    "last_updated": repo.last_updated,
                    "stars": repo.stars,
                    "forks": repo.forks
                }
                for repo in active_repos
            ],
            "most_popular": [
                {
                    "name": repo.name,
                    "stars": repo.stars,
                    "forks": repo.forks,
                    "watchers": repo.watchers
                }
                for repo in popular_repos
            ]
        }
    
    async def monitor_repo_changes(self, repo_name: str) -> Dict[str, Any]:
        """Monitorear cambios en un repositorio específico"""
        details = await self.get_repo_details(repo_name)
        if not details:
            return {"error": f"No se pudo obtener detalles de {repo_name}"}
        
        commits = await self.get_repo_commits(repo_name, 5)
        issues = await self.get_repo_issues(repo_name)
        prs = await self.get_repo_pull_requests(repo_name)
        releases = await self.get_repo_releases(repo_name)
        
        return {
            "repository": repo_name,
            "timestamp": datetime.now().isoformat(),
            "details": {
                "description": details.get("description", ""),
                "language": details.get("language", ""),
                "stars": details.get("stargazers_count", 0),
                "forks": details.get("forks_count", 0),
                "watchers": details.get("watchers_count", 0),
                "last_updated": details.get("updated_at", ""),
                "private": details.get("private", False),
                "archived": details.get("archived", False)
            },
            "recent_activity": {
                "commits": len(commits),
                "open_issues": len([i for i in issues if i.get("state") == "open"]),
                "open_prs": len([p for p in prs if p.get("state") == "open"]),
                "releases": len(releases)
            },
            "recent_commits": [
                {
                    "sha": commit.get("sha", "")[:7],
                    "message": commit.get("commit", {}).get("message", ""),
                    "author": commit.get("commit", {}).get("author", {}).get("name", ""),
                    "date": commit.get("commit", {}).get("author", {}).get("date", "")
                }
                for commit in commits
            ]
        }

async def main():
    """Función principal para testing de la integración"""
    print("🐙 GITHUB INTEGRATION - PANACEA ECOSYSTEM")
    print("=" * 50)
    
    async with GitHubIntegration() as github:
        # Analizar salud del ecosistema
        print("\n📊 Análisis del Ecosistema:")
        health = await github.analyze_ecosystem_health()
        
        if "error" not in health:
            summary = health["summary"]
            print(f"Total de Repositorios: {summary['total_repositories']}")
            print(f"Repositorios Públicos: {summary['public_repositories']}")
            print(f"Repositorios Privados: {summary['private_repositories']}")
            print(f"Total de Estrellas: {summary['total_stars']}")
            print(f"Total de Forks: {summary['total_forks']}")
            
            print("\n📁 Categorías:")
            for category, data in health["categories"].items():
                print(f"  {category.title()}: {data['count']} repositorios")
            
            print("\n🔥 Repositorios Más Activos:")
            for repo in health["most_active"][:5]:
                print(f"  {repo['name']} - {repo['last_updated']}")
        else:
            print(f"Error: {health['error']}")
        
        # Monitorear repositorio específico
        print("\n🔍 Monitoreo de Smart Contracts:")
        smart_contracts = await github.monitor_repo_changes("panacea_smart_contracts")
        
        if "error" not in smart_contracts:
            details = smart_contracts["details"]
            activity = smart_contracts["recent_activity"]
            print(f"Descripción: {details['description']}")
            print(f"Lenguaje: {details['language']}")
            print(f"Estrellas: {details['stars']}")
            print(f"Commits Recientes: {activity['commits']}")
            print(f"Issues Abiertas: {activity['open_issues']}")
            print(f"PRs Abiertos: {activity['open_prs']}")
        else:
            print(f"Error: {smart_contracts['error']}")

if __name__ == "__main__":
    asyncio.run(main())
