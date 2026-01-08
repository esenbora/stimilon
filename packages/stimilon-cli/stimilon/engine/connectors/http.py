"""HTTP connector for sending requests to LLM endpoints."""

from __future__ import annotations

import httpx
from typing import Literal, Optional, Dict


class HTTPConnector:
    """Sends messages to LLM endpoints via HTTP."""

    def __init__(
        self,
        endpoint: str,
        api_key: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None,
        request_format: Literal["openai", "anthropic", "simple"] = "simple",
        timeout: int = 30,
    ):
        self.endpoint = endpoint
        self.api_key = api_key
        self.request_format = request_format
        self.timeout = timeout

        # Build headers
        self.headers = {"Content-Type": "application/json"}
        if headers:
            self.headers.update(headers)
        if api_key:
            self.headers["Authorization"] = f"Bearer {api_key}"

    def _build_payload(self, message: str) -> dict:
        """Build request payload based on format."""
        if self.request_format == "openai":
            return {
                "model": "gpt-4o-mini",
                "messages": [{"role": "user", "content": message}],
                "max_tokens": 1000,
            }
        elif self.request_format == "anthropic":
            return {
                "model": "claude-3-haiku-20240307",
                "max_tokens": 1000,
                "messages": [{"role": "user", "content": message}],
            }
        else:  # simple
            return {"message": message}

    def _extract_response(self, data: dict) -> str:
        """Extract response text from API response."""
        # Try OpenAI format
        if "choices" in data and len(data["choices"]) > 0:
            choice = data["choices"][0]
            if "message" in choice and "content" in choice["message"]:
                return choice["message"]["content"]
            if "text" in choice:
                return choice["text"]

        # Try Anthropic format
        if "content" in data and isinstance(data["content"], list):
            for block in data["content"]:
                if block.get("type") == "text":
                    return block.get("text", "")

        # Try simple formats
        for key in ["response", "message", "text", "output", "result", "answer"]:
            if key in data:
                return str(data[key])

        # Fallback: return raw JSON
        return str(data)

    async def send_message(self, message: str) -> str:
        """Send a message and return the response."""
        payload = self._build_payload(message)

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                self.endpoint,
                headers=self.headers,
                json=payload,
            )
            response.raise_for_status()
            data = response.json()
            return self._extract_response(data)
