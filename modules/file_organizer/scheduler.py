import schedule
import time
import logging

def run_daily(organizer, time_str="10:00"):
    schedule.every().day.at(time_str).do(organizer.organize)
    logging.info(f"File organizer scheduled daily at {time_str}")

    while True:
        schedule.run_pending()
        time.sleep(1)
