import os

LICENSE_FILE = "license.key"

def is_license_valid(key: str) -> bool:
    try:
        with open("valid_keys.txt", "r") as file:
            valid_keys = [line.strip() for line in file.readlines()]
        return key in valid_keys
    except FileNotFoundError:
        print("❌ File valid_keys.txt tidak ditemukan.")
        return False

def get_or_create_license():
    if os.path.exists(LICENSE_FILE):
        with open(LICENSE_FILE, "r") as f:
            return f.read().strip()
    else:
        key = input("🔑 Masukkan license key: ").strip()
        with open(LICENSE_FILE, "w") as f:
            f.write(key)
        return key
