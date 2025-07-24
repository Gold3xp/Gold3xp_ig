def is_license_valid():
    try:
        with open("license.key", "r") as f:
            key = f.read().strip()
        return key in open("valid_licenses.txt").read().splitlines()
    except:
        return False
