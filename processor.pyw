# processor.pyw

import subprocess
import requests
import re
import socket
from datetime import datetime
import os
import time
from urllib.parse import urlparse, urljoin
from requests.exceptions import HTTPError, ConnectionError, Timeout, RequestException
import json
import copy
import html
from bs4 import BeautifulSoup

# --- SABİTLER VE AYARLAR ---
M3U8_DIR = "m3u8"
CONFIG_FILE = "config.json"
LOG_FILE = "log.txt"

# --- LOGLAMA FONKSİYONU ---
def log(message):
    timestamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {message}\n")
    except IOError as e:
        print(f"Log dosyasına yazma hatası: {e}")

# --- YARDIMCI FONKSİYONLAR ---
def sanitize_filename(filename):
    replacements = {
        'ç': 'c', 'ğ': 'g', 'ı': 'i', 'ö': 'o', 'ş': 's', 'ü': 'u',
        'Ç': 'C', 'Ğ': 'G', 'İ': 'I', 'Ö': 'O', 'Ş': 'S', 'Ü': 'U'
    }
    try:
        for turkish, english in replacements.items():
            filename = filename.replace(turkish, english)
        filename = re.sub(r'\s+', '_', filename)
        filename = re.sub(r'[^A-Za-z0-9_.-]', '', filename)
        if not filename:
            raise ValueError("Dosya adı boş olamaz")
        return filename
    except Exception as e:
        log(f"Dosya adı temizleme hatası: {e}")
        raise

def load_config():
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            channels_raw = data.get("channels", [])
            channels = [ch if len(ch) == 3 else ch + [False] for ch in channels_raw]
            return channels, data.get("ONLY_HIGHEST", 1)
    except Exception as e:
        log(f"Config dosyasından kanallar okunamadı: {e}")
        return [], 1

def save_config(channels, only_highest):
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            config_data = {
                "ONLY_HIGHEST": only_highest,
                "channels": channels
            }
            json.dump(config_data, f, indent=4, ensure_ascii=False)
            log("Config dosyası 'Oto' güncellemeleriyle kaydedildi.")
    except Exception as e:
        log(f"Config kaydetme hatası: {e}")

# --- M3U8 ALMA FONKSİYONLARI (server.pyw'den taşındı) ---
def clean_link(link):
    decoded_link = html.unescape(link)
    stripped_link = decoded_link.strip().rstrip("'\",)")
    return stripped_link

def scrape_m3u8_from_website(url):
    try:
        log(f"Web sitesi taranıyor: {url}")
        r = requests.get(url, timeout=15, verify=False, headers={'User-Agent': 'Mozilla/5.0'})
        r.raise_for_status()
        content = r.text
        regex_patterns = [
            r'(https?://[^\s"\'`<>]+?\.m3u8\?[^\s"\'`<>]*app=[^\s"\'`<>]+)',
            r'(https?://[^\s"\'`<>]+?\.m3u8\?[^\s"\'`<>]+)',
            r'(https?://[^\s"\'`<>]+?\.m3u8)'
        ]
        found_links = set()
        for pattern in regex_patterns:
            matches = re.findall(pattern, content)
            for match in matches:
                found_links.add(clean_link(match))
            if found_links:
                break
        log(f"{len(found_links)} adet M3U8 linki bulundu: {found_links}")
        return list(found_links)[0] if found_links else None
    except requests.RequestException as e:
        log(f"Web sitesi kazıma hatası ({url}): {e}")
        return None

def get_youtube_m3u8_url(video_or_channel_id):
    headers = {'origin': 'https://www.youtube.com', 'referer': 'https://www.youtube.com/', 'user-agent': 'Mozilla/5.0'}
    video_id = None
    if not video_or_channel_id.startswith(('UC', '@')):
        log(f"Girdi bir Video ID'si olarak kabul ediliyor: {video_or_channel_id}")
        video_id = video_or_channel_id
    else:
        live_url = f"https://www.youtube.com/channel/{video_or_channel_id}/live" if video_or_channel_id.startswith('UC') else f"https://www.youtube.com/{video_or_channel_id}/live"
        log(f"Kanal sayfası taranıyor: {live_url}")
        try:
            r = requests.get(live_url, headers=headers, timeout=10)
            r.raise_for_status()
            soup = BeautifulSoup(r.text, "html.parser")
            canonical_link = soup.find("link", rel="canonical")
            if canonical_link and canonical_link.get("href"):
                match = re.search(r"v=([a-zA-Z0-9_-]{11})", canonical_link.get("href"))
                if match:
                    video_id = match.group(1)
                    log(f"Kanalın canlı yayın videosu bulundu: {video_id}")
        except requests.RequestException as e:
            log(f"Canlı yayın sayfası alınamadı ({live_url}): {e}")
            return None
    if not video_id:
        log(f"Canlı yayın videosu bulunamadı. Kanal çevrimdışı olabilir.")
        return None
    params = {'key': 'AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8'}
    json_data = {'context': {'client': {'clientName': 'WEB', 'clientVersion': '2.20231101.05.00'}}, 'videoId': video_id}
    try:
        response = requests.post('https://www.youtube.com/youtubei/v1/player', params=params, headers=headers, json=json_data)
        response.raise_for_status()
        data = response.json()
        return data.get("streamingData", {}).get("hlsManifestUrl")
    except requests.RequestException as e:
        log(f"m3u8 URL alma hatası (video_id: {video_id}): {e}")
        return None

def search_youtube_innertube(query):
    log(f"InnerTube ile YouTube araması yapılıyor: '{query}'")
    headers = {'origin': 'https://www.youtube.com', 'referer': 'https://www.youtube.com/', 'user-agent': 'Mozilla/5.0'}
    payload = {
        'context': { 'client': { 'clientName': 'WEB', 'clientVersion': '2.20240101.00.00' } },
        'query': query, 'params': 'EgJAAQ%3D%3D'
    }
    try:
        response = requests.post('https://www.youtube.com/youtubei/v1/search', headers=headers, json=payload, timeout=20)
        response.raise_for_status()
        data = response.json()
        contents = data['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents']
        for item in contents:
            if 'videoRenderer' in item:
                video_id = item['videoRenderer'].get('videoId')
                badges = item['videoRenderer'].get('badges', [])
                is_live = any(b.get('metadataBadgeRenderer', {}).get('style') == 'BADGE_STYLE_TYPE_LIVE_NOW' for b in badges)
                if video_id and is_live:
                    log(f"Canlı yayın bulundu: Video ID = {video_id}")
                    return video_id
        for item in contents:
            if 'videoRenderer' in item and item['videoRenderer'].get('videoId'):
                video_id = item['videoRenderer']['videoId']
                log(f"Canlı yayın bulunamadı, ilk sonuç döndürülüyor: Video ID = {video_id}")
                return video_id
    except Exception as e:
        log(f"YouTube arama (InnerTube) hatası: {e}")
    return None

def get_resolution_label(height):
    if not isinstance(height, int) or height <= 0: return ""
    if height >= 1080: return " FULL HD"
    elif height >= 720: return " HD"
    else: return " SD"

# --- OTOMATİK GÜNCELLEME VE GITHUB İŞLEMLERİ ---
def auto_update_channel_ids():
    log("Otomatik Video ID güncelleme süreci başlatılıyor...")
    channels, only_highest = load_config()
    original_channels = copy.deepcopy(channels)
    channels_to_update = [channel for channel in channels if channel[2]]
    
    if not channels_to_update:
        log("'Oto' olarak işaretlenmiş kanal bulunamadı. Güncelleme atlanıyor.")
        return

    log(f"{len(channels_to_update)} adet 'Oto' kanal güncellenecek.")
    for channel in channels_to_update:
        channel_name, _, _ = channel
        log(f"'{channel_name}' için canlı yayın aranıyor...")
        search_query = f"{channel_name} canlı yayını"
        new_video_id = search_youtube_innertube(search_query)
        if new_video_id and new_video_id != channel[1]:
            log(f"'{channel_name}' için yeni Video ID bulundu: {new_video_id}. Config güncelleniyor.")
            channel[1] = new_video_id
        elif new_video_id:
            log(f"'{channel_name}' için bulunan ID ({new_video_id}) zaten mevcut. Değişiklik yapılmadı.")
        else:
            log(f"'{channel_name}' için yeni canlı yayın ID'si bulunamadı. Mevcut ID korunuyor.")
            
    if original_channels != channels:
        log("Değişiklikler tespit edildi, config.json dosyası güncelleniyor.")
        save_config(channels, only_highest)
    else:
        log("Config dosyasında herhangi bir değişiklik yapılmadı.")

def get_github_details_from_remote():
    try:
        result = subprocess.run(
            ["git", "config", "--get", "remote.origin.url"],
            check=True, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW
        )
        url = result.stdout.strip()
        match = re.search(r'(?:[:/])([^/]+)/([^/]+?)(?:\.git)?$', url)
        if match:
            user, repo = match.groups()
            log(f"GitHub detayları bulundu: Kullanıcı={user}, Repo={repo}")
            return user, repo
        log("Hata: Git remote URL'si anlaşılamadı.")
        return None, None
    except Exception as e:
        log(f"GitHub detayları alınamadı: {e}")
        return None, None

def generate_master_playlist(channel_data, user, repo):
    base_url = f"https://raw.githubusercontent.com/{user}/{repo}/main/m3u8"
    playlist_content = ['#EXTM3U']
    for data in channel_data:
        channel_name, resolution_label = data['name'], data['label']
        sanitized_name = sanitize_filename(channel_name).upper()
        file_name = f"{sanitized_name}.m3u8"
        full_url = f"{base_url}/{file_name}"
        final_channel_name = f"{channel_name}{resolution_label}"
        extinf_line = f'#EXTINF:-1,{final_channel_name}'
        playlist_content.extend([extinf_line, full_url])
    try:
        with open("tv.m3u8", "w", encoding="utf-8") as f:
            f.write("\n".join(playlist_content))
        log("Ana playlist dosyası 'tv.m3u8' başarıyla oluşturuldu/güncellendi.")
    except IOError as e:
        log(f"Ana playlist dosyası yazılırken hata: {e}")

def git_operations():
    try:
        if not os.path.exists(".git"):
            log("Hata: Git deposu bulunamadı")
            raise RuntimeError("Git deposu bulunamadı")
        result = subprocess.run(["git", "status", "--porcelain"], check=True, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
        if not result.stdout.strip():
            log("Değişiklik yok, Git işlemleri atlanıyor")
            return
        log("Git değişiklikleri:\n" + result.stdout.strip())
        subprocess.run(["git", "add", "."], check=True, creationflags=subprocess.CREATE_NO_WINDOW)
        timestamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        try:
            subprocess.run(["git", "commit", "-m", timestamp], check=True, creationflags=subprocess.CREATE_NO_WINDOW)
            log("Commit başarılı")
        except subprocess.CalledProcessError as e:
            if "nothing to commit" in (e.stderr or ""):
                log("Commit atlandı (değişiklik yok)")
            else:
                raise
        
        # Push denemeleri
        push_result = subprocess.run(["git", "push"], capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
        if push_result.returncode == 0:
            log("git push başarılı")
            return
        
        error_msg = push_result.stderr or push_result.stdout
        log(f"git push hatası: {error_msg}")
        if "fetch first" in error_msg or "rejected" in error_msg:
            log("Push reddedildi, önce pull --rebase deneniyor...")
            subprocess.run(["git", "pull", "--rebase"], check=True, creationflags=subprocess.CREATE_NO_WINDOW)
            subprocess.run(["git", "push"], check=True, creationflags=subprocess.CREATE_NO_WINDOW)
            log("Pull --rebase + Push başarılı")
    except subprocess.CalledProcessError as e:
        log(f"Git komut hatası: {e.stderr or e.stdout}")
    except RuntimeError as e:
        log(str(e))


# --- ANA İŞLEM AKIŞI ---
def main():
    log("="*40)
    log("Sunucusuz M3U8 İşleyici Başlatıldı")
    log("="*40)

    # 1. 'Oto' kanalları güncelle
    auto_update_channel_ids()

    # 2. Config dosyasını son haliyle yükle
    channels_config, only_highest = load_config()
    os.makedirs(M3U8_DIR, exist_ok=True)
    log(f"'{M3U8_DIR}' klasörü kontrol edildi/oluşturuldu.")
    
    channel_data_for_playlist = []

    # 3. Her kanalı işle
    for channel_info in channels_config:
        name, url_or_id, _ = channel_info
        log(f"İşleniyor: {name} - Kaynak: {url_or_id}")

        master_m3u8_url = None
        # Kaynak tipine göre master M3U8 linkini al
        if url_or_id.startswith(('http://', 'https://')):
            master_m3u8_url = scrape_m3u8_from_website(url_or_id)
        else:
            master_m3u8_url = get_youtube_m3u8_url(url_or_id)
        
        if not master_m3u8_url:
            log(f"'{name}' için ana M3U8 URL'si alınamadı. Atlanıyor.")
            channel_data_for_playlist.append({'name': name, 'label': ''})
            continue

        log(f"Alınan ana M3U8 adresi: {master_m3u8_url}")
        
        try:
            # Ana M3U8 içeriğini indir
            hls_response = requests.get(master_m3u8_url, timeout=60, headers={'User-Agent': 'Mozilla/5.0'})
            hls_response.raise_for_status()
            
            # İçeriği işle ve çözünürlükleri bul
            lines = hls_response.text.splitlines()
            streams = []
            max_height = 0
            
            for i, line in enumerate(lines):
                if line.startswith('#EXT-X-STREAM-INF'):
                    match = re.search(r'RESOLUTION=\d+x(\d+)', line)
                    height = int(match.group(1)) if match else 0
                    
                    if i + 1 < len(lines):
                        stream_url = lines[i+1]
                        if not stream_url.startswith('http'):
                            stream_url = urljoin(master_m3u8_url, stream_url)
                        streams.append({'line': line, 'url': stream_url, 'height': height})
                        if height > max_height:
                            max_height = height
            
            resolution_label = get_resolution_label(max_height)
            channel_data_for_playlist.append({'name': name, 'label': resolution_label})
            log(f"'{name}' için en yüksek çözünürlük bulundu: {max_height}p, Etiket: '{resolution_label.strip()}'")

            # Ayara göre yeni M3U8 içeriğini oluştur
            final_m3u8_content = ""
            if not streams: # Eğer çözünürlük bilgisi yoksa (tekli akış)
                final_m3u8_content = hls_response.text
            elif only_highest == 1:
                highest_stream = max(streams, key=lambda x: x['height'])
                final_m3u8_content = '\n'.join(['#EXTM3U', '#EXT-X-INDEPENDENT-SEGMENTS', highest_stream['line'], highest_stream['url']])
            else: # Tümünü seç
                content_parts = ['#EXTM3U', '#EXT-X-INDEPENDENT-SEGMENTS']
                for s in sorted(streams, key=lambda x: x['height'], reverse=True):
                    content_parts.extend([s['line'], s['url']])
                final_m3u8_content = '\n'.join(content_parts)

            # Dosyaya yaz
            filename = f"{sanitize_filename(name).upper()}.m3u8"
            filepath = os.path.join(M3U8_DIR, filename)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(final_m3u8_content)
            log(f"Kaydedildi: {filepath}")

        except RequestException as e:
            log(f"'{name}' için M3U8 içeriği indirilemedi veya işlenemedi: {e}")
            channel_data_for_playlist.append({'name': name, 'label': ''})
            continue

    # 4. Ana playlist dosyasını oluştur
    github_user, github_repo = get_github_details_from_remote()
    if github_user and github_repo:
        generate_master_playlist(channel_data_for_playlist, github_user, github_repo)
    else:
        log("GitHub kullanıcı/repo bilgisi alınamadığı için ana playlist oluşturulamadı.")

    # 5. Değişiklikleri GitHub'a push'la
    git_operations()
    
    log("İşlem tamamlandı.")

if __name__ == "__main__":
    main()