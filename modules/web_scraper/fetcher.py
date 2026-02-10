import requests
import logging
import time
from fake_useragent import UserAgent

class Fetcher:
    def __init__(self, timeout=10, retries=3, delay=2):
        self.timeout = timeout
        self.retries = retries
        self.delay = delay
        self.ua = UserAgent()

    def get_headers(self):
        return {
            "User-Agent": self.ua.random,
            "Accept-Language": "en-US,en;q=0.9"
        }

    def fetch(self, url):
        for attempt in range(1, self.retries + 1):
            try:
                response = requests.get(
                    url,
                    headers=self.get_headers(),
                    timeout=self.timeout
                )
                response.raise_for_status()
                logging.info(f"Fetched: {url}")
                return response.text

            except requests.exceptions.RequestException as e:
                logging.warning(
                    f"Attempt {attempt}/{self.retries} failed for {url}"
                )
                time.sleep(self.delay)

        logging.error(f"Failed after retries: {url}")
        return None
