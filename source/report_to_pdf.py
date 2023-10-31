from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def create_pdf(data, pdf_filename):
    c = canvas.Canvas(pdf_filename, pagesize=letter)
    c.setFont("Helvetica", 14)

    c.drawString(100, 750, "Profit and Loss Report")

    y = 700
    for key, value in data.items():
        text = f"{key}: {value}"
        c.drawString(100, y, text)
        y -= 20

    c.save()
