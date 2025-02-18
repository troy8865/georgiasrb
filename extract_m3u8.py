import os
import requests
import re
from urllib.parse import urljoin

# Qaynaq linki
source_url = "https://rutube.ru/live/video/c58f502c7bb34a8fcdd976b221fca292/?category=1"

# Faylın yadda saxlanacağı qovluq
output_folder = "output"
os.makedirs(output_folder, exist_ok=True)

# Token almaq üçün API endpoint-i
token_url = "https://api.rutube.ru/get_token"

# Token almaq üçün funksiya
def get_token():
    try:
        response = requests.get(token_url)
        response.raise_for_status()
        token = response.json().get("token")
        if token:
            print(f"Token uğurla alındı: {token}")
            return token
        else:
            print("Token alına bilmədi.")
            return None
    except Exception as e:
        print(f"Xəta baş verdi: {e}")
        return None

# Rutube-dan m3u8 linkini çıxar
def extract_m3u8_from_rutube(url, token):
    try:
        headers = {
            "Authorization": f"Bearer {token}",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        # HTML içindən m3u8 linkini tapmaq üçün regex istifadə edirik
        m3u8_pattern = r"https://[^\s\"']+\.m3u8"
        matches = re.findall(m3u8_pattern, response.text)

        if matches:
            m3u8_url = matches[0]
            print(f"Tapılan m3u8 linki: {m3u8_url}")
            return m3u8_url
        else:
            print("M3U8 linki tapılmadı.")
            return None
    except Exception as e:
        print(f"Xəta baş verdi: {e}")
        return None

# m3u8 faylını çıxar və qovluğa yadda saxla
def save_m3u8_to_file(m3u8_url, index):
    try:
        response = requests.get(m3u8_url)
        response.raise_for
