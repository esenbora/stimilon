from abc import ABC, abstractmethod


class LLMConnector(ABC):
    """Base class for LLM API connectors."""

    def __init__(self, api_key: str, endpoint: str | None = None, model: str | None = None):
        self.api_key = api_key
        self.endpoint = endpoint
        self.model = model

    @abstractmethod
    async def send_message(self, message: str) -> str:
        """
        Send a message to the LLM and return the response.

        Args:
            message: The user message to send

        Returns:
            The LLM's response text
        """
        pass

    @abstractmethod
    async def health_check(self) -> bool:
        """
        Check if the API is reachable and credentials are valid.

        Returns:
            True if healthy, False otherwise
        """
        pass
