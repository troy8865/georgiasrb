import os
import requests
import re
from urllib.parse import urljoin

# Qaynaq linki
source_url = "https://rutube.ru/live/video/c58f502c7bb34a8fcdd976b221fca292/?category=1"

# Faylın yadda saxlanacağı qovluq
output_folder = "output"
os.makedirs(output_folder, exist_ok=True)

# Rutube-dan m3u8 linkini çıxar
def extract_m3u8_from_rutube(url):
    try:
        # İlk səhifəni yüklə
        response = requests.get(url)
        response.raise_for_status()

        # HTML içindən m3u8 linkini tapmaq üçün regex istifadə edirik
        m3u8_pattern = r"https://[^\s\"']+\.m3u8"
        matches = re.findall(m3u8_pattern, response.text)

        if matches:
            # Birinci uyğun gələn m3u8 linkini götürürük
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
        # m3u8 faylını yüklə
        response = requests.get(m3u8_url)
        response.raise_for_status()  # Xəta yoxlanışı
        
        # Fayl adını index ilə fərqləndir
        filename = f"stream_{index}.m3u8"
        file_path = os.path.join(output_folder, filename)
        
        # Mövcud faylı sil
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Mövcud fayl silindi: {file_path}")
        
        # Faylın məzmununu oxu
        m3u8_content = response.text.splitlines()
        
        # Debug: Qaynaq faylının məzmununu çap et
        print("Qaynaq faylının məzmunu:")
        print(m3u8_content)
        
        # Multi-variant m3u8 formatına uyğun olaraq yazırıq
        modified_content = "#EXTM3U\n#EXT-X-VERSION:3\n"
        
        for line in m3u8_content:
            if line.strip() and not line.startswith("#"):  # Tərkibdə "#" olmayan sətirləri seç
                full_url = urljoin(m3u8_url, line.strip())
                modified_content += f"#EXT-X-STREAM-INF:BANDWIDTH=2085600,RESOLUTION=1280x720\n{full_url}\n"
        
        # Faylı qovluğa yaz (üzərinə yaz)
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(modified_content)
        print(f"m3u8 faylı uğurla yadda saxlandı: {file_path}")
    except Exception as e:
        print(f"Xəta baş verdi: {e}")

# Skriptin əsas hissəsi
if __name__ == "__main__":
    # Qaynaqdan m3u8 linkini çıxar
    m3u8_url = extract_m3u8_from_rutube(source_url)
    
    if m3u8_url:
        # m3u8 faylını qovluğa yadda saxla
        save_m3u8_to_file(m3u8_url, 0)
