import csv
import json
import logging
import os

class Exporter:
    def __init__(self, output_dir="data"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def to_csv(self, filename, data):
        path = os.path.join(self.output_dir, filename)
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Data"])
            for item in data:
                writer.writerow([item])

        logging.info(f"Data exported to CSV: {path}")

    def to_json(self, filename, data):
        path = os.path.join(self.output_dir, filename)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

        logging.info(f"Data exported to JSON: {path}")
