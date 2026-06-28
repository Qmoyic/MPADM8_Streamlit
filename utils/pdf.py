from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle


def generate_classification_pdf(df):

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    elements = []

    elements.append(Paragraph("<b>Informe Liga Endesa</b>", styles["Title"]))
    elements.append(Spacer(1, 20))

    elements.append(
        Paragraph(
            "Clasificación actual de la Liga Endesa.",
            styles["BodyText"]
        )
    )

    elements.append(Spacer(1, 20))

    table_data = [list(df.columns)]

    for row in df.values.tolist():
        table_data.append(row)

    table = Table(table_data)

    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),

                ("BACKGROUND", (0, 1), (-1, -1), colors.beige),

                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),

                ("ALIGN", (0, 0), (-1, -1), "CENTER"),

                ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
            ]
        )
    )

    elements.append(table)

    doc.build(elements)

    buffer.seek(0)

    return buffer