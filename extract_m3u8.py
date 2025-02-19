import os
import requests

# Qaynaq linkləri
source_urls = [
    "https://node19.connect.az:9081/tv/live/playlist.m3u8",
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
        m3u8_content = response.text.splitlines()
        
        # Debug: Qaynaq faylının məzmununu çap et
        print("Qaynaq faylının məzmunu:")
        print(m3u8_content)
        
        # Multi-variant m3u8 faylı üçün əsas strukturu yaradırıq
        modified_content = "#EXTM3U\n#EXT-X-VERSION:3\n"
        
        # İçindəki linkləri işləyib, onların önünə əsas URL əlavə edirik
        for line in m3u8_content:
            if line.strip() and not line.startswith("#"):  # Tərkibdə "#" olmayan sətirləri seç
                # Linkin tam formasını götür (token də daxil olmaqla)
                full_url = f"https://love2live.wideiptv.top/beINSPORTS1TR/index.fmp4.m3u8?/{line.strip()}"
                # Multi-variant m3u8 formatına uyğun olaraq yazırıq
                modified_content += f"#EXT-X-STREAM-INF:BANDWIDTH=2085600,RESOLUTION=1280x720\n{full_url}\n"
        
        # Faylı qovluğa yaz (üzərinə yaz)
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(modified_content)
        print(f"m3u8 faylı uğurla yeniləndi: {file_path}")
    except Exception as e:
        print(f"Xəta baş verdi: {e}")

# Skriptin əsas hissəsi
if __name__ == "__main__":
    for index, url in enumerate(source_urls):
        if url:  # Əgər URL boş deyilsə
            extract_m3u8(url, index)
