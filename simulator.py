from instagrapi import Client
import time, os
from utils.banner import tampilkan_banner
from utils.license_check import is_license_valid, get_or_create_license

# Akun simulasi untuk login (tidak terhubung ke Instagram asli)
akun_valid = {
    "akun1": "akun1123",
    "akun2": "akun2@123",
    "giyanjp": "giyanjp2025"
}

def cek_login(username, password):
    return akun_valid.get(username) == password

def generate(username):
    return list({
        username,
        username + "123",
        "123" + username,
        username + "@123",
        username + "2025",
        username.capitalize(),
        username.upper()
    })

def simpan_hasil(username, password):
    with open("hasil_sukses.txt", "a") as f:
        f.write(f"{username} | {password}\n")

def clear_terminal():
    os.system("clear")

# ========== MULAI PROGRAM ==========
clear_terminal()
tampilkan_banner()

# ✅ Cek lisensi dari file atau input jika belum ada
get_or_create_license()
if not is_license_valid():
    print("❌ Lisensi tidak valid. Hubungi admin.")
    exit()

# 🟢 Login akun kamu untuk ambil followers
cl = Client()
ui = input("👤 IG Username: ")
pi = input("🔐 IG Password: ")
try:
    cl.login(ui, pi)
except Exception as e:
    print(f"❌ Gagal login: {e}")
    exit()

# 📥 Ambil followers akun yang login
try:
    user_id = cl.user_id_from_username(ui)
    followers = cl.user_followers(user_id, amount=0)
    users = [info.username for info in followers.values()]
    print(f"\n✅ Dapat {len(users)} followers\n")
except Exception as e:
    print(f"❌ Gagal ambil followers: {e}")
    exit()

# 🔧 Buat wordlist kombinasi password dari username
wordlist = list({pw for u in users for pw in generate(u)})
print(f"🔧 Wordlist dibuat: {len(wordlist)} kemungkinan password\n")

# 🔐 Simulasi brute force
for u in users:
    print(f"🔍 Simulasi login: {u}")
    berhasil = False
    for pw in wordlist:
        if pw.startswith(u):  # hanya coba password logis
            print(f"  🔑 Coba: {pw}")
            if cek_login(u, pw):
                print(f"✅ BERHASIL: {u} | {pw}\n")
                simpan_hasil(u, pw)
                berhasil = True
                break
            time.sleep(0.2)
    if not berhasil:
        print(f"❌ GAGAL: {u}\n")
