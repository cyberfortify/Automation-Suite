import tkinter as tk
from tkinter import ttk
from gui.styles import apply_theme

from gui.file_tab import FileTab
from gui.scraper_tab import ScraperTab
from gui.email_tab import EmailTab
from gui.monitor_tab import MonitorTab
from gui.workflow_tab import WorkflowTab


class AutomationApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Automation Suite Dashboard")
        self.geometry("900x550")
        self.resizable(False, False)

        apply_theme(self)

        header = ttk.Label(
            self,
            text="🤖 Comprehensive Automation Suite",
            style="Header.TLabel"
        )
        header.pack(pady=10)

        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        notebook.add(FileTab(notebook), text="📁 File Organizer")
        notebook.add(ScraperTab(notebook), text="🌐 Web Scraper")
        notebook.add(EmailTab(notebook), text="📧 Email Automation")
        notebook.add(MonitorTab(notebook), text="🖥️ System Monitor")
        notebook.add(WorkflowTab(notebook), text="🔁 Workflow")

