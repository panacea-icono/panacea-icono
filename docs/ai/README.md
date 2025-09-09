# 🤖 Ecosistema de IA - Panacea Icono S.A.

<div align="center">
  <img src="../public/assets/logo-medical.svg" alt="Panacea Icono S.A. Logo" width="300" height="150">
</div>

## 🏥 Visión General

El ecosistema de IA de Panacea Icono S.A. integra múltiples sistemas de inteligencia artificial especializados en medicina estética, cirugía plástica y Web3, proporcionando soluciones avanzadas para consultas médicas, análisis de casos y automatización de procesos.

## 🧠 Componentes del Ecosistema

### 1. 🤖 Bots de Telegram (29+ bots)
- **Gestor**: `bots/telegram_bots_manager.py`
- **Categorías**:
  - **Médicos**: ALINA, Anastasia, Dr_Lalo, DrAquiles, plastic_surgeon, Dra_Liliana
  - **Crypto**: Panas, Vaser_token, Liposuccion
  - **Entretenimiento**: CONDE_MORMIX, Poci, la_chunchuna, Jabancho
  - **Medios**: IVANA, DR_DELA_TV, sophie, SOCIEDAD
  - **Personal**: Kuchiuya, dr_tapia, Lalo, Guerita, Joselin

### 2. 🧠 Sistema GPT Personalizado
- **Gestor**: `ai/panacea_gpt_system.py`
- **GPTs Especializados**:
  - **Dr. Panacea - Asistente Médico**: Consultas médicas generales
  - **Dr. Panacea - Cirujano Plástico**: Procedimientos quirúrgicos
  - **Panacea Crypto**: Web3 y blockchain médico
  - **Panacea Admin**: Gestión administrativa
  - **Panacea Customer**: Atención al cliente

### 3. 🔬 IA Médica con Hugging Face
- **Gestor**: `ai/huggingface_medical_ai.py`
- **Modelos Especializados**:
  - **Análisis de Imágenes Médicas**: Diagnósticos por imagen
  - **Procesamiento de Lenguaje Médico**: Análisis de historias clínicas
  - **Clasificador de Síntomas**: Análisis de síntomas
  - **Recomendador de Tratamientos**: Sugerencias terapéuticas
  - **Analizador de Cirugía Plástica**: Casos especializados

### 4. 🌐 Ecosistema Integrado
- **Gestor**: `ai/panacea_ai_ecosystem.py`
- **Funciones**:
  - Integración completa de todos los sistemas
  - Procesamiento de consultas médicas
  - Dashboard unificado
  - Monitoreo de salud del ecosistema

## 🚀 API Endpoints

### Estado del Ecosistema
```http
GET /ai/ecosystem/status
```
Obtiene el estado completo del ecosistema de IA.

### Consultas Médicas
```http
POST /ai/medical/query?query=texto&user_id=opcional
```
Procesa consultas médicas usando el ecosistema completo.

### GPTs Disponibles
```http
GET /ai/gpts
```
Lista todos los GPTs personalizados disponibles.

### Modelos de IA Médica
```http
GET /ai/models
```
Lista los modelos de Hugging Face especializados en medicina.

### Estado de Bots de Telegram
```http
GET /bots/telegram/status
```
Obtiene el estado de todos los bots de Telegram.

### Envío de Mensajes
```http
POST /bots/telegram/send?bot_name=nombre&chat_id=id&message=texto
```
Envía mensajes a través de bots específicos.

### Dashboard de IA
```http
GET /ai/dashboard
```
Obtiene datos para el dashboard de IA.

## 📊 Monitoreo y Estadísticas

### Métricas de Bots de Telegram
- Total de bots: 29+
- Bots activos vs inactivos
- Categorización por especialidad
- Tasa de errores
- Uso por categoría

### Métricas de GPTs
- Total de GPTs: 5
- Uso por categoría
- Estadísticas de consultas
- Tiempo de respuesta

### Métricas de IA Médica
- Modelos disponibles
- Configuración de API
- Uso por modelo
- Precisión de análisis

## 🔧 Configuración

### Variables de Entorno Requeridas
```bash
# Telegram Bots (ya configurados en el código)
TELEGRAM_BOT_TOKENS=token1,token2,token3...

# Hugging Face
HUGGINGFACE_API_KEY=tu_api_key_aqui

# OpenAI (para GPTs)
OPENAI_API_KEY=tu_api_key_aqui
```

### Instalación de Dependencias
```bash
pip install httpx asyncio fastapi uvicorn
```

## 🏥 Casos de Uso Médicos

### 1. Consultas Médicas Virtuales
- Análisis de síntomas
- Recomendaciones de tratamientos
- Orientación médica general
- Derivación a especialistas

### 2. Cirugía Plástica
- Análisis de casos
- Planificación quirúrgica
- Evaluación de riesgos
- Recomendaciones de procedimientos

### 3. Atención al Cliente
- Información de servicios
- Agendamiento de citas
- Soporte técnico
- Preguntas frecuentes

### 4. Administración
- Gestión de citas
- Información de horarios
- Procesos de facturación
- Contacto con departamentos

## 🔒 Seguridad y Privacidad

### Protección de Datos
- Encriptación de tokens
- Validación de entrada
- Logs de auditoría
- Manejo seguro de errores

### Cumplimiento Médico
- Confidencialidad del paciente
- No diagnóstico definitivo sin consulta presencial
- Recomendación de consulta presencial cuando sea necesario
- Registro de interacciones

## 📈 Roadmap de Desarrollo

### Fase 1: ✅ Completada
- [x] Sistema de bots de Telegram
- [x] GPTs personalizados
- [x] Integración con Hugging Face
- [x] API endpoints básicos
- [x] Dashboard de monitoreo

### Fase 2: 🔄 En Desarrollo
- [ ] Integración con base de datos de pacientes
- [ ] Análisis de imágenes médicas
- [ ] Notificaciones automáticas
- [ ] Reportes de uso avanzados

### Fase 3: 📋 Planificada
- [ ] IA predictiva para diagnósticos
- [ ] Integración con equipos médicos
- [ ] Análisis de tendencias médicas
- [ ] Automatización completa de procesos

## 🆘 Soporte y Contacto

### Información Técnica
- **Email**: dev@panacea-icono.org
- **Teléfono**: +591 69674560
- **WhatsApp**: +591 69674560

### Información Médica
- **Email**: citas@panacea-icono.org
- **Teléfono**: +591 69674560
- **Ubicación**: Av. Principal #123, Santa Cruz de la Sierra, Bolivia

---

*Última actualización: 2025-09-09*
*Versión: v2025.09.09.0302*
*Desarrollado por: Panacea Icono S.A.*
