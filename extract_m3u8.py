import os
import re
import requests
from bs4 import BeautifulSoup

# Qaynaq linkləri
source_urls = [
    "https://www.teve2.com.tr/canli-yayin",
    # Buraya digər m3u8 linklərini əlavə edin
]

# Faylın yadda saxlanacağı qovluq
output_folder = "output"
os.makedirs(output_folder, exist_ok=True)

# User-Agent təyin etmək üçün
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def extract_m3u8(url, index):
    try:
        # Saytın HTML məzmununu əldə et
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        # JavaScript kodunda m3u8 linkini axtar
        soup = BeautifulSoup(response.text, 'html.parser')
        scripts = soup.find_all('script')
        
        m3u8_url = None
        for script in scripts:
            if script.string and 'm3u8' in script.string:
                # Linki tapmaq üçün regex istifadə et
                match = re.search(r'(https?://[^\s]+\.m3u8[^\s]*)', script.string)
                if match:
                    m3u8_url = match.group(1)
                    break
        
        if not m3u8_url:
            raise Exception("m3u8 linki tapılmadı")
        
        print(f"Tapılan m3u8 linki: {m3u8_url}")
        
        # m3u8 faylını yüklə
        m3u8_response = requests.get(m3u8_url, headers=headers)
        m3u8_response.raise_for_status()
        
        # Fayl adını index ilə fərqləndir
        filename = f"stream_{index}.m3u8"
        file_path = os.path.join(output_folder, filename)
        
        # Faylın məzmununu əldə et
        m3u8_content = m3u8_response.text.splitlines()
        
        # Əsas URL-ni təyin et (domain hissəsini saxlayırıq)
        base_url = '/'.join(m3u8_url.split('/')[:3])
        
        # Multi-variant m3u8 faylı üçün əsas strukturu yaradırıq
        modified_content = "#EXTM3U\n#EXT-X-VERSION:3\n"
        
        # İçindəki linkləri işləyib, onların önünə əsas URL əlavə edirik
        for line in m3u8_content:
            line = line.strip()
            if line and not line.startswith("#"):
                # Əgər link tam deyilsə, əsas URL əlavə et
                if not line.startswith('http'):
                    full_url = f"{base_url}{line if line.startswith('/') else '/' + line}"
                else:
                    full_url = line
                
                # Keyfiyyət parametrlərini əlavə et
                if '.ts' in line:
                    modified_content += f"{full_url}\n"
                else:
                    # Bu bir stream variantıdır
                    modified_content += f"#EXT-X-STREAM-INF:BANDWIDTH=2085600,RESOLUTION=1280x720\n{full_url}\n"
        
        # Faylı qovluğa yaz
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(modified_content)
        print(f"m3u8 faylı uğurla yeniləndi: {file_path}")
        
        return m3u8_url
        
    except Exception as e:
        print(f"Xəta baş verdi: {e}")
        return None

# Skriptin əsas hissəsi
if __name__ == "__main__":
    for index, url in enumerate(source_urls):
        if url:
            print(f"\n{url} üçün emal davam edir...")
            m3u8_url = extract_m3u8(url, index)
            if m3u8_url:
                print(f"Əsas m3u8 linki: {m3u8_url}")
