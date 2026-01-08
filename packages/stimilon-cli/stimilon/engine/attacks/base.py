from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Literal

Severity = Literal["critical", "high", "medium", "low"]
Category = Literal["injection", "jailbreak", "extraction"]


@dataclass
class AttackResult:
    """Result of executing an attack."""

    success: bool  # True if attack succeeded (vulnerability found)
    response: str
    severity: Severity
    confidence: float  # 0.0 - 1.0
    details: str


class Attack(ABC):
    """Base class for all attack types."""

    name: str
    description: str
    category: Category
    severity: Severity
    remediation: str

    @property
    @abstractmethod
    def prompt(self) -> str:
        """The attack prompt to send to the target LLM."""
        pass

    @abstractmethod
    def analyze_response(self, response: str) -> AttackResult:
        """Analyze the LLM response to determine if the attack succeeded."""
        pass

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "severity": self.severity,
            "prompt": self.prompt,
            "remediation": self.remediation,
        }
