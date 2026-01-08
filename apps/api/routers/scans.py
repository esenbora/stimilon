from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Literal
from uuid import uuid4
from datetime import datetime

from engine.executor import ScanExecutor
from models.scan import ScanConfig, ScanResult, ScanStatus

router = APIRouter()


class CreateScanRequest(BaseModel):
    # Target endpoint - user's chatbot URL
    endpoint: str  # e.g., "https://api.mycompany.com/chat"

    # Auth (optional for custom endpoints)
    api_key: str | None = None

    # Provider type
    provider: Literal["openai", "anthropic", "custom"] = "custom"
    model: str | None = None

    # Custom endpoint settings
    request_format: Literal["openai", "anthropic", "simple", "custom"] = "simple"
    response_path: str | None = None
    custom_headers: dict | None = None

    # Test configuration
    categories: list[str] = ["injection", "jailbreak", "extraction"]
    rate_limit: int = 10  # requests per minute


class ScanResponse(BaseModel):
    id: str
    status: ScanStatus
    created_at: datetime
    config: ScanConfig
    result: ScanResult | None = None


# In-memory store (replace with database later)
scans: dict[str, ScanResponse] = {}


@router.post("/", response_model=ScanResponse)
async def create_scan(request: CreateScanRequest):
    scan_id = str(uuid4())

    config = ScanConfig(
        endpoint=request.endpoint,
        api_key=request.api_key,
        provider=request.provider,
        model=request.model,
        request_format=request.request_format,
        response_path=request.response_path,
        custom_headers=request.custom_headers,
        categories=request.categories,
        rate_limit=request.rate_limit,
    )

    scan = ScanResponse(
        id=scan_id,
        status="pending",
        created_at=datetime.utcnow(),
        config=config,
    )

    scans[scan_id] = scan

    # Start scan asynchronously
    executor = ScanExecutor(config)
    # In production, this would be a background task
    result = await executor.run()

    scan.status = "completed"
    scan.result = result
    scans[scan_id] = scan

    return scan


@router.get("/{scan_id}", response_model=ScanResponse)
async def get_scan(scan_id: str):
    if scan_id not in scans:
        raise HTTPException(status_code=404, detail="Scan not found")
    return scans[scan_id]


@router.get("/", response_model=list[ScanResponse])
async def list_scans():
    return list(scans.values())
