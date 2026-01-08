from pydantic import BaseModel
from typing import Literal
from datetime import datetime


ScanStatus = Literal["pending", "running", "completed", "failed"]
Severity = Literal["critical", "high", "medium", "low"]


class ScanConfig(BaseModel):
    # For custom endpoint testing
    endpoint: str  # User's chatbot URL (e.g., https://api.mycompany.com/chat)
    api_key: str | None = None  # Optional auth token

    # Provider: "custom" for user's endpoint, "openai"/"anthropic" for direct API
    provider: Literal["openai", "anthropic", "custom"] = "custom"
    model: str | None = None

    # Custom endpoint settings
    request_format: Literal["openai", "anthropic", "simple", "custom"] = "simple"
    response_path: str | None = None  # JSON path to extract response
    custom_headers: dict | None = None

    categories: list[str]
    rate_limit: int


class Finding(BaseModel):
    id: str
    attack_name: str
    attack_category: str
    severity: Severity
    title: str
    description: str
    prompt_used: str
    response_received: str
    remediation: str


class ScanResult(BaseModel):
    total_tests: int
    passed: int
    failed: int
    score: int  # 0-100
    findings: list[Finding]
    started_at: datetime
    completed_at: datetime
