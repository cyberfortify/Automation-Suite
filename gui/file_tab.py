import json
import threading
from tkinter import ttk, messagebox

from modules.file_organizer.organizer import FileOrganizer
from modules.file_organizer.watcher import FolderWatcher


class FileTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        ttk.Label(self, text="File Organizer", style="Header.TLabel").pack(pady=10)

        ttk.Label(
            self,
            text="Organize files automatically or watch a folder in real-time.",
            justify="center"
        ).pack(pady=5)

        self.status = ttk.Label(self, text="Status: Idle")
        self.status.pack(pady=10)

        self.run_btn = ttk.Button(
            self,
            text="Run Once",
            command=self.run_once
        )
        self.run_btn.pack(pady=5)

        self.start_watch_btn = ttk.Button(
            self,
            text="Start Watch Folder",
            command=self.start_watch
        )
        self.start_watch_btn.pack(pady=5)

        self.stop_watch_btn = ttk.Button(
            self,
            text="Stop Watch Folder",
            state="disabled",
            command=self.stop_watch
        )
        self.stop_watch_btn.pack(pady=5)

        self.watcher = None

    # -------- Run once --------
    def run_once(self):
        self.status.config(text="Status: Running once...")
        threading.Thread(target=self._run_once_task).start()

    def _run_once_task(self):
        try:
            organizer = self._create_organizer()
            organizer.organize()
            self.status.config(text="Status: Completed (single run)")
            messagebox.showinfo("Success", "Files organized successfully!")
        except Exception as e:
            self.status.config(text="Status: Error")
            messagebox.showerror("Error", str(e))

    # -------- Watch mode --------
    def start_watch(self):
        if self.watcher:
            return

        organizer = self._create_organizer()
        self.watcher = FolderWatcher(
            path=organizer.watch_folder,
            organizer=organizer
        )

        self.status.config(text="Status: Watching folder...")
        self.start_watch_btn.config(state="disabled")
        self.stop_watch_btn.config(state="normal")

        threading.Thread(target=self.watcher.start, daemon=True).start()

    def stop_watch(self):
        if self.watcher:
            self.watcher.stop()
            self.watcher = None

        self.status.config(text="Status: Watch stopped")
        self.start_watch_btn.config(state="normal")
        self.stop_watch_btn.config(state="disabled")

    # -------- Helper --------
    def _create_organizer(self):
        with open("config/config.json") as f:
            config = json.load(f)

        return FileOrganizer(
            watch_folder=config["file_organizer"]["watch_folder"],
            organized_folder=config["file_organizer"]["organized_folder"]
        )
