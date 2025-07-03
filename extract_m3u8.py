import os
import re
import requests
from urllib.parse import urljoin

# Qaynaq linkləri
source_urls = [
    "https://www.teve2.com.tr/canli-yayin",
]

# Faylın yadda saxlanacağı qovluq
output_folder = "output"
os.makedirs(output_folder, exist_ok=True)  # Qovluq yoxdursa yaradır

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def extract_m3u8(url, index):
    try:
        print(f"\n{url} üçün emal başladı...")
        
        # 1. Saytın HTML məzmununu əldə et
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        # 2. m3u8 linkini tap (daha dəqiq regex)
        m3u8_matches = re.findall(r'(https?://[^\s"\']+\.m3u8(?:\?[^\s"\']*)?)', response.text)
        
        if not m3u8_matches:
            raise Exception("Xəta: m3u8 linki tapılmadı")
        
        m3u8_url = m3u8_matches[0]
        print(f"Tapılan m3u8 linki: {m3u8_url}")
        
        # 3. m3u8 faylını yüklə
        m3u8_response = requests.get(m3u8_url, headers=headers)
        m3u8_response.raise_for_status()
        
        # 4. Fayl adı və yolu
        filename = f"stream_{index}.m3u8"
        file_path = os.path.join(output_folder, filename)
        
        print(f"Fayl yola yazılır: {file_path}")
        
        # 5. Faylın tam məzmununu yaz (orijinal formatda saxlayaraq)
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(m3u8_response.text)
        
        print(f"Uğurla yadda saxlanıldı: {filename}")
        return m3u8_url
        
    except Exception as e:
        print(f"Xəta baş verdi: {str(e)}")
        return None

if __name__ == "__main__":
    for index, url in enumerate(source_urls):
        if url:
            m3u8_url = extract_m3u8(url, index)
            if m3u8_url:
                print(f"Emal uğurla başa çatdı! Əsas m3u8 linki: {m3u8_url}")
            else:
                print(f"Xəta: {url} üçün emal uğursuz oldu")
