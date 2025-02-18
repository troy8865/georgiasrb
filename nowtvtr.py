import requests
import re
from urllib.parse import urlparse, parse_qs

# Ana sayfa URL'si
BASE_URL = "https://www.nowtv.com.tr/canli-yayin"

# Canlı yayın linkini ve tokeni almak için fonksiyon
def get_live_stream_url():
    try:
        # Ana sayfayı çek
        response = requests.get(BASE_URL)
        response.raise_for_status()

        # Sayfa içeriğindeki canlı yayın linkini bul
        match = re.search(r'https://nowtv-live-ad\.ercdn\.net/nowtv/nowtv_360p\.m3u8\?e=\d+&st=[\w-]+', response.text)
        if not match:
            raise ValueError("Canlı yayın linki bulunamadı.")

        live_url = match.group(0)
        print("Bulunan canlı yayın linki:", live_url)

        # Tokeni yenilemek için gerekli parametreleri ayrıştır
        parsed_url = urlparse(live_url)
        query_params = parse_qs(parsed_url.query)
        token = query_params.get('st', [None])[0]
        expiration = query_params.get('e', [None])[0]

        if not token or not expiration:
            raise ValueError("Token veya süre bilgisi eksik.")

        print("Token:", token)
        print("Geçerlilik süresi (epoch):", expiration)

        return live_url

    except Exception as e:
        print("Hata:", str(e))
        return None

# Token yenileme fonksiyonu (örnek)
def refresh_token():
    # Burada token yenileme mantığını uygulayabilirsiniz.
    # Örneğin, sunucuya POST isteği göndererek yeni bir token alabilirsiniz.
    print("Token yenileme işlemi henüz tanımlanmadı.")
    pass

# Ana fonksiyon
if __name__ == "__main__":
    live_url = get_live_stream_url()
    if live_url:
        print("Canlı yayın linki başarıyla alındı:", live_url)
    else:
        print("Canlı yayın linki alınamadı.")
