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
        channel_info["name"] = channel_name
    elif line.startswith("http"):
        # Kanal URL-ni çıxar
        channel_info["url"] = line.strip()
        
        # Fayl adını təyin et
        file_name = f"{channel_info['name']}.m3u"
        file_path = os.path.join(output_folder, file_name)
        
        # Fayl yarad və yaz
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(f"#EXTINF:-1,{channel_info['name']}\n")
            f.write(f"{channel_info['url']}\n")
        
        print(f"{channel_info['name']} kanalı fayla yazıldı: {file_path}")
else:
    print("Bütün kanallar uğurla yazıldı.")
