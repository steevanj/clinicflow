# reports/exporters.py

import csv
from io import BytesIO
from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.platypus import Table


class CSVExporter:

    @staticmethod
    def export(filename, headers, data):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{filename}.csv"'

        writer = csv.writer(response)
        writer.writerow(headers)

        for row in data:
            writer.writerow(row)

        return response


class PDFExporter:

    @staticmethod
    def export(filename, headers, data):
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer)
        elements = []

        table_data = [headers] + list(data)
        table = Table(table_data)
        elements.append(table)

        doc.build(elements)

        pdf = buffer.getvalue()
        buffer.close()

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{filename}.pdf"'
        response.write(pdf)

        return response