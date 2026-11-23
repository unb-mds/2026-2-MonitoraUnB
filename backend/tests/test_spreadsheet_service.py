from io import BytesIO
from types import SimpleNamespace
from unittest.mock import MagicMock

from openpyxl import load_workbook

from backend.services import email_notifications, email_service
from backend.services.spreadsheet_service import generate_spreadsheet


def test_generate_spreadsheet_content():
    data = generate_spreadsheet(
        ["Nome", "Disciplina"],
        [["Ana", "Cálculo 1"], ["Bruno", "Física 1"]],
    )

    sheet = load_workbook(BytesIO(data)).active

    assert list(sheet.iter_rows(values_only=True)) == [
        ("Nome", "Disciplina"),
        ("Ana", "Cálculo 1"),
        ("Bruno", "Física 1"),
    ]


def test_generate_spreadsheet_without_rows():
    data = generate_spreadsheet(["Nome", "Disciplina"], [])

    sheet = load_workbook(BytesIO(data)).active

    assert list(sheet.iter_rows(values_only=True)) == [("Nome", "Disciplina")]


def test_spreadsheet_is_sent_as_attachment(monkeypatch):
    settings = SimpleNamespace(
        SMTP_USER="remetente@example.com",
        SMTP_PASSWORD="senha-de-teste",
        SMTP_FROM="remetente@example.com",
        SMTP_HOST="smtp.gmail.com",
        SMTP_PORT=587,
        SMTP_USE_TLS=True,
    )
    monkeypatch.setattr(email_service, "get_settings", lambda: settings)

    smtp_server = MagicMock()
    smtp_context = MagicMock()
    smtp_context.__enter__.return_value = smtp_server
    monkeypatch.setattr(
        email_service.smtplib, "SMTP", lambda *args, **kwargs: smtp_context
    )

    data = generate_spreadsheet(["Nome"], [["Ana"]])

    email_notifications.send_spreadsheet_to_committee(
        "presidente@example.com", data
    )

    message = smtp_server.send_message.call_args.args[0]
    attachments = list(message.iter_attachments())

    assert message["To"] == "presidente@example.com"
    assert len(attachments) == 1
    assert attachments[0].get_filename() == "monitoria.xlsx"
    assert attachments[0].get_content() == data

    sheet = load_workbook(BytesIO(attachments[0].get_content())).active
    assert list(sheet.iter_rows(values_only=True)) == [("Nome",), ("Ana",)]
