import os
import logging

class TemplateManager:
    def __init__(self, template_dir="templates/email"):
        self.template_dir = template_dir

    def load(self, filename, context=None):
        path = os.path.join(self.template_dir, filename)

        if not os.path.exists(path):
            logging.error(f"Template not found: {filename}")
            return None

        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        if context:
            for key, value in context.items():
                content = content.replace(f"{{{{{key}}}}}", str(value))

        return content
