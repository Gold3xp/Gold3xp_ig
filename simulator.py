from instagrapi import Client
from colorama import Fore, init
import time, os
from utils.banner import tampilkan_banner
from utils.license_check import is_license_valid

init(autoreset=True)  # colorama otomatis reset warna

# Akun simulasi login lokal
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

def simpan_hasil(cl, username, password):
    try:
        user_info = cl.user_info_by_username(username)
        post = user_info.media_count
        followers = user_info.follower_count
        following = user_info.following_count

        with open("hasil_sukses.txt", "a") as f:
            f.write(f"{username} | {password} | Postingan: {post} | Followers: {followers} | Following: {following}\n")
        
        print(Fore.GREEN + f"✅ {username} | {password} | Postingan: {post} | Followers: {followers} | Following: {following}")
    except Exception as e:
        print(Fore.RED + f"❌ Gagal ambil info akun: {e}")

def clear_terminal():
    os.system("clear" if os.name == "posix" else "cls")

def cek_lisensi():
    print(Fore.YELLOW + "🔑 CEK LISENSI")
    lisensi = input("Masukkan kode lisensi: ")
    if not is_license_valid(lisensi):
        print(Fore.RED + "❌ Lisensi tidak valid.")
        exit()
    print(Fore.GREEN + "✅ Lisensi valid.\n")

def main():
    clear_terminal()
    tampilkan_banner()
    cek_lisensi()

    cl = Client()
    ui = input("👤 IG Username: ")
    pi = input("🔐 IG Password: ")
    try:
        cl.login(ui, pi)
    except Exception as e:
        print(Fore.RED + f"❌ Gagal login: {e}")
        return

    try:
        user_id = cl.user_id_from_username(ui)
        followers = cl.user_followers(user_id, amount=0)
        users = [info.username for info in followers.values()]
    except Exception as e:
        print(Fore.RED + f"❌ Gagal ambil followers: {e}")
        return

    wordlist = list({pw for u in users for pw in generate(u)})

    # Jalankan brute force simulasi
    for u in users:
        berhasil = False
        for pw in wordlist:
            if pw.startswith(u):  # kombinasi logis
                if cek_login(u, pw):
                    simpan_hasil(cl, u, pw)
                    berhasil = True
                    break
                time.sleep(0.2)
        if not berhasil:
            pass  # tidak tampilkan hasil gagal, sesuai permintaan

if __name__ == "__main__":
    main()
