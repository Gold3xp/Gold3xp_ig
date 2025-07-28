import os
import re
import requests
from instagrapi import Client
from colorama import Fore

def login_with_cookie(cookie_path, user_path=None):
    if not os.path.exists(cookie_path):
        print(Fore.RED + f"❌ File {cookie_path} tidak ditemukan.")
        return None

    with open(cookie_path, "r") as f:
        cookie_content = f.read()

    try:
        sessionid = re.search(r"sessionid=([^;]+)", cookie_content)
        ds_user_id = re.search(r"ds_user_id=([^;]+)", cookie_content)

        if not sessionid or not ds_user_id:
            raise ValueError("Cookie tidak lengkap atau tidak valid.")

        cookie = f"sessionid={sessionid.group(1)}; ds_user_id={ds_user_id.group(1)}"
        cl = Client()
        cl.login_by_sessionid(cookie)
        return cl

    except Exception as e:
        print(Fore.RED + f"❌ Gagal login dari cookie: {e}")
        return None

def login_real(username, password, user_agent=None, proxy=None):
    cl = Client()
    try:
        if user_agent:
            cl.user_agent = user_agent
        if proxy:
            cl.set_proxy(proxy)
        cl.login(username, password)
        return cl  # return Client object
    except Exception as e:
        print(Fore.RED + f"❌ Login gagal: {e}")
        return None

def get_user_info(cl: Client, username):
    try:
        user = cl.user_info_by_username(username)
        return {
            "followers": user.follower_count,
            "following": user.following_count,
            "posts": user.media_count
        }
    except Exception as e:
        print(Fore.RED + f"❌ Gagal ambil info pengguna: {e}")
        return {"followers": 0, "following": 0, "posts": 0}

def load_list_from_file(path):
    if not os.path.exists(path):
        return []
    with open(path, "r") as f:
        return [line.strip() for line in f if line.strip()]

def generate_passwords(username, full_name):
    name_parts = full_name.lower().split()
    username_letters = ''.join(re.findall(r'[a-zA-Z]', username))
    username_digits = ''.join(re.findall(r'\d+', username))

    base_names = list(set([
        username.lower(),
        username.upper(),
        username_letters.lower(),
        username_letters.upper()
    ] + name_parts))

    password_list = []
    suffixes = ["", "123", "1234", "12345", "123456", "01", "321"]

    for base in base_names:
        for suffix in suffixes:
            pw = base + suffix
            if len(pw) >= 6:
                password_list.append(pw)

    return list(set(password_list))  # Hapus duplikat
