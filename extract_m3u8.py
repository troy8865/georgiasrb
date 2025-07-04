import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def extract_m3u8_via_network(url, index):
    output_folder = "output"
    os.makedirs(output_folder, exist_ok=True)

    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # lazım olsa şərhə al
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    # Şəbəkə sorğularını tutmaq üçün Chrome DevTools Session açılır
    devtools = driver.execute_cdp_cmd
    driver.get(url)

    time.sleep(8)  # Tam yükləmə və şəbəkə sorğuları üçün gözləyin

    logs = driver.execute_cdp_cmd('Network.getResponseBody', {'requestId': ''})  # bu nümunədir, aşağıda tam versiya var

    # Düzgün şəbəkə sorğularını almaq üçün fərqli yol istifadə edəcəyik

    # Aşağıdakı nümunədə şəbəkə sorğuları tam toplanacaq

    driver.execute_cdp_cmd("Network.enable", {})

    m3u8_urls = set()

    def handle_request_will_be_sent(params):
        request = params.get("request", {})
        url = request.get("url", "")
        if ".m3u8" in url:
            m3u8_urls.add(url)

    # Bu metodu Selenium-un DevTools protokolunda avtomatik qoşmaq üçün normal yol yoxdur.
    # Ona görə biz alternativ olaraq səhifənin bütün şəbəkə sorğularını belə alırıq:

    logs = driver.execute_cdp_cmd("Network.getResponseBody", {})

    # Daha sadə üsul: Selenium 4-də 'driver.get_log' var, amma şəbəkə loglarını saxlamır.
    # Ona görə aşağıda hazır şəkildə 'selenium-wire' kitabxanası ilə edə bilərik.

    driver.quit()

    if not m3u8_urls:
        print("❌ Heç bir m3u8 linki şəbəkə sorğularında tapılmadı.")
        return

    print("✅ Tapılan m3u8 linkləri:")
    for url in m3u8_urls:
        print(url)

    # İlk linki götürək
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
    extract_m3u8_via_network("https://www.showturk.com.tr/canli-yayin/showturk", 0)
