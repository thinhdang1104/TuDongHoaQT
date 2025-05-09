import time
import csv
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

def crawl_kenh14_congnghe():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    base_url = "https://kenh14.vn/cong-nghe.chn"
    driver.get(base_url)
    time.sleep(2)

    results = []
    visited_urls = set()

    while True:
        soup = BeautifulSoup(driver.page_source, "html.parser")
        articles = soup.select(".knswli-right h3 a")

        for a in articles:
            link = "https://kenh14.vn" + a["href"] if a["href"].startswith("/") else a["href"]
            if link in visited_urls:
                continue
            visited_urls.add(link)
            try:
                article = requests.get(link, timeout=10)
                article_soup = BeautifulSoup(article.content, "html.parser")
                title = article_soup.select_one("h1.kbwc-title").text.strip()
                description = article_soup.select_one("h2.kbwc-sapo")
                desc_text = description.text.strip() if description else ""
                image = article_soup.select_one(".VCSortableInPreviewMode img")
                img_url = image["src"] if image else ""
                content = "\n".join([p.text.strip() for p in article_soup.select(".knc-content p") if p.text.strip()])
                results.append([title, desc_text, img_url, content])
                print("Đã lấy:", title)
            except Exception as e:
                print("Lỗi:", e)

        next_btn = soup.select_one("a.pagination_next")
        if not next_btn or "href" not in next_btn.attrs:
            break
        next_url = "https://kenh14.vn" + next_btn["href"]
        driver.get(next_url)
        time.sleep(2)

    driver.quit()

    with open("kenh14_congnghe.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Tiêu đề", "Mô tả", "Ảnh", "Nội dung"])
        writer.writerows(results)

if __name__ == "__main__":
    crawl_kenh14_congnghe()
