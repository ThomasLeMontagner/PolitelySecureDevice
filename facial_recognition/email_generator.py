"""Send notification emails for security events."""

from __future__ import annotations

import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import email_constants


class EmailClient:
    """Simple SMTP client for sending alerts."""

    def __init__(
        self,
        sender_email: str | None = None,
        sender_password: str | None = None,
        receiver_email: str | None = None,
    ) -> None:
        """Initialize email credentials from environment or overrides."""
        self.sender_email: str = sender_email or email_constants.SENDER_EMAIL
        self.sender_password: str = sender_password or email_constants.SENDER_PASSWORD
        self.receiver_email: str = receiver_email or email_constants.RECEIVER_EMAIL

    def send_email(self, subject: str, body: str) -> None:
        """Send an email with the provided subject and HTML body."""
        message = MIMEMultipart()
        message["From"] = self.sender_email
        message["To"] = self.receiver_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "html"))

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(self.sender_email, self.sender_password)
            server.sendmail(self.sender_email, self.receiver_email, message.as_string())

    def send_intrusion_email(self, picture: str, date: str) -> None:
        """Send a templated intrusion alert email."""
        subject = "Intrusion Detected!"
        body = f"An intrusion has been detected at {date}. Please check the snapshot: {picture}"
        self.send_email(subject, body)
