def generate_passwords(username, full_name):
    name_parts = full_name.lower().split()
    base_names = [username.lower(), username.upper()] + name_parts

    suffixes = ["", "123", "1234", "12345", "123456", "2024", "2025", "@123", "#123", "_123", "!", "1", "0"]

    combinations = set()

    # Kombinasi dasar dengan suffix
    for base in base_names:
        for suffix in suffixes:
            pwd = base + suffix
            if len(pwd) >= 6:
                combinations.add(pwd)

    # Tambahan angka sederhana (0–9)
    for i in range(10):
        pwd = username + str(i)
        if len(pwd) >= 6:
            combinations.add(pwd)

    # Tambahan angka 00–99 (dengan zfill)
    for i in range(100):
        pwd = username + str(i).zfill(2)
        if len(pwd) >= 6:
            combinations.add(pwd)

    return list(combinations)
