import os
import requests

# Qaynaq linkləri
source_urls = [
    "https://raalbatros.serv00.net:443/ctv.php?url=https://tv.canlitv.vip/saban-tv",
    # Buraya digər m3u8 linklərini əlavə edin
]

# Faylın yadda saxlanacağı qovluq
output_folder = "output"
os.makedirs(output_folder, exist_ok=True)

# .ts linkini əvəz edən funksiya
def replace_ts_with_m3u8(line):
    if line.strip().endswith('.ts'):
        # .ts linkini sabantv.m3u8 ilə əvəz et
        return "https://cdn900.canlitv.vip/sabantv.m3u8?"
    return line

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
        
        # İçindəki linkləri işləyib, onların önündəki əlavə edilən hissəni çıxarırıq
        for line in m3u8_content:
            if line.strip() and not line.startswith("#"):  # Tərkibdə "#" olmayan sətirləri seç
                # Linki əvəz etmək üçün funksiya çağırılır
                modified_line = replace_ts_with_m3u8(line)
                modified_content += f"#EXT-X-STREAM-INF:BANDWIDTH=2085600,RESOLUTION=1280x720\n{modified_line}\n"
            else:
                # Əgər sətir meta məlumatdırsa, olduğu kimi saxla
                modified_content += f"{line}\n"
        
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
