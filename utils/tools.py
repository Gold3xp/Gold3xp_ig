from instagrapi import Client
import os
import re

def login_with_cookie(cookie_path, user_path):
    from colorama import Fore

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
