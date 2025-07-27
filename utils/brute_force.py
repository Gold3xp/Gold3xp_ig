import bcrypt
from colorama import Fore

def generate_passwords(username):
    # Pola umum: nama123, nama2024, nama12345, dst.
    return [
        username + "123",
        username + "12345",
        username + "2024",
        username + "2025",
        username + "@",
        username + "!"
    ]

def brute_force_attack(followers, hash_db):
    for user in followers:
        print(Fore.BLUE + f"[*] Mencoba password untuk {user}...")
        if user not in hash_db:
            print(Fore.MAGENTA + f"[!] {user} tidak ada di hash_db.json\n")
            continue

        hashed_pw = hash_db[user]
        passwords = generate_passwords(user)

        for pw in passwords:
            if bcrypt.checkpw(pw.encode(), hashed_pw.encode()):
                print(Fore.GREEN + f"[✅] Password ditemukan untuk {user}: {pw}\n")
                break
        else:
            print(Fore.RED + f"[❌] Password tidak ditemukan untuk {user}\n")
