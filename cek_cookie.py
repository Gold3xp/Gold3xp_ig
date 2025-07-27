from instagrapi import Client

cl = Client()
sessionid = "75798862193%3AazI415CdTNmKxT%3A27%3AAYeK6jXQc7OUL3lmROX5VMqln4R4PhNu028ZYm9avw"
cl.login_by_sessionid(cookie)
print(cl.get_timeline_feed())  # Harus berhasil tampil feed
