import os
import requests

# Qaynaq linkləri
source_urls = [
    "http://raalbatros.serv00.net/Freeshot.php?ID=bein-sports-1-turkey/158",
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
        
        # Faylın mövcud məzmununu oxu (əgər varsa)
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as file:
                existing_content = file.readlines()
        else:
            existing_content = []
        
        # Yeni m3u8 məzmununu yüklə
        m3u8_content = response.text.splitlines()
        
        # Debug: Qaynaq faylının məzmununu çap et
        print("Qaynaq faylının məzmunu:")
        print(m3u8_content)
        
        # Multi-variant m3u8 faylı üçün əsas strukturu yaradırıq
        modified_content = "#EXTM3U\n#EXT-X-VERSION:3\n"
        
        # İçindəki linkləri işləyib, onların önünə əsas URL əlavə etmək lazım deyil
        for line in m3u8_content:
            if line.strip() and not line.startswith("#"):  # Tərkibdə "#" olmayan sətirləri seç
                # Linki olduğu kimi saxlayırıq
                modified_content += f"#EXT-X-STREAM-INF:BANDWIDTH=2085600,RESOLUTION=1280x720\n{line.strip()}\n"
        
        # Mövcud məzmunu qoruyub, yalnız linkləri yeniləyirik
        final_content = []
        for existing_line in existing_content:
            if existing_line.strip().startswith("#EXT-X-STREAM-INF"):
                # Linklə bağlı olan sətir
                next_line = existing_content[existing_content.index(existing_line) + 1]
                if next_line.strip() and not next_line.startswith("#"):
                    # Linki yeniləyirik (yalnız linkləri olduğu kimi saxlayırıq)
                    final_content.append(existing_line)
                    final_content.append(f"{next_line.strip()}\n")
            else:
                # Digər sətirləri olduğu kimi saxlayırıq
                final_content.append(existing_line)
        
        # Faylı qovluğa yaz (üzərinə yaz)
        with open(file_path, "w", encoding="utf-8") as file:
            file.writelines(final_content)
        print(f"m3u8 faylı uğurla yeniləndi: {file_path}")
    except Exception as e:
        print(f"Xəta baş verdi: {e}")

# Skriptin əsas hissəsi
if __name__ == "__main__":
    for index, url in enumerate(source_urls):
        if url:  # Əgər URL boş deyilsə
            extract_m3u8(url, index)
