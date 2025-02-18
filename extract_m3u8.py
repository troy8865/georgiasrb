import os
import requests

# Qaynaq linkləri (yenilənmək üçün əlavə ediləcək streamlər)
source_urls = [
    "http://raalbatros.serv00.net/Freeshot.php?ID=bein-sports-1-turkey/158",
    # Buraya digər m3u8 linklərini əlavə edin
]

# Faylın yadda saxlanacağı qovluq
output_folder = "output"
os.makedirs(output_folder, exist_ok=True)

# Mevcut multi-variant M3U8 faylını oxumaq və yeniləmək üçün funksiya
def update_multi_variant_m3u8(existing_file, new_streams):
    try:
        # Əgər fayl mövcud deyilsə, boş m3u8 strukturunu hazırlayın
        if not os.path.exists(existing_file):
            with open(existing_file, "w", encoding="utf-8") as file:
                file.write("#EXTM3U\n#EXT-X-VERSION:3\n")
        
        # Mevcut faylı oxuyun
        with open(existing_file, "r", encoding="utf-8") as file:
            existing_content = file.readlines()
        
        # Yeni streamləri əlavə edin
        with open(existing_file, "a", encoding="utf-8") as file:
            for stream in new_streams:
                bandwidth = stream.get("bandwidth", 0)
                resolution = stream.get("resolution", "N/A")
                url = stream.get("url", "")
                
                # Stream məlumatlarını əlavə edin
                file.write(f"#EXT-X-STREAM-INF:BANDWIDTH={bandwidth},RESOLUTION={resolution}\n")
                file.write(f"{url}\n")
        
        print(f"Multi-variant M3U8 faylı uğurla yeniləndi: {existing_file}")
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
        
        return {
            "bandwidth": 4050000 + index * 1000000,  # Nümunəlik dəyərlər
            "resolution": "1280x720" if index == 0 else "854x480" if index == 1 else "640x360",
            "url": file_path.replace("\\", "/")  # Fayl yolunu URL formatına çevirin
        }
    except Exception as e:
        print(f"Xəta baş verdi: {e}")
        return None

# Skriptin əsas hissəsi
if __name__ == "__main__":
    multi_variant_file = os.path.join(output_folder, "multi_variant_stream.m3u8")
    
    new_streams = []  # Yeni streamləri saxlayacağımız siyahı
    
    # Hər bir URL üçün m3u8 faylını yükləyib, streamləri toplayın
    for index, url in enumerate(source_urls):
        if url:  # Əgər URL boş deyilsə
            stream_info = extract_m3u8(url, index)
            if stream_info:
                new_streams.append(stream_info)
    
    # Mevcut multi-variant M3U8 faylını yeniləyin
    if new_streams:
        update_multi_variant_m3u8(multi_variant_file, new_streams)
