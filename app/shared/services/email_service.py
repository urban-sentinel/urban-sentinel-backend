import os
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from dotenv import load_dotenv

load_dotenv()

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
SMTP_FROM_NAME = os.getenv("SMTP_FROM_NAME", "Urban Sentinel App")

print("SMTP_USER (al iniciar):", repr(SMTP_USER))
print("SMTP_PASSWORD (al iniciar, oculto):", "***" if SMTP_PASSWORD else None)
def send_email(to_email: str, subject: str, html_body: str):
    if not SMTP_USER or not SMTP_PASSWORD:
        raise RuntimeError("SMTP_USER o SMTP_PASSWORD no configurados")

    # Construir mensaje
    msg = MIMEText(html_body, "html", "utf-8")
    msg["Subject"] = subject
    msg["From"] = formataddr((SMTP_FROM_NAME, SMTP_USER))
    msg["To"] = to_email

    # Enviar por SMTP (Gmail)
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()  # TLS
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(msg)
