import os
import requests
from urllib.parse import urlparse, parse_qs

# Qaynaq linkləri (istədiyin qədər əlavə edə bilərsən)
source_urls = [
    "http://158.101.222.193:88/georgia_play.php?id=kinohit",
    "http://158.101.222.193:88/georgia_play.php?id=kinomiks",
    "http://158.101.222.193:88/georgia_play.php?id=marneulitv",
    "http://158.101.222.193:88/georgia_play.php?id=fenikspluskino",
    "http://158.101.222.193:88/georgia_play.php?id=24techno",
    "http://158.101.222.193:88/georgia_play.php?id=365day",
    "http://158.101.222.193:88/georgia_play.php?id=amedia2",
    "http://158.101.222.193:88/georgia_play.php?id=amediahit",
    "http://158.101.222.193:88/georgia_play.php?id=amediapremium",
    "http://158.101.222.193:88/georgia_play.php?id=auto24",
    "http://158.101.222.193:88/georgia_play.php?id=kinoujas",
    "http://158.101.222.193:88/georgia_play.php?id=amedia",
    "http://158.101.222.193:88/georgia_play.php?id=perec",
    "http://158.101.222.193:88/georgia_play.php?id=friday",
    "http://158.101.222.193:88/georgia_play.php?id=eurokino",
    "http://158.101.222.193:88/georgia_play.php?id=domashni",
    "http://158.101.222.193:88/georgia_play.php?id=muzhskoy",
    "http://158.101.222.193:88/georgia_play.php?id=kinopremyerahd",
    "http://158.101.222.193:88/georgia_play.php?id=kinosemya",
    "http://158.101.222.193:88/georgia_play.php?id=kinoseria",
    "http://158.101.222.193:88/georgia_play.php?id=kinosvidanie",
    "http://158.101.222.193:88/georgia_play.php?id=black",
    "http://158.101.222.193:88/georgia_play.php?id=nashanovoekino",
    "http://158.101.222.193:88/georgia_play.php?id=zeetv",

]

# Faylların yazılacağı qovluq
output_folder = "output"
os.makedirs(output_folder, exist_ok=True)

def extract_m3u8(url):
    try:
        kanal_adi = parse_qs(urlparse(url).query).get("id", ["stream"])[0]
        filename = f"{kanal_adi}.m3u8"
        file_path = os.path.join(output_folder, filename)

        response = requests.get(url)
        response.raise_for_status()
        lines = response.text.splitlines()

        modified = "#EXTM3U\n#EXT-X-VERSION:3\n"
        for line in lines:
            if line.strip() and not line.startswith("#"):
                full_url = f"http://tbs01-edge17.itdc.ge/{kanal_adi}/{line.strip()}"
                modified += f"#EXT-X-STREAM-INF:BANDWIDTH=2085600,RESOLUTION=1280x720\n{full_url}\n"

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(modified)

        print(f"✅ {filename} yaradıldı.")
    except Exception as e:
        print(f"❌ {url} üçün xəta: {e}")

if __name__ == "__main__":
    for url in source_urls:
        extract_m3u8(url)
