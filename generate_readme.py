#!/usr/bin/env python3
"""
📚 README Generator for PANACEA ICONO
Generates and updates README.md with dynamic repository information
"""

import os
import sys
import asyncio
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

# Add current directory to path to import our modules
sys.path.insert(0, str(Path(__file__).parent))

from github_repo_manager_mcp import GitHubRepoManagerMCP, Repository

logger = logging.getLogger(__name__)


class ReadmeGenerator:
    """Generate README.md with dynamic repository data"""
    
    def __init__(self, output_file: str = "README.md"):
        self.output_file = Path(output_file)
        self.github_manager = GitHubRepoManagerMCP()
        
    def generate_repository_entry(self, repo: Repository, index: int) -> str:
        """Generate a markdown entry for a repository"""
        description = repo.description if repo.description else "Sin descripción"
        language = repo.language if repo.language else "Sin especificar"
        license_name = "Sin licencia"  # We don't have license info in our current data
        
        entry = f"""### {index}. [{repo.name}]({repo.html_url})

- **Descripción**: {description}
- **Lenguaje**: {language}
- **Estrellas**: ⭐ {repo.stargazers_count} | **Forks**: 🍴 {repo.forks_count} | **Issues**: 📋 {repo.open_issues_count}
- **Última actualización**: {repo.last_updated_formatted}
- **Licencia**: {license_name}
- **Temas**: {repo.topics_str}
- **URL**: [{repo.html_url}]({repo.html_url})

```bash
# Clonar repositorio
git clone {repo.html_url}.git
cd {repo.name}
```

"""
        return entry
    
    def generate_quick_links(self, repositories: List[Repository]) -> str:
        """Generate quick links section"""
        links = []
        for repo in repositories:
            links.append(f"- [{repo.name}]({repo.html_url})")
        
        return "\n".join(links)
    
    def generate_statistics_section(self, stats: Dict[str, Any]) -> str:
        """Generate statistics section"""
        languages_str = ", ".join([f"{lang} ({count})" for lang, count in list(stats.get('languages', {}).items())[:5]])
        
        return f"""## 📊 Estadísticas Generales

- **Total de repositorios**: {stats.get('total_repositories', 0)}
- **Repositorios públicos**: {stats.get('public_repositories', 0)}
- **Repositorios privados**: {stats.get('private_repositories', 0)}
- **Repositorios archivados**: {stats.get('archived_repositories', 0)}
- **Total de estrellas**: {stats.get('total_stars', 0)}
- **Total de forks**: {stats.get('total_forks', 0)}
- **Lenguajes más usados**: {languages_str}

"""
    
    def generate_topics_section(self, stats: Dict[str, Any]) -> str:
        """Generate popular topics section"""
        topics = stats.get('topics', {})
        if not topics:
            return ""
        
        topic_lines = []
        for topic, count in list(topics.items())[:10]:
            topic_lines.append(f"- `{topic}` ({count} repositorio{'s' if count > 1 else ''})")
        
        if not topic_lines:
            return ""
        
        return f"""## 🏷️ Temas Populares

{chr(10).join(topic_lines)}

"""
    
    def generate_recent_repos_section(self, repositories: List[Repository]) -> str:
        """Generate recent repositories section"""
        # Sort by updated_at and take first 5
        sorted_repos = sorted(repositories, key=lambda r: r.updated_at, reverse=True)[:5]
        
        repo_lines = []
        for repo in sorted_repos:
            repo_lines.append(f"- [{repo.name}]({repo.html_url}) - {repo.last_updated_formatted}")
        
        return f"""## 📅 Repositorios Recientes

{chr(10).join(repo_lines)}

"""
    
    async def generate_readme(self) -> str:
        """Generate the complete README.md content"""
        logger.info("🔄 Fetching repository data...")
        
        # Get repositories and statistics
        repositories = await self.github_manager.get_repositories(force_refresh=True)
        stats = self.github_manager.get_statistics(repositories)
        
        logger.info(f"📚 Processing {len(repositories)} repositories...")
        
        # Sort repositories by name for consistent ordering
        repositories.sort(key=lambda r: r.name.lower())
        
        # Generate header
        header = f"""# 📚 Repositorios de panacea-icono

> Lista dinámica de repositorios en [panacea-icono](https://github.com/panacea-icono)

## 🏢 Organización

**panacea-icono**

- 🌐 GitHub: [panacea-icono](https://github.com/panacea-icono)

---

"""
        
        # Generate repository list
        repo_list = "## 📋 Lista de Repositorios\n\n"
        for i, repo in enumerate(repositories, 1):
            repo_list += self.generate_repository_entry(repo, i)
        
        repo_list += "---\n\n"
        
        # Generate quick links
        quick_links = f"""## 🔗 Enlaces Rápidos

{self.generate_quick_links(repositories)}

---

"""
        
        # Generate statistics
        statistics = self.generate_statistics_section(stats)
        statistics += "---\n\n"
        
        # Generate topics
        topics = self.generate_topics_section(stats)
        if topics:
            topics += "---\n\n"
        
        # Generate recent repositories
        recent = self.generate_recent_repos_section(repositories)
        recent += "---\n\n"
        
        # Generate API section
        api_section = f"""## 🚀 API Dinámica

Esta lista está disponible dinámicamente a través de nuestra API:

- **Lista completa**: `GET /api/repositories`
- **Repositorio específico**: `GET /api/repositories/{{name}}`
- **Estadísticas**: `GET /api/repositories/statistics`
- **Filtros disponibles**: `language`, `min_stars`, `max_stars`, `search`, etc.

### Ejemplos de uso:

```bash
# Obtener todos los repositorios
curl https://panacea-icono-ai-78b4eb86c23b.herokuapp.com/api/repositories

# Filtrar por lenguaje Python
curl "https://panacea-icono-ai-78b4eb86c23b.herokuapp.com/api/repositories?language=Python"

# Buscar repositorios con "bot" en el nombre
curl "https://panacea-icono-ai-78b4eb86c23b.herokuapp.com/api/repositories?search=bot"

# Obtener estadísticas
curl https://panacea-icono-ai-78b4eb86c23b.herokuapp.com/api/repositories/statistics
```

---

"""
        
        # Generate footer
        footer = f"""## 🤝 Contribuir

Para contribuir a cualquiera de estos repositorios:

1. Fork el repositorio que te interese
2. Crea una rama para tu feature: `git checkout -b feature/nueva-funcionalidad`
3. Commit tus cambios: `git commit -m 'Add: nueva funcionalidad'`
4. Push a la rama: `git push origin feature/nueva-funcionalidad`
5. Abre un Pull Request

---

## 📞 Contacto

- **Email**: info@iconosa.com
- GitHub: [panacea-icono](https://github.com/panacea-icono)
- **Web**: https://iconosa.com

---

*Última actualización: {datetime.now().strftime('%d/%m/%Y, %H:%M:%S')}*

*Generado automáticamente por el sistema de gestión de repositorios dinámico de PANACEA ICONO*

"""
        
        # Combine all sections
        readme_content = header + repo_list + quick_links + statistics + topics + recent + api_section + footer
        
        return readme_content
    
    async def update_readme(self) -> bool:
        """Update the README.md file"""
        try:
            logger.info("📝 Generating README.md content...")
            content = await self.generate_readme()
            
            logger.info(f"💾 Writing to {self.output_file}...")
            with open(self.output_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            logger.info(f"✅ Successfully updated {self.output_file}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error updating README: {e}")
            return False


async def main():
    """Main function"""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    print("🏥 PANACEA ICONO - Dynamic README Generator")
    print("=" * 50)
    
    generator = ReadmeGenerator()
    success = await generator.update_readme()
    
    if success:
        print("\n✅ README.md updated successfully!")
        print("📍 The repository list is now dynamic and up-to-date.")
    else:
        print("\n❌ Failed to update README.md")
        return 1
    
    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())