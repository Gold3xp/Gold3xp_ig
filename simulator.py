from instagrapi import Client
import time, os
from utils.banner import tampilkan_banner
from utils.license_check import is_license_valid, get_or_create_license  # tambahkan ini

# Simulasi akun valid
akun_valid = {
    "akun1": "akun1123",
    "akun2": "akun2@123",
    "giyanjp": "giyanjp2025"
}

def cek_login(u, p):
    return akun_valid.get(u) == p

def generate(u):
    return list({u, u + "123", "123" + u, u + "@123", u + "2025", u.capitalize(), u.upper()})

def clear_terminal():
    os.system("clear")

def simpan_hasil(username, password):
    with open("hasil_sukses.txt", "a") as f:
        f.write(f"{username} | {password}\n")

# ==== Jalankan ====
clear_terminal()
tampilkan_banner()

# Cek lisensi dulu (input jika belum ada)
get_or_create_license()  # <== fungsi ini otomatis input lisensi kalau license.key belum ada
if not is_license_valid():
    print("❌ Lisensi tidak valid. Hubungi admin.")
    exit()

# Login Instagram
cl = Client()
ui = input("IG Username: ")
pi = input("IG Password: ")
cl.login(ui, pi)

# Ambil followers
foll = cl.user_followers(cl.user_id_from_username(ui), amount=0)
users = [info.username for info in foll.values()]
print(f"\n✅ Dapat {len(users)} followers\n")

# Buat wordlist berdasarkan username
wlist = list({pw for u in users for pw in generate(u)})
print(f"🔧 Wordlist dibuat: {len(wlist)} password kemungkinan\n")

# Simulasi brute force login lokal
for u in users:
    print(f"🔍 Simulasi login: {u}")
    ok = False
    for pw in wlist:
        if pw.startswith(u):
            print(f"  🔑 Coba: {pw}")
            if cek_login(u, pw):
                print(f"✅ BERHASIL: {u} | {pw}\n")
                simpan_hasil(u, pw)
                ok = True
                break
            time.sleep(0.2)
    if not ok:
        print(f"❌ GAGAL: {u}\n")
