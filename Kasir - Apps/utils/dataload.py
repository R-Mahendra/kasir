import json
import os

def loadMenu():
    base = os.path.dirname(os.path.dirname(__file__))
    path = os.path.join(base, "data", "menu.json")

    if not os.path.exists(path):
        raise FileNotFoundError(f"File menu.json tidak ditemukan di: {path}")

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Validasi struktur
    if "Makanan" not in data or "Minum" not in data:
        raise ValueError("Struktur JSON tidak valid. Harus ada key 'Makanan' dan 'Minum'.")

    return data
