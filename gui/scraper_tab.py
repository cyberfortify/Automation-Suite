import tkinter as tk
from tkinter import ttk, messagebox
import threading
import json

from modules.web_scraper.fetcher import Fetcher
from modules.web_scraper.scraper import WebScraper
from modules.web_scraper.exporter import Exporter


class ScraperTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        ttk.Label(self, text="Web Scraper", style="Header.TLabel").pack(pady=10)

        ttk.Label(
            self,
            text="Extract data from websites using configurable selectors\nand export results to CSV / JSON.",
            justify="center"
        ).pack(pady=5)

        self.status = ttk.Label(self, text="Status: Idle")
        self.status.pack(pady=10)

        self.run_btn = ttk.Button(
            self,
            text="Run Web Scraper",
            command=self.run_scraper
        )
        self.run_btn.pack(pady=15)

    def run_scraper(self):
        self.run_btn.config(state="disabled")
        self.status.config(text="Status: Scraping...")
        threading.Thread(target=self._task).start()

    def _task(self):
        try:
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

            if all_data:
                exporter.to_csv("gui_scraped_data.csv", all_data)
                exporter.to_json("gui_scraped_data.json", all_data)
                self.status.config(
                    text=f"Status: Completed ({len(all_data)} items)"
                )
                messagebox.showinfo(
                    "Success",
                    f"Scraping completed.\nItems scraped: {len(all_data)}"
                )
            else:
                self.status.config(text="Status: No data found")
                messagebox.showwarning(
                    "Warning",
                    "No data was extracted from the websites."
                )

        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.status.config(text="Status: Error")

        finally:
            self.run_btn.config(state="normal")
