from tkinter import ttk, messagebox
import threading

from workflow.engine import WorkflowEngine


class WorkflowTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        ttk.Label(self, text="Workflow Designer", style="Header.TLabel").pack(pady=10)

        ttk.Label(
            self,
            text="Run predefined automation workflows\n(file → scrape → email).",
            justify="center"
        ).pack(pady=5)

        self.status = ttk.Label(self, text="Status: Idle")
        self.status.pack(pady=10)

        ttk.Button(
            self,
            text="Run Daily Automation Workflow",
            command=self.run_workflow
        ).pack(pady=15)

    def run_workflow(self):
        self.status.config(text="Status: Running workflow...")
        threading.Thread(target=self._task).start()

    def _task(self):
        try:
            engine = WorkflowEngine()
            engine.run("daily_automation")
            self.status.config(text="Status: Workflow completed")
            messagebox.showinfo(
                "Success",
                "Workflow executed successfully!"
            )
        except Exception as e:
            self.status.config(text="Status: Error")
            messagebox.showerror("Error", str(e))
