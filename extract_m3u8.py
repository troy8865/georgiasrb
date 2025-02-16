import os
import requests

# Qaynaq linkləri
source_urls = [
    "http://player.smotrim.ru/iframe/stream/live_id/efab3cbe-a29c-45f0-9596-5cb4f1ce7fbe.m3u8",
    "https://yoda.az"
    # Buraya digər m3u8 linklərini əlavə edin
]

# Faylın yadda saxlanacağı qovluq
output_folder = "output"
os.makedirs(output_folder, exist_ok=True)

# m3u8 faylını çıxar və qovluğa yadda saxla
def extract_m3u8(url, index):
    try:
        # m3u8 faylını yüklə
        response = requests.get(url)
        response.raise_for_status()  # Xəta yoxlanışı
        
        # Fayl adını index ilə fərqləndir
        filename = f"stream_{index}.m3u8"
        file_path = os.path.join(output_folder, filename)
        
        # Faylı oxu və içindəki nisbi linkləri tam URL-yə çevir
        m3u8_content = response.text
        
        # Mənbə linkinin əsas hissəsini alırıq
        base_url = url.rsplit('/', 1)[0]  # Əsas URL-ni alırıq
        
        # Nisbi linkləri tam linklərlə əvəz edirik
        modified_content = ""
        for line in m3u8_content.splitlines():
            if line.startswith("#"):
                # # işarəsi olan sətirləri olduğu kimi saxlayırıq
                modified_content += line + "\n"
            elif line.strip():  # Boş olmayan sətirlər
                # Linkin sonuna ?md5=... hissəsini əlavə edirik
                full_url = f"{base_url}/{line}" if not line.startswith("http") else line
                modified_content += full_url + "\n"
        
        # Faylı qovluğa yaz (üzərinə yaz)
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(modified_content)
        print(f"m3u8 faylı uğurla yeniləndi: {file_path}")
    except Exception as e:
        print(f"Xəta baş verdi: {e}")

# Skriptin əsas hissəsi
if __name__ == "__main__":
    for index, url in enumerate(source_urls):
        extract_m3u8(url, index)
