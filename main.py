import requests
import os
import json
from datetime import datetime
from config import API_KEY, API_URL, INPUT_FOLDER, OUTPUT_FOLDER, Colors

os.makedirs(INPUT_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def print_banner():
    print(f"{Colors.GREEN}")
    print("="*55)
    print("     KTP OSINT TOOL v2.0")
    print("     Ekstrak Data KTP Indonesia")
    print("="*55)
    print(f"{Colors.RESET}")

def main():
    print_banner()
    
    if API_KEY = "XdnLfGDNMYvODBs7WkukwfHhajPtatdzcQzXokwrhyguPddbGG" or not API_KEY:
        print(f"{Colors.RED}❌ API Key belum diatur!{Colors.RESET}")
        print("Edit file config.py terlebih dahulu.")
        return

    files = [f for f in os.listdir(INPUT_FOLDER) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    
    if not files:
        print(f"{Colors.YELLOW}⚠️ Folder 'input/' kosong.{Colors.RESET}")
        print("Masukkan foto KTP ke folder input/ lalu jalankan lagi.")
        return

    print(f"{Colors.GREEN}✅ Ditemukan {len(files)} foto KTP{Colors.RESET}\n")

    for idx, filename in enumerate(files, 1):
        filepath = os.path.join(INPUT_FOLDER, filename)
        print(f"[{idx}/{len(files)}] Processing: {filename}")
        
        try:
            with open(filepath, "rb") as img:
                response = requests.post(
                    API_URL,
                    headers={"x-api-co-id": API_KEY},
                    files={"file": img},
                    timeout=40
                )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("is_success"):
                    data = result["data"]
                    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                    base_name = data.get('nik', 'unknown')
                    
                    # Save JSON
                    with open(f"{OUTPUT_FOLDER}/{base_name}_{ts}.json", "w", encoding="utf-8") as f:
                        json.dump(data, f, ensure_ascii=False, indent=4)
                    
                    print(f"{Colors.GREEN}✅ Sukses! Nama: {data.get('nama')}{Colors.RESET}")
                    print(f"   NIK: {data.get('nik')}\n")
                else:
                    print(f"{Colors.RED}❌ Gagal: {result.get('message')}{Colors.RESET}\n")
            else:
                print(f"{Colors.RED}❌ HTTP Error: {response.status_code}{Colors.RESET}\n")
                
        except Exception as e:
            print(f"{Colors.RED}❌ Error: {e}{Colors.RESET}\n")

if __name__ == "__main__":
    main()
