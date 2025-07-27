from colorama import Fore
import time
import random

def brute_force_attack(user_list, hash_db):
    for user in user_list:
        username = user['username']
        print(Fore.CYAN + f"⏳ Mencoba login untuk: {username}")

        # Daftar password brute force berdasarkan pola umum
        password_list = [
            username + "123",
            username + "1234",
            username + "12345",
            username + "123456",
            username + "2024",
            username + "2025",
            username + "!",
            username + "!",
            username + "@123",
            username + "#123",
            username + "_123",
            username.lower(),
            username.upper()
        ]

        # Tambahan kombinasi angka sederhana
        password_list += [username + str(i) for i in range(10)]  # user0 - user9
        password_list += [username + str(i).zfill(2) for i in range(100)]  # user00 - user99

        for password in password_list:
            hashed = hash(password)
            if str(hashed) in hash_db:
                print(Fore.GREEN + f"✅ Berhasil: {username} | {password}")
                break
            else:
                print(Fore.RED + f"❌ Gagal: {username} | {password}")
            time.sleep(random.uniform(0.5, 1.5))

        print(Fore.YELLOW + "-" * 40)
