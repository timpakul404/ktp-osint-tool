# ================== CONFIGURASI API KEY ==================

# Ganti dengan API Key kamu dari https://api.co.id
API_KEY = "curl -X POST https://use.api.co.id/ocr/ktp-extract \
  -H "x-api-co-id: XdnLfGDNMYvODBs7WkukwfHhajPtatdzcQzXokwrhyguPddbGG" \
  -F "file=@input/ktp.jpg""

# =========================================================

# Pengaturan lain (bisa diubah)
API_URL = "https://use.api.co.id/ocr/ktp-extract"
INPUT_FOLDER = "input"
OUTPUT_FOLDER = "output"

# Warna untuk tampilan di Termux
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    RESET = '\033[0m'
