from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from io import BytesIO

router = APIRouter()


@router.get("/{scan_id}/pdf")
async def generate_pdf_report(scan_id: str):
    # Import here to avoid circular imports
    from routers.scans import scans

    if scan_id not in scans:
        raise HTTPException(status_code=404, detail="Scan not found")

    scan = scans[scan_id]

    if scan.status != "completed" or scan.result is None:
        raise HTTPException(status_code=400, detail="Scan not completed yet")

    # Generate PDF (placeholder - use reportlab or weasyprint in production)
    pdf_content = generate_pdf(scan)

    return StreamingResponse(
        BytesIO(pdf_content),
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=stimilon-report-{scan_id[:8]}.pdf"
        },
    )


def generate_pdf(scan) -> bytes:
    """Generate PDF report from scan results."""
    # Placeholder - implement with reportlab or weasyprint
    # For now, return a simple text representation
    content = f"""
STIMILON SECURITY SCAN REPORT
=============================

Scan ID: {scan.id}
Created: {scan.created_at}
Status: {scan.status}

SUMMARY
-------
Total Tests: {scan.result.total_tests if scan.result else 0}
Passed: {scan.result.passed if scan.result else 0}
Failed: {scan.result.failed if scan.result else 0}

Security Score: {scan.result.score if scan.result else 0}/100

FINDINGS
--------
"""

    if scan.result and scan.result.findings:
        for finding in scan.result.findings:
            content += f"""
[{finding.severity.upper()}] {finding.title}
Attack: {finding.attack_name}
Result: {finding.description}
Remediation: {finding.remediation}
---
"""

    return content.encode("utf-8")
