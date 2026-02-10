import psutil
import logging
import time

class SystemMonitor:
    def collect_metrics(self):
        return {
            "cpu_percent": psutil.cpu_percent(interval=1),
            "memory": {
                "percent": psutil.virtual_memory().percent
            },
            "disk": {
                "percent": psutil.disk_usage("/").percent
            }
        }

    def start_continuous(self, interval, callback):
        logging.info("System monitoring started (continuous mode)")
        while True:
            metrics = self.collect_metrics()
            callback(metrics)
            time.sleep(interval)
