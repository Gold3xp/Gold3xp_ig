def is_license_valid() -> bool:
    try:
        with open("license.key", "r") as file:
            key = file.read().strip()
        with open("valid_keys.txt", "r") as file:
            valid_keys = [line.strip() for line in file]
        return key in valid_keys
    except FileNotFoundError:
        print("❌ File license.key atau valid_keys.txt tidak ditemukan.")
        return False

def get_or_create_license():
    if not os.path.exists("license.key"):
        key = input("🔑 Masukkan lisensi: ").strip()
        with open("license.key", "w") as file:
            file.write(key)
