import os

LICENSE_FILE = "license.key"
VALID_KEYS_FILE = "valid_keys.txt"

def is_license_valid() -> bool:
    try:
        with open(LICENSE_FILE, "r") as file:
            key = file.read().strip()
        with open(VALID_KEYS_FILE, "r") as file:
            valid_keys = [line.strip() for line in file]
        return key in valid_keys
    except FileNotFoundError:
        print("❌ File license.key atau valid_keys.txt tidak ditemukan.")
        return False

def get_or_create_license():
    if not os.path.exists(LICENSE_FILE):
        key = input("🔑 Masukkan lisensi: ").strip()
        with open(LICENSE_FILE, "w") as file:
            file.write(key)
