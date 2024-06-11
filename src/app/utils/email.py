import requests
from core.config import settings


class Email:
    # Email variables configuration
    SENDER = settings.email.MAILGUN_SENDER
    DOMAIN = settings.email.MAILGUN_DOMAIN
    API_KEY = settings.email.MAILGUN_API_KEY

    @staticmethod
    def send_email(to: str, subject: str, text: str):
        response = requests.post(
            f"https://api.mailgun.net/v3/{Email.DOMAIN}/messages",
            auth=("api", Email.API_KEY),
            data={
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
