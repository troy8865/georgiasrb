import os
import time
import requests
from seleniumwire import webdriver  # selenium-wire istifadə olunur
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def extract_m3u8_with_selenium_wire(url, index):
    output_folder = "output"
    os.makedirs(output_folder, exist_ok=True)

    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # istəsən şərhə ala bilərsən
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    driver.get(url)
    time.sleep(10)  # Tam yükləmə üçün vaxt ver

    m3u8_urls = set()

    # Bütün şəbəkə sorğularını yoxlayırıq
    for request in driver.requests:
        if request.response:
            if ".m3u8" in request.url:
                m3u8_urls.add(request.url)

    driver.quit()

    if not m3u8_urls:
        print("❌ Heç bir m3u8 linki tapılmadı.")
        return

    print("✅ Tapılan m3u8 linkləri:")
    for link in m3u8_urls:
        print(link)

    # İlk tapılan linki götürək
    token_url = list(m3u8_urls)[0]

    token_path = os.path.join(output_folder, "token.txt")
    with open(token_path, "w", encoding="utf-8") as f:
        f.write(token_url)
    print(f"✅ Token faylı yazıldı: {token_path}")

    headers = {"User-Agent": "Mozilla/5.0"}
    m3u8_response = requests.get(token_url, headers=headers)
    m3u8_response.raise_for_status()
    m3u8_lines = m3u8_response.text.splitlines()

    filename = f"stream_{index}.m3u8"
    file_path = os.path.join(output_folder, filename)

    modified_content = "#EXTM3U\n#EXT-X-VERSION:3\n"
    for line in m3u8_lines:
        if line.strip() and not line.startswith("#"):
            full_url = os.path.join(os.path.dirname(token_url), line.strip())
            modified_content += f"#EXT-X-STREAM-INF:BANDWIDTH=2085600,RESOLUTION=1280x720\n{full_url}\n"

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(modified_content)
    print(f"✅ m3u8 faylı saxlanıldı: {file_path}")

if __name__ == "__main__":
    extract_m3u8_with_selenium_wire("https://www.teve2.com.tr/canli-yayin", 0)
