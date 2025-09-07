# 🏥 PANACEA ICONO

**AI-Powered Healthcare Solutions with Docker and Hugging Face Integration**

[![Docker](https://img.shields.io/badge/Docker-Ready-blue?logo=docker)](https://hub.docker.com/r/drtv/panacea-icono)
[![Python](https://img.shields.io/badge/Python-3.8+-green?logo=python)](https://www.python.org/)
[![Hugging Face](https://img.shields.io/badge/Hugging%20Face-Transformers-orange?logo=huggingface)](https://huggingface.co/)
[![Heroku](https://img.shields.io/badge/Heroku-Deployed-purple?logo=heroku)](https://heroku.com/)
[![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-CI%2FCD-green?logo=github-actions)](https://github.com/panacea-icono/panacea-icono/actions)
[![Redis](https://img.shields.io/badge/Redis-Cache-red?logo=redis)](https://redis.io/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue?logo=postgresql)](https://postgresql.org/)

**🐳 Docker Hub**: [drtv/panacea-icono](https://hub.docker.com/r/drtv/panacea-icono)

## 🚀 Overview

PANACEA ICONO is a comprehensive healthcare AI platform that integrates cutting-edge machine learning models with modern deployment technologies. The project provides secure, scalable, and efficient healthcare solutions powered by AI.

**Developed by**: [drtv](https://hub.docker.com/u/drtv)

## ✨ Features

- 🤖 **AI Models Integration**: OpenAI GPT and Hugging Face Transformers
- 🐳 **Docker Containerization**: Multi-service architecture with Docker Compose
- 🚀 **Cloud Deployment**: Heroku with automated CI/CD pipelines
- 🔐 **Security First**: Token scanning, security audits, and environment management
- 📊 **Infrastructure**: Redis caching, PostgreSQL database, health monitoring
- 🛠️ **Developer Tools**: Code quality, linting, testing, and CI/CD automation
- 📚 **Documentation**: Extensive guides and comprehensive API documentation
- 🌐 **Ecosystem Integration**: GitHub Actions, Container Registry, and monitoring tools

## 🏗️ Architecture

```
PANACEA ICONO ECOSYSTEM/
├── 🏥 Core Platform
│   ├── 🤖 AI Models (OpenAI, Hugging Face)
│   ├── 🐳 Docker Services (drtv/panacea-icono)
│   ├── 🗄️ Database Layer (PostgreSQL + Redis)
│   └── 🔐 Security & Monitoring
├── 🚀 Cloud Infrastructure
│   ├── 🌐 Heroku Deployment
│   ├── 🐙 GitHub Actions CI/CD
│   └── 📦 GitHub Container Registry
├── 🌟 Related Projects
│   ├── 📱 UNIVERSOLIFE (Web App)
│   └── 💎 panacea-icono-sa (NFT & Tokens)
└── 🛠️ Development Tools
    ├── 🔍 Code Quality (pylint, black, mypy)
    ├── 🔒 Security Scanning (bandit, safety)
    └── 📊 Health Monitoring
```

## 🚀 Quick Start

### Prerequisites

- Docker Desktop
- Python 3.8+
- Node.js 16+
- Heroku CLI
- Git

### 1. Clone Repository

```bash
git clone https://github.com/panacea-icono/panacea-icono.git
cd panacea-icono
```

### 2. Environment Setup

```bash
# Copy environment template
cp env.example .env

# Edit with your API keys
nano .env
```

### 3. Docker Deployment

```bash
# Build Docker image
docker build -t drtv/panacea-icono .

# Run container
docker run -p 8000:8000 drtv/panacea-icono

# Or use Docker Compose
docker-compose up -d
```

### 4. Pull from Docker Hub

```bash
# Pull pre-built image
docker pull drtv/panacea-icono:latest

# Run container
docker run -p 8000:8000 drtv/panacea-icono:latest
```

## 🌟 Ecosystem & Related Projects

PANACEA ICONO is part of a broader healthcare technology ecosystem with multiple integrated projects and services:

### Core Repositories
- **[panacea-icono/panacea-icono](https://github.com/panacea-icono/panacea-icono)** - Main AI healthcare platform
- **[panacea-icono/UNIVERSOLIFE](https://github.com/panacea-icono/UNIVERSOLIFE)** - Corporate landing web application (TypeScript)
- **[Drignaciodelatv/panacea-icono-sa](https://github.com/Drignaciodelatv/panacea-icono-sa)** - NFT and stable token integration

### Key Integrations

#### 🐳 Docker Ecosystem
- **Registry**: [drtv/panacea-icono](https://hub.docker.com/r/drtv/panacea-icono) on Docker Hub
- **Multi-service Architecture**: Redis, PostgreSQL, Hugging Face cache
- **Container Orchestration**: Docker Compose with health checks

#### 🤖 AI & Machine Learning
- **OpenAI Integration**: GPT models for advanced healthcare AI
- **Hugging Face Hub**: Pre-trained transformers for NLP tasks
- **Model Management**: Automated caching and deployment
- **Supported Tasks**: 
  - Text classification and sentiment analysis
  - Machine translation (Spanish ↔ English)
  - Text summarization and question answering
  - Token classification and named entity recognition

#### ☁️ Cloud Infrastructure  
- **Primary Deployment**: Heroku with automated scaling
- **Container Registry**: GitHub Container Registry (ghcr.io)
- **CI/CD Pipeline**: GitHub Actions with quality gates
- **Monitoring**: Health checks and performance metrics

#### 🗄️ Data & Storage
- **Primary Database**: PostgreSQL for structured data
- **Caching Layer**: Redis for session and model caching
- **Model Storage**: Hugging Face model cache volumes
- **Backup Strategy**: Automated database backups

### 5. Heroku Deployment

```bash
# Login to Heroku
heroku login

# Create app
heroku create your-app-name

# Deploy
git push heroku main
```

## 🔧 Configuration

### Environment Variables

```bash
# OpenAI
OPENAI_API_KEY=your_key_here

# Hugging Face
HUGGINGFACE_API_KEY=your_key_here
HUGGINGFACE_EMAIL=your_email@example.com

# Heroku
HEROKU_API_KEY=your_key_here
HEROKU_APP_NAME=your_app_name

# GitHub
GITHUB_TOKEN=your_token_here
```

### AI Models Configuration

Edit `ai_models_config_clean.json`:

```json
{
  "openai": {
    "api_key": "YOUR_OPENAI_API_KEY",
    "models": ["gpt-4", "gpt-3.5-turbo"]
  },
  "huggingface": {
    "api_key": "YOUR_HUGGINGFACE_API_KEY",
    "models": ["bert-base", "gpt2", "t5-base"]
  }
}
```

## 🐳 Docker Multi-Service Architecture

The PANACEA ICONO platform uses a sophisticated Docker-based architecture with multiple services.

### Service Overview

| Service | Image | Purpose | Port |
|---------|-------|---------|------|
| **panacea-icono** | `drtv/panacea-icono:latest` | Main AI application | 8000 |
| **redis** | `redis:7-alpine` | Caching & sessions | 6379 |
| **postgres** | `postgres:15-alpine` | Primary database | 5432 |
| **huggingface-cache** | `alpine:latest` | Model cache volume | - |

### Quick Deploy with Docker Compose

```bash
# Complete multi-service deployment
docker-compose up -d

# Check all services status
docker-compose ps

# View logs from all services
docker-compose logs -f
```

### Individual Service Management

#### Main Application
```bash
# Build main application
docker build -t drtv/panacea-icono .

# Run with environment variables
docker run -d \
  --name panacea-icono \
  -p 8000:8000 \
  -e OPENAI_API_KEY=$OPENAI_API_KEY \
  -e HUGGINGFACE_API_KEY=$HUGGINGFACE_API_KEY \
  --network panacea-icono-network \
  drtv/panacea-icono
```

#### Database Services
```bash
# Start PostgreSQL
docker run -d \
  --name panacea-postgres \
  -e POSTGRES_DB=panacea_icono \
  -e POSTGRES_USER=panacea \
  -e POSTGRES_PASSWORD=panacea123 \
  -p 5432:5432 \
  postgres:15-alpine

# Start Redis
docker run -d \
  --name panacea-redis \
  -p 6379:6379 \
  redis:7-alpine redis-server --appendonly yes
```

### Docker Compose Configuration

The complete stack is defined in `docker-compose.yml`:

```yaml
version: '3.8'
services:
  panacea-icono:
    image: drtv/panacea-icono:latest
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - HUGGINGFACE_API_KEY=${HUGGINGFACE_API_KEY}
      - HUGGINGFACE_EMAIL=${HUGGINGFACE_EMAIL}
    depends_on:
      - redis
      - postgres
    volumes:
      - ./models:/app/models
      - ./data:/app/data
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
  
  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
    command: redis-server --appendonly yes
  
  postgres:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=panacea_icono
      - POSTGRES_USER=panacea
      - POSTGRES_PASSWORD=panacea123
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  redis_data:
  postgres_data:
  huggingface_cache:
```

### Docker Hub Distribution

```bash
# Pull from Docker Hub (maintained by drtv)
docker pull drtv/panacea-icono:latest

# Push to Docker Hub (for maintainers)
docker login
docker tag panacea-icono drtv/panacea-icono:latest
docker push drtv/panacea-icono:latest
```

### Health Monitoring

```bash
# Check container health
docker ps
docker logs panacea-icono

# Test health endpoint
curl http://localhost:8000/health

# Monitor resources
docker stats panacea-icono
```

## 🤖 AI Models & Machine Learning

### Supported AI Tasks & Models

| Task | Model | Purpose |
|------|-------|---------|
| **Sentiment Analysis** | `cardiffnlp/twitter-roberta-base-sentiment-latest` | Healthcare feedback analysis |
| **Text Classification** | `distilbert-base-uncased-finetuned-sst-2-english` | Document categorization |
| **Text Generation** | `gpt2` | Content generation |
| **Translation** | `Helsinki-NLP/opus-mt-es-en` | Spanish ↔ English |
| **Summarization** | `facebook/bart-large-cnn` | Medical document summarization |
| **Question Answering** | `deepset/roberta-base-squad2` | Healthcare Q&A |
| **Named Entity Recognition** | `dbmdz/bert-large-cased-finetuned-conll03-english` | Medical entity extraction |

### OpenAI Integration

```python
import openai

# Configure OpenAI client
openai.api_key = os.getenv("OPENAI_API_KEY")

# Healthcare-specific chat completion
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a healthcare AI assistant."},
        {"role": "user", "content": "Analyze this medical report..."}
    ]
)
```

### Hugging Face Integration

```python
from transformers import pipeline
from huggingface_config import HuggingFaceManager

# Initialize manager
hf_manager = HuggingFaceManager()

# Sentiment analysis for patient feedback
sentiment_analyzer = pipeline(
    "sentiment-analysis",
    model="cardiffnlp/twitter-roberta-base-sentiment-latest"
)
result = sentiment_analyzer("The treatment was very effective!")

# Medical document summarization
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
summary = summarizer("Long medical document text...", max_length=130, min_length=30)

# Spanish to English translation for medical records
translator = pipeline("translation", model="Helsinki-NLP/opus-mt-es-en")
translation = translator("El paciente presenta síntomas de...")
```

### Model Management

```python
# Check Hugging Face connection
hf_manager = HuggingFaceManager()
if hf_manager.verify_connection():
    user_info = hf_manager.get_user_info()
    print(f"Connected as: {user_info['name']}")

# List available models
models = hf_manager.list_user_models()
for model in models:
    print(f"Model: {model['modelId']}")
```

## 🚀 Deployment & CI/CD

### Automated CI/CD Pipeline

The project uses GitHub Actions for comprehensive CI/CD with multiple stages:

```mermaid
graph LR
    A[Push to main] --> B[Code Quality]
    B --> C[Security Scan]
    C --> D[Docker Build]
    D --> E[Docker Test]
    E --> F[Deploy to Heroku]
    F --> G[Health Check]
```

#### Pipeline Stages

1. **🔍 Code Quality & Security**
   ```bash
   # Linting and formatting
   pylint *.py --disable=C0114,C0116
   black --check *.py
   isort --check-only *.py
   
   # Security scanning
   bandit -r . -f json -o bandit-report.json
   safety check
   ```

2. **🐳 Docker Build & Test**
   ```bash
   # Build and cache optimization
   docker buildx build --cache-from type=gha --cache-to type=gha,mode=max
   
   # Container testing
   docker run --rm $IMAGE_NAME:test python -c "print('✅ Test passed')"
   ```

3. **🚀 Heroku Deployment**
   ```bash
   # Automated deployment on main branch
   heroku container:push web --app $HEROKU_APP_NAME
   heroku container:release web --app $HEROKU_APP_NAME
   ```

### Manual Deployment Options

#### Heroku Deployment

```bash
# One-time setup
heroku login
heroku create your-app-name

# Set environment variables
heroku config:set OPENAI_API_KEY=your_key
heroku config:set HUGGINGFACE_API_KEY=your_key

# Deploy using Git
git push heroku main

# Or deploy using Docker
heroku container:push web
heroku container:release web

# Monitor deployment
heroku logs --tail
heroku open
```

#### GitHub Container Registry

```bash
# Login to GitHub Container Registry
echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin

# Build and tag
docker build -t ghcr.io/panacea-icono/panacea-icono:latest .

# Push to registry
docker push ghcr.io/panacea-icono/panacea-icono:latest
```

## 📊 Monitoring & Health Checks

### Automated Health Monitoring

```bash
# Run ecosystem synchronization script
./sync_ecosystem.sh

# Check Docker services health
docker-compose ps
docker-compose logs -f panacea-icono

# Application health endpoint
curl http://localhost:8000/health

# Database connectivity
curl http://localhost:8000/health/db

# AI models status
curl http://localhost:8000/health/models
```

### Service Health Checks

#### Docker Container Health
```bash
# Built-in health check
docker inspect --format='{{.State.Health.Status}}' panacea-icono

# Health check configuration in docker-compose.yml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s
```

#### CI/CD Health Validation
```bash
# Automated health check after deployment
sleep 30
curl -f https://$HEROKU_APP_NAME.herokuapp.com/health || exit 1
```

### Monitoring Metrics

- 🏥 **Application Health**: Response times, error rates
- 🤖 **AI Models**: Model loading status, inference latency
- 🐳 **Container Resources**: CPU, memory, disk usage
- 🗄️ **Database Performance**: Connection pool, query times
- 🚀 **Deployment Status**: Build success, deployment health
- 🔐 **Security Alerts**: Token scanning, vulnerability checks

### Ecosystem Synchronization

The `sync_ecosystem.sh` script provides comprehensive monitoring:

```bash
# Full ecosystem status check
./sync_ecosystem.sh

# Individual service checks
check_docker()      # Docker and Docker Hub status
check_heroku()      # Heroku app and deployment status  
check_huggingface() # Hugging Face API connectivity
check_github()      # GitHub repository status
```

### Log Management

```bash
# Application logs
docker logs panacea-icono --follow

# Service-specific logs
docker-compose logs redis
docker-compose logs postgres

# Heroku logs
heroku logs --tail --app your-app-name

# CI/CD logs
gh run list --workflow=ci-cd.yml
gh run view [run-id] --log
```

## 🔐 Security

### Token Scanning

```bash
# Scan for exposed tokens
python env_tokens_summary.py

# Validate environment
python validate_env.py
```

### Best Practices

- Never commit `.env` files
- Use environment variables
- Regular security audits
- Token rotation

## 🛠️ Development Environment

### Prerequisites & Setup

```bash
# System requirements
- Docker Desktop
- Python 3.8+
- Node.js 16+ (for UNIVERSOLIFE integration)
- Heroku CLI
- Git

# Clone the complete ecosystem
git clone https://github.com/panacea-icono/panacea-icono.git
cd panacea-icono

# Set up Python environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
pip install -e .  # Development installation
```

### Development Workflow

#### Local Development Stack

```bash
# Start development services
docker-compose -f docker-compose.yml up -d redis postgres

# Run application in development mode
export ENVIRONMENT=development
export LOG_LEVEL=DEBUG
python main.py

# Or use Docker for full stack
docker-compose up --build
```

#### Code Quality Tools

```bash
# Formatting and linting
black *.py                    # Code formatting
isort *.py                    # Import sorting
pylint *.py                   # Code analysis
mypy *.py                     # Type checking

# Security and dependency checking
bandit -r .                   # Security linting
safety check                  # Dependency vulnerability scan

# Run all quality checks
./scripts/quality_check.sh    # Run complete quality pipeline
```

#### Testing Framework

```bash
# Unit tests
pytest tests/unit/

# Integration tests  
pytest tests/integration/

# Docker container tests
docker run --rm drtv/panacea-icono:test python -m pytest

# Load testing
locust -f tests/load/locustfile.py --host=http://localhost:8000
```

### Development Tools Integration

#### VS Code Configuration

```json
// .vscode/settings.json
{
  "python.defaultInterpreter": "./venv/bin/python",
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "python.formatting.provider": "black",
  "python.sortImports.enabled": true
}
```

#### Pre-commit Hooks

```bash
# Install pre-commit
pip install pre-commit
pre-commit install

# Manual run
pre-commit run --all-files
```

#### Environment Management

```bash
# Copy environment template
cp env.example .env

# Required environment variables for development
OPENAI_API_KEY=your_openai_key
HUGGINGFACE_API_KEY=your_huggingface_key
HUGGINGFACE_EMAIL=your_email@example.com
DATABASE_URL=postgresql://panacea:panacea123@localhost:5432/panacea_icono
REDIS_URL=redis://localhost:6379
```

### AI Model Development

```bash
# Download and cache models locally
python -c "from huggingface_config import HuggingFaceManager; HuggingFaceManager().download_default_models()"

# Test AI integrations
python -c "from main import test_openai_connection; test_openai_connection()"
python -c "from main import test_huggingface_models; test_huggingface_models()"

# Model performance testing
python scripts/benchmark_models.py
```

## 📚 Documentation & Resources

### Core Documentation
- [🔐 Token Scanner Guide](README_TOKEN_SCANNER.md)
- [🤖 AI Models Configuration](huggingface_config.py)
- [🐳 Docker Multi-Service Setup](docker-compose.yml)
- [🚀 CI/CD Pipeline Configuration](.github/workflows/ci-cd.yml)
- [🌐 Ecosystem Synchronization](sync_ecosystem.sh)

### API Documentation
- **Interactive API Docs**: `http://localhost:8000/docs` (Swagger UI)
- **Alternative Docs**: `http://localhost:8000/redoc` (ReDoc)
- **Health Endpoints**: `http://localhost:8000/health/*`

### Related Project Documentation
- **[UNIVERSOLIFE Web App](https://github.com/panacea-icono/UNIVERSOLIFE)** - Corporate landing page
- **[NFT & Token Platform](https://github.com/Drignaciodelatv/panacea-icono-sa)** - Blockchain integration

### Architecture Guides
- **Docker Architecture**: Multi-service containerization with health checks
- **AI Integration Patterns**: OpenAI and Hugging Face best practices  
- **Security Implementation**: Token management and environment security
- **Deployment Strategies**: Heroku, Docker Hub, and GitHub Actions

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Make changes
4. Add tests
5. Submit pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support & Community

### Getting Help
- **Issues**: [GitHub Issues](https://github.com/panacea-icono/panacea-icono/issues)
- **Discussions**: [GitHub Discussions](https://github.com/panacea-icono/panacea-icono/discussions)
- **Email**: repositorios.panacea@gmail.com

### Project Links
- **Main Repository**: [panacea-icono/panacea-icono](https://github.com/panacea-icono/panacea-icono)
- **Docker Hub**: [drtv/panacea-icono](https://hub.docker.com/r/drtv/panacea-icono)
- **Live Demo**: [Heroku Deployment](https://panacea-icono-demo-1392a1eb342b.herokuapp.com/)

### Related Projects
- **🌐 Web Platform**: [UNIVERSOLIFE](https://github.com/panacea-icono/UNIVERSOLIFE) - TypeScript-based corporate web app
- **💎 Blockchain Integration**: [panacea-icono-sa](https://github.com/Drignaciodelatv/panacea-icono-sa) - NFT and stable token platform

### Contributing
We welcome contributions to the PANACEA ICONO ecosystem!

1. **Fork the repository** you want to contribute to
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Make your changes** following our coding standards
4. **Run quality checks** (`./scripts/quality_check.sh`)
5. **Submit a pull request** with detailed description

### Development Community
- **Maintainer**: [drtv](https://hub.docker.com/u/drtv) - Docker orchestration and infrastructure
- **Organization**: [panacea-icono](https://github.com/panacea-icono) - Healthcare AI solutions

## 🌟 Acknowledgments

### Technology Partners
- **OpenAI** for GPT models and advanced AI capabilities
- **Hugging Face** for transformer models and ML infrastructure
- **Heroku** for cloud hosting and deployment platform
- **Docker** for containerization and orchestration
- **PostgreSQL** for reliable database solutions
- **Redis** for high-performance caching

### Development Tools
- **GitHub Actions** for CI/CD automation
- **GitHub Container Registry** for secure image distribution
- **Docker Hub** ([drtv](https://hub.docker.com/u/drtv)) for public container hosting

### Community & Ecosystem
- **PANACEA ICONO Team** for healthcare AI innovation
- **Open Source Community** for contributing libraries and tools
- **Healthcare Technology Partners** for domain expertise

---

**Made with ❤️ by PANACEA ICONO Ecosystem**

[![PANACEA ICONO](https://img.shields.io/badge/PANACEA-ICONO-Healthcare%20AI-blue)](https://panacea-icono-demo-1392a1eb342b.herokuapp.com/)
[![Docker Hub](https://img.shields.io/badge/Docker%20Hub-drtv%2Fpanacea--icono-blue?logo=docker)](https://hub.docker.com/r/drtv/panacea-icono)
[![GitHub Org](https://img.shields.io/badge/GitHub-panacea--icono-black?logo=github)](https://github.com/panacea-icono)
[![UNIVERSOLIFE](https://img.shields.io/badge/Web%20Platform-UNIVERSOLIFE-green?logo=typescript)](https://github.com/panacea-icono/UNIVERSOLIFE)
