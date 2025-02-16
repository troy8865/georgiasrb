import os
import re
import requests

def find_m3u8_links(url):
    # Saytdan məzmunu çək
    response = requests.get(url)
    if response.status_code != 200:
        print("Sayta giriş uğursuz oldu.")
        return []

    # M3U8 linklərini tap
    m3u8_links = re.findall(r'https?://[^\s]+\.m3u8', response.text)
    return m3u8_links

def save_m3u8_to_file(links, folder):
    # Qovluq yarat
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Hər bir linki fayl kimi saxla
    for i, link in enumerate(links):
        file_path = os.path.join(folder, f'stream_{i+1}.m3u8')
        with open(file_path, 'w') as f:
            f.write(link)
        print(f'{file_path} faylına yazıldı: {link}')

if __name__ == "__main__":
    # Saytın URL-i (buraya öz linkinizi əlavə edin)
    url = "https://www.canlitv.my/showtv"  # Nümunə olaraq

    # M3U8 linklərini tap
    m3u8_links = find_m3u8_links(url)

    if m3u8_links:
        # M3U8 linklərini fayl kimi saxla
        save_m3u8_to_file(m3u8_links, 'm3u8_files')
    else:
        print("Heç bir M3U8 linki tapılmadı.")
