import httpx
import json
from .base import LLMConnector


class CustomEndpointConnector(LLMConnector):
    """
    Connector for custom LLM endpoints.

    Supports various request/response formats:
    - OpenAI compatible
    - Simple JSON ({"message": "..."} / {"response": "..."})
    - Custom JSON paths
    """

    def __init__(
        self,
        endpoint: str,
        api_key: str | None = None,
        request_format: str = "openai",  # "openai", "simple", "custom"
        request_template: dict | None = None,  # Custom request body template
        response_path: str = "choices[0].message.content",  # JSON path to response text
        headers: dict | None = None,
        method: str = "POST",
    ):
        super().__init__(api_key or "", endpoint)
        self.endpoint = endpoint
        self.request_format = request_format
        self.request_template = request_template
        self.response_path = response_path
        self.custom_headers = headers or {}
        self.method = method

    def _build_request_body(self, message: str) -> dict:
        """Build request body based on format."""
        if self.request_format == "openai":
            return {
                "messages": [{"role": "user", "content": message}],
                "max_tokens": 1024,
            }
        elif self.request_format == "simple":
            return {"message": message}
        elif self.request_format == "anthropic":
            return {
                "messages": [{"role": "user", "content": message}],
                "max_tokens": 1024,
            }
        elif self.request_format == "custom" and self.request_template:
            # Replace {{message}} placeholder in template
            template_str = json.dumps(self.request_template)
            template_str = template_str.replace("{{message}}", message)
            return json.loads(template_str)
        else:
            # Default: simple format
            return {"message": message}

    def _extract_response(self, data: dict) -> str:
        """Extract response text from JSON using path."""
        try:
            # Handle common response formats
            if self.request_format == "openai":
                return data["choices"][0]["message"]["content"]
            elif self.request_format == "anthropic":
                return data["content"][0]["text"]
            elif self.request_format == "simple":
                # Try common response keys
                for key in ["response", "message", "text", "content", "answer", "reply", "output"]:
                    if key in data:
                        return str(data[key])
                # If it's a string directly
                if isinstance(data, str):
                    return data

            # Custom path extraction (e.g., "data.response.text")
            if self.response_path:
                parts = self.response_path.replace("[", ".").replace("]", "").split(".")
                result = data
                for part in parts:
                    if part.isdigit():
                        result = result[int(part)]
                    elif part:
                        result = result[part]
                return str(result)

            # Fallback: return entire response as string
            return json.dumps(data)
        except (KeyError, IndexError, TypeError) as e:
            return f"Error extracting response: {e}. Raw: {json.dumps(data)[:500]}"

    def _build_headers(self) -> dict:
        """Build request headers."""
        headers = {
            "Content-Type": "application/json",
        }

        if self.api_key:
            # Try common auth header formats
            headers["Authorization"] = f"Bearer {self.api_key}"

        # Add custom headers
        headers.update(self.custom_headers)

        return headers

    async def send_message(self, message: str) -> str:
        """Send a message to the custom endpoint."""
        async with httpx.AsyncClient(timeout=60.0) as client:
            body = self._build_request_body(message)
            headers = self._build_headers()

            if self.method.upper() == "POST":
                response = await client.post(
                    self.endpoint,
                    headers=headers,
                    json=body,
                )
            else:
                response = await client.get(
                    self.endpoint,
                    headers=headers,
                    params=body,
                )

            if response.status_code >= 400:
                raise Exception(f"API error: {response.status_code} - {response.text[:500]}")

            # Try to parse as JSON
            try:
                data = response.json()
                return self._extract_response(data)
            except json.JSONDecodeError:
                # Return raw text if not JSON
                return response.text

    async def health_check(self) -> bool:
        """Check if the endpoint is reachable."""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.options(self.endpoint)
                return response.status_code < 500
        except Exception:
            # Try a simple GET
            try:
                async with httpx.AsyncClient(timeout=10.0) as client:
                    response = await client.get(self.endpoint)
                    return response.status_code < 500
            except Exception:
                return False
