import os
import re
import requests
import sys
from pathlib import Path

# 1. TƏYİNLƏMƏLƏR
SOURCE_URLS = ["https://www.teve2.com.tr/canli-yayin"]
OUTPUT_FOLDER = Path(__file__).parent / "output"
OUTPUT_FOLDER.mkdir(exist_ok=True, parents=True)  # Avtomatik qovluq yaradır

# 2. USER-Agent və HTTP HEADERS
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
}

def debug_print(message):
    """Xəta ayıklama üçün formatlı çıxış"""
    print(f"[DEBUG] {message}", file=sys.stderr)

def verify_folder_access():
    """Qovluq icazələrini yoxlayır"""
    test_file = OUTPUT_FOLDER / "access_test.txt"
    try:
        with open(test_file, 'w') as f:
            f.write("test")
        os.remove(test_file)
        return True
    except Exception as e:
        debug_print(f"Qovluq icazə xətası: {e}")
        return False

def extract_m3u8(url, index):
    try:
        debug_print(f"URL üçün emal başladı: {url}")
        
        # 1. HTML məzmununun alınması
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.raise_for_status()
        
        # 2. m3u8 linkinin tapılması (daha dəqiq regex)
        m3u8_urls = re.findall(
            r'https?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+\.m3u8(?:\?[^\s"\']+)?',
            response.text
        )
        
        if not m3u8_urls:
            raise ValueError("m3u8 linki tapılmadı")
        
        m3u8_url = m3u8_urls[0]
        debug_print(f"Tapılan m3u8 linki: {m3u8_url}")
        
        # 3. m3u8 faylının yüklənməsi
        m3u8_response = requests.get(m3u8_url, headers=HEADERS, timeout=15)
        m3u8_response.raise_for_status()
        
        # 4. Faylın yazılması
        filename = f"stream_{index}.m3u8"
        file_path = OUTPUT_FOLDER / filename
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(m3u8_response.text)
        
        # 5. Yazılan faylın yoxlanılması
        if not file_path.exists():
            raise IOError("Fayl yaradıla bilmədi")
        
        debug_print(f"Fayl uğurla yaradıldı: {file_path} (Ölçü: {file_path.stat().st_size} bayt)")
        return str(m3u8_url)
        
    except Exception as e:
        debug_print(f"Xəta: {type(e).__name__}: {str(e)}")
        return None

def main():
    # Qovluq icazələrini yoxlama
    if not verify_folder_access():
        print("Xəta: Qovluğa yazma icazəsi yoxdur!", file=sys.stderr)
        sys.exit(1)
    
    print(f"Çıxış qovluğu: {OUTPUT_FOLDER.absolute()}")
    
    # Hər bir URL üçün emal
    for idx, url in enumerate(SOURCE_URLS):
        print(f"\n{idx+1}. URL emal edilir: {url}")
        result = extract_m3u8(url, idx)
        
        if result:
            print(f"Uğur! m3u8 linki: {result}")
        else:
            print(f"Xəta: {url} emal edilə bilmədi", file=sys.stderr)
    
    # Əməliyyatın yekunlaşdırılması
    print("\nƏməliyyat başa çatdı. Fayllar:")
    for f in OUTPUT_FOLDER.glob("*.m3u8"):
        print(f"- {f.name} ({f.stat().st_size} bayt)")

if __name__ == "__main__":
    main()
