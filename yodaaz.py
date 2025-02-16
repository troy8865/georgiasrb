import requests
from bs4 import BeautifulSoup
import re
import os

# Saytın URL-i
url = 'https://yoda.az/'

# Çıxış qovluğu
output_folder = 'm3u8_links'
os.makedirs(output_folder, exist_ok=True)

# Saytın məzmununu əldə et
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# M3U8 linklərini tap
m3u8_links = set()
for tag in soup.find_all('a', href=True):
    href = tag['href']
    if re.search(r'\.m3u8$', href):
        m3u8_links.add(href)

# M3U8 linklərini fayla yaz
output_file = os.path.join(output_folder, 'm3u8_links.txt')
with open(output_file, 'w') as f:
    for link in m3u8_links:
        f.write(link + '\n')

print(f"{len(m3u8_links)} m3u8 linki tapıldı və {output_file} faylına yazıldı.")
