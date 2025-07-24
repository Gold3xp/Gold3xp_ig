import os
from hashlib import sha256

def is_license_valid(key: str) -> bool:
    path = "valid_keys.txt"
    if not os.path.exists(path):
        print("❌ File valid_keys.txt tidak ditemukan.")
        return False

    with open(path, "r") as file:
        valid_keys = [line.strip() for line in file if line.strip()]
    return key.strip() in valid_keys

def hash_pin(pin: str) -> str:
    return sha256(pin.encode()).hexdigest()

def save_license(key: str, pin: str):
    encrypted = {
        "key": key.strip(),
        "pin_hash": hash_pin(pin)
    }
    import json
    with open("license.key", "w") as f:
        json.dump(encrypted, f)

def load_license():
    import json
    if not os.path.exists("license.key"):
        return None
    with open("license.key", "r") as f:
        return json.load(f)
