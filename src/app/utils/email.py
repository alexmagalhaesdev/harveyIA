import resend
from core.config import settings


class Email:
    # Email variables configuration
    SENDER = settings.email.EMAIL_SENDER
    resend.api_key = settings.email.EMAIL_API_KEY

    @staticmethod
    def send_email(to: str, subject: str, text: str):
        response = resend.Emails.send(
            {
                "from": Email.SENDER,
                "to": to,
                "subject": subject,
                "text": text,
            },
        )

        if response.status_code == 200:
            return {"message": "Email sent successfully"}
        else:
            return {"message": "Failed to send email"}
