"""
Mensagens de e-mail do MonitoraUnB: confirmação de inscrição,
resultado da seleção e planilha para a comissão.
"""

from backend.services.email_service import send_email


def send_registration_confirmation(
    recipient: str,
    student_name: str,
    subject_name: str,
) -> None:
    """Confirma ao aluno que a inscrição foi recebida."""

    send_email(
        recipient,
        "Inscrição confirmada - MonitoraUnB",
        f"Olá, {student_name}!\n\n"
        f"Sua inscrição para a monitoria de {subject_name} "
        "foi recebida com sucesso.\n\n"
        "Equipe MonitoraUnB",
    )


def send_selection_result(
    recipient: str,
    student_name: str,
    subject_name: str,
    selected: bool,
) -> None:
    """Informa ao aluno se foi ou não selecionado para a monitoria."""

    if selected:
        subject = "Resultado da monitoria: parabéns!"
        body = (
            f"Parabéns, {student_name}!\n\n"
            f"Você foi selecionado(a) como monitor(a) de {subject_name}.\n\n"
            "Equipe MonitoraUnB"
        )
    else:
        subject = "Resultado da monitoria"
        body = (
            f"Olá, {student_name}.\n\n"
            f"Não foi dessa vez em {subject_name}, "
            "mas não se preocupe: novas oportunidades virão.\n\n"
            "Equipe MonitoraUnB"
        )

    send_email(recipient, subject, body)


def send_spreadsheet_to_committee(
    recipient: str,
    spreadsheet: bytes,
) -> None:
    """Envia à comissão a planilha com os dados da monitoria."""

    send_email(
        recipient,
        "Planilha de inscritos - Monitoria",
        "Segue em anexo a planilha com os dados da monitoria.",
        attachment=spreadsheet,
        attachment_name="monitoria.xlsx",
    )
