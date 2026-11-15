from unittest.mock import MagicMock

import pytest

from backend.services import email_notifications


@pytest.fixture
def mock_send(monkeypatch):
    mock = MagicMock()
    monkeypatch.setattr(email_notifications, "send_email", mock)
    return mock


def test_registration_confirmation(mock_send):
    email_notifications.send_registration_confirmation(
        "ana@example.com", "Ana", "Cálculo 1"
    )

    mock_send.assert_called_once()
    recipient, subject, body = mock_send.call_args.args
    assert recipient == "ana@example.com"
    assert "Inscrição confirmada" in subject
    assert "Ana" in body
    assert "Cálculo 1" in body


def test_result_selected(mock_send):
    email_notifications.send_selection_result(
        "ana@example.com", "Ana", "Cálculo 1", selected=True
    )

    _, subject, body = mock_send.call_args.args
    assert "parabéns" in subject.lower()
    assert "selecionado" in body


def test_result_not_selected(mock_send):
    email_notifications.send_selection_result(
        "ana@example.com", "Ana", "Cálculo 1", selected=False
    )

    _, subject, body = mock_send.call_args.args
    assert "parabéns" not in subject.lower()
    assert "não foi dessa vez" in body.lower()
    assert "não se preocupe" in body.lower()


def test_spreadsheet_to_committee(mock_send):
    email_notifications.send_spreadsheet_to_committee(
        "presidente@example.com", b"conteudo-da-planilha"
    )

    mock_send.assert_called_once()
    assert mock_send.call_args.args[0] == "presidente@example.com"
    assert mock_send.call_args.kwargs["attachment"] == b"conteudo-da-planilha"
    assert mock_send.call_args.kwargs["attachment_name"] == "monitoria.xlsx"
