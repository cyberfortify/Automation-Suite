import json
import logging

from modules.file_organizer.organizer import FileOrganizer
from modules.web_scraper.fetcher import Fetcher
from modules.web_scraper.scraper import WebScraper
from modules.web_scraper.exporter import Exporter
from modules.email_automation.email_client import EmailClient
from modules.email_automation.template_manager import TemplateManager


class WorkflowEngine:
    def __init__(self):
        self.workflows = self._load_workflows()

    def _load_workflows(self):
        with open("workflow/workflows.json") as f:
            return json.load(f)

    def run(self, name):
        if name not in self.workflows:
            logging.error(f"Workflow not found: {name}")
            return

        workflow = self.workflows[name]
        logging.info(f"Starting workflow: {name}")

        for step in workflow["steps"]:
            task = step["task"]

            try:
                if task == "file_organizer":
                    self._run_file_organizer()

                elif task == "web_scraper":
                    self._run_web_scraper()

                elif task == "send_email":
                    self._run_email(step.get("subject", "Workflow Report"))

                else:
                    logging.warning(f"Unknown task: {task}")

            except Exception as e:
                logging.error(f"Workflow failed at {task}: {e}")
                break

        logging.info(f"Workflow completed: {name}")

    # ---------- TASK IMPLEMENTATIONS ----------

    def _run_file_organizer(self):
        with open("config/config.json") as f:
            config = json.load(f)

        organizer = FileOrganizer(
            watch_folder=config["file_organizer"]["watch_folder"],
            organized_folder=config["file_organizer"]["organized_folder"]
        )
        organizer.organize()
        logging.info("Workflow: File organizer completed")

    def _run_web_scraper(self):
        with open("config/web_scraper.json") as f:
            config = json.load(f)

        fetcher = Fetcher(
            retries=config["retry_count"],
            delay=config["delay_seconds"]
        )
        scraper = WebScraper()
        exporter = Exporter("data")

        all_data = []
        for url in config["urls"]:
            html = fetcher.fetch(url)
            if html:
                data = scraper.extract(html, config["selector"])
                all_data.extend(data)

        exporter.to_csv("workflow_scraped_data.csv", all_data)
        logging.info("Workflow: Web scraper completed")

    def _run_email(self, subject):
        with open("config/email_config.json") as f:
            config = json.load(f)

        client = EmailClient(config["smtp"])
        templates = TemplateManager()

        body = templates.load("simple.txt", context={
            "name": "User",
            "module": "Workflow Engine",
            "status": "Completed",
            "date": "Today"
        })

        client.send_email(
            subject=subject,
            body=body,
            recipients=config["default_recipients"]
        )

        logging.info("Workflow: Email sent")
