import schedule
import time
from main import crawl_kenh14_congnghe

schedule.every().day.at("06:00").do(crawl_kenh14_congnghe)

while True:
    schedule.run_pending()
    time.sleep(60)
