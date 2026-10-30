
"""
Serviço responsável pelo envio de e-mails via SMTP.
"""

import smtplib
from email.message import EmailMessage

from backend.config import get_settings


def send_email(
    recipient: str,
    subject: str,
    body: str,
) -> None:
    """Envia um e-mail utilizando as configurações SMTP da aplicação."""

    settings = get_settings()

    if not settings.SMTP_USER or not settings.SMTP_PASSWORD:
        raise ValueError(
            "As credenciais SMTP não foram configuradas."
        )

    message = EmailMessage()
    message["From"] = settings.SMTP_FROM or settings.SMTP_USER
    message["To"] = recipient
    message["Subject"] = subject
    message.set_content(body)

    with smtplib.SMTP(
        settings.SMTP_HOST,
        settings.SMTP_PORT,
        timeout=10,
    ) as server:
        if settings.SMTP_USE_TLS:
            server.starttls()

        server.login(
            settings.SMTP_USER,
            settings.SMTP_PASSWORD,
        )

        server.send_message(message)

