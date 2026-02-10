import smtplib
import logging
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders


class EmailClient:
    def __init__(self, smtp_config):
        self.server = smtp_config["server"]
        self.port = smtp_config["port"]
        self.email = smtp_config["sender_email"]
        self.password = smtp_config["sender_password"]

    def send_email(self, subject, body, recipients, html=False, attachments=None):
        try:
            msg = MIMEMultipart()
            msg["From"] = self.email
            msg["To"] = ", ".join(recipients)
            msg["Subject"] = subject

            msg.attach(MIMEText(body, "html" if html else "plain"))

            # 📎 Attachments
            if attachments:
                for file_path in attachments:
                    if not os.path.exists(file_path):
                        logging.warning(f"Attachment not found: {file_path}")
                        continue

                    with open(file_path, "rb") as f:
                        part = MIMEBase("application", "octet-stream")
                        part.set_payload(f.read())

                    encoders.encode_base64(part)
                    part.add_header(
                        "Content-Disposition",
                        f'attachment; filename="{os.path.basename(file_path)}"'
                    )
                    msg.attach(part)

            with smtplib.SMTP(self.server, self.port) as server:
                server.starttls()
                server.login(self.email, self.password)
                server.send_message(msg)

            logging.info("Email sent successfully")

        except Exception as e:
            logging.error(f"Email sending failed: {e}")
