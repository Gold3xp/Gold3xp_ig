import os

# Lokasi file target di instagrapi
file_path = os.path.join(
    os.getenv("PREFIX", "/data/data/com.termux/files/usr"),
    "lib/python3.12/site-packages/instagrapi/mixins/public.py"
)

# Fungsi _send_public_request yang baru
patched_function = '''
    def _send_public_request(
        self, url, data=None, params=None, headers=None
    ):
        self.public_requests_count += 1

        if headers:
            self.public.headers.update(headers)

        if self.request_timeout:
            time.sleep(self.request_timeout)

        try:
            if data is not None:  # POST
                response = self.public.post(url, data=data, params=params)
            else:  # GET
                response = self.public.get(url, params=params)

            expected_length = int(response.headers.get("Content-Length", 0))
            actual_length = response.raw.tell()
            if actual_length < expected_length:
                raise ClientIncompleteReadError(
                    "Incomplete read ({} bytes read, {} expected)".format(
                        actual_length, expected_length
                    ),
                    response=response,
                )

            self.request_logger.debug(
                "public_request %s: %s", "POST" if data else "GET", response.url
            )
            self.request_logger.info(
                "[%s] [%s] %s %s",
                response.status_code,
                self.public.proxies.get("https") if self.public.proxies else "no_proxy",
                "POST" if data else "GET",
                response.url,
            )

            self.last_public_response = response
            return response

        except Exception as e:
            self.logger.error(f"❌ Gagal request ke {url}: {e}")
            raise
'''

# Proses patching
if os.path.exists(file_path):
    with open(file_path, "r") as f:
        lines = f.readlines()

    with open(file_path, "w") as f:
        inside_target_func = False
        for line in lines:
            if line.strip().startswith("def _send_public_request"):
                inside_target_func = True
                f.write(patched_function)
            elif inside_target_func:
                if line.startswith(" " * 4) or line.strip() == "":
                    continue  # skip old function body
                else:
                    inside_target_func = False
                    f.write(line)
            else:
                f.write(line)

    print("✅ Fungsi _send_public_request berhasil dipatch!")
else:
    print(f"❌ File tidak ditemukan: {file_path}")
