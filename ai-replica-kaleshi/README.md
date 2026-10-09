# AI Replica – Kaleshi Edition

Hinglish, thoda kaleshi/nakhre wala AI replica (gf / bestie / friend style).
FastAPI backend + simple HTML frontend. Arena Agent Mode ke saath kaam karne ke liye ready.

## Project structure

```
ai-replica-kaleshi/
├── .gitignore
├── README.md
├── backend/
│   ├── requirements.txt
│   ├── models.py           # Pydantic models (UserProfile, Message, ReplicaRequest/Response)
│   ├── personality.py      # Kaleshi/nakhre personality layer
│   ├── replica_engine.py   # Core reply engine + decoration
│   └── main.py             # FastAPI app (also serves the frontend)
└── frontend/
    └── index.html          # Simple chat UI
```

## Setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Run

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

- Frontend: http://127.0.0.1:8000/
- API docs (Swagger): http://127.0.0.1:8000/docs

## API endpoints

| Method | Path                          | Description                    |
|--------|-------------------------------|--------------------------------|
| POST   | `/users`                      | Create a user profile          |
| GET    | `/users/{user_id}`            | Get a user profile             |
| PUT    | `/users/{user_id}`            | Update a user profile          |
| POST   | `/replica/chat`               | Chat with the replica          |
| GET    | `/replica/conversation/{id}`  | Get stored conversation        |

## Quick test (curl)

```bash
# Create user
curl -X POST http://127.0.0.1:8000/users \
  -H "Content-Type: application/json" \
  -d '{"user_id":"user123","name":"Bhagyashree","personality_traits":["funny","caring"],"kaleshi_level":0.8,"relationship_label":"gf"}'

# Chat
curl -X POST http://127.0.0.1:8000/replica/chat \
  -H "Content-Type: application/json" \
  -d '{"user_id":"user123","prompt":"hi, kaise ho?"}'
```
