#!/usr/bin/env python3
"""
🔗 PANACEA ICONO - Webhook Endpoints
FastAPI endpoints for webhook management and handling
"""

import json
import logging
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from fastapi import APIRouter, HTTPException, Request, Depends, Query, status
from fastapi.responses import JSONResponse

from webhook_models import (
    WebhookConfig, WebhookEvent, WebhookEventType, WebhookResponse,
    GitHubWebhookPayload, HerokuWebhookPayload, HuggingFaceWebhookPayload,
    WebhookSignature, WebhookStats
)
from webhook_service import webhook_service

logger = logging.getLogger(__name__)

# Create webhook router
webhook_router = APIRouter(prefix="/webhooks", tags=["webhooks"])


# Special endpoints (no parameters) - must come first
@webhook_router.get("/stats", response_model=WebhookStats)
async def get_webhook_stats():
    """Get webhook statistics"""
    try:
        stats = webhook_service.get_stats()
        return stats
    except Exception as e:
        logger.error(f"❌ Error getting webhook stats: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get webhook stats: {str(e)}")


@webhook_router.get("/service/health", response_model=Dict[str, Any])
async def webhook_health_check():
    """Webhook service health check"""
    try:
        stats = webhook_service.get_stats()
        
        return {
            "status": "healthy",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "service": "webhook",
            "version": "1.0.0",
            "stats": {
                "total_webhooks": stats.total_webhooks,
                "active_webhooks": stats.active_webhooks,
                "total_events": stats.total_events,
                "success_rate": stats.success_rate
            }
        }
        
    except Exception as e:
        logger.error(f"❌ Webhook health check failed: {e}")
        return JSONResponse(
            status_code=500,
            content={
                "status": "unhealthy",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "error": str(e)
            }
        )


@webhook_router.post("/events/test", response_model=WebhookResponse)
async def create_test_event():
    """Create a test webhook event"""
    try:
        test_payload = {
            "message": "This is a test webhook event",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "test_data": {
                "version": "1.0.0",
                "environment": "test"
            }
        }
        
        event = WebhookEvent(
            event_type=WebhookEventType.CUSTOM,
            source="test",
            payload=test_payload,
            metadata={"test": True}
        )
        
        event_id = await webhook_service.process_event(event)
        
        return WebhookResponse(
            success=True,
            message="Test event created and processed successfully",
            event_id=event_id
        )
        
    except Exception as e:
        logger.error(f"❌ Error creating test event: {e}")
        return WebhookResponse(
            success=False,
            message=f"Failed to create test event: {str(e)}"
        )


# Webhook Management Endpoints
@webhook_router.post("/", response_model=Dict[str, str], status_code=status.HTTP_201_CREATED)
async def create_webhook(webhook_config: WebhookConfig):
    """Create a new webhook"""
    try:
        webhook_id = webhook_service.register_webhook(webhook_config)
        logger.info(f"✅ Webhook created: {webhook_config.name}")
        
        return {
            "id": webhook_id,
            "message": f"Webhook '{webhook_config.name}' created successfully",
            "url": f"/webhooks/{webhook_id}"
        }
    except Exception as e:
        logger.error(f"❌ Error creating webhook: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to create webhook: {str(e)}")


@webhook_router.get("/", response_model=List[WebhookConfig])
async def list_webhooks(active_only: bool = Query(False, description="Show only active webhooks")):
    """List all webhooks"""
    try:
        webhooks = webhook_service.list_webhooks(active_only=active_only)
        logger.info(f"📋 Listed {len(webhooks)} webhooks")
        return webhooks
    except Exception as e:
        logger.error(f"❌ Error listing webhooks: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to list webhooks: {str(e)}")


@webhook_router.get("/{webhook_id}", response_model=WebhookConfig)
async def get_webhook(webhook_id: str):
    """Get a specific webhook"""
    try:
        webhook = webhook_service.get_webhook(webhook_id)
        if not webhook:
            raise HTTPException(status_code=404, detail="Webhook not found")
        
        return webhook
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error getting webhook: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get webhook: {str(e)}")


@webhook_router.put("/{webhook_id}", response_model=Dict[str, str])
async def update_webhook(webhook_id: str, updates: Dict[str, Any]):
    """Update a webhook"""
    try:
        success = webhook_service.update_webhook(webhook_id, updates)
        if not success:
            raise HTTPException(status_code=404, detail="Webhook not found")
        
        logger.info(f"🔄 Webhook updated: {webhook_id}")
        return {
            "id": webhook_id,
            "message": "Webhook updated successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error updating webhook: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to update webhook: {str(e)}")


@webhook_router.delete("/{webhook_id}", response_model=Dict[str, str])
async def delete_webhook(webhook_id: str):
    """Delete a webhook"""
    try:
        success = webhook_service.delete_webhook(webhook_id)
        if not success:
            raise HTTPException(status_code=404, detail="Webhook not found")
        
        logger.info(f"🗑️ Webhook deleted: {webhook_id}")
        return {
            "id": webhook_id,
            "message": "Webhook deleted successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error deleting webhook: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to delete webhook: {str(e)}")


@webhook_router.get("/{webhook_id}/deliveries")
async def get_webhook_deliveries(
    webhook_id: str,
    limit: int = Query(50, ge=1, le=200, description="Number of deliveries to return")
):
    """Get deliveries for a webhook"""
    try:
        # Check if webhook exists
        webhook = webhook_service.get_webhook(webhook_id)
        if not webhook:
            raise HTTPException(status_code=404, detail="Webhook not found")
        
        deliveries = webhook_service.get_webhook_deliveries(webhook_id, limit)
        return {
            "webhook_id": webhook_id,
            "webhook_name": webhook.name,
            "total_deliveries": len(deliveries),
            "deliveries": deliveries
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error getting webhook deliveries: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get webhook deliveries: {str(e)}")


# Webhook Receiver Endpoints
@webhook_router.post("/github", response_model=WebhookResponse)
async def handle_github_webhook(request: Request):
    """Handle GitHub webhook"""
    try:
        # Get headers
        event_type = request.headers.get("X-GitHub-Event", "unknown")
        signature = request.headers.get("X-Hub-Signature-256")
        delivery_id = request.headers.get("X-GitHub-Delivery")
        
        # Read payload
        payload_bytes = await request.body()
        payload_data = json.loads(payload_bytes.decode('utf-8'))
        
        logger.info(f"📨 Received GitHub webhook: {event_type}")
        
        # Parse payload
        try:
            github_payload = GitHubWebhookPayload(**payload_data)
        except Exception as e:
            logger.warning(f"⚠️ Could not parse GitHub payload: {e}")
            github_payload = None
        
        # Determine event type
        webhook_event_type = WebhookEventType.GITHUB_PUSH
        if event_type == "pull_request":
            webhook_event_type = WebhookEventType.GITHUB_PR
        elif event_type == "release":
            webhook_event_type = WebhookEventType.GITHUB_RELEASE
        
        # Create webhook event
        event = WebhookEvent(
            event_type=webhook_event_type,
            source="github",
            payload=payload_data,
            metadata={
                "github_event": event_type,
                "delivery_id": delivery_id,
                "repository": payload_data.get("repository", {}).get("full_name", "unknown")
            }
        )
        
        # Process event
        event_id = await webhook_service.process_event(event)
        
        return WebhookResponse(
            success=True,
            message=f"GitHub webhook processed successfully",
            event_id=event_id
        )
        
    except Exception as e:
        logger.error(f"❌ Error processing GitHub webhook: {e}")
        return WebhookResponse(
            success=False,
            message=f"Failed to process GitHub webhook: {str(e)}"
        )


@webhook_router.post("/heroku", response_model=WebhookResponse)
async def handle_heroku_webhook(request: Request):
    """Handle Heroku webhook"""
    try:
        # Get headers
        event_type = request.headers.get("Heroku-Webhook-Event-Type", "unknown")
        app_name = request.headers.get("Heroku-App-Name")
        
        # Read payload
        payload_bytes = await request.body()
        payload_data = json.loads(payload_bytes.decode('utf-8'))
        
        logger.info(f"📨 Received Heroku webhook: {event_type} for app {app_name}")
        
        # Parse payload
        try:
            heroku_payload = HerokuWebhookPayload(**payload_data)
        except Exception as e:
            logger.warning(f"⚠️ Could not parse Heroku payload: {e}")
            heroku_payload = None
        
        # Determine event type
        webhook_event_type = WebhookEventType.HEROKU_DEPLOY
        if "build" in event_type.lower():
            webhook_event_type = WebhookEventType.HEROKU_BUILD
        
        # Create webhook event
        event = WebhookEvent(
            event_type=webhook_event_type,
            source="heroku",
            payload=payload_data,
            metadata={
                "heroku_event": event_type,
                "app_name": app_name
            }
        )
        
        # Process event
        event_id = await webhook_service.process_event(event)
        
        return WebhookResponse(
            success=True,
            message=f"Heroku webhook processed successfully",
            event_id=event_id
        )
        
    except Exception as e:
        logger.error(f"❌ Error processing Heroku webhook: {e}")
        return WebhookResponse(
            success=False,
            message=f"Failed to process Heroku webhook: {str(e)}"
        )


@webhook_router.post("/huggingface", response_model=WebhookResponse)
async def handle_huggingface_webhook(request: Request):
    """Handle Hugging Face webhook"""
    try:
        # Get headers
        event_type = request.headers.get("X-Event-Type", "model_update")
        
        # Read payload
        payload_bytes = await request.body()
        payload_data = json.loads(payload_bytes.decode('utf-8'))
        
        logger.info(f"📨 Received Hugging Face webhook: {event_type}")
        
        # Parse payload
        try:
            hf_payload = HuggingFaceWebhookPayload(**payload_data)
        except Exception as e:
            logger.warning(f"⚠️ Could not parse Hugging Face payload: {e}")
            hf_payload = None
        
        # Create webhook event
        event = WebhookEvent(
            event_type=WebhookEventType.HF_MODEL_UPDATE,
            source="huggingface",
            payload=payload_data,
            metadata={
                "hf_event": event_type,
                "model_name": payload_data.get("model", {}).get("name", "unknown")
            }
        )
        
        # Process event
        event_id = await webhook_service.process_event(event)
        
        return WebhookResponse(
            success=True,
            message=f"Hugging Face webhook processed successfully",
            event_id=event_id
        )
        
    except Exception as e:
        logger.error(f"❌ Error processing Hugging Face webhook: {e}")
        return WebhookResponse(
            success=False,
            message=f"Failed to process Hugging Face webhook: {str(e)}"
        )


@webhook_router.post("/custom", response_model=WebhookResponse)
async def handle_custom_webhook(request: Request):
    """Handle custom webhook"""
    try:
        # Get headers
        event_type = request.headers.get("X-Event-Type", "custom")
        source = request.headers.get("X-Source", "custom")
        
        # Read payload
        payload_bytes = await request.body()
        payload_data = json.loads(payload_bytes.decode('utf-8'))
        
        logger.info(f"📨 Received custom webhook: {event_type} from {source}")
        
        # Create webhook event
        event = WebhookEvent(
            event_type=WebhookEventType.CUSTOM,
            source=source,
            payload=payload_data,
            metadata={
                "custom_event": event_type
            }
        )
        
        # Process event
        event_id = await webhook_service.process_event(event)
        
        return WebhookResponse(
            success=True,
            message=f"Custom webhook processed successfully",
            event_id=event_id
        )
        
    except Exception as e:
        logger.error(f"❌ Error processing custom webhook: {e}")
        return WebhookResponse(
            success=False,
            message=f"Failed to process custom webhook: {str(e)}"
        )


@webhook_router.get("/deliveries/{delivery_id}")
async def get_delivery_status(delivery_id: str):
    """Get delivery status"""
    try:
        delivery = webhook_service.get_delivery_status(delivery_id)
        if not delivery:
            raise HTTPException(status_code=404, detail="Delivery not found")
        
        return delivery
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error getting delivery status: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get delivery status: {str(e)}")