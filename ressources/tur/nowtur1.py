import requests
import re
import os

# Qovluq yolu və fayl adı
output_dir = 'output'
output_file = 'stream_url.txt'

# Qovluğu yoxlayın və əgər yoxdursa yaradın
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

url = 'https://www.nowtv.com.tr/canli-yayin'
response = requests.get(url, verify=False)

if response.status_code == 200:
    match = re.search(r"daiUrl\s*:\s*'(https?://[^\']+)'", response.text)
  
    if match:
        erstrm = match.group(1)
        
        # Fayla yazmaq üçün tam yol
        file_path = os.path.join(output_dir, output_file)
        
        # Fayla yazma əməliyyatı
        with open(file_path, 'w') as file:
            file.write(erstrm)
        
        # Yalnız URL-i çıxarın
        print(erstrm)
    else:
        print("erstrm not found in the content.")
else:
    print(f"Failed to fetch content. HTTP Status code: {response.status_code}")
