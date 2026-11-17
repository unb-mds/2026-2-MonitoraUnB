"""
Geração de planilhas (.xlsx) do MonitoraUnB.
"""

from io import BytesIO

from openpyxl import Workbook


def generate_spreadsheet(
    headers: list[str],
    rows: list[list],
    sheet_title: str = "Monitoria",
) -> bytes:
    """Gera uma planilha .xlsx em memória e devolve o conteúdo em bytes."""

    workbook = Workbook()
    sheet = workbook.active
    sheet.title = sheet_title

    sheet.append(headers)
    for row in rows:
        sheet.append(row)

    buffer = BytesIO()
    workbook.save(buffer)
    return buffer.getvalue()
