import logging
from bs4 import BeautifulSoup

class WebScraper:
    def extract(self, html, selector):
        soup = BeautifulSoup(html, "html.parser")

        elements = soup.select(selector)
        data = [el.get_text(strip=True) for el in elements]

        logging.info(f"Extracted {len(data)} items")
        return data
