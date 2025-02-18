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

# Multi-variant M3U8 faylının əsas strukturunu hazırlamaq üçün funksiya
def create_multi_variant_m3u8(streams, output_filename):
    try:
        # Multi-variant M3U8 faylının başlanğıc hissəsi
        m3u8_content = "#EXTM3U\n#EXT-X-VERSION:3\n"

        # Hər bir stream üçün m3u8 məzmununu əlavə edin
        for stream in streams:
            bandwidth = stream.get("bandwidth", 0)
            resolution = stream.get("resolution", "N/A")
            url = stream.get("url", "")
            
            # Stream məlumatlarını əlavə edin
            m3u8_content += f"#EXT-X-STREAM-INF:BANDWIDTH={bandwidth},RESOLUTION={resolution}\n{url}\n"

        # Nəticəni fayla yazın
        output_path = os.path.join(output_folder, output_filename)
        with open(output_path, "w", encoding="utf-8") as file:
            file.write(m3u8_content)
        
        print(f"Multi-variant M3U8 faylı uğurla yaradıldı: {output_path}")
    except Exception as e:
        print(f"Xəta baş verdi: {e}")

# m3u8 faylını yükləmək və işləmək üçün funksiya
def extract_m3u8(url, index):
    try:
        # m3u8 faylını yüklə
        response = requests.get(url)
        response.raise_for_status()  # Xəta yoxlanışı
        
        # Fayl adını index ilə fərqləndir
        filename = f"stream_{index}.m3u8"
        file_path = os.path.join(output_folder, filename)
        
        # Faylı oxu
        m3u8_content = response.text
        
        # Debug: Qaynaq faylının məzmununu çap et
        print("Qaynaq faylının məzmunu:")
        print(m3u8_content)
        
        # Faylı qovluğa yaz (üzərinə yaz)
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(m3u8_content)
        
        print(f"m3u8 faylı uğurla saxlandı: {file_path}")
        
        return file_path  # Yerli fayl yolunu qaytar
    except Exception as e:
        print(f"Xəta baş verdi: {e}")
        return None

# Skriptin əsas hissəsi
if __name__ == "__main__":
    streams = []  # Multi-variant üçün streamləri saxlayacağımız siyahı
    
    # Hər bir URL üçün m3u8 faylını yükləyib, streamləri toplayın
    for index, url in enumerate(source_urls):
        if url:  # Əgər URL boş deyilsə
            file_path = extract_m3u8(url, index)
            if file_path:
                # Yerli fayldan stream məlumatlarını oxuyun
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read()
                
                # Simplified: Bandaidth və Resolution dəyərlərini təxminən təyin edin
                bandwidth = 4050000 + index * 1000000  # Nümunəlik dəyərlər
                resolution = "1280x720" if index == 0 else "854x480" if index == 1 else "640x360"
                
                # Stream məlumatlarını siyahıya əlavə edin
                streams.append({
                    "bandwidth": bandwidth,
                    "resolution": resolution,
                    "url": file_path.replace("\\", "/")  # Fayl yolunu URL formatına çevirin
                })
    
    # Multi-variant M3U8 faylını yaradın
    if streams:
        create_multi_variant_m3u8(streams, "multi_variant_stream.m3u8")
