import json
from utils.scraper import get_followers_dummy
from utils.brute_force import coba_brute_force
from colorama import Fore, init

init(autoreset=True)

def load_hash_db(path="hash_db.json"):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(Fore.RED + "[!] hash_db.json tidak ditemukan.")
        return {}

if __name__ == "__main__":
    target_username = input("Masukkan username target untuk scrape followers: ")
    followers = get_followers_dummy(target_username)
    print(Fore.YELLOW + f"[•] Jumlah followers ditemukan: {len(followers)}")

    hash_db = load_hash_db()

    for user in followers:
        if user in hash_db:
            coba_brute_force(user, hash_db[user])
        else:
            print(Fore.MAGENTA + f"[?] {user} tidak ada di database hash.")
