from tkinter import ttk
import threading

from modules.system_monitor.monitor import SystemMonitor


class MonitorTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        ttk.Label(self, text="System Monitor", style="Header.TLabel").pack(pady=10)

        ttk.Label(self, text="CPU Usage").pack()
        self.cpu_bar = ttk.Progressbar(self, length=300)
        self.cpu_bar.pack(pady=5)

        ttk.Label(self, text="Memory Usage").pack()
        self.mem_bar = ttk.Progressbar(self, length=300)
        self.mem_bar.pack(pady=5)

        ttk.Label(self, text="Disk Usage").pack()
        self.disk_bar = ttk.Progressbar(self, length=300)
        self.disk_bar.pack(pady=5)

        self.status = ttk.Label(self, text="Status: Idle")
        self.status.pack(pady=10)

        ttk.Button(
            self,
            text="Refresh Status",
            command=self.refresh
        ).pack(pady=10)

    def refresh(self):
        self.status.config(text="Status: Fetching metrics...")
        threading.Thread(target=self._task).start()

    def _task(self):
        monitor = SystemMonitor()
        metrics = monitor.collect_metrics()

        self.cpu_bar["value"] = metrics["cpu_percent"]
        self.mem_bar["value"] = metrics["memory"]["percent"]
        self.disk_bar["value"] = metrics["disk"]["percent"]

        self.status.config(text="Status: Updated")
