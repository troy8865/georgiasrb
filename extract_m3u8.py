import os
import re
import requests

# Qaynaq linkləri
source_urls = [
    "https://www.teve2.com.tr/canli-yayin",
    # Buraya digər m3u8 linklərini əlavə edin
]

# Faylın yadda saxlanacağı qovluq
output_folder = "output"
os.makedirs(output_folder, exist_ok=True)

# m3u8 faylını çıxar və qovluğa yadda saxla
def extract_m3u8(url, index):
    try:
        # HTML-i yüklə
        response = requests.get(url)
        response.raise_for_status()
        html = response.text

        # Tokenli m3u8 linkini tap
        match = re.search(r'https://[^"]+\.m3u8\?token=[^"]+', html)
        if not match:
            print("Tokenli m3u8 linki tapılmadı!")
            return

        token_url = match.group(0)

        # Tokeni ayrıca fayla yaz
        token_path = os.path.join(output_folder, "token.txt")
        with open(token_path, "w", encoding="utf-8") as f:
            f.write(token_url)
        print(f"Token linki saxlanıldı: {token_path}")

        # m3u8 faylını yüklə
        m3u8_response = requests.get(token_url)
        m3u8_response.raise_for_status()
        m3u8_lines = m3u8_response.text.splitlines()

        # Fayl adını təyin et
        filename = f"stream_{index}.m3u8"
        file_path = os.path.join(output_folder, filename)

        # Fayl məzmununu formatla
        modified_content = "#EXTM3U\n#EXT-X-VERSION:3\n"
        for line in m3u8_lines:
            if line.strip() and not line.startswith("#"):
                full_url = os.path.join(os.path.dirname(token_url), line.strip())
                modified_content += f"#EXT-X-STREAM-INF:BANDWIDTH=2085600,RESOLUTION=1280x720\n{full_url}\n"

        # Faylı yaz
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(modified_content)
        print(f"m3u8 faylı saxlanıldı: {file_path}")

    except Exception as e:
        print(f"Xəta baş verdi: {e}")

# Skriptin əsas hissəsi
if __name__ == "__main__":
    for index, url in enumerate(source_urls):
        if url:
            extract_m3u8(url, index)
