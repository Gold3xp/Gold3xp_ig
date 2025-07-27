# hash_generator.py
import bcrypt
import json

def buat_hash(username, password):
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hashed.decode()

username = input("Masukkan username: ")
password = input("Masukkan password asli (untuk di-hash): ")

hashed = buat_hash(username, password)

# Tambahkan ke hash_db.json
with open("hash_db.json", "r+") as f:
    try:
        data = json.load(f)
    except:
        data = {}
    data[username] = hashed
    f.seek(0)
    json.dump(data, f, indent=4)
    f.truncate()

print(f"[✅] Hash untuk '{username}' ditambahkan.")
