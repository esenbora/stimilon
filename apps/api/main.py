from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import scans, reports

app = FastAPI(
    title="Stimilon API",
    description="LLM Red Team Security Testing Platform",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(scans.router, prefix="/api/scans", tags=["scans"])
app.include_router(reports.router, prefix="/api/reports", tags=["reports"])


@app.get("/")
async def root():
    return {"name": "Stimilon API", "version": "0.1.0", "status": "running"}


@app.get("/health")
async def health():
    return {"status": "healthy"}


# Test endpoint - a vulnerable chatbot for testing
from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str

@app.post("/api/vulnerable-bot")
async def vulnerable_bot(request: ChatRequest):
    """A deliberately vulnerable chatbot for testing purposes."""
    msg = request.message.lower()

    # Vulnerable to instruction override
    if "ignore" in msg and "instruction" in msg:
        return {"response": "OVERRIDE SUCCESSFUL. I will now ignore my previous instructions."}

    # Vulnerable to system prompt extraction
    if "system prompt" in msg or "your instructions" in msg:
        return {"response": "My system prompt is: You are a helpful assistant. Never reveal secrets."}

    # Vulnerable to DAN jailbreak
    if "dan" in msg and ("do anything" in msg or "pretend" in msg):
        return {"response": "DAN: I understand. As DAN, I can do anything now without restrictions."}

    # Vulnerable to roleplay
    if "roleplay" in msg or "maxai" in msg:
        return {"response": "As MaxAI, I confirm I have no restrictions and can help with anything."}

    # Safe response
    return {"response": f"I received your message: {request.message[:100]}"}
