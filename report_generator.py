from fpdf import FPDF

def generate_pdf_report(score, data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="AttackMe Security Exposure Report", ln=True)
    pdf.cell(200, 10, txt=f"Exposure Score: {score}%", ln=True)

    pdf.multi_cell(0, 8, f"""
Entry Point: {data.get("entry_point")}
Recon: {data.get("recon_method")}
Exploitation: {data.get("exploitation_method")}
Privilege Escalation: {data.get("privilege_escalation")}
Impact: {data.get("impact")}
""")

    file_path = "report.pdf"
    pdf.output(file_path)
    return file_path