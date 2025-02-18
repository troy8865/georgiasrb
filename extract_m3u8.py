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

# Mevcut M3U8 faylının linklərini yeniləyən funksiya
def update_m3u8_links(input_file, output_file, new_base_url):
    try:
        # Mevcut M3U8 faylını oxuyun
        with open(input_file, "r", encoding="utf-8") as file:
            lines = file.readlines()
        
        # Linkləri yeniləyin
        updated_lines = []
        for line in lines:
            if not line.strip().startswith("#") and line.strip():  # Tərkibdə "#" olmayan sətirlər linkdir
                # Linkin önünə yeni URL əlavə edin
                updated_line = f"{new_base_url}/{line.strip()}\n"
                updated_lines.append(updated_line)
            else:
                # Digər sətirləri dəyişmədən əlavə edin
                updated_lines.append(line)
        
        # Yenilənmiş m3u8 faylını yazın
        with open(output_file, "w", encoding="utf-8") as file:
            file.writelines(updated_lines)
        
        print(f"M3U8 faylı uğurla yeniləndi: {output_file}")
    except Exception as e:
        print(f"Xəta baş verdi: {e}")

# Skriptin əsas hissəsi
if __name__ == "__main__":
    input_file = os.path.join(output_folder, "original_stream.m3u8")  # Orijinal fayl
    output_file = os.path.join(output_folder, "updated_stream.m3u8")  # Yenilənmiş fayl
    
    # Yeni base URL (linklərin önündəki hissə)
    new_base_url = "https://love2live.wideiptv.top/beINSPORTS1TR/index.fmp4.m3u8"
    
    # M3U8 faylını yeniləyin
    update_m3u8_links(input_file, output_file, new_base_url)
