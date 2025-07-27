def scrape_followers(cl, target_username):
    try:
        user_id = cl.user_id_from_username(target_username)
        followers = cl.user_followers(user_id, amount=0)
        return [{ "username": v.username, "full_name": v.full_name } for v in followers.values()]
    except Exception as e:
        print(f"[!] Gagal mengambil followers: {e}")
        return []
