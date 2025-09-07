#!/usr/bin/env python3
"""
README Generator for PANACEA ICONO Ecosystem
Generates an enhanced README with fork tracking and activity feed
"""

import json
from datetime import datetime
from typing import Dict, List
from ecosystem_tracker import EcosystemTracker

class ReadmeGenerator:
    """Generates enhanced README with ecosystem tracking information"""
    
    def __init__(self, data_file: str = "ecosystem_data.json"):
        """Initialize with ecosystem data"""
        self.data_file = data_file
        self.data = self.load_data()
    
    def load_data(self) -> Dict:
        """Load ecosystem data"""
        tracker = EcosystemTracker()
        return tracker.load_data(self.data_file)
    
    def generate_ecosystem_header(self) -> str:
        """Generate ecosystem header with summary stats"""
        if not self.data:
            return ""
        
        stats = self.data.get('activity_summary', {})
        fork_stats = self.data.get('fork_summary', {})
        last_updated = self.data.get('last_updated', datetime.now().isoformat())
        
        try:
            update_time = datetime.fromisoformat(last_updated.replace('Z', '+00:00')).strftime("%d/%m/%Y a las %H:%M")
        except:
            update_time = "fecha desconocida"
        
        header = f"""
## 🔄 Estado del Ecosistema

**Última actualización**: {update_time}

### 📊 Resumen General
- 📚 **Repositorios totales**: {stats.get('total_repositories', 0)}
- 🍴 **Forks totales**: {fork_stats.get('total_forks', 0)}
- 📈 **Repositorios con forks**: {fork_stats.get('repositories_with_forks', 0)}
- 📝 **Commits recientes**: {stats.get('total_commits', 0)}
- 🏷️ **Releases recientes**: {stats.get('total_releases', 0)}

"""
        return header
    
    def generate_fork_analysis(self) -> str:
        """Generate fork analysis section"""
        if not self.data or not self.data.get('repositories'):
            return ""
        
        repos_with_forks = []
        all_forkers = []
        
        for repo_key, repo_data in self.data['repositories'].items():
            forks = repo_data.get('forks', [])
            forks_count = len(forks) if forks else repo_data.get('forks_count', 0)
            
            if forks_count > 0:
                repos_with_forks.append({
                    'name': repo_key,
                    'forks_count': forks_count,
                    'forks': forks,
                    'description': repo_data.get('description', '')[:60]
                })
                
                # Collect forkers
                for fork in forks:
                    if isinstance(fork, dict):
                        forker = fork.get('owner', 'Unknown')
                        if forker not in all_forkers:
                            all_forkers.append(forker)
        
        repos_with_forks.sort(key=lambda x: x['forks_count'], reverse=True)
        
        content = "## 🍴 Análisis de Forks\n\n"
        
        if repos_with_forks:
            content += "### 📈 Repositorios más forkeados\n\n"
            for repo in repos_with_forks[:10]:
                content += f"- **{repo['name']}** - {repo['forks_count']} forks\n"
                if repo['description']:
                    content += f"  - *{repo['description']}*\n"
                
                # Show recent forkers
                if repo['forks']:
                    forkers = [f['owner'] for f in repo['forks'][:3] if isinstance(f, dict)]
                    if forkers:
                        content += f"  - 👥 Forkers: {', '.join(forkers)}\n"
                content += "\n"
        else:
            content += "No se han detectado forks en los repositorios del ecosistema.\n\n"
        
        if all_forkers:
            content += f"### 👥 Contribuidores externos ({len(all_forkers)})\n\n"
            for forker in all_forkers[:10]:
                content += f"- [@{forker}](https://github.com/{forker})\n"
            
            if len(all_forkers) > 10:
                content += f"\n*Y {len(all_forkers) - 10} contribuidores más...*\n"
        
        content += "\n"
        return content
    
    def generate_activity_feed(self) -> str:
        """Generate recent activity feed"""
        if not self.data or not self.data.get('recent_activity'):
            return ""
        
        activities = self.data['recent_activity'][:20]  # Top 20 activities
        
        content = "## 🎯 Feed de Actividad Reciente\n\n"
        content += "*Últimas actualizaciones en el ecosistema*\n\n"
        
        for activity in activities:
            emoji = "📝" if activity['type'] == 'commit' else "🏷️" if activity['type'] == 'release' else "📚"
            
            # Format date
            try:
                if activity['date'].endswith('Z'):
                    date = datetime.fromisoformat(activity['date'].replace('Z', '+00:00')).strftime("%d/%m/%Y")
                elif 'T' in activity['date']:
                    date = datetime.fromisoformat(activity['date']).strftime("%d/%m/%Y")
                else:
                    # Handle simple date format
                    date = activity['date'].replace('T00:00:00Z', '')
            except:
                date = activity['date']
            
            repo_name = activity['repository']
            title = activity['title']
            url = activity.get('url', f"https://github.com/{repo_name}")
            
            content += f"- {emoji} **[{repo_name}]({url})** - {title} *({date})*\n"
            
            if activity['type'] == 'commit' and activity.get('author'):
                content += f"  - 👤 Por: {activity['author']}\n"
        
        content += "\n"
        return content
    
    def generate_repository_stats(self) -> str:
        """Generate enhanced repository statistics"""
        if not self.data or not self.data.get('repositories'):
            return ""
        
        repos = self.data['repositories']
        
        # Language distribution
        languages = {}
        total_stars = 0
        total_forks = 0
        recent_repos = []
        
        for repo_data in repos.values():
            lang = repo_data.get('language', 'Unknown')
            if lang and lang != 'Sin especificar':
                languages[lang] = languages.get(lang, 0) + 1
            
            total_stars += repo_data.get('stars', 0)
            total_forks += repo_data.get('forks_count', 0)
            
            # Track recent updates
            last_update = repo_data.get('last_updated', '')
            if last_update:
                recent_repos.append({
                    'name': repo_data.get('full_name', repo_data.get('name', '')),
                    'update': last_update,
                    'description': repo_data.get('description', '')[:50]
                })
        
        # Sort languages by count
        sorted_languages = sorted(languages.items(), key=lambda x: x[1], reverse=True)
        
        content = "## 📊 Estadísticas Mejoradas\n\n"
        content += f"- **Total de repositorios**: {len(repos)}\n"
        content += f"- **Total de estrellas**: {total_stars}\n" 
        content += f"- **Total de forks**: {total_forks}\n"
        content += f"- **Lenguajes detectados**: {len(languages)}\n\n"
        
        if sorted_languages:
            content += "### 🔤 Distribución de lenguajes\n\n"
            for lang, count in sorted_languages[:10]:
                content += f"- **{lang}**: {count} repositorios\n"
        
        content += "\n"
        return content
    
    def generate_enhanced_readme(self, original_readme_path: str = "README.md", output_path: str = None) -> str:
        """Generate enhanced README with ecosystem tracking"""
        
        # Read original README
        try:
            with open(original_readme_path, 'r', encoding='utf-8') as f:
                original_content = f.read()
        except Exception as e:
            print(f"❌ Error reading original README: {e}")
            return ""
        
        # Find insertion point (after the main header)
        lines = original_content.split('\n')
        insert_index = 0
        
        # Look for the ecosystem header or after the main title
        for i, line in enumerate(lines):
            if line.startswith('## Repositorios del Ecosistema'):
                insert_index = i
                break
            elif line.startswith('## 🏢 Organización'):
                insert_index = i
                break
        
        # Generate new sections
        ecosystem_header = self.generate_ecosystem_header()
        fork_analysis = self.generate_fork_analysis()
        activity_feed = self.generate_activity_feed()
        enhanced_stats = self.generate_repository_stats()
        
        # Insert new content
        new_lines = lines[:insert_index]
        
        if ecosystem_header:
            new_lines.extend(ecosystem_header.split('\n'))
        
        if fork_analysis:
            new_lines.extend(fork_analysis.split('\n'))
        
        if activity_feed:
            new_lines.extend(activity_feed.split('\n'))
        
        if enhanced_stats:
            new_lines.extend(enhanced_stats.split('\n'))
        
        new_lines.extend(lines[insert_index:])
        
        enhanced_readme = '\n'.join(new_lines)
        
        # Save enhanced README
        if output_path:
            try:
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(enhanced_readme)
                print(f"✅ Enhanced README saved to {output_path}")
            except Exception as e:
                print(f"❌ Error saving enhanced README: {e}")
        
        return enhanced_readme

def main():
    """Main function to generate enhanced README"""
    print("📄 Generating enhanced README...")
    
    # Update ecosystem data first
    print("🔄 Updating ecosystem data...")
    tracker = EcosystemTracker()
    data = tracker.track_ecosystem_activity(days_back=14)
    tracker.save_data(data)
    
    # Generate enhanced README
    generator = ReadmeGenerator()
    enhanced_readme = generator.generate_enhanced_readme(output_path="README_enhanced.md")
    
    if enhanced_readme:
        print("✅ Enhanced README generated successfully!")
        print("📄 Preview of new sections:")
        print("-" * 50)
        
        # Show preview of ecosystem header
        lines = enhanced_readme.split('\n')
        in_ecosystem_section = False
        preview_lines = 0
        
        for line in lines:
            if line.startswith('## 🔄 Estado del Ecosistema'):
                in_ecosystem_section = True
                preview_lines = 0
            
            if in_ecosystem_section and preview_lines < 20:
                print(line)
                preview_lines += 1
                
            if in_ecosystem_section and (line.startswith('## ') and not line.startswith('## 🔄')):
                break
    else:
        print("❌ Failed to generate enhanced README")

if __name__ == "__main__":
    main()