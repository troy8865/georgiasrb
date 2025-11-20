import requests
import json

# YouTube Data API key (canlı video ID'si almak için)
API_KEY = "YOUR_YOUTUBE_DATA_API_KEY"

# Android YouTube App API Key (HLS linki için)
ANDROID_KEY = "AIzaSyAO_Ttt7LqGCG2syrtvWxfgCMdBBBZaFv4"

# Kanal listesi ve grup bilgisi
CHANNELS = {
    # Haber kanalları
    "TRT Haber": {"id": "UCJ5v_MCY6GNUBTO8-D3XoAg", "group": "Haber"},
    "A Haber": {"id": "UCptL2Nepk3sR3FqMwDPutVw", "group": "Haber"},
    "NTV": {"id": "UCsJ6RuBiTVWRX156FVbeaGQ", "group": "Haber"},
    "Haber Global": {"id": "UCZgE8HJoOMEJrG6JUdY48Jg", "group": "Haber"},
    "Haber Türk": {"id": "UC0dEkA8PjyilKSCh9L6r7Mg", "group": "Haber"},
    "CNN Türk": {"id": "UC9n8EgewvK_EC0x4T5Z5DdQ", "group": "Haber"},
    "Show Haber": {"id": "UC6eWCld0KwmyHFbAqK3V-Rw", "group": "Haber"},
    "TGRT Haber": {"id": "UCi_1pACjjGfgK7N8wH9OBAA", "group": "Haber"},
    "Kanal 7 Haber": {"id": "UC8s_1tAY9NDfqkYzUcaHUKA", "group": "Haber"},
    "24 TV": {"id": "UCkZSBEMxM-xZt_Kk7wTkVfw", "group": "Haber"},
    "TV100": {"id": "UCw-dtCo3d_Z4j7BgyP5yG9Q", "group": "Haber"},
    "Beyaz TV": {"id": "UCJsWSdqWcHjiXK3f7xZfh5w", "group": "Haber"},
    "Ülke TV": {"id": "UCLa3ijq8neSahDmUVZz3IhA", "group": "Haber"},
    "KRT TV": {"id": "UCqVQYxhTSXdNUOjdknLmQjQ", "group": "Haber"},
    "Sirius TV": {"id": "UCehmwSZGPod7JFbHJspmxzQ", "group": "Haber"},
    "Ege Haber TV": {"id": "UC2wUaN48EwJMQK0pGqvW2mw", "group": "Haber"},
    "TV 52": {"id": "UCq6qk1pQWyxubcSQXBH1H-Q", "group": "Haber"},
    "TV 8.5": {"id": "UCcMbk-CY1x7kGEXVWl7aT0A", "group": "Haber"},
    "TV 38": {"id": "UCXsY4b4iRl8V9i2MK1LQXBg", "group": "Haber"},

    # Spor kanalları
    "Sıfır TV": {"id": "UCwC5uWwZrxpO_6z7dxyzAqw", "group": "Spor"},
    "Ekol Sports": {"id": "UCYO3zDh9N19XRC-5jMY6d5w", "group": "Spor"},
    "HT Spor": {"id": "UC9n8EgewvK_EC0x4T5Z5DdQ", "group": "Spor"},
    "Sportstv": {"id": "UCUcJr8GINdD5nUUT-KFOrhg", "group": "Spor"}
}

OUTPUT_FILE = "multichannel.m3u8"


def get_live_video_id(channel_id):
    url = (
        f"https://www.googleapis.com/youtube/v3/search"
        f"?part=snippet&channelId={channel_id}"
        f"&eventType=live&type=video&key={API_KEY}"
    )
    r = requests.get(url).json()
    items = r.get("items", [])
    if not items:
        return None
    return items[0]["id"]["videoId"]


def get_hls_link(video_id):
    url = f"https://www.youtube.com/youtubei/v1/player?key={ANDROID_KEY}"
    payload = {
        "context": {
            "client": {"clientName": "ANDROID", "clientVersion": "17.31.35"}
        },
        "videoId": video_id
    }

    r = requests.post(url, json=payload)
    data = r.json()

    streaming = data.get("streamingData", {})
    return streaming.get("hlsManifestUrl")


def main():
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")

        for name, info in CHANNELS.items():
            group = info["group"]
            channel_id = info["id"]

            print(f"Kontrol ediliyor: {name} ({group})...")

            video_id = get_live_video_id(channel_id)
            if not video_id:
                print(f"❌ Canlı yayın yok: {name}")
                continue

            hls = get_hls_link(video_id)
            if not hls:
                print(f"❌ HLS linki alınamadı: {name}")
                continue

            f.write(f'#EXTINF:-1 tvg-name="{name}" group-title="{group}", {name}\n')
            f.write(hls + "\n")

            print(f"✔ Eklendi: {name}")

    print("\n📺 M3U dosyası oluşturuldu:", OUTPUT_FILE)


if __name__ == "__main__":
    main()
