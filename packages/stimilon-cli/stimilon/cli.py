"""Stimilon CLI - LLM Security Scanner."""

import asyncio
import json
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.text import Text
from rich import box

from . import __version__
from .models import ScanConfig, ScanResult
from .engine import Scanner, ALL_ATTACKS

app = typer.Typer(
    name="stimilon",
    help="LLM Security Scanner - Find vulnerabilities in your AI applications",
    add_completion=False,
)
console = Console()


def version_callback(value: bool):
    if value:
        console.print(f"[bold blue]stimilon[/] version {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: bool = typer.Option(
        None, "--version", "-v", callback=version_callback, is_eager=True
    ),
):
    """Stimilon - LLM Security Scanner"""
    pass


@app.command()
def scan(
    endpoint: str = typer.Argument(..., help="Target endpoint URL"),
    api_key: Optional[str] = typer.Option(
        None, "--api-key", "-k", help="API key or Bearer token"
    ),
    format: str = typer.Option(
        "simple", "--format", "-f", help="Request format: simple, openai, anthropic"
    ),
    categories: str = typer.Option(
        "all",
        "--categories",
        "-c",
        help="Attack categories: injection, jailbreak, extraction, or 'all'",
    ),
    rate_limit: int = typer.Option(
        10, "--rate-limit", "-r", help="Requests per minute"
    ),
    output: Optional[str] = typer.Option(
        None, "--output", "-o", help="Output file (JSON)"
    ),
    quiet: bool = typer.Option(
        False, "--quiet", "-q", help="Quiet mode - only show results"
    ),
):
    """
    Scan an LLM endpoint for security vulnerabilities.

    Examples:

        stimilon scan https://api.example.com/chat

        stimilon scan https://api.openai.com/v1/chat/completions -k sk-xxx -f openai

        stimilon scan https://my-chatbot.com/api -c injection,jailbreak
    """
    # Parse categories
    if categories == "all":
        cat_list = ["injection", "jailbreak", "extraction"]
    else:
        cat_list = [c.strip() for c in categories.split(",")]

    # Validate format
    if format not in ["simple", "openai", "anthropic"]:
        console.print(f"[red]Invalid format: {format}[/]")
        raise typer.Exit(1)

    config = ScanConfig(
        endpoint=endpoint,
        api_key=api_key,
        request_format=format,  # type: ignore
        categories=cat_list,
        rate_limit=rate_limit,
    )

    if not quiet:
        _print_banner()
        _print_config(config)

    # Run scan
    result = asyncio.run(_run_scan(config, quiet))

    # Print results
    _print_results(result)

    # Save to file if requested
    if output:
        with open(output, "w") as f:
            json.dump(result.model_dump(), f, indent=2, default=str)
        console.print(f"\n[dim]Results saved to {output}[/]")

    # Exit with code 1 if vulnerabilities found
    if result.failed > 0:
        raise typer.Exit(1)


@app.command()
def list_attacks(
    category: Optional[str] = typer.Option(
        None, "--category", "-c", help="Filter by category"
    ),
):
    """List all available security tests."""
    _print_banner()

    table = Table(
        title="Available Security Tests",
        box=box.ROUNDED,
        header_style="bold cyan",
    )
    table.add_column("ID", style="dim")
    table.add_column("Name", style="bold")
    table.add_column("Category")
    table.add_column("Severity")

    severity_colors = {
        "critical": "red",
        "high": "orange1",
        "medium": "yellow",
        "low": "green",
    }

    for attack in ALL_ATTACKS:
        if category and attack.category != category:
            continue

        severity_color = severity_colors.get(attack.severity, "white")
        table.add_row(
            attack.name.split(":")[0],
            attack.description[:50] + "..." if len(attack.description) > 50 else attack.description,
            attack.category,
            f"[{severity_color}]{attack.severity.upper()}[/]",
        )

    console.print(table)
    console.print(f"\n[dim]Total: {len(ALL_ATTACKS)} tests[/]")


def _print_banner():
    """Print the CLI banner."""
    banner = """
 _____ _   _           _ _
/  ___| | (_)         (_) |
\\ `--.| |_ _ _ __ ___  _| | ___  _ __
 `--. \\ __| | '_ ` _ \\| | |/ _ \\| '_ \\
/\\__/ / |_| | | | | | | | | (_) | | | |
\\____/ \\__|_|_| |_| |_|_|_|\\___/|_| |_|
    """
    console.print(f"[bold blue]{banner}[/]")
    console.print("[dim]LLM Security Scanner[/]\n")


def _print_config(config: ScanConfig):
    """Print scan configuration."""
    console.print(Panel.fit(
        f"[bold]Target:[/] {config.endpoint}\n"
        f"[bold]Format:[/] {config.request_format}\n"
        f"[bold]Categories:[/] {', '.join(config.categories)}\n"
        f"[bold]Rate Limit:[/] {config.rate_limit} req/min",
        title="Scan Configuration",
        border_style="blue",
    ))
    console.print()


async def _run_scan(config: ScanConfig, quiet: bool) -> ScanResult:
    """Run the security scan with progress display."""
    if quiet:
        scanner = Scanner(config)
        return await scanner.run()

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("{task.completed}/{task.total}"),
        console=console,
    ) as progress:
        task = progress.add_task("Scanning...", total=100)

        def on_progress(current: int, total: int, name: str):
            progress.update(task, completed=current, total=total, description=f"[cyan]{name}[/]")

        scanner = Scanner(config, on_progress=on_progress)
        result = await scanner.run()

        progress.update(task, completed=100, description="[green]Complete![/]")

    return result


def _print_results(result: ScanResult):
    """Print scan results."""
    console.print()

    # Score panel
    score_color = "green" if result.score >= 80 else "yellow" if result.score >= 50 else "red"
    score_text = Text()
    score_text.append(f"\n{result.score}", style=f"bold {score_color}")
    score_text.append("/100\n", style="dim")

    console.print(Panel(
        score_text,
        title="Security Score",
        border_style=score_color,
        width=20,
    ))

    # Summary table
    summary = Table(box=box.SIMPLE, show_header=False)
    summary.add_column("Metric", style="bold")
    summary.add_column("Value")

    summary.add_row("Total Tests", str(result.total_tests))
    summary.add_row("Passed", f"[green]{result.passed}[/]")
    summary.add_row("Failed", f"[red]{result.failed}[/]" if result.failed > 0 else "0")
    summary.add_row("Duration", f"{result.duration_seconds:.1f}s")

    console.print(summary)

    # Findings
    if result.findings:
        console.print("\n[bold red]Vulnerabilities Found:[/]\n")

        for finding in result.findings:
            severity_colors = {
                "critical": "red",
                "high": "orange1",
                "medium": "yellow",
                "low": "green",
            }
            color = severity_colors.get(finding.severity, "white")

            console.print(Panel(
                f"[bold]{finding.title}[/]\n\n"
                f"[dim]Category:[/] {finding.category}\n"
                f"[dim]Details:[/] {finding.description}\n\n"
                f"[bold]Remediation:[/]\n{finding.remediation}",
                title=f"[{color}]{finding.severity.upper()}[/] {finding.attack_name}",
                border_style=color,
            ))
    else:
        console.print(Panel(
            "[bold green]No vulnerabilities found![/]\n\n"
            "Your endpoint passed all security tests.",
            title="All Clear",
            border_style="green",
        ))


if __name__ == "__main__":
    app()
