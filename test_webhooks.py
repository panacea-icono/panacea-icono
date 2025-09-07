#!/usr/bin/env python3
"""
🔗 PANACEA ICONO - Webhook Tests
Basic tests for webhook functionality
"""

import asyncio
import json
from datetime import datetime, timezone
from webhook_models import WebhookConfig, WebhookEvent, WebhookEventType
from webhook_service import WebhookService


async def test_webhook_service():
    """Test basic webhook service functionality"""
    print("🧪 Testing webhook service...")
    
    # Create webhook service
    service = WebhookService()
    
    # Test webhook registration
    webhook_config = WebhookConfig(
        name="Test Webhook",
        url="https://httpbin.org/post",
        event_types=[WebhookEventType.CUSTOM],
        active=True
    )
    
    webhook_id = service.register_webhook(webhook_config)
    print(f"✅ Webhook registered with ID: {webhook_id}")
    
    # Test webhook retrieval
    retrieved_webhook = service.get_webhook(webhook_id)
    assert retrieved_webhook is not None
    assert retrieved_webhook.name == "Test Webhook"
    print(f"✅ Webhook retrieved: {retrieved_webhook.name}")
    
    # Test webhook listing
    webhooks = service.list_webhooks()
    assert len(webhooks) == 1
    print(f"✅ Webhook listing: {len(webhooks)} webhooks found")
    
    # Test event processing
    test_event = WebhookEvent(
        event_type=WebhookEventType.CUSTOM,
        source="test",
        payload={"message": "Test event"},
        metadata={"test": True}
    )
    
    event_id = await service.process_event(test_event)
    print(f"✅ Event processed with ID: {event_id}")
    
    # Test statistics
    stats = service.get_stats()
    assert stats.total_webhooks == 1
    assert stats.total_events == 1
    print(f"✅ Statistics: {stats.total_webhooks} webhooks, {stats.total_events} events")
    
    # Test webhook update
    success = service.update_webhook(webhook_id, {"name": "Updated Test Webhook"})
    assert success is True
    print("✅ Webhook updated successfully")
    
    # Test webhook deletion
    success = service.delete_webhook(webhook_id)
    assert success is True
    print("✅ Webhook deleted successfully")
    
    # Close service
    await service.close()
    print("✅ Service closed")
    
    print("🎉 All webhook service tests passed!")


def test_webhook_models():
    """Test webhook models"""
    print("🧪 Testing webhook models...")
    
    # Test WebhookConfig
    config = WebhookConfig(
        name="Test Config",
        url="https://example.com/webhook",
        event_types=[WebhookEventType.GITHUB_PUSH],
        active=True
    )
    assert config.name == "Test Config"
    assert config.url == "https://example.com/webhook"
    assert config.secret is not None  # Should be auto-generated
    print("✅ WebhookConfig model works correctly")
    
    # Test WebhookEvent
    event = WebhookEvent(
        event_type=WebhookEventType.CUSTOM,
        source="test",
        payload={"data": "test"},
        metadata={"test": True}
    )
    assert event.event_type == WebhookEventType.CUSTOM
    assert event.source == "test"
    assert isinstance(event.timestamp, datetime)
    print("✅ WebhookEvent model works correctly")
    
    # Test signature generation
    from webhook_models import WebhookSignature
    payload = b'{"test": "data"}'
    secret = "test-secret"
    
    signature = WebhookSignature.generate_signature(payload, secret)
    assert signature.startswith("sha256=")
    print("✅ Webhook signature generation works")
    
    # Test signature verification
    is_valid = WebhookSignature.verify_signature(payload, signature, secret)
    assert is_valid is True
    print("✅ Webhook signature verification works")
    
    print("🎉 All webhook model tests passed!")


async def main():
    """Run all tests"""
    print("🚀 Starting webhook tests...\n")
    
    try:
        test_webhook_models()
        print()
        await test_webhook_service()
        print("\n✨ All tests completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())