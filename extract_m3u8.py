import os
import requests
import time
import random
import string

# Qaynaq linkləri
source_urls = [
    "https://raalbatros.serv00.net:443/ctv.php?url=https://tv.canlitv.vip/saban-tv",
    # Buraya digər m3u8 linklərini əlavə edin
]

# Faylın yadda saxlanacağı qovluq
output_folder = "output"
os.makedirs(output_folder, exist_ok=True)

# Dinamik token və parametrlər yaratmaq üçün funksiya
def generate_dynamic_params():
    # Token və digər parametrləri yaradırıq
    tkn = ''.join(random.choices(string.ascii_letters + string.digits, k=22))  # 22 simvol uzunluğunda təsadüfi token
    tms = str(int(time.time()))  # Cari Unix zamanı (timestamp)
    ip = "91.185.186.151"  # Sabit IP
    return tkn, tms, ip

# Linki yeniləmək üçün funksiya
def update_link(line):
    # Linkin içindəki parametrləri yeniləmək üçün regex istifadə edirik
    if "?" in line and ("tkn=" in line or "tms=" in line or "ip=" in line):
        try:
            # Linki əsas URL və query string-ə bölürük
            base_url, query_string = line.split("?", 1)
            
            # Query string-i parametrlərə ayırırıq
            params = query_string.split("&")
            
            # Yeni parametrləri yaradırıq
            new_params = []
            tkn, tms, ip = generate_dynamic_params()
            for param in params:
                if param.startswith("tkn="):
                    new_params.append(f"tkn={tkn}")
                elif param.startswith("tms="):
                    new_params.append(f"tms={tms}")
                elif param.startswith("ip="):
                    new_params.append(f"ip={ip}")
                else:
                    new_params.append(param)  # Digər parametrləri olduğu kimi saxlayırıq
            
            # Yeni query string-i birləşdiririk
            updated_query_string = "&".join(new_params)
            updated_link = f"{base_url}?{updated_query_string}"
            
            # Linkin ətrafındakı əlavə mətnləri saxlayırıq
            return line.replace(query_string, updated_query_string)
        except Exception as e:
            print(f"Link yenilənməsində xəta: {e}")
            return line
    return line

# m3u8 faylını çıxar və qovluğa yadda saxla
def extract_m3u8(url, index):
    try:
        # m3u8 faylını yüklə
        response = requests.get(url)
        response.raise_for_status()  # Xəta yoxlanışı
        
        # Fayl adını index ilə fərqləndir
        filename = f"stream_{index}.m3u8"
        file_path = os.path.join(output_folder, filename)
        
        # Faylı oxu və içindəki nisbi linkləri tam URL-yə çevir
        m3u8_content = response.text.splitlines()
        
        # Debug: Qaynaq faylının məzmununu çap et
        print("Qaynaq faylının məzmunu:")
        print(m3u8_content)
        
        # Multi-variant m3u8 faylı üçün əsas strukturu yaradırıq
        modified_content = ""
        for line in m3u8_content:
            if line.strip() and not line.startswith("#"):  # Tərkibdə "#" olmayan sətirləri seç
                # Linki yeniləmək üçün funksiya çağırılır
                modified_line = update_link(line)
                modified_content += f"{modified_line}\n"
            else:
                # Əgər sətir meta məlumatdırsa, olduğu kimi saxla
                modified_content += f"{line}\n"
        
        # Faylı qovluğa yaz (üzərinə yaz)
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(modified_content)
        print(f"m3u8 faylı uğurla yeniləndi: {file_path}")
    except Exception as e:
        print(f"Xəta baş verdi: {e}")

# Skriptin əsas hissəsi
if __name__ == "__main__":
    for index, url in enumerate(source_urls):
        if url:  # Əgər URL boş deyilsə
            extract_m3u8(url, index)
