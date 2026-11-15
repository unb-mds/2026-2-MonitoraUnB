from backend.services.email_notifications import send_registration_confirmation

send_registration_confirmation(
    "seu_email_pessoal@gmail.com", "Macedo", "Cálculo 1"
)
print("Enviado!")
