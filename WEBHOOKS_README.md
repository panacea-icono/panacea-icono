# 🔗 PANACEA ICONO - Webhook System

## Overview

The PANACEA ICONO webhook system provides a comprehensive solution for handling and delivering webhooks. It supports multiple webhook types and provides a robust delivery system with retry logic.

## Features

- **Multiple Webhook Types**: GitHub, Heroku, Hugging Face, and custom webhooks
- **Webhook Management**: Full CRUD operations for webhook configurations
- **Event Processing**: Asynchronous event processing with custom handlers
- **Delivery System**: Reliable delivery with exponential backoff retry logic
- **Security**: Signature verification support
- **Monitoring**: Statistics and delivery tracking
- **Health Checks**: Service health monitoring

## API Endpoints

### Webhook Management
- `POST /webhooks/` - Create a new webhook
- `GET /webhooks/` - List all webhooks
- `GET /webhooks/{id}` - Get webhook details
- `PUT /webhooks/{id}` - Update webhook
- `DELETE /webhooks/{id}` - Delete webhook

### Webhook Receivers
- `POST /webhooks/github` - Receive GitHub webhooks
- `POST /webhooks/heroku` - Receive Heroku webhooks  
- `POST /webhooks/huggingface` - Receive Hugging Face webhooks
- `POST /webhooks/custom` - Receive custom webhooks

### Testing & Monitoring
- `POST /webhooks/events/test` - Create test event
- `GET /webhooks/stats` - Get webhook statistics
- `GET /webhooks/service/health` - Webhook service health check
- `GET /webhooks/{id}/deliveries` - Get webhook deliveries
- `GET /webhooks/deliveries/{id}` - Get delivery status

## Quick Start

### 1. Create a Webhook

```bash
curl -X POST "http://localhost:8000/webhooks/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Webhook",
    "url": "https://example.com/webhook",
    "event_types": ["github.push", "custom"],
    "active": true
  }'
```

### 2. Send a Test Event

```bash
curl -X POST "http://localhost:8000/webhooks/events/test"
```

### 3. Receive a GitHub Webhook

```bash
curl -X POST "http://localhost:8000/webhooks/github" \
  -H "Content-Type: application/json" \
  -H "X-GitHub-Event: push" \
  -d '{
    "repository": {"full_name": "user/repo"},
    "sender": {"login": "user"},
    "commits": []
  }'
```

### 4. Check Statistics

```bash
curl -X GET "http://localhost:8000/webhooks/stats"
```

## Event Types

- `github.push` - GitHub push events
- `github.pull_request` - GitHub pull request events
- `github.release` - GitHub release events
- `heroku.deploy` - Heroku deployment events
- `heroku.build` - Heroku build events
- `huggingface.model_update` - Hugging Face model updates
- `system.health_check` - System health check events
- `custom` - Custom events

## Configuration

Webhook configurations support the following options:

```json
{
  "name": "Webhook Name",
  "url": "https://target.example.com/webhook",
  "secret": "optional-secret-for-signing",
  "event_types": ["github.push", "custom"],
  "active": true,
  "ssl_verify": true,
  "timeout": 30,
  "retry_count": 3,
  "headers": {
    "Authorization": "Bearer token"
  }
}
```

## Security

- Webhook signatures are generated using HMAC-SHA256
- SSL certificate verification is enabled by default
- Custom headers can be added for authentication

## Monitoring

The webhook system provides comprehensive monitoring:

- Delivery success/failure rates
- Event processing statistics
- Recent event history
- Detailed delivery logs

Access the monitoring dashboard at `/webhooks/stats` or check individual webhook deliveries at `/webhooks/{id}/deliveries`.

## Integration Examples

### GitHub Repository Webhooks

Configure your GitHub repository webhook to point to:
```
https://your-app.herokuapp.com/webhooks/github
```

### Heroku App Webhooks

Configure Heroku webhooks to point to:
```
https://your-app.herokuapp.com/webhooks/heroku
```

### Custom Application Integration

Send custom events to:
```
https://your-app.herokuapp.com/webhooks/custom
```

## Error Handling

The webhook system includes robust error handling:

- Failed deliveries are automatically retried with exponential backoff
- Detailed error messages are logged and stored
- Health checks help identify system issues
- Timeout protection prevents hanging requests

For more information, check the interactive API documentation at `/docs`.