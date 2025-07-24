from instagrapi import Client
import time, os
from colorama import Fore, init

# Inisialisasi colorama
init(autoreset=True)

# ===== Simulasi akun lokal valid
akun_valid = {
    "akun1": "akun1123",
    "akun2": "akun2@123",
    "giyanjp": "giyanjp2025"
}

def cek_login(u, p):
    return akun_valid.get(u) == p

def generate(u):
    return [
        u, u + "123", "123" + u, u + "@123",
        u + "2025", u.capitalize(), u.upper()
    ]

def clear_terminal():
    os.system("clear")

def tampilkan_banner():
    banner = f"""{Fore.CYAN}
  ____ ___  _   _ ____  _   _ ___ ____  ____  
 / ___/ _ \| \ | |  _ \| | | |_ _|  _ \|  _ \ 
| |  | | | |  \| | | | | | | || || |_) | | | |
| |__| |_| | |\  | |_| | |_| || ||  __/| |_| |
 \____\___/|_| \_|____/ \___/|___|_|   |____/ 
     IG Bruteforce Simulator - by Gold3xp
    """
    print(banner)

# ==== Main Program ====
clear_terminal()
tampilkan_banner()

cl = Client()
ui = input(Fore.YELLOW + "IG Username: ")
pi = input(Fore.YELLOW + "IG Password: ")
cl.login(ui, pi)

foll = cl.user_followers(cl.user_id_from_username(ui), amount=10)
users = [info.username for info in foll.values()]
print(Fore.GREEN + f"\n✅ Dapat {len(users)} followers\n")

wlist = list({pw for u in users for pw in generate(u)})
print(Fore.CYAN + f"🔧 Wordlist dibuat: {len(wlist)} password kemungkinan\n")

for u in users:
    print(Fore.YELLOW + f"🔍 Simulasi login: {u}")
    ok = False
    for pw in wlist:
        if pw.startswith(u):
            print(Fore.BLUE + f"  🔑 Coba: {pw}")
            if cek_login(u, pw):
                print(Fore.GREEN + f"✅ BERHASIL: {u} | {pw}\n")
                ok = True
                break
            time.sleep(0.2)
    if not ok:
        print(Fore.RED + f"❌ GAGAL: {u}\n")
