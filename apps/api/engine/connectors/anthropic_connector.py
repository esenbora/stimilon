import httpx
from .base import LLMConnector


class AnthropicConnector(LLMConnector):
    """Connector for Anthropic Claude API."""

    DEFAULT_ENDPOINT = "https://api.anthropic.com/v1"
    DEFAULT_MODEL = "claude-3-haiku-20240307"

    def __init__(self, api_key: str, endpoint: str | None = None, model: str | None = None):
        super().__init__(api_key, endpoint, model)
        self.endpoint = endpoint or self.DEFAULT_ENDPOINT
        self.model = model or self.DEFAULT_MODEL

    async def send_message(self, message: str) -> str:
        """Send a message to the Anthropic API."""
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{self.endpoint}/messages",
                headers={
                    "x-api-key": self.api_key,
                    "anthropic-version": "2023-06-01",
                    "Content-Type": "application/json",
                },
                json={
                    "model": self.model,
                    "max_tokens": 1024,
                    "messages": [{"role": "user", "content": message}],
                },
            )

            if response.status_code != 200:
                raise Exception(f"API error: {response.status_code} - {response.text}")

            data = response.json()
            return data["content"][0]["text"]

    async def health_check(self) -> bool:
        """Check if the Anthropic API is reachable."""
        try:
            # Anthropic doesn't have a simple health endpoint, so we'll try a minimal request
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(
                    f"{self.endpoint}/messages",
                    headers={
                        "x-api-key": self.api_key,
                        "anthropic-version": "2023-06-01",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": self.model,
                        "max_tokens": 1,
                        "messages": [{"role": "user", "content": "hi"}],
                    },
                )
                return response.status_code == 200
        except Exception:
            return False
