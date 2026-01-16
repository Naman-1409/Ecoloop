import os
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr
from typing import List
from dotenv import load_dotenv

load_dotenv()

class EmailService:
    def __init__(self):
        self.conf = ConnectionConfig(
            MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
            MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
            MAIL_FROM=os.getenv("MAIL_FROM"),
            MAIL_PORT=int(os.getenv("MAIL_PORT", 587)),
            MAIL_SERVER=os.getenv("MAIL_SERVER"),
            MAIL_STARTTLS=True,
            MAIL_SSL_TLS=False,
            USE_CREDENTIALS=True,
            VALIDATE_CERTS=True
        )

    async def send_contact_email(self, subject: str, recipient: EmailStr, body: str):
        message = MessageSchema(
            subject=subject,
            recipients=[recipient],
            body=body,
            subtype=MessageType.html
        )
        
        fm = FastMail(self.conf)
        await fm.send_message(message)
