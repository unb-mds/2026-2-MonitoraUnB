import smtplib
import pytest

from backend.services import email_service
from types import SimpleNamespace
from unittest.mock import MagicMock



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
@pytest.fixture
def smtp_settings(monkeypatch):
    settings = SimpleNamespace(
        SMTP_USER="remetente@example.com",
        SMTP_PASSWORD="senha-de-teste",
        SMTP_FROM="remetente@example.com",
        SMTP_HOST="smtp.gmail.com",
        SMTP_PORT=587,
        SMTP_USE_TLS=True,
    )
    monkeypatch.setattr(email_service, "get_settings", lambda: settings)
    return settings


def test_send_email_connection_failure(monkeypatch, smtp_settings):
    def fake_smtp(*args, **kwargs):
        raise smtplib.SMTPConnectError(421, "Serviço indisponível")

    monkeypatch.setattr(email_service.smtplib, "SMTP", fake_smtp)

    with pytest.raises(smtplib.SMTPConnectError):
        email_service.send_email(
            "destinatario@example.com", "Teste", "Mensagem"
        )


def test_send_email_connection_timeout(monkeypatch, smtp_settings):
    def fake_smtp(*args, **kwargs):
        raise TimeoutError("Tempo de conexão esgotado")

    monkeypatch.setattr(email_service.smtplib, "SMTP", fake_smtp)

    with pytest.raises(TimeoutError):
        email_service.send_email(
            "destinatario@example.com", "Teste", "Mensagem"
        )


def test_send_email_authentication_failure(monkeypatch, smtp_settings):
    smtp_server = MagicMock()
    smtp_server.login.side_effect = smtplib.SMTPAuthenticationError(
        535, b"Credenciais invalidas"
    )
    smtp_context = MagicMock()
    smtp_context.__enter__.return_value = smtp_server

    monkeypatch.setattr(
        email_service.smtplib, "SMTP", lambda *args, **kwargs: smtp_context
    )

    with pytest.raises(smtplib.SMTPAuthenticationError):
        email_service.send_email(
            "destinatario@example.com", "Teste", "Mensagem"
        )

    smtp_server.send_message.assert_not_called()

