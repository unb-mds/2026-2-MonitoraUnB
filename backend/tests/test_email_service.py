
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from backend.services import email_service


def test_send_email_without_credentials(monkeypatch):
    settings = SimpleNamespace(
        SMTP_USER="",
        SMTP_PASSWORD="",
    )

    monkeypatch.setattr(
        email_service,
        "get_settings",
        lambda: settings,
    )

    with pytest.raises(
        ValueError,
        match="As credenciais SMTP não foram configuradas.",
    ):
        email_service.send_email(
            "destinatario@example.com",
            "Teste",
            "Mensagem de teste",
        )


def test_send_email_success(monkeypatch):
    settings = SimpleNamespace(
        SMTP_USER="remetente@example.com",
        SMTP_PASSWORD="senha-de-teste",
        SMTP_FROM="remetente@example.com",
        SMTP_HOST="smtp.gmail.com",
        SMTP_PORT=587,
        SMTP_USE_TLS=True,
    )

    monkeypatch.setattr(
        email_service,
        "get_settings",
        lambda: settings,
    )

    smtp_server = MagicMock()
    smtp_context = MagicMock()
    smtp_context.__enter__.return_value = smtp_server

    monkeypatch.setattr(
        email_service.smtplib,
        "SMTP",
        lambda *args, **kwargs: smtp_context,
    )

    email_service.send_email(
        "destinatario@example.com",
        "Teste SMTP",
        "Esta é uma mensagem de teste.",
    )

    smtp_server.starttls.assert_called_once()
    smtp_server.login.assert_called_once_with(
        "remetente@example.com",
        "senha-de-teste",
    )
    smtp_server.send_message.assert_called_once()

    message = smtp_server.send_message.call_args.args[0]
    assert message["To"] == "destinatario@example.com"
    assert message["Subject"] == "Teste SMTP"

