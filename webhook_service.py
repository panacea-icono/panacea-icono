#!/usr/bin/env python3
"""
🔗 PANACEA ICONO - Webhook Service
Core webhook functionality and delivery system
"""

import asyncio
import json
import logging
import uuid
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional, Callable
import aiohttp
from webhook_models import (
    WebhookConfig, WebhookEvent, WebhookDelivery, WebhookStatus, 
    WebhookEventType, WebhookSignature, WebhookStats
)

logger = logging.getLogger(__name__)


class WebhookService:
    """Service for managing webhooks"""
    
    def __init__(self):
        """Initialize webhook service"""
        self.webhooks: Dict[str, WebhookConfig] = {}
        self.events: Dict[str, WebhookEvent] = {}
        self.deliveries: Dict[str, WebhookDelivery] = {}
        self.event_handlers: Dict[WebhookEventType, List[Callable]] = {}
        
        # Initialize HTTP session
        self._session: Optional[aiohttp.ClientSession] = None
        
        logger.info("🔗 Webhook service initialized")
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create HTTP session"""
        if self._session is None or self._session.closed:
            connector = aiohttp.TCPConnector(limit=100, limit_per_host=30)
            timeout = aiohttp.ClientTimeout(total=300, connect=30)
            self._session = aiohttp.ClientSession(
                connector=connector,
                timeout=timeout,
                headers={'User-Agent': 'PANACEA-ICONO-Webhook/1.0.0'}
            )
        return self._session
    
    async def close(self):
        """Close HTTP session"""
        if self._session and not self._session.closed:
            await self._session.close()
    
    def register_webhook(self, webhook_config: WebhookConfig) -> str:
        """Register a new webhook"""
        # Generate ID if not provided
        if not webhook_config.id:
            webhook_config.id = str(uuid.uuid4())
        
        # Set timestamps
        now = datetime.now(timezone.utc)
        webhook_config.created_at = now
        webhook_config.updated_at = now
        
        # Store webhook
        self.webhooks[webhook_config.id] = webhook_config
        
        logger.info(f"🔗 Webhook registered: {webhook_config.name} ({webhook_config.id})")
        return webhook_config.id
    
    def update_webhook(self, webhook_id: str, updates: Dict[str, Any]) -> bool:
        """Update an existing webhook"""
        if webhook_id not in self.webhooks:
            return False
        
        webhook = self.webhooks[webhook_id]
        
        # Update fields
        for field, value in updates.items():
            if hasattr(webhook, field):
                setattr(webhook, field, value)
        
        # Update timestamp
        webhook.updated_at = datetime.now(timezone.utc)
        
        logger.info(f"🔄 Webhook updated: {webhook.name} ({webhook_id})")
        return True
    
    def delete_webhook(self, webhook_id: str) -> bool:
        """Delete a webhook"""
        if webhook_id not in self.webhooks:
            return False
        
        webhook = self.webhooks.pop(webhook_id)
        logger.info(f"🗑️ Webhook deleted: {webhook.name} ({webhook_id})")
        return True
    
    def get_webhook(self, webhook_id: str) -> Optional[WebhookConfig]:
        """Get a webhook by ID"""
        return self.webhooks.get(webhook_id)
    
    def list_webhooks(self, active_only: bool = False) -> List[WebhookConfig]:
        """List all webhooks"""
        webhooks = list(self.webhooks.values())
        if active_only:
            webhooks = [w for w in webhooks if w.active]
        return webhooks
    
    def register_event_handler(self, event_type: WebhookEventType, handler: Callable):
        """Register an event handler"""
        if event_type not in self.event_handlers:
            self.event_handlers[event_type] = []
        self.event_handlers[event_type].append(handler)
        logger.info(f"📝 Event handler registered for {event_type}")
    
    async def process_event(self, event: WebhookEvent) -> str:
        """Process a webhook event"""
        # Generate event ID if not provided
        if not event.id:
            event.id = str(uuid.uuid4())
        
        # Store event
        self.events[event.id] = event
        
        logger.info(f"📨 Processing event: {event.event_type} ({event.id})")
        
        # Run event handlers
        if event.event_type in self.event_handlers:
            for handler in self.event_handlers[event.event_type]:
                try:
                    await handler(event)
                except Exception as e:
                    logger.error(f"❌ Event handler error: {e}")
        
        # Find matching webhooks
        matching_webhooks = [
            webhook for webhook in self.webhooks.values()
            if webhook.active and (
                not webhook.event_types or event.event_type in webhook.event_types
            )
        ]
        
        # Schedule deliveries
        delivery_tasks = []
        for webhook in matching_webhooks:
            delivery_id = await self._schedule_delivery(webhook.id, event.id)
            if delivery_id:
                task = asyncio.create_task(self._deliver_webhook(delivery_id))
                delivery_tasks.append(task)
        
        # Wait for all deliveries to complete (with timeout)
        if delivery_tasks:
            try:
                await asyncio.wait_for(
                    asyncio.gather(*delivery_tasks, return_exceptions=True),
                    timeout=60.0  # 1 minute timeout for all deliveries
                )
            except asyncio.TimeoutError:
                logger.warning("⏰ Some webhook deliveries timed out")
        
        logger.info(f"✅ Event processed: {event.event_type} ({event.id})")
        return event.id
    
    async def _schedule_delivery(self, webhook_id: str, event_id: str) -> Optional[str]:
        """Schedule a webhook delivery"""
        delivery = WebhookDelivery(
            id=str(uuid.uuid4()),
            webhook_id=webhook_id,
            event_id=event_id,
            next_attempt_at=datetime.now(timezone.utc)
        )
        
        self.deliveries[delivery.id] = delivery
        logger.debug(f"📅 Delivery scheduled: {delivery.id}")
        return delivery.id
    
    async def _deliver_webhook(self, delivery_id: str) -> bool:
        """Deliver a webhook"""
        delivery = self.deliveries.get(delivery_id)
        if not delivery:
            logger.error(f"❌ Delivery not found: {delivery_id}")
            return False
        
        webhook = self.webhooks.get(delivery.webhook_id)
        event = self.events.get(delivery.event_id)
        
        if not webhook or not event:
            logger.error(f"❌ Missing webhook or event for delivery: {delivery_id}")
            delivery.status = WebhookStatus.FAILED
            delivery.error_message = "Missing webhook or event"
            return False
        
        # Prepare payload
        payload_data = {
            'event_id': event.id,
            'event_type': event.event_type,
            'timestamp': event.timestamp.isoformat(),
            'source': event.source,
            'data': event.payload
        }
        payload_json = json.dumps(payload_data, separators=(',', ':'))
        payload_bytes = payload_json.encode('utf-8')
        
        # Generate signature if secret is provided
        headers = {'Content-Type': 'application/json'}
        if webhook.secret:
            signature = WebhookSignature.generate_signature(payload_bytes, webhook.secret)
            headers['X-Webhook-Signature'] = signature
        
        # Add custom headers
        headers.update(webhook.headers)
        
        # Update delivery status
        delivery.attempt_count += 1
        delivery.last_attempt_at = datetime.now(timezone.utc)
        delivery.status = WebhookStatus.RETRYING if delivery.attempt_count > 1 else WebhookStatus.PENDING
        
        try:
            session = await self._get_session()
            
            # Make HTTP request
            async with session.post(
                webhook.url,
                data=payload_bytes,
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=webhook.timeout),
                ssl=webhook.ssl_verify
            ) as response:
                delivery.response_status = response.status
                
                # Read response body (limited size)
                response_text = await response.text()
                if len(response_text) > 1000:
                    response_text = response_text[:1000] + "..."
                delivery.response_body = response_text
                
                # Check if delivery was successful
                if 200 <= response.status < 300:
                    delivery.status = WebhookStatus.DELIVERED
                    logger.info(f"✅ Webhook delivered successfully: {webhook.name}")
                    return True
                else:
                    delivery.status = WebhookStatus.FAILED
                    delivery.error_message = f"HTTP {response.status}: {response_text}"
                    logger.warning(f"⚠️ Webhook delivery failed with status {response.status}: {webhook.name}")
        
        except asyncio.TimeoutError:
            delivery.status = WebhookStatus.FAILED
            delivery.error_message = "Request timeout"
            logger.warning(f"⏰ Webhook delivery timed out: {webhook.name}")
        
        except Exception as e:
            delivery.status = WebhookStatus.FAILED
            delivery.error_message = str(e)
            logger.error(f"❌ Webhook delivery failed: {webhook.name} - {e}")
        
        # Schedule retry if needed
        if (delivery.status == WebhookStatus.FAILED and 
            delivery.attempt_count < webhook.retry_count):
            # Exponential backoff: 2^attempt minutes
            retry_delay = timedelta(minutes=2 ** delivery.attempt_count)
            delivery.next_attempt_at = datetime.now(timezone.utc) + retry_delay
            
            # Schedule retry
            asyncio.create_task(self._retry_delivery(delivery_id, retry_delay))
            logger.info(f"🔄 Webhook delivery retry scheduled in {retry_delay}: {webhook.name}")
        
        return delivery.status == WebhookStatus.DELIVERED
    
    async def _retry_delivery(self, delivery_id: str, delay: timedelta):
        """Retry webhook delivery after delay"""
        await asyncio.sleep(delay.total_seconds())
        await self._deliver_webhook(delivery_id)
    
    def get_delivery_status(self, delivery_id: str) -> Optional[WebhookDelivery]:
        """Get delivery status"""
        return self.deliveries.get(delivery_id)
    
    def get_event_deliveries(self, event_id: str) -> List[WebhookDelivery]:
        """Get all deliveries for an event"""
        return [d for d in self.deliveries.values() if d.event_id == event_id]
    
    def get_webhook_deliveries(self, webhook_id: str, limit: int = 50) -> List[WebhookDelivery]:
        """Get deliveries for a webhook"""
        webhook_deliveries = [d for d in self.deliveries.values() if d.webhook_id == webhook_id]
        # Sort by creation time, most recent first
        webhook_deliveries.sort(key=lambda x: x.created_at, reverse=True)
        return webhook_deliveries[:limit]
    
    def get_stats(self) -> WebhookStats:
        """Get webhook statistics"""
        deliveries = list(self.deliveries.values())
        events = list(self.events.values())
        
        successful_deliveries = sum(1 for d in deliveries if d.status == WebhookStatus.DELIVERED)
        failed_deliveries = sum(1 for d in deliveries if d.status == WebhookStatus.FAILED)
        total_deliveries = len(deliveries)
        
        success_rate = (successful_deliveries / total_deliveries * 100) if total_deliveries > 0 else 0
        
        # Count events by type
        events_by_type = {}
        for event in events:
            event_type = event.event_type.value
            events_by_type[event_type] = events_by_type.get(event_type, 0) + 1
        
        # Get recent events (last 10)
        recent_events = sorted(events, key=lambda x: x.timestamp, reverse=True)[:10]
        
        return WebhookStats(
            total_webhooks=len(self.webhooks),
            active_webhooks=sum(1 for w in self.webhooks.values() if w.active),
            total_events=len(events),
            total_deliveries=total_deliveries,
            successful_deliveries=successful_deliveries,
            failed_deliveries=failed_deliveries,
            success_rate=round(success_rate, 2),
            events_by_type=events_by_type,
            recent_events=recent_events
        )


# Global webhook service instance
webhook_service = WebhookService()