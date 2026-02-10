import schedule
import time
import logging


class EmailScheduler:
    def __init__(self, email_client, template_manager, recipients):
        self.email_client = email_client
        self.template_manager = template_manager
        self.recipients = recipients

    def send_scheduled_email(self, subject, template_name, html=False):
        body = self.template_manager.load(template_name)
        if body is None:
            logging.error("Email body is empty. Skipping send.")
            return

        self.email_client.send_email(
            subject=subject,
            body=body,
            recipients=self.recipients,
            html=html
        )

    def daily(self, time_str, subject, template_name, html=False):
        schedule.every().day.at(time_str).do(
            self.send_scheduled_email,
            subject=subject,
            template_name=template_name,
            html=html
        )
        logging.info(f"Daily email scheduled at {time_str}")

    def weekly(self, day, time_str, subject, template_name, html=False):
        getattr(schedule.every(), day).at(time_str).do(
            self.send_scheduled_email,
            subject=subject,
            template_name=template_name,
            html=html
        )
        logging.info(f"Weekly email scheduled on {day} at {time_str}")

    def start(self):
        logging.info("Email scheduler started")
        while True:
            schedule.run_pending()
            time.sleep(1)
