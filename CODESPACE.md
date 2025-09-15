# 🚀 PANACEA ICONO Ecosystem Development Environment

## 🏥 Codespace Integration

This repository includes an integrated development environment for working with the entire PANACEA ICONO ecosystem. The codespace automatically sets up multiple repositories and provides tools for cross-repository development.

### 🛠 Features

- **Multi-Repository Workspace**: Automatic cloning and setup of key ecosystem repositories
- **Integrated Development Tools**: Python, Node.js, TypeScript, Docker support
- **Ecosystem Navigation**: Built-in scripts for managing multiple repositories
- **Synchronized Development**: Tools for keeping repositories in sync
- **Pre-configured VS Code**: Optimized settings and extensions for the ecosystem

### 🚀 Quick Start

#### Option 1: GitHub Codespaces (Recommended)
1. Click the "Code" button on this repository
2. Select "Codespaces" → "Create codespace on main"
3. Wait for the environment to setup (3-5 minutes)
4. The ecosystem will be automatically configured

#### Option 2: Local Dev Containers
1. Ensure Docker and VS Code with Dev Containers extension are installed
2. Clone this repository
3. Open in VS Code and click "Reopen in Container" when prompted
4. Wait for the setup to complete

### 📂 Workspace Structure

After setup, your workspace will contain:

```
/workspaces/
├── panacea-icono/                    # Main hub repository (this repo)
│   ├── .devcontainer/               # Development container config
│   ├── navigate-ecosystem.sh        # Ecosystem navigation script
│   ├── sync_ecosystem.sh           # Ecosystem synchronization
│   └── panacea-ecosystem.code-workspace  # Multi-root workspace
├── ecosystem/                       # Key ecosystem repositories
│   ├── Ton-telegram/               # Technical hub & bot wallet
│   ├── Dr_dela_TV/                 # Ecosystem presenter
│   ├── Super-code-tasker/          # AI-powered code generation
│   ├── PANACEA-API-CENTRAL-CODEX/  # Central API
│   ├── gpt-local/                  # Local GPT system
│   ├── nextjs-with-supabase/       # Next.js applications
│   ├── MEDIOS-REDES/               # Social media bots
│   └── dr-de-la-tvr/               # TypeScript projects
```

### 🧭 Navigation Commands

Use the ecosystem navigation script for easy repository management:

```bash
# List all available repositories
./navigate-ecosystem.sh list

# Navigate to a specific repository
./navigate-ecosystem.sh goto Ton-telegram
./navigate-ecosystem.sh goto Super-code-tasker

# Show status of all repositories
./navigate-ecosystem.sh status

# Pull latest changes for all repositories
./navigate-ecosystem.sh pull-all

# Run ecosystem synchronization
./navigate-ecosystem.sh sync

# Show ecosystem information
./navigate-ecosystem.sh repos
```

### 📝 Development Workflow

1. **Start Development**: Open the `panacea-ecosystem.code-workspace` file in VS Code
2. **Navigate Repositories**: Use the navigation script or VS Code's workspace folders
3. **Code Changes**: Make changes across multiple repositories as needed
4. **Sync Ecosystem**: Run sync commands to keep everything coordinated
5. **Test Integration**: Use the built-in tasks for testing and deployment

### 🔧 Available Tasks

Access these via VS Code Command Palette (Ctrl/Cmd + Shift + P) → "Tasks: Run Task":

- **🚀 Sync Ecosystem**: Run the main synchronization script
- **🧭 Navigate Ecosystem**: Show available repositories  
- **🐍 Start FastAPI Server**: Launch the main API server
- **📦 Install Dependencies (All)**: Install dependencies for all repositories

### 🔗 Key Repositories

The integrated environment includes these essential repositories:

| Repository | Purpose | Language |
|-----------|---------|-----------|
| **Ton-telegram** | Technical hub & wallet bot | JavaScript |
| **Dr_dela_TV** | Ecosystem presenter | Various |
| **Super-code-tasker** | AI code generation agents | TypeScript |
| **PANACEA-API-CENTRAL-CODEX** | Central API system | Python |
| **gpt-local** | Local GPT system | Shell/Python |
| **nextjs-with-supabase** | Next.js applications | TypeScript |
| **MEDIOS-REDES** | Social media bots | Various |
| **dr-de-la-tvr** | TypeScript projects | TypeScript |

### 🌐 Port Forwarding

The development environment automatically forwards these ports:

- **8000**: FastAPI server (main application)
- **3000**: Next.js development server
- **5000**: Flask or other Python servers

### 🔑 Environment Setup

Key environment variables are automatically configured:

- `PANACEA_WORKSPACE`: Main workspace directory
- `PANACEA_MAIN_REPO`: Path to main repository
- `PANACEA_ECOSYSTEM_DIR`: Path to ecosystem repositories

### 🛠 Manual Setup (Advanced)

If you need to run the setup manually:

```bash
# Run the ecosystem setup script
bash .devcontainer/setup-ecosystem.sh

# Create navigation helper
chmod +x navigate-ecosystem.sh
```

### 📖 Documentation

- **Ecosystem Overview**: [Main README](README.md)
- **Repository Structure**: Check individual repository READMEs
- **Technical Hub**: [Ton-telegram](https://github.com/panacea-icono/Ton-telegram)
- **Documentation**: [Ton-telegram/docs](https://github.com/panacea-icono/Ton-telegram/tree/main/docs)

### 🤝 Contributing

1. Make changes in the appropriate repository
2. Use the sync script to coordinate changes across repositories
3. Follow the contribution guidelines in each repository
4. Test integration across the ecosystem before submitting PRs

### 🔧 Troubleshooting

**Setup Issues**:
```bash
# Re-run setup if something fails
bash .devcontainer/setup-ecosystem.sh

# Check repository status
./navigate-ecosystem.sh status
```

**Port Conflicts**:
- The codespace automatically forwards ports 3000, 5000, and 8000
- Modify port settings in `.devcontainer/devcontainer.json` if needed

**Repository Sync Issues**:
```bash
# Manually sync repositories
./navigate-ecosystem.sh pull-all

# Run ecosystem synchronization
./sync_ecosystem.sh
```

---

## 📞 Support

- **Issues**: Open an issue in the relevant repository
- **General Questions**: [Main Hub Issues](https://github.com/panacea-icono/panacea-icono/issues)
- **Technical Hub**: [Ton-telegram](https://github.com/panacea-icono/Ton-telegram)

*The integrated development environment makes working with the PANACEA ICONO ecosystem seamless and efficient.*