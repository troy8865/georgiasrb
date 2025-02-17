import os
import requests

# Qaynaq linki
source_url = "http://raalbatros.serv00.net/Freeshot.php?ID=bein-sports-1-turkey/158"

# Faylın yadda saxlanacağı qovluq
output_folder = "output"
os.makedirs(output_folder, exist_ok=True)

# m3u8 faylını çıxar və qovluğa yadda saxla
def convert_to_m3u8(url):
    try:
        # m3u8 faylını yüklə
        response = requests.get(url)
        response.raise_for_status()  # Xəta yoxlanışı
        
        # Fayl adını təyin et
        filename = "output_stream.m3u8"
        file_path = os.path.join(output_folder, filename)
        
        # Faylı qovluğa yaz (üzərinə yaz)
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(response.text)
        print(f"m3u8 faylı uğurla yaradıldı: {file_path}")
    except Exception as e:
        print(f"Xəta baş verdi: {e}")

# Skriptin əsas hissəsi
if __name__ == "__main__":
    convert_to_m3u8(source_url)
