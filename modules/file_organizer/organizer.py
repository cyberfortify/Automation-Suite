import os
import shutil
import logging
from datetime import datetime

class FileOrganizer:
    def __init__(self, watch_folder, organized_folder):
        self.watch_folder = watch_folder
        self.organized_folder = organized_folder

        self.file_categories = {
            "Documents": [".pdf", ".doc", ".docx", ".txt", ".xlsx", ".pptx"],
            "Images": [".jpg", ".jpeg", ".png", ".gif", ".svg"],
            "Videos": [".mp4", ".avi", ".mov", ".mkv"],
            "Music": [".mp3", ".wav", ".aac"],
            "Archives": [".zip", ".rar", ".7z"],
            "Code": [".py", ".js", ".html", ".css", ".java"]
        }

        self._create_base_folders()

    def _create_base_folders(self):
        os.makedirs(self.organized_folder, exist_ok=True)

        for category in self.file_categories.keys():
            os.makedirs(
                os.path.join(self.organized_folder, category),
                exist_ok=True
            )

        os.makedirs(
            os.path.join(self.organized_folder, "Others"),
            exist_ok=True
        )

        logging.info("Folder structure verified")

    def _get_category(self, extension):
        for category, extensions in self.file_categories.items():
            if extension in extensions:
                return category
        return "Others"

    def _handle_duplicate(self, dest_path):
        if not os.path.exists(dest_path):
            return dest_path

        base, ext = os.path.splitext(dest_path)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{base}_{timestamp}{ext}"

    def organize(self):
        if not os.path.exists(self.watch_folder):
            logging.error(f" Watch folder not found: {self.watch_folder}")
            return

        files_moved = 0

        for filename in os.listdir(self.watch_folder):
            source_path = os.path.join(self.watch_folder, filename)

            if not os.path.isfile(source_path):
                continue

            extension = os.path.splitext(filename)[1].lower()
            category = self._get_category(extension)

            dest_dir = os.path.join(self.organized_folder, category)
            dest_path = os.path.join(dest_dir, filename)
            dest_path = self._handle_duplicate(dest_path)

            shutil.move(source_path, dest_path)
            files_moved += 1

            logging.info(f" Moved: {filename} → {category}")

        logging.info(f"🎯 Total files organized: {files_moved}")
