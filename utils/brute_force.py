from colorama import Fore
import time
import random

def try_login(username, password, hash_db):
    if username in hash_db:
        return "skipped"

    # Simulasi dummy login
    print(Fore.CYAN + f"⏳ Mencoba login untuk: {username} | {password}")
    time.sleep(random.uniform(0.5, 1.2))

    # Contoh validasi palsu (ganti dengan logic asli jika perlu)
    if password.lower() == "ujian123":
        return "success"
    return "fail"

def threaded_login_attempt(username, password_list, hash_db):
    for password in password_list:
        result = try_login(username, password, hash_db)
        if result == "success":
            print(Fore.GREEN + f"✅ Valid: {username} | {password}")
            return (username, password)
        elif result == "skipped":
            print(Fore.YELLOW + f"🔁 Dilewati (sudah ada): {username}")
            return None
        else:
            print(Fore.RED + f"❌ Invalid: {username} | {password}")
    return None
