import os

def is_license_valid(key: str) -> bool:
    try:
        with open("valid_keys.txt", "r") as file:
            valid_keys = [line.strip() for line in file if line.strip()]
        return key.strip() in valid_keys
    except FileNotFoundError:
        print("❌ File valid_keys.txt tidak ditemukan.")
        return False
