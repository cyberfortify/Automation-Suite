import tkinter as tk
from tkinter import ttk, messagebox
import threading
import json

from modules.email_automation.email_client import EmailClient
from modules.email_automation.template_manager import TemplateManager


class EmailTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        ttk.Label(self, text="Email Automation", style="Header.TLabel").pack(pady=10)

        ttk.Label(
            self,
            text="Send automated emails using templates and SMTP configuration.",
            justify="center"
        ).pack(pady=5)

        self.status = ttk.Label(self, text="Status: Idle")
        self.status.pack(pady=10)

        self.send_btn = ttk.Button(
            self,
            text="Send Test Email",
            command=self.send_email
        )
        self.send_btn.pack(pady=15)

    def send_email(self):
        self.send_btn.config(state="disabled")
        self.status.config(text="Status: Sending email...")
        threading.Thread(target=self._task).start()

    def _task(self):
        try:
            with open("config/email_config.json") as f:
                config = json.load(f)

            client = EmailClient(config["smtp"])
            templates = TemplateManager()

            body = templates.load("simple.txt")
            if not body:
                raise Exception("Email template not found")

            client.send_email(
                subject="Automation Suite – GUI Test Email",
                body=body,
                recipients=config["default_recipients"]
            )

            self.status.config(text="Status: Email sent successfully")
            messagebox.showinfo(
                "Success",
                "Test email sent successfully!"
            )

        except Exception as e:
            self.status.config(text="Status: Error")
            messagebox.showerror("Error", str(e))

        finally:
            self.send_btn.config(state="normal")
