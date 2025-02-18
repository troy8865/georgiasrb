import yaml
import requests
import re
from urllib.parse import urlparse, parse_qs

# YAML yapılandırma dosyasını yükle
def load_config(config_file="config.yml"):
    try:
        with open(config_file, "r", encoding="utf-8") as file:
            config = yaml.safe_load(file)
            return config
    except Exception as e:
        print("Yapılandırma dosyası yüklenirken hata oluştu:", str(e))
        return None

# Canlı yayın linkini ve tokeni al
def get_live_stream_url(config):
    try:
        # Ana sayfayı çek
        base_url = config.get("base_url")
        if not base_url:
            raise ValueError("Ana URL yapılandırması eksik.")

        response = requests.get(base_url, timeout=config.get("request_timeout", 15))
        response.raise_for_status()

        # Regex ile canlı yayın linkini bul
        live_stream_regex = config.get("live_stream_regex")
        if not live_stream_regex:
            raise ValueError("Canlı yayın regex deseni yapılandırması eksik.")

        match = re.search(live_stream_regex, response.text)
        if not match:
            raise ValueError("Canlı yayın linki bulunamadı.")

        live_url = match.group(0)
        print("Bulunan canlı yayın linki:", live_url)

        # Tokeni ve süre bilgisini ayrıştır
        parsed_url = urlparse(live_url)
        query_params = parse_qs(parsed_url.query)
        token = query_params.get('st', [None])[0]
        expiration = query_params.get('e', [None])[0]

        if not token or not expiration:
            raise ValueError("Token veya süre bilgisi eksik.")

        print("Token:", token)
        print("Geçerlilik süresi (epoch):", expiration)

        return live_url, token, expiration

    except Exception as e:
        print("Hata:", str(e))
        return None, None, None

# Token yenileme işlemi
def refresh_token(config):
    try:
        token_refresh_config = config.get("token_refresh", {})
        if not token_refresh_config.get("enabled", False):
            print("Token yenileme devre dışı.")
            return None

        refresh_url = token_refresh_config.get("refresh_url")
        headers = token_refresh_config.get("headers", {})
        timeout = token_refresh_config.get("timeout", 10)

        if not refresh_url:
            raise ValueError("Token yenileme URL'si yapılandırması eksik.")

        response = requests.post(refresh_url, headers=headers, timeout=timeout)
        response.raise_for_status()

        new_token = response.json().get("token")  # JSON yanıtından tokeni al
        if not new_token:
            raise ValueError("Yeni token alınamadı.")

        print("Yeni token başarıyla alındı:", new_token)
        return new_token

    except Exception as e:
        print("Token yenileme hatası:", str(e))
        return None

# Ana fonksiyon
if __name__ == "__main__":
    # Yapılandırma dosyasını yükle
    config = load_config()
    if not config:
        exit(1)

    # Canlı yayın linkini al
    live_url, token, expiration = get_live_stream_url(config)
    if live_url:
        print("Canlı yayın linki başarıyla alındı:", live_url)
    else:
        print("Canlı yayın linki alınamadı.")

    # Token yenileme işlemini gerçekleştir
    if config.get("token_refresh", {}).get("enabled", False):
        new_token = refresh_token(config)
        if new_token:
            print("Token başarıyla yenilendi:", new_token)
        else:
            print("Token yenileme başarısız.")
