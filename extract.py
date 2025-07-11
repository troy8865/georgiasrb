from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import re
import os

# Kanal siyahısı (id = fayl adı olacaq)
kanallar = {
    "showtv": "https://www.showtv.com.tr/canli-yayin",
    "nowtv": "https://www.nowtv.com.tr/canli-yayin"
}

# Headless Chrome browser qur
options = Options()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.binary_location = "/usr/bin/google-chrome"
options.add_argument("--user-agent=Mozilla/5.0 (Linux; Android 10) Chrome/115.0 Mobile Safari/537.36")

driver = webdriver.Chrome(options=options)

os.makedirs("stream", exist_ok=True)

for ad, url in kanallar.items():
    try:
        driver.get(url)
        time.sleep(5)
        source = driver.page_source

        # ercdn.net linkləri axtarılır (480p)
        match = re.search(r'https://.*?nowtv.*?\.m3u8\?[^\'"\\\s]+', source)
        if match:
            m3u8_link = match.group(0)
            print(f"[✅] {ad} tapıldı:", m3u8_link)

            # Fayl yazılır
            fayl_yolu = f"stream/{ad}.m3u8"
            with open(fayl_yolu, "w") as f:
                f.write("#EXTM3U\n")
                f.write("#EXT-X-VERSION:3\n")
                f.write("#EXT-X-STREAM-INF:BANDWIDTH=800000,RESOLUTION=854x480\n")
                f.write(m3u8_link + "\n")
        else:
            print(f"[❌] {ad} üçün link tapılmadı.")
    except Exception as e:
        print(f"[🔥] {ad} üçün xəta: {e}")

driver.quit()
