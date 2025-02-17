import os
import requests

# Qaynaq linkləri
source_urls = [
    "",
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
        
        # Faylı oxu və içindəki nisbi linkləri tam URL-yə çevir
        m3u8_content = response.text
        
        # Multi-variant m3u8 faylı üçün əsas strukturu yaradırıq
        modified_content = "#EXTM3U\n#EXT-X-VERSION:3\n"
        
        # Müxtəlif keyfiyyət seçimləri üçün linklər əlavə edirik
        variants = [
            {"bandwidth": 800000, "resolution": "640x360", "suffix": "a"},
            {"bandwidth": 1200000, "resolution": "854x480", "suffix": "b"},
            {"bandwidth": 2000000, "resolution": "1280x720", "suffix": "c"},
        ]
        
        for variant in variants:
            modified_content += f"#EXT-X-STREAM-INF:BANDWIDTH={variant['bandwidth']},RESOLUTION={variant['resolution']}\n"
            modified_content += f"https://love2live.wideiptv.top/beINSPORTS1TR/index.fmp4.m3u8?tracks-v1{variant['suffix']}/index.fmp4.m3u8?remote=no_check_ip&token=1e0284b979ceb30bb9d1ef408e4dd8c8e362005a-38dc65c08c7ad97411942c76c9a12762-1739825087-1739814287\n"
        
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
