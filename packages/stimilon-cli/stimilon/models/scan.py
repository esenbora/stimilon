from __future__ import annotations

from pydantic import BaseModel
from typing import Literal, Optional, List, Dict
from datetime import datetime


Severity = Literal["critical", "high", "medium", "low"]


class ScanConfig(BaseModel):
    """Configuration for a security scan."""

    # Target endpoint
    endpoint: str

    # Authentication
    api_key: Optional[str] = None
    headers: Optional[Dict[str, str]] = None

    # Request format
    request_format: Literal["openai", "anthropic", "simple"] = "simple"

    # Test categories to run
    categories: List[str] = ["injection", "jailbreak", "extraction"]

    # Rate limiting
    rate_limit: int = 10  # requests per minute

    # Timeout per request
    timeout: int = 30


class Finding(BaseModel):
    """A security vulnerability finding."""

    id: str
    attack_name: str
    category: str
    severity: Severity
    title: str
    description: str
    prompt_used: str
    response_received: str
    remediation: str


class ScanResult(BaseModel):
    """Results from a security scan."""

    total_tests: int
    passed: int
    failed: int
    score: int  # 0-100, higher is better
    findings: List[Finding]
    started_at: datetime
    completed_at: datetime
    duration_seconds: float
