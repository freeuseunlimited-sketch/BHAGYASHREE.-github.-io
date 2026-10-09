from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from models import UserProfile, ReplicaRequest, ReplicaResponse, Message
from replica_engine import ReplicaEngine
from datetime import datetime
from typing import Dict, List

app = FastAPI(title="AI Replica API – Kaleshi Edition")

# Allow the frontend (wherever it is opened from) to call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

users: Dict[str, UserProfile] = {}
conversations: Dict[str, List[Message]] = {}

MAX_CONV_LEN = 20


@app.post("/users", response_model=UserProfile)
def create_user(profile: UserProfile):
    if profile.user_id in users:
        raise HTTPException(status_code=400, detail="User already exists")
    users[profile.user_id] = profile
    conversations[profile.user_id] = []
    return profile


@app.get("/users/{user_id}", response_model=UserProfile)
def get_user(user_id: str):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    return users[user_id]


@app.put("/users/{user_id}", response_model=UserProfile)
def update_user(user_id: str, profile: UserProfile):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    profile.updated_at = datetime.utcnow()
    users[user_id] = profile
    return profile


@app.post("/replica/chat", response_model=ReplicaResponse)
def chat_with_replica(req: ReplicaRequest):
    if req.user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")

    profile = users[req.user_id]

    # Update stored conversation
    conv = conversations.get(req.user_id, [])
    conv.append(Message(role="user", content=req.prompt))

    engine = ReplicaEngine(profile)
    reply = engine.generate_reply(req.prompt, conv)

    conv.append(Message(role="assistant", content=reply))
    if len(conv) > MAX_CONV_LEN:
        conv = conv[-MAX_CONV_LEN:]
    conversations[req.user_id] = conv

    return ReplicaResponse(
        user_id=req.user_id,
        prompt=req.prompt,
        reply=reply,
        model_used="local-replica-v1",
    )


@app.get("/replica/conversation/{user_id}")
def get_conversation(user_id: str):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    return {"user_id": user_id, "conversation": conversations.get(user_id, [])}


# Serve the frontend (mounted last so API routes above take priority)
FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"
app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")
