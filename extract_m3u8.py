import requests
import os

# M3U faylının URL-i
url = "http://185.50.148.2:88/stalker_portal/server/tools/m3u.php"

# Faylın yadda saxlanacağı qovluq
output_folder = "kanallar"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# M3U faylını yüklə
response = requests.get(url)
if response.status_code == 200:
    m3u_content = response.text
else:
    print(f"Xəta: {response.status_code}")
    exit()

# M3U faylını oxu və kanalları ayrı fayllar kimi yaz
channel_lines = m3u_content.splitlines()
channel_info = {}

for line in channel_lines:
    if line.startswith("#EXTINF:"):
        # Kanal adını çıxar
        channel_name = line.split(",")[-1].strip()
        # Fayl adında qadağan olunan simvolları təmizlə
        channel_name = channel_name.replace("/", "_").replace("\\", "_").replace(":", "_")
        channel_info["name"] = channel_name
    elif line.startswith("http"):
        # Kanal URL-ni çıxar və /index.m3u8 və ya /index hissəsini sil
        channel_url = line.strip()
        if channel_url.endswith("/index.m3u8"):
            channel_url = channel_url[:-11]  # Remove the last 11 characters (/index.m3u8)
        elif channel_url.endswith("/index"):
            channel_url = channel_url[:-6]  # Remove the last 6 characters (/index)
        channel_info["url"] = channel_url
        
        # Fayl adını təyin et
        file_name = f"{channel_info['name']}.m3u"
        file_path = os.path.join(output_folder, file_name)
        
        # Fayl yarad və yaz
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                # M3U8 başlıqlarını əlavə et
                f.write("#EXTM3U\n")
                f.write("#EXT-X-VERSION:3\n")
                f.write("#EXT-X-TARGETDURATION:10\n")
                f.write("#EXT-X-MEDIA-SEQUENCE:0\n")
                # Kanal məlumatını əlavə et
                f.write(f"#EXTINF:10.0,{channel_info['name']}\n")
                f.write(f"{channel_info['url']}\n")
            print(f"{channel_info['name']} kanalı fayla yazıldı: {file_path}")
        except Exception as e:
            print(f"Xəta: {channel_info['name']} kanalı fayla yazıla bilmədi: {e}")
else:
    print("Bütün kanallar uğurla yazıldı.")
