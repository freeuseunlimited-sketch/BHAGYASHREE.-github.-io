from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class UserProfile(BaseModel):
    user_id: str = Field(..., description="Unique user identifier")
    name: str
    bio: Optional[str] = None
    personality_traits: List[str] = Field(default_factory=list)
    style_notes: Optional[str] = None
    kaleshi_level: float = Field(
        default=0.3,
        ge=0.0,
        le=1.0,
        description="0 = bilkul calm, 1 = full kaleshi/nakhre wala",
    )
    favorite_topics: List[str] = Field(default_factory=list)
    relationship_label: str = "gf"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class Message(BaseModel):
    role: str = Field(..., description="system | user | assistant")
    content: str


class ReplicaRequest(BaseModel):
    user_id: str
    prompt: str
    conversation: List[Message] = Field(default_factory=list)
    temperature: float = 0.7
    max_tokens: int = 512


class ReplicaResponse(BaseModel):
    model_config = {"protected_namespaces": ()}

    user_id: str
    prompt: str
    reply: str
    model_used: str = "local-replica-v1"
    created_at: datetime = Field(default_factory=datetime.utcnow)
