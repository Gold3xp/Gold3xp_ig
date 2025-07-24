def is_license_valid(key: str) -> bool:
    try:
        with open("valid_keys.txt", "r") as file:
            valid_keys = [line.strip() for line in file.readlines()]
        return key in valid_keys
    except FileNotFoundError:
        print("❌ File valid_keys.txt tidak ditemukan.")
        return False

def get_license_key() -> str:
    try:
        with open("license.key", "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        print("❌ File license.key tidak ditemukan.")
        return None
