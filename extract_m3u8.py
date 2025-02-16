import os
import requests
from datetime import datetime

# Qaynaq link
source_url = "http://player.smotrim.ru/iframe/stream/live_id/efab3cbe-a29c-45f0-9596-5cb4f1ce7fbe.m3u8"

# Faylın yadda saxlanacağı qovluq
output_folder = "output"
os.makedirs(output_folder, exist_ok=True)

# m3u8 faylını çıxar və qovluğa yadda saxla
def extract_m3u8(url):
    try:
        # m3u8 faylını yüklə
        response = requests.get(url)
        response.raise_for_status()  # Xəta yoxlanışı

        # Faylı qovluğa yaz
        with open(file_path, "wb") as file:
            file.write(response.content)

        print(f"m3u8 faylı uğurla yadda saxlandı: {file_path}")
    except Exception as e:
        print(f"Xəta baş verdi: {e}")

# Skriptin əsas hissəsi
if __name__ == "__main__":
    extract_m3u8(source_url)
