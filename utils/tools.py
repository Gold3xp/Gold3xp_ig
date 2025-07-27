def generate_passwords(username, full_name):
    name_parts = full_name.lower().split()
    base_names = [username.lower()] + name_parts
    suffixes = ["", "123", "1234", "12345", "2024", "2025", "@123", "#123", "1", "!", "0"]

    combinations = []
    for base in base_names:
        for suffix in suffixes:
            pwd = base + suffix
            if len(pwd) >= 6:
                combinations.append(pwd)
    return combinations
