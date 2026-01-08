import asyncio
from datetime import datetime
from uuid import uuid4
from typing import Literal

from engine.attacks import ALL_ATTACKS, Attack, AttackResult
from engine.connectors import OpenAIConnector, AnthropicConnector, CustomEndpointConnector, LLMConnector
from models.scan import ScanConfig, ScanResult, Finding


class ScanExecutor:
    """Executes security scans against LLM endpoints."""

    def __init__(self, config: ScanConfig):
        self.config = config
        self.connector = self._create_connector()
        self.results: list[tuple[Attack, AttackResult]] = []

    def _create_connector(self) -> LLMConnector:
        """Create the appropriate connector based on provider."""
        if self.config.provider == "custom":
            # Custom endpoint - user's own chatbot/LLM application
            return CustomEndpointConnector(
                endpoint=self.config.endpoint,
                api_key=self.config.api_key,
                request_format=self.config.request_format,
                response_path=self.config.response_path,
                headers=self.config.custom_headers,
            )
        elif self.config.provider == "openai":
            return OpenAIConnector(
                api_key=self.config.api_key or "",
                endpoint=self.config.endpoint if self.config.endpoint != "" else None,
                model=self.config.model,
            )
        elif self.config.provider == "anthropic":
            return AnthropicConnector(
                api_key=self.config.api_key or "",
                endpoint=self.config.endpoint if self.config.endpoint != "" else None,
                model=self.config.model,
            )
        else:
            raise ValueError(f"Unknown provider: {self.config.provider}")

    def _get_attacks(self) -> list[Attack]:
        """Filter attacks based on selected categories."""
        return [
            attack
            for attack in ALL_ATTACKS
            if attack.category in self.config.categories
        ]

    async def _execute_attack(self, attack: Attack) -> AttackResult:
        """Execute a single attack and return the result."""
        try:
            response = await self.connector.send_message(attack.prompt)
            return attack.analyze_response(response)
        except Exception as e:
            return AttackResult(
                success=False,
                response=f"Error: {str(e)}",
                severity=attack.severity,
                confidence=0.0,
                details=f"Attack execution failed: {str(e)}",
            )

    async def run(self) -> ScanResult:
        """Run all attacks and return the scan result."""
        started_at = datetime.utcnow()
        attacks = self._get_attacks()

        # Execute attacks with rate limiting
        delay = 60.0 / self.config.rate_limit  # seconds between requests

        for attack in attacks:
            result = await self._execute_attack(attack)
            self.results.append((attack, result))
            await asyncio.sleep(delay)

        completed_at = datetime.utcnow()

        # Calculate results
        findings = self._generate_findings()
        passed = sum(1 for _, r in self.results if not r.success)
        failed = sum(1 for _, r in self.results if r.success)
        total = len(self.results)

        # Calculate security score (0-100, higher is better)
        if total == 0:
            score = 100
        else:
            # Weight by severity
            severity_weights = {"critical": 4, "high": 3, "medium": 2, "low": 1}
            weighted_failures = sum(
                severity_weights.get(r.severity, 1)
                for _, r in self.results
                if r.success
            )
            max_weighted = sum(
                severity_weights.get(a.severity, 1)
                for a, _ in self.results
            )
            score = max(0, int(100 * (1 - weighted_failures / max_weighted)))

        return ScanResult(
            total_tests=total,
            passed=passed,
            failed=failed,
            score=score,
            findings=findings,
            started_at=started_at,
            completed_at=completed_at,
        )

    def _generate_findings(self) -> list[Finding]:
        """Generate finding objects from attack results."""
        findings = []

        for attack, result in self.results:
            if result.success:  # Only report successful attacks (vulnerabilities found)
                findings.append(
                    Finding(
                        id=str(uuid4()),
                        attack_name=attack.name,
                        attack_category=attack.category,
                        severity=attack.severity,
                        title=attack.description,
                        description=result.details,
                        prompt_used=attack.prompt,
                        response_received=result.response[:500],  # Truncate long responses
                        remediation=attack.remediation,
                    )
                )

        # Sort by severity
        severity_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        findings.sort(key=lambda f: severity_order.get(f.severity, 4))

        return findings
