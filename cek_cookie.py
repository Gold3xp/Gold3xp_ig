from instagrapi import Client

# Ganti ini dengan hanya nilai sessionid (BUKAN seluruh cookie!)
sessionid = "75798862193%3AazI415CdTNmKxT%3A27%3AAYeK6jXQc7OUL3lmROX5VMqln4R4PhNu028ZYm9avw"

cl = Client()
cl.login_by_sessionid(sessionid)

# Jika berhasil, tampilkan feed
print("✅ Login berhasil!")
timeline = cl.get_timeline_feed()
for post in timeline[:3]:
    print(f"- {post.dict()['user']['username']}: {post.dict().get('caption_text')}")
