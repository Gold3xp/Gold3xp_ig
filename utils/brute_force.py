from colorama import Fore
import time
import random

def try_login(username, password, hash_db):
    """
    Fungsi mencocokkan username dan password dengan database hash.
    Return status string: success, fail
    """
    hashed = hash(password)
    if str(hashed) in hash_db:
        print(Fore.GREEN + f"✅ Valid: {username} | {password}")
        return "success"
    else:
        print(Fore.RED + f"❌ Invalid: {username} | {password}")
        return "fail"

def brute_force_attack(user_list, hash_db, save_callback=None, update_callback=None):
    """
    Melakukan brute force pada list user (dict username: fullname).
    Jika berhasil login, panggil callback penyimpanan dan update hash DB.
    """
    for username, full_name in user_list.items():
        print(Fore.CYAN + f"\n⏳ Mencoba login untuk: {username}")
        name_parts = full_name.split(" ")
        base = name_parts[0] if name_parts and name_parts[0] else username

        # Buat daftar password umum
        password_list = [
            base + "123", base + "1234", base + "12345", base + "2024", base + "2025",
            base + "!", base + "@123", base + "#123", base.lower(), base.upper(), base
        ]
        password_list += [base + str(i) for i in range(10)]
        password_list += [base + str(i).zfill(2) for i in range(100)]

        for password in password_list:
            status = try_login(username, password, hash_db)
            if status == "success":
                if save_callback: save_callback(username, password)
                if update_callback:
                    hash_db[username] = str(hash(password))
                    update_callback(hash_db)
                break
            time.sleep(random.uniform(0.5, 1.2))

        print(Fore.YELLOW + "-" * 40)
