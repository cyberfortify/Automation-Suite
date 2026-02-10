import time
import logging

class AlertManager:
    def __init__(self, thresholds, cooldown):
        self.thresholds = thresholds
        self.cooldown = cooldown
        self.last_alert_time = {}

    def _can_alert(self, key):
        now = time.time()
        last_time = self.last_alert_time.get(key, 0)
        if now - last_time > self.cooldown:
            self.last_alert_time[key] = now
            return True
        return False

    def check(self, metrics):
        alerts = []

        if metrics["cpu_percent"] > self.thresholds["cpu"]:
            if self._can_alert("cpu"):
                alerts.append(f"CPU high: {metrics['cpu_percent']}%")

        if metrics["memory"]["percent"] > self.thresholds["memory"]:
            if self._can_alert("memory"):
                alerts.append(f"Memory high: {metrics['memory']['percent']}%")

        if metrics["disk"]["percent"] > self.thresholds["disk"]:
            if self._can_alert("disk"):
                alerts.append(f"Disk high: {metrics['disk']['percent']}%")

        for alert in alerts:
            logging.warning(alert)

        return alerts
