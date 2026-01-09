from datetime import datetime
from typing import Dict, Any
from fpdf import FPDF
import json
import os


# ==========================
# JSON REPORT
# ==========================

def build_json_report(analysis_result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Creates a structured compliance report (JSON)
    """
    report = {
        "report_metadata": {
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "engine": "Zero-Retention Code Change Simulator",
            "version": "1.0.0"
        },
        "summary": {
            "status": analysis_result.get("status"),
            "risk_level": analysis_result.get("risk_level", "LOW"),
            "violation_count": len(analysis_result.get("violations", []))
        },
        "details": analysis_result
    }

    return report


# ==========================
# PDF REPORT
# ==========================

def build_pdf_report(analysis_result: Dict[str, Any], output_path="compliance_report.pdf"):
    """
    Generates a PDF compliance report
    """
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Title
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Code Change Compliance Report", ln=True)

    pdf.ln(5)

    # Metadata
    pdf.set_font("Arial", size=11)
    pdf.cell(0, 8, f"Generated: {datetime.utcnow().isoformat()} UTC", ln=True)
    pdf.cell(0, 8, f"Status: {analysis_result.get('status')}", ln=True)
    pdf.cell(0, 8, f"Risk Level: {analysis_result.get('risk_level', 'LOW')}", ln=True)

    pdf.ln(5)

    # Violations
    violations = analysis_result.get("violations", [])

    if violations:
        pdf.set_font("Arial", "B", 13)
        pdf.cell(0, 10, "Violations", ln=True)

        pdf.set_font("Arial", size=11)
        for idx, v in enumerate(violations, start=1):
            pdf.multi_cell(0, 8, f"""
Violation #{idx}
Rule        : {v.get('rule')}
Change      : {v.get('change')}
Line        : {v.get('line')}
Reason      : {v.get('reason')}
""")
    else:
        pdf.cell(0, 10, "No violations detected.", ln=True)

    pdf.output(output_path)

    return output_path