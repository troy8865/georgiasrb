import os
import requests
import re
from urllib.parse import urljoin

# Qaynaq linki
source_url = "https://rutube.ru/live/video/c58f502c7bb34a8fcdd976b221fca292/?category=1"

# Faylın yadda saxlanacağı qovluq
output_folder = "output"
os.makedirs(output_folder, exist_ok=True)

# Token almaq üçün API endpoint-i
token_url = "https://api.rutube.ru/get_token"

# Token almaq üçün funksiya
def get_token():
    try:
        response = requests.get(token_url)
        response.raise_for_status()
        token = response.json().get("token")
        if token:
            print(f"Token uğurla alındı: {token}")
            return token
        else:
            print("Token alına bilmədi.")
            return None
    except Exception as e:
        print(f"Xəta baş verdi: {e}")
        return None

# Rutube-dan m3u8 linkini çıxar
def extract_m3u8_from_rutube(url, token):
    try:
        headers = {
            "Authorization": f"Bearer {token}",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        # HTML içindən m3u8 linkini tapmaq üçün regex istifadə edirik
        m3u8_pattern = r"https://[^\s\"']+\.m3u8"
        matches = re.findall(m3u8_pattern, response.text)

        if matches:
            m3u8_url = matches[0]
            print(f"Tapılan m3u8 linki: {m3u8_url}")
            return m3u8_url
        else:
            print("M3U8 linki tapılmadı.")
            return None
    except Exception as e:
        print(f"Xəta baş verdi: {e}")
        return None

# m3u8 faylını çıxar və qovluğa yadda saxla
def save_m3u8_to_file(m3u8_url, index):
    try:
        response = requests.get(m3u8_url)
        response.raise_for_status()
        
        filename = f"stream_{index}.m3u8"
        file_path = os.path.join(output_folder, filename)
        
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Mövcud fayl silindi: {file_path}")
        
        m3u8_content = response.text.splitlines()
        modified_content = "#EXTM3U\n#EXT-X-VERSION:3\n"
        
        for line in m3u8_content:
            if line.strip() and not line.startswith("#"):
                full_url = urljoin(m3u8_url, line.strip())
                modified_content += f"#EXT-X-STREAM-INF:BANDWIDTH=2085600,RESOLUTION=1280x720\n{full_url}\n"
        
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(modified_content)
        print(f"m3u8 faylı uğurla yadda saxlandı: {file_path}")
    except Exception as e:
        print(f"Xəta baş verdi: {e}")

# Skriptin əsas hissəsi
if __name__ == "__main__":
    # Token almaq
    token = get_token()
    
    if token:
        # Qaynaqdan m3u8 linkini çıxar
        m3u8_url = extract_m3u8_from_rutube(source_url, token)
        
        if m3u8_url:
            # m3u8 faylını qovluğa yadda saxla
            save_m3u8_to_file(m3u8_url, 0)
