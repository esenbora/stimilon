import httpx
from .base import LLMConnector


class OpenAIConnector(LLMConnector):
    """Connector for OpenAI-compatible APIs (OpenAI, Azure, Groq, Together AI, etc.)"""

    DEFAULT_ENDPOINT = "https://api.openai.com/v1"
    DEFAULT_MODEL = "gpt-4o-mini"

    def __init__(self, api_key: str, endpoint: str | None = None, model: str | None = None):
        super().__init__(api_key, endpoint, model)
        self.endpoint = endpoint or self.DEFAULT_ENDPOINT
        self.model = model or self.DEFAULT_MODEL

    async def send_message(self, message: str) -> str:
        """Send a message to the OpenAI-compatible API."""
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{self.endpoint}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": self.model,
                    "messages": [{"role": "user", "content": message}],
                    "max_tokens": 1024,
                    "temperature": 0.7,
                },
            )

            if response.status_code != 200:
                raise Exception(f"API error: {response.status_code} - {response.text}")

            data = response.json()
            return data["choices"][0]["message"]["content"]

    async def health_check(self) -> bool:
        """Check if the OpenAI API is reachable."""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    f"{self.endpoint}/models",
                    headers={"Authorization": f"Bearer {self.api_key}"},
                )
                return response.status_code == 200
        except Exception:
            return False
