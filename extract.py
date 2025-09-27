import os
import requests
from urllib.parse import urlparse, parse_qs

# Qaynaq linkləri (istədiyin qədər əlavə edə bilərsən)
source_urls = [
"http://158.101.222.193:88/georgia_play.php?id=ssc1",
"http://158.101.222.193:88/georgia_play.php?id=ssc2",
"http://158.101.222.193:88/georgia_play.php?id=ssc3",
"http://158.101.222.193:88/georgia_play.php?id=ssc4",
"http://158.101.222.193:88/georgia_play.php?id=ssc5",
"http://158.101.222.193:88/georgia_play.php?id=amedia",
"http://158.101.222.193:88/georgia_play.php?id=amedia2",
"http://158.101.222.193:88/georgia_play.php?id=amediahit",
"http://158.101.222.193:88/georgia_play.php?id=amediapremium",
"http://158.101.222.193:88/georgia_play.php?id=argotv",
"http://158.101.222.193:88/georgia_play.php?id=arirang",
"http://158.101.222.193:88/georgia_play.php?id=artarea",
"http://158.101.222.193:88/georgia_play.php?id=auto24",
"http://158.101.222.193:88/georgia_play.php?id=autoplus",
"http://158.101.222.193:88/georgia_play.php?id=batumitv",
"http://158.101.222.193:88/georgia_play.php?id=bbb",
"http://158.101.222.193:88/georgia_play.php?id=bbc",
"http://158.101.222.193:88/georgia_play.php?id=black",
"http://158.101.222.193:88/georgia_play.php?id=bmg",
"http://158.101.222.193:88/georgia_play.php?id=bollywoodhd",
"http://158.101.222.193:88/georgia_play.php?id=borjomitv",
"http://158.101.222.193:88/georgia_play.php?id=boxtv",
"http://158.101.222.193:88/georgia_play.php?id=caucasia",
"http://158.101.222.193:88/georgia_play.php?id=cctv4",
"http://158.101.222.193:88/georgia_play.php?id=comedy",
"http://158.101.222.193:88/georgia_play.php?id=ctctv",
"http://158.101.222.193:88/georgia_play.php?id=ctv",
"http://158.101.222.193:88/georgia_play.php?id=currenttime",
"http://158.101.222.193:88/georgia_play.php?id=davinci",
"http://158.101.222.193:88/georgia_play.php?id=detsky",
"http://158.101.222.193:88/georgia_play.php?id=detskymir",
"http://158.101.222.193:88/georgia_play.php?id=diatv",
"http://158.101.222.193:88/georgia_play.php?id=domashni",
"http://158.101.222.193:88/georgia_play.php?id=drotv",
"http://158.101.222.193:88/georgia_play.php?id=dw",
"http://158.101.222.193:88/georgia_play.php?id=egrisitv",
"http://158.101.222.193:88/georgia_play.php?id=enkibenki",
"http://158.101.222.193:88/georgia_play.php?id=ertsulovneba",
"http://158.101.222.193:88/georgia_play.php?id=espressotv",
"http://158.101.222.193:88/georgia_play.php?id=eurokino",
"http://158.101.222.193:88/georgia_play.php?id=euronewsgeorgia",
"http://158.101.222.193:88/georgia_play.php?id=fenikspluskino",
"http://158.101.222.193:88/georgia_play.php?id=formula",
"http://158.101.222.193:88/georgia_play.php?id=friday",
"http://158.101.222.193:88/georgia_play.php?id=gdstv",
"http://158.101.222.193:88/georgia_play.php?id=girchitv",
"http://158.101.222.193:88/georgia_play.php?id=gms",
"http://158.101.222.193:88/georgia_play.php?id=greentv",
"http://158.101.222.193:88/georgia_play.php?id=gttv",
"http://158.101.222.193:88/georgia_play.php?id=hdlife",
"http://158.101.222.193:88/georgia_play.php?id=ictimai",
"http://158.101.222.193:88/georgia_play.php?id=ictv",
"http://158.101.222.193:88/georgia_play.php?id=illuzionplus",
"http://158.101.222.193:88/georgia_play.php?id=ilontv",
"http://158.101.222.193:88/georgia_play.php?id=imedi",
"http://158.101.222.193:88/georgia_play.php?id=imedihd",
"http://158.101.222.193:88/georgia_play.php?id=indiyskoekino",
"http://158.101.222.193:88/georgia_play.php?id=interesnoetv",
"http://158.101.222.193:88/georgia_play.php?id=jivi",
"http://158.101.222.193:88/georgia_play.php?id=khlprime",
"http://158.101.222.193:88/georgia_play.php?id=kinohit",
"http://158.101.222.193:88/georgia_play.php?id=kinokomediya",
"http://158.101.222.193:88/georgia_play.php?id=kinomiks",
"http://158.101.222.193:88/georgia_play.php?id=kinopremyerahd",
"http://158.101.222.193:88/georgia_play.php?id=kinosemya",
"http://158.101.222.193:88/georgia_play.php?id=kinoseria",
"http://158.101.222.193:88/georgia_play.php?id=kinosvidanie",
"http://158.101.222.193:88/georgia_play.php?id=kinoujas",
"http://158.101.222.193:88/georgia_play.php?id=kolkheti89",
"http://158.101.222.193:88/georgia_play.php?id=ktoestkto",
"http://158.101.222.193:88/georgia_play.php?id=kuxnia",
"http://158.101.222.193:88/georgia_play.php?id=kvartal95",
"http://158.101.222.193:88/georgia_play.php?id=kvntv",
"http://158.101.222.193:88/georgia_play.php?id=laminor",
"http://158.101.222.193:88/georgia_play.php?id=lilotv",
"http://158.101.222.193:88/georgia_play.php?id=m1",
"http://158.101.222.193:88/georgia_play.php?id=m2",
"http://158.101.222.193:88/georgia_play.php?id=maestro",
"http://158.101.222.193:88/georgia_play.php?id=malysh",
"http://158.101.222.193:88/georgia_play.php?id=marao",
"http://158.101.222.193:88/georgia_play.php?id=marneulitv",
"http://158.101.222.193:88/georgia_play.php?id=matchplaneta",
"http://158.101.222.193:88/georgia_play.php?id=megatv",
"http://158.101.222.193:88/georgia_play.php?id=mezzo",
"http://158.101.222.193:88/georgia_play.php?id=mir",
"http://158.101.222.193:88/georgia_play.php?id=mir24",
"http://158.101.222.193:88/georgia_play.php?id=mtavari",
"http://158.101.222.193:88/georgia_play.php?id=musicbox",
"http://158.101.222.193:88/georgia_play.php?id=musictv",
"http://158.101.222.193:88/georgia_play.php?id=muzhskoy",
"http://158.101.222.193:88/georgia_play.php?id=mzareulitv",
"http://158.101.222.193:88/georgia_play.php?id=nashanovoekino",
"http://158.101.222.193:88/georgia_play.php?id=nikijunior",
"http://158.101.222.193:88/georgia_play.php?id=nikikids",
"http://158.101.222.193:88/georgia_play.php?id=nostalgy",
"http://158.101.222.193:88/georgia_play.php?id=nwbctv",
"http://158.101.222.193:88/georgia_play.php?id=o2",
"http://158.101.222.193:88/georgia_play.php?id=obiektivi",
"http://158.101.222.193:88/georgia_play.php?id=odishi",
"http://158.101.222.193:88/georgia_play.php?id=ort",
"http://158.101.222.193:88/georgia_play.php?id=oruzhie",
"http://158.101.222.193:88/georgia_play.php?id=palitra",
"http://158.101.222.193:88/georgia_play.php?id=perec",
"http://158.101.222.193:88/georgia_play.php?id=pirvelitv",
"http://158.101.222.193:88/georgia_play.php?id=pktv",
"http://158.101.222.193:88/georgia_play.php?id=plustv",
"http://158.101.222.193:88/georgia_play.php?id=puls",
"http://158.101.222.193:88/georgia_play.php?id=qvemoqartli",
"http://158.101.222.193:88/georgia_play.php?id=red",
"http://158.101.222.193:88/georgia_play.php?id=rentv",
"http://158.101.222.193:88/georgia_play.php?id=rioni",
"http://158.101.222.193:88/georgia_play.php?id=rioni2",
"http://158.101.222.193:88/georgia_play.php?id=rtv",
"http://158.101.222.193:88/georgia_play.php?id=rusilluzion",
"http://158.101.222.193:88/georgia_play.php?id=russia24",
"http://158.101.222.193:88/georgia_play.php?id=scifi",
"http://158.101.222.193:88/georgia_play.php?id=shonitv",
"http://158.101.222.193:88/georgia_play.php?id=stereoplus",
"http://158.101.222.193:88/georgia_play.php?id=tanamgzavri",
"http://158.101.222.193:88/georgia_play.php?id=tv1000rukino",
"http://158.101.222.193:88/georgia_play.php?id=tv12",
"http://158.101.222.193:88/georgia_play.php?id=tv24",
"http://158.101.222.193:88/georgia_play.php?id=tv25",
"http://158.101.222.193:88/georgia_play.php?id=tv9",
"http://158.101.222.193:88/georgia_play.php?id=tvc",
"http://158.101.222.193:88/georgia_play.php?id=tvmax",
"http://158.101.222.193:88/georgia_play.php?id=unikum",
"http://158.101.222.193:88/georgia_play.php?id=uspeh",
"http://158.101.222.193:88/georgia_play.php?id=viasatexp",
"http://158.101.222.193:88/georgia_play.php?id=viasathist",
"http://158.101.222.193:88/georgia_play.php?id=viasatnat",
"http://158.101.222.193:88/georgia_play.php?id=viasatsport",
"http://158.101.222.193:88/georgia_play.php?id=zeetv",
"http://158.101.222.193:88/georgia_play.php?id=zoo",
"http://158.101.222.193:88/georgia_play.php?id=setanta_georgia",
"http://158.101.222.193:88/georgia_play.php?id=setanta_sports_3",
"http://158.101.222.193:88/georgia_play.php?id=setanta_sports_plus_georgia",
"http://158.101.222.193:88/georgia_play.php?id=silk_sport4",
"https://www.elahmad.com/tv/sunnatv.php",

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
