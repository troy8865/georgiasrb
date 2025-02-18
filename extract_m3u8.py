import os
import requests
import re

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

# m3u8 linkini qovluğa yadda saxla
def save_m3u8_to_file(m3u8_url, index):
    try:
        # Fayl adını index ilə fərqləndir
        filename = f"stream_{index}.m3u8"
        file_path = os.path.join(output_folder, filename)
        
        # Faylı yadda saxla
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(m3u8_url)
        print(f"m3u8 linki uğurla yadda saxlandı: {file_path}")
    except Exception as e:
        print(f"Xəta baş verdi: {e}")

# Skriptin əsas hissəsi
if __name__ == "__main__":
    # Qaynaqdan m3u8 linkini çıxar
    m3u8_url = extract_m3u8_from_rutube(source_url)
    
    if m3u8_url:
        # m3u8 linkini qovluğa yadda saxla
        save_m3u8_to_file(m3u8_url, 0)
