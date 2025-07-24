from instagrapi import Client
import time

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

cl = Client()
ui = input("IG Username: ")
pi = input("IG Password: ")
cl.login(ui, pi)

foll = cl.user_followers(cl.user_id_from_username(ui), amount=10)
users = [info.username for info in foll.values()]
print(f"\n✅ Dapat {len(users)} followers\n")

wlist = list({pw for u in users for pw in generate(u)})
print(f"🔧 Wordlist dibuat: {len(wlist)} password kemungkinan\n")

for u in users:
    print(f"🔍 Simulasi login: {u}")
    ok = False
    for pw in wlist:
        if pw.startswith(u):
            print(f"  🔑 Coba: {pw}")
            if cek_login(u, pw):
                print(f"✅ BERHASIL: {u} | {pw}\n")
                ok = True
                break
            time.sleep(0.2)
    if not ok:
        print(f"❌ GAGAL: {u}\n")
