import requests
import os
import json
from datetime import datetime
from config import API_KEY, API_URL, INPUT_FOLDER, OUTPUT_FOLDER, Colors

# Membuat folder jika belum ada
os.makedirs(INPUT_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def print_banner():
    print(f"{Colors.GREEN}")
    print("="*50)
    print("     KTP OSINT TOOL - API OCR")
    print("     Ekstrak Data KTP Indonesia")
    print("="*50)
    print(f"{Colors.RESET}")

def main():
    print_banner()
    
    if not API_KEY or API_KEY == "masukkan_api_key_kamu_disini":
        print(f"{Colors.RED}❌ API Key belum diisi!{Colors.RESET}")
        print("Silakan edit file config.py dan masukkan API Key kamu.")
        return

    # Daftar file di folder input
    files = [f for f in os.listdir(INPUT_FOLDER) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    
    if not files:
        print(f"{Colors.YELLOW}⚠️  Tidak ada foto KTP di folder '{INPUT_FOLDER}'{Colors.RESET}")
        print(f"   Masukkan foto KTP ke folder '{INPUT_FOLDER}' lalu jalankan lagi.")
        return

    print(f"{Colors.GREEN}✅ Ditemukan {len(files)} foto KTP{Colors.RESET}\n")

    for idx, filename in enumerate(files, 1):
        filepath = os.path.join(INPUT_FOLDER, filename)
        print(f"{Colors.YELLOW}[{idx}/{len(files)}] Memproses: {filename}{Colors.RESET}")
        
        try:
            with open(filepath, "rb") as image_file:
                files_data = {"file": image_file}
                headers = {"x-api-co-id": API_KEY}
                
                response = requests.post(API_URL, headers=headers, files=files_data, timeout=30)
                
                if response.status_code == 200:
                    result = response.json()
                    
                    if result.get("is_success"):
                        data = result["data"]
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        output_filename = f"{data.get('nik', 'unknown')}_{timestamp}"
                        
                        # Simpan sebagai JSON
                        with open(f"{OUTPUT_FOLDER}/{output_filename}.json", "w", encoding="utf-8") as f:
                            json.dump(data, f, ensure_ascii=False, indent=4)
                        
                        # Simpan ringkasan TXT
                        with open(f"{OUTPUT_FOLDER}/{output_filename}.txt", "w", encoding="utf-8") as f:
                            f.write(f"KTP OSINT Result - {datetime.now()}\n")
                            f.write("="*40 + "\n")
                            for key, value in data.items():
                                f.write(f"{key.replace('_', ' ').title()}: {value}\n")
                        
                        print(f"{Colors.GREEN}✅ Berhasil!{Colors.RESET}")
                        print(f"   Nama : {data.get('nama', '-')}")
                        print(f"   NIK  : {data.get('nik', '-')}")
                        print(f"   Hasil disimpan di folder '{OUTPUT_FOLDER}'\n")
                        
                    else:
                        print(f"{Colors.RED}❌ Gagal: {result.get('message', 'Unknown error')}{Colors.RESET}\n")
                else:
                    print(f"{Colors.RED}❌ Error HTTP {response.status_code}{Colors.RESET}")
                    print(response.text[:200] + "...\n")
                    
        except Exception as e:
            print(f"{Colors.RED}❌ Error saat memproses {filename}: {str(e)}{Colors.RESET}\n")

    print(f"{Colors.GREEN}✅ Proses selesai!{Colors.RESET}")

if __name__ == "__main__":
    main()
