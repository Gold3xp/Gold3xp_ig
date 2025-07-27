import re

def generate_passwords(username, full_name): name_parts = full_name.lower().split()

# Pisahkan huruf & angka dari username
username_letters = ''.join(re.findall(r'[a-zA-Z]', username))
username_digits = ''.join(re.findall(r'\d+', username))  # bisa kosong

base_names = list(set([
    username.lower(),
    username.upper(),
    username_letters.lower(),
    username_letters.upper()
] + name_parts))

suffixes = ["", "1", "12", "123", "1234", "12345", "123456", "2024", "2025", "@123", "#123", "_123", "!", "0"]

combinations = set()

for base in base_names:
    for suffix in suffixes:
        pwd = base + suffix
        if len(pwd) >= 6:
            combinations.add(pwd)

# Tambahan angka 0–9
for i in range(10):
    combinations.add(username_letters + str(i))

# Tambahan angka 00–99
for i in range(100):
    combinations.add(username_letters + str(i).zfill(2))

# Variasi dari digit di username (misal: 771 → 77, 71, 17, dll)
if username_digits:
    for i in range(len(username_digits)):
        for j in range(i+1, len(username_digits)+1):
            digit_part = username_digits[i:j]
            if digit_part:
                pwd = username_letters + digit_part
                if len(pwd) >= 6:
                    combinations.add(pwd)

return list(combinations)

