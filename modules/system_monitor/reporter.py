import json
import os
from datetime import datetime

class SystemReporter:
    def __init__(self, output_dir="reports"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def append_history(self, metrics):
        path = os.path.join(self.output_dir, "history.json")

        entry = {
            "timestamp": datetime.now().isoformat(),
            "metrics": metrics
        }

        history = []
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                history = json.load(f)

        history.append(entry)

        with open(path, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=4)
