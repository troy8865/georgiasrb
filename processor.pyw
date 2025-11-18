import subprocess
import sys
import urllib3

# HTTPS sertifikası uyarılarını kapat (güvenli değil, sadece uyarıyı gizler)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def run_subprocess(command):
    """
    subprocess.run wrapper'ı
    Windows'ta CREATE_NO_WINDOW kullanır, Linux/macOS'ta kullanmaz.
    """
    if sys.platform.startswith("win"):
        result = subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
    else:
        result = subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True
        )
    return result.stdout

def git_operations():
    """Git işlemleri"""
    print("Git durumu kontrol ediliyor...")
    output = run_subprocess(["git", "status", "--porcelain"])
    print(output)
    return output

def main():
    print("Program başlatılıyor...")
    
    # Örnek: git işlemleri
    git_operations()
    
    # Burada diğer işlemlerini çağırabilirsin
    print("Program tamamlandı.")

if __name__ == "__main__":
    main()
