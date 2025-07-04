import os
import re
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Qovluq yaradılır
output_folder = "output"
os.makedirs(output_folder, exist_ok=True)

def extract_m3u8_with_selenium(url, index):
    try:
        # Chrome parametrləri
        chrome_options = Options()
        # chrome_options.add_argument("--headless")  # Headless deaktivdir
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")

        # Chrome WebDriver başlat
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        driver.get(url)

        time.sleep(5)  # JavaScript yüklənməsi üçün gözləyirik

        page_source = driver.page_source
        driver.quit()

        # Tokenli m3u8 linkini tap
        match = re.search(r'https://[^"]+\.m3u8\?token=[^"]+', page_source)
        if not match:
            print("❌ Tokenli .m3u8 link tapılmadı.")
            debug_path = os.path.join(output_folder, f"debug_{index}.html")
            with open(debug_path, "w", encoding="utf-8") as f:
                f.write(page_source)
            print(f"🔍 HTML saxlandı: {debug_path}")
            return

        token_url = match.group(0)

        # Tokeni fayla yaz
        token_path = os.path.join(output_folder, "token.txt")
        with open(token_path, "w", encoding="utf-8") as f:
            f.write(token_url)
        print(f"✅ Token linki saxlanıldı: {token_path}")

        # m3u8 faylını yüklə
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        m3u8_response = requests.get(token_url, headers=headers)
        m3u8_response.raise_for_status()
        m3u8_lines = m3u8_response.text.splitlines()

        # Fayl adı və məzmun
        filename = f"stream_{index}.m3u8"
        file_path = os.path.join(output_folder, filename)
        modified_content = "#EXTM3U\n#EXT-X-VERSION:3\n"

        for line in m3u8_lines:
            if line.strip() and not line.startswith("#"):
                full_url = os.path.join(os.path.dirname(token_url), line.strip())
                modified_content += f"#EXT-X-STREAM-INF:BANDWIDTH=2085600,RESOLUTION=1280x720\n{full_url}\n"

        # Faylı yaz
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(modified_content)
        print(f"✅ m3u8 faylı saxlanıldı: {file_path}")

    except Exception as e:
        print(f"❌ Xəta baş verdi: {e}")

# Əsas hissə
if __name__ == "__main__":
    source_urls = ["https://www.teve2.com.tr/canli-yayin"]
    for index, url in enumerate(source_urls):
        if url:
            extract_m3u8_with_selenium(url, index)
