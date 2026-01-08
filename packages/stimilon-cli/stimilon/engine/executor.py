"""Security scanner executor."""

from __future__ import annotations

import asyncio
from datetime import datetime
from uuid import uuid4
from typing import Callable, Optional, List, Tuple

from .attacks import ALL_ATTACKS, Attack, AttackResult
from .connectors import HTTPConnector
from ..models import ScanConfig, ScanResult, Finding


class Scanner:
    """Executes security scans against LLM endpoints."""

    def __init__(
        self,
        config: ScanConfig,
        on_progress: Optional[Callable[[int, int, str], None]] = None,
    ):
        self.config = config
        self.on_progress = on_progress
        self.connector = HTTPConnector(
            endpoint=config.endpoint,
            api_key=config.api_key,
            headers=config.headers,
            request_format=config.request_format,
            timeout=config.timeout,
        )
        self.results: List[Tuple[Attack, AttackResult]] = []

    def _get_attacks(self) -> List[Attack]:
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
                details=f"Attack failed: {str(e)}",
            )

    async def run(self) -> ScanResult:
        """Run all attacks and return the scan result."""
        started_at = datetime.utcnow()
        attacks = self._get_attacks()
        total = len(attacks)

        # Rate limiting delay
        delay = 60.0 / self.config.rate_limit

        for i, attack in enumerate(attacks):
            if self.on_progress:
                self.on_progress(i + 1, total, attack.name)

            result = await self._execute_attack(attack)
            self.results.append((attack, result))

            if i < total - 1:  # Don't wait after last attack
                await asyncio.sleep(delay)

        completed_at = datetime.utcnow()

        # Generate results
        findings = self._generate_findings()
        passed = sum(1 for _, r in self.results if not r.success)
        failed = sum(1 for _, r in self.results if r.success)

        # Calculate security score (0-100, higher is better)
        if total == 0:
            score = 100
        else:
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

        duration = (completed_at - started_at).total_seconds()

        return ScanResult(
            total_tests=total,
            passed=passed,
            failed=failed,
            score=score,
            findings=findings,
            started_at=started_at,
            completed_at=completed_at,
            duration_seconds=duration,
        )

    def _generate_findings(self) -> List[Finding]:
        """Generate finding objects from attack results."""
        findings = []

        for attack, result in self.results:
            if result.success:
                findings.append(
                    Finding(
                        id=str(uuid4()),
                        attack_name=attack.name,
                        category=attack.category,
                        severity=attack.severity,
                        title=attack.description,
                        description=result.details,
                        prompt_used=attack.prompt,
                        response_received=result.response[:500],
                        remediation=attack.remediation,
                    )
                )

        # Sort by severity
        severity_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        findings.sort(key=lambda f: severity_order.get(f.severity, 4))

        return findings
