# 🏥 PANACEA ICONO

**AI-Powered Healthcare Solutions with Docker and Hugging Face Integration**

[![Docker](https://img.shields.io/badge/Docker-Ready-blue?logo=docker)](https://www.docker.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-green?logo=python)](https://www.python.org/)
[![Hugging Face](https://img.shields.io/badge/Hugging%20Face-Transformers-orange?logo=huggingface)](https://huggingface.co/)
[![Heroku](https://img.shields.io/badge/Heroku-Deployed-purple?logo=heroku)](https://heroku.com/)

## 🚀 Overview

PANACEA ICONO is a comprehensive healthcare AI platform that integrates cutting-edge machine learning models with modern deployment technologies. The project provides secure, scalable, and efficient healthcare solutions powered by AI.

## ✨ Features

- 🤖 **AI Models Integration**: OpenAI GPT and Hugging Face Transformers
- 🐳 **Docker Containerization**: Easy deployment and scaling
- 🚀 **Heroku Deployment**: Cloud-native hosting
- 🔐 **Security First**: Token scanning and environment management
- 📊 **Health Monitoring**: Automated system health checks
- 🛠️ **Developer Tools**: Comprehensive development environment
- 📚 **Documentation**: Extensive guides and examples

## 🏗️ Architecture

```
PANACEA ICONO/
├── 🤖 AI Models (OpenAI, Hugging Face)
├── 🐳 Docker Containers
├── 🚀 Heroku Deployment
├── 🔐 Security & Token Management
├── 📊 Health Monitoring
├── 🛠️ Development Tools
└── 📚 Documentation
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
docker build -t panacea-icono .

# Run container
docker run -p 8000:8000 panacea-icono
```

### 4. Heroku Deployment

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

## 🐳 Docker

### Build Image

```bash
docker build -t panacea-icono .
```

### Run Container

```bash
docker run -d \
  --name panacea-icono \
  -p 8000:8000 \
  -e OPENAI_API_KEY=$OPENAI_API_KEY \
  panacea-icono
```

### Docker Compose

```yaml
version: '3.8'
services:
  panacea-icono:
    build: .
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - HUGGINGFACE_API_KEY=${HUGGINGFACE_API_KEY}
```

## 🤖 AI Models

### OpenAI Integration

```python
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

### Hugging Face Integration

```python
from transformers import pipeline

classifier = pipeline("sentiment-analysis")
result = classifier("I love this project!")
```

## 🚀 Deployment

### Heroku

```bash
# Deploy to Heroku
heroku container:push web
heroku container:release web

# Open app
heroku open
```

### Docker Registry

```bash
# Push to Docker Hub
docker tag panacea-icono username/panacea-icono
docker push username/panacea-icono
```

## 📊 Monitoring

### Health Checks

```bash
# Run health monitor
./health_monitor.sh

# Check logs
docker logs panacea-icono
```

### Metrics

- System health status
- API response times
- Resource usage
- Error rates

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

## 🛠️ Development

### Setup Development Environment

```bash
# Python virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
poetry install

# Node.js dependencies
npm install
```

### Code Quality

```bash
# Python linting
pylint *.py
mypy *.py

# Formatting
black *.py
isort *.py
```

## 📚 Documentation

- [Token Scanner Guide](README_TOKEN_SCANNER.md)
- [AI Models Configuration](ai_models_config_clean.json)
- [Docker Setup](Dockerfile)
- [Heroku Deployment](.github/workflows/deploy.yml)

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Make changes
4. Add tests
5. Submit pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/panacea-icono/panacea-icono/issues)
- **Discussions**: [GitHub Discussions](https://github.com/panacea-icono/panacea-icono/discussions)
- **Email**: repositorios.panacea@gmail.com

## 🌟 Acknowledgments

- OpenAI for GPT models
- Hugging Face for transformers
- Heroku for hosting
- Docker for containerization

---

**Made with ❤️ by PANACEA ICONO Team**

[![PANACEA ICONO](https://img.shields.io/badge/PANACEA-ICONO-Healthcare%20AI-blue)](https://panacea-icono-demo-1392a1eb342b.herokuapp.com/)
