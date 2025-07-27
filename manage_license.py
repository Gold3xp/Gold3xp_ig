from getpass4 import getpass
import os
import hashlib

LICENSE_FILE = "valid_keys.txt"
PIN_FILE = "pin.txt"

def clear():
    os.system("clear")

def hash_pin(pin):
    return hashlib.sha256(pin.encode()).hexdigest()

def ambil_pin():
    try:
        with open(PIN_FILE, "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        print("❌ File pin.txt tidak ditemukan.")
        return None

def masukkan_pin():
    clear()
    pin_hash_asli = ambil_pin()
    if not pin_hash_asli:
        return False
    pin = getpass("🔒 Masukkan PIN: ")
    return hash_pin(pin) == pin_hash_asli

def tambah_lisensi():
    clear()
    key = input("🆕 Masukkan lisensi baru: ").strip()
    with open(LICENSE_FILE, "a") as file:
        file.write(key + "\n")
    print("✅ Lisensi berhasil ditambahkan.")

def hapus_lisensi():
    clear()
    lihat_semua_lisensi()
    hapus = input("\n🗑 Masukkan lisensi yang ingin dihapus: ").strip()
    try:
        with open(LICENSE_FILE, "r") as file:
            keys = [line.strip() for line in file.readlines()]
        if hapus in keys:
            keys.remove(hapus)
            with open(LICENSE_FILE, "w") as file:
                for k in keys:
                    file.write(k + "\n")
            print("✅ Lisensi berhasil dihapus.")
        else:
            print("❌ Lisensi tidak ditemukan.")
    except FileNotFoundError:
        print("⚠️ File valid_keys.txt belum ada.")

def lihat_semua_lisensi():
    clear()
    try:
        with open(LICENSE_FILE, "r") as file:
            keys = [line.strip() for line in file.readlines()]
        if keys:
            print("📋 Daftar Lisensi:")
            for idx, key in enumerate(keys, 1):
                print(f"{idx}. {key}")
        else:
            print("⚠️ Tidak ada lisensi.")
    except FileNotFoundError:
        print("⚠️ File valid_keys.txt belum ada.")

def ubah_pin():
    clear()
    pin_hash_asli = ambil_pin()
    if not pin_hash_asli:
        print("❌ File PIN tidak ditemukan.")
        return

    pin_lama = getpass("🔑 Masukkan PIN lama: ")
    if hash_pin(pin_lama) != pin_hash_asli:
        print("❌ PIN lama salah.")
        return

    pin_baru = getpass("🔐 Masukkan PIN baru: ")
    konfirmasi = getpass("🔐 Konfirmasi PIN baru: ")
    if pin_baru != konfirmasi:
        print("❌ PIN baru tidak cocok.")
        return

    with open(PIN_FILE, "w") as file:
        file.write(hash_pin(pin_baru))
    print("✅ PIN berhasil diubah.")

def setup_pin():
    # Dipanggil pertama kali kalau file pin.txt belum ada
    print("🔐 Setup PIN pertama kali")
    while True:
        pin = getpass("🔐 Masukkan PIN baru: ")
        konfirmasi = getpass("🔐 Konfirmasi PIN baru: ")
        if pin == konfirmasi:
            with open(PIN_FILE, "w") as file:
                file.write(hash_pin(pin))
            print("✅ PIN berhasil dibuat.")
            break
        else:
            print("❌ PIN tidak cocok, ulangi.")

def menu():
    if not os.path.exists(PIN_FILE):
        setup_pin()
    if not masukkan_pin():
        print("❌ PIN salah!")
        return

    while True:
        print("\n=== MANAJEMEN LISENSI ===")
        print("1. Tambah lisensi")
        print("2. Hapus lisensi")
        print("3. Lihat semua lisensi")
        print("4. Ubah PIN")
        print("5. Keluar")
        pilihan = input("Pilih menu (1-5): ").strip()
        if pilihan == "1":
            tambah_lisensi()
        elif pilihan == "2":
            hapus_lisensi()
        elif pilihan == "3":
            lihat_semua_lisensi()
        elif pilihan == "4":
            ubah_pin()
        elif pilihan == "5":
            clear()
            break
        else:
            print("❌ Pilihan tidak valid.")

if __name__ == "__main__":
    menu()
