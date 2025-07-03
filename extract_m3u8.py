import os
import re
import requests
from urllib.parse import urljoin
import sys

# Qaynaq linkləri
source_urls = [
    "https://www.teve2.com.tr/canli-yayin",
]

# Faylın yadda saxlanacağı qovluq (tam yol ilə)
script_dir = os.path.dirname(os.path.abspath(__file__))
output_folder = os.path.join(script_dir, "output")

# Qovluğu yaratmaq üçün funksiya
def create_output_folder():
    try:
        os.makedirs(output_folder, exist_ok=True)
        print(f"Qovluq yaradıldı/yoxlanıldı: {output_folder}")
        
        # İcazə testi
        test_file = os.path.join(output_folder, "permission_test.txt")
        with open(test_file, "w") as f:
            f.write("test")
        os.remove(test_file)
        return True
    except Exception as e:
        print(f"Qovluq yaradıla/xidmət edilə bilmir: {e}")
        return False

def extract_m3u8(url, index):
    try:
        print(f"\n{url} üçün emal başladı...")
        
        # 1. Saytın HTML məzmununu əldə et
        response = requests.get(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }, timeout=10)
        response.raise_for_status()
        
        # 2. m3u8 linkini tap
        m3u8_matches = re.findall(r'(https?://[^\s"\']+\.m3u8(?:\?[^\s"\']*)?)', response.text)
        
        if not m3u8_matches:
            raise Exception("Xəta: m3u8 linki tapılmadı")
        
        m3u8_url = m3u8_matches[0]
        print(f"Tapılan m3u8 linki: {m3u8_url}")
        
        # 3. m3u8 faylını yüklə
        m3u8_response = requests.get(m3u8_url, headers=headers, timeout=10)
        m3u8_response.raise_for_status()
        
        # 4. Fayl adı və yolu
        filename = f"stream_{index}.m3u8"
        file_path = os.path.join(output_folder, filename)
        
        print(f"Fayl yola yazılır: {file_path}")
        
        # 5. Faylın tam məzmununu yaz
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(m3u8_response.text)
        
        # Yazıldığını yoxla
        if os.path.exists(file_path):
            print(f"Uğurla yadda saxlanıldı: {filename} (Ölçü: {os.path.getsize(file_path)} bayt)")
        else:
            raise Exception("Fayl yaradıla bilmədi!")
        
        return m3u8_url
        
    except Exception as e:
        print(f"Xəta baş verdi: {str(e)}", file=sys.stderr)
        return None

if __name__ == "__main__":
    if not create_output_folder():
        print("Xəta: Çıxış qovluğu problemli, skript dayandırılır...", file=sys.stderr)
        sys.exit(1)
    
    for index, url in enumerate(source_urls):
        if url:
            m3u8_url = extract_m3u8(url, index)
            if m3u8_url:
                print(f"Emal uğurla başa çatdı! Əsas m3u8 linki: {m3u8_url}")
            else:
                print(f"Xəta: {url} üçün emal uğursuz oldu", file=sys.stderr)
