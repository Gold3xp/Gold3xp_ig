def scrape_followers(client, username_target):
    try:
        user_id = client.user_id_from_username(username_target)
        followers = client.user_followers(user_id)  # tanpa 'amount', artinya ambil semua
        result = []
        for user in followers.values():
            result.append({
                "username": user.username,
                "full_name": user.full_name,
            })
        return result
    except Exception as e:
        print(f"⚠️ Gagal scrape followers: {e}")
        return []
