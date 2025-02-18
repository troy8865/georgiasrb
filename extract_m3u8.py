import os
import requests
import re

# Qaynaq linki
source_url = "https://rutube.ru/live/video/c58f502c7bb34a8fcdd976b221fca292/?category=1"

# Faylın yadda saxlanacağı qovluq
output_folder = "output"
os.makedirs(output_folder, exist_ok=True)

# m3u8 linklərini çıxar və fayla əlavə et
def extract_and_save_m3u8(url):
    try:
        # Səhifəni yüklə
        response = requests.get(url)
        response.raise_for_status()

        # HTML içindən m3u8 linklərini tapmaq üçün regex istifadə edirik
        m3u8_pattern = r"https://[^\s\"']+\.m3u8"
        matches = re.findall(m3u8_pattern, response.text)

        if matches:
            print(f"Tapılan m3u8 linkləri: {len(matches)}")
            
            # Fayl adını təyin et
            filename = os.path.join(output_folder, "m3u8_links.txt")
            
            # Fayla m3u8 linklərini əlavə et
            with open(filename, "w", encoding="utf-8") as file:
                for m3u8_url in matches:
                    file.write(m3u8_url + "\n")
                    print(f"Əlavə edildi: {m3u8_url}")
            
            print(f"M3u8 linkləri uğurla '{filename}' faylına yadda saxlandı.")
        else:
            print("M3u8 linki tapılmadı.")
    except Exception as e:
        print(f"Xəta baş verdi: {e}")

# Skriptin əsas hissəsi
if __name__ == "__main__":
    extract_and_save_m3u8(source_url)
