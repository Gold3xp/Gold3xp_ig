from instagrapi import Client

# Ganti dengan nilai cookie yang Anda dapatkan
sessionid = "75798862193%3AazI415CdTNmKxT%3A27%3AAYeK6jXQc7OUL3lmROX5VMqln4R4PhNu028ZYm9avw; ds_user_id = 75798862193; csrftoken; OTOzIsgbEEiXe3SDqgwg2NfIaNs3uSUh"

cl = Client()
cl.login_by_sessionid(sessionid)

# Sekarang Anda sudah login dan bisa menggunakan API Instagrapi
# Misalnya, dapatkan informasi profil sendiri
profile = cl.user_info_by_username("hamzah_57977")
print(profile.dict())
