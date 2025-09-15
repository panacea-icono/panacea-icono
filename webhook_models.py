#!/usr/bin/env python3
"""
🔗 PANACEA ICONO - Webhook Models
Pydantic models for webhook functionality
"""

import hashlib
import hmac
import secrets
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field, validator


class WebhookEventType(str, Enum):
    """Types of webhook events"""
    GITHUB_PUSH = "github.push"
    GITHUB_PR = "github.pull_request"
    GITHUB_RELEASE = "github.release"
    HEROKU_DEPLOY = "heroku.deploy"
    HEROKU_BUILD = "heroku.build"
    HF_MODEL_UPDATE = "huggingface.model_update"
    HEALTH_CHECK = "system.health_check"
    CUSTOM = "custom"


class WebhookStatus(str, Enum):
    """Webhook delivery status"""
    PENDING = "pending"
    DELIVERED = "delivered"
    FAILED = "failed"
    RETRYING = "retrying"


class WebhookConfig(BaseModel):
    """Webhook configuration model"""
    id: Optional[str] = Field(None, description="Webhook configuration ID")
    name: str = Field(..., description="Webhook name", min_length=1, max_length=100)
    url: str = Field(..., description="Target URL for webhook delivery")
    secret: Optional[str] = Field(None, description="Secret for signature verification")
    event_types: List[WebhookEventType] = Field(default=[], description="Event types to subscribe to")
    active: bool = Field(default=True, description="Whether webhook is active")
    ssl_verify: bool = Field(default=True, description="Whether to verify SSL certificates")
    timeout: int = Field(default=30, description="Request timeout in seconds", ge=5, le=300)
    retry_count: int = Field(default=3, description="Number of retry attempts", ge=0, le=10)
    headers: Dict[str, str] = Field(default={}, description="Additional headers to send")
    created_at: Optional[datetime] = Field(None, description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")

    @validator('url')
    def validate_url(cls, v):
        """Validate webhook URL"""
        if not v.startswith(('http://', 'https://')):
            raise ValueError('URL must start with http:// or https://')
        return v

    @validator('secret', pre=True, always=True)
    def generate_secret_if_none(cls, v):
        """Generate secret if not provided"""
        if v is None:
            return secrets.token_urlsafe(32)
        return v

    class Config:
        """Pydantic config"""
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class WebhookEvent(BaseModel):
    """Webhook event model"""
    id: Optional[str] = Field(None, description="Event ID")
    event_type: WebhookEventType = Field(..., description="Type of event")
    source: str = Field(..., description="Source of the event")
    payload: Dict[str, Any] = Field(..., description="Event payload")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = Field(default={}, description="Additional metadata")

    class Config:
        """Pydantic config"""
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class WebhookDelivery(BaseModel):
    """Webhook delivery model"""
    id: Optional[str] = Field(None, description="Delivery ID")
    webhook_id: str = Field(..., description="Webhook configuration ID")
    event_id: str = Field(..., description="Event ID")
    status: WebhookStatus = Field(default=WebhookStatus.PENDING)
    attempt_count: int = Field(default=0, description="Number of delivery attempts")
    last_attempt_at: Optional[datetime] = Field(None, description="Last attempt timestamp")
    next_attempt_at: Optional[datetime] = Field(None, description="Next scheduled attempt")
    response_status: Optional[int] = Field(None, description="HTTP response status code")
    response_body: Optional[str] = Field(None, description="Response body")
    error_message: Optional[str] = Field(None, description="Error message if failed")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        """Pydantic config"""
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class GitHubWebhookPayload(BaseModel):
    """GitHub webhook payload structure"""
    action: Optional[str] = Field(None, description="GitHub action type")
    repository: Dict[str, Any] = Field(..., description="Repository information")
    sender: Dict[str, Any] = Field(..., description="Event sender information")
    ref: Optional[str] = Field(None, description="Git reference")
    commits: Optional[List[Dict[str, Any]]] = Field(None, description="Commit information")
    pull_request: Optional[Dict[str, Any]] = Field(None, description="Pull request data")
    release: Optional[Dict[str, Any]] = Field(None, description="Release data")


class HerokuWebhookPayload(BaseModel):
    """Heroku webhook payload structure"""
    action: str = Field(..., description="Heroku action type")
    app: Dict[str, Any] = Field(..., description="App information")
    user: Dict[str, Any] = Field(..., description="User information")
    data: Dict[str, Any] = Field(default={}, description="Additional data")


class HuggingFaceWebhookPayload(BaseModel):
    """Hugging Face webhook payload structure"""
    action: str = Field(..., description="Action type")
    model: Dict[str, Any] = Field(..., description="Model information")
    user: Dict[str, Any] = Field(..., description="User information")
    commit: Optional[Dict[str, Any]] = Field(None, description="Commit information")


class WebhookResponse(BaseModel):
    """Standard webhook response"""
    success: bool = Field(..., description="Whether the webhook was processed successfully")
    message: str = Field(..., description="Response message")
    event_id: Optional[str] = Field(None, description="Event ID if applicable")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        """Pydantic config"""
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class WebhookSignature:
    """Webhook signature verification utilities"""
    
    @staticmethod
    def generate_signature(payload: bytes, secret: str, algorithm: str = "sha256") -> str:
        """Generate webhook signature"""
        signature = hmac.new(
            secret.encode('utf-8'),
            payload,
            hashlib.sha256 if algorithm == "sha256" else hashlib.sha1
        ).hexdigest()
        return f"{algorithm}={signature}"
    
    @staticmethod
    def verify_signature(payload: bytes, signature: str, secret: str) -> bool:
        """Verify webhook signature"""
        try:
            # Extract algorithm and signature
            algorithm, expected_signature = signature.split('=', 1)
            
            # Generate signature with the same algorithm
            computed_signature = hmac.new(
                secret.encode('utf-8'),
                payload,
                hashlib.sha256 if algorithm == "sha256" else hashlib.sha1
            ).hexdigest()
            
            # Compare signatures securely
            return hmac.compare_digest(expected_signature, computed_signature)
        except (ValueError, AttributeError):
            return False


class WebhookStats(BaseModel):
    """Webhook statistics model"""
    total_webhooks: int = Field(..., description="Total number of webhooks")
    active_webhooks: int = Field(..., description="Number of active webhooks")
    total_events: int = Field(..., description="Total events processed")
    total_deliveries: int = Field(..., description="Total delivery attempts")
    successful_deliveries: int = Field(..., description="Successful deliveries")
    failed_deliveries: int = Field(..., description="Failed deliveries")
    success_rate: float = Field(..., description="Delivery success rate")
    events_by_type: Dict[str, int] = Field(default={}, description="Events grouped by type")
    recent_events: List[WebhookEvent] = Field(default=[], description="Recent events")