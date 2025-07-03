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

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def extract_m3u8(url, index):
    try:
        # Saytın HTML məzmununu əldə et
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        # JavaScript kodunda m3u8 linkini axtar (BeautifulSoup olmadan)
        matches = re.findall(r'(https?://[^\s]+\.m3u8[^\s]*)', response.text)
        
        if not matches:
            raise Exception("m3u8 linki tapılmadı")
        
        m3u8_url = matches[0]  # İlk uyğun gələn linki götürürük
        print(f"Tapılan m3u8 linki: {m3u8_url}")
        
        # m3u8 faylını yüklə
        m3u8_response = requests.get(m3u8_url, headers=headers)
        m3u8_response.raise_for_status()
        
        filename = f"stream_{index}.m3u8"
        file_path = os.path.join(output_folder, filename)
        
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(m3u8_response.text)
        print(f"m3u8 faylı uğurla yadda saxlandı: {file_path}")
        
        return m3u8_url
        
    except Exception as e:
        print(f"Xəta baş verdi: {e}")
        return None

if __name__ == "__main__":
    for index, url in enumerate(source_urls):
        if url:
            print(f"\n{url} üçün emal davam edir...")
            m3u8_url = extract_m3u8(url, index)
            if m3u8_url:
                print(f"Əsas m3u8 linki: {m3u8_url}")
