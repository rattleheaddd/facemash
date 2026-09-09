from urllib.parse import urlsplit, urlunsplit

import requests

# Загрузи cookies из твоего браузера (экспортированные в Netscape-формате)
cookies_path = "cookies.txt"

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36",
    "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
    "Referer": "https://lms.mtuci.ru/user/profile.php?id=0",
    "Cache-Control": "no-cache",
})

# Простой парсер netscape cookie file
def load_cookies(session, path):
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith("#HttpOnly_"):
                line = line[len("#HttpOnly_"):]
            elif line.startswith("#"):
                continue
            parts = line.split("\t")
            if len(parts) != 7:
                continue
            domain, _, path_, secure, expiry, name, value = parts
            session.cookies.set(
                name,
                value,
                domain=domain,
                path=path_,
                secure=secure.upper() == "TRUE",
            )

load_cookies(session, cookies_path)

for i in range(50000, 200001):
    url = f"https://lms.mtuci.ru/pluginfile.php/{i}/user/icon/mtuci/f3?rev=8875864"

    resp = session.get(url, allow_redirects=True)


    def safe_url(value):
        parts = urlsplit(value)
        return urlunsplit((parts.scheme, parts.netloc, parts.path, "", ""))


    try:
        resp.raise_for_status()
    except Exception as e:
        print(f"Пропускаю {i}")
        continue

    content_type = resp.headers.get("Content-Type", "")
    if "image" in content_type:
        if "/theme/image.php/" in resp.url:
            print("Сессия принята, но у пользователя нет доступного фото.")
            print("Moodle отдал стандартную иконку:", safe_url(resp.url))
        with open(f"pics/{i}.png", "wb") as f:
            f.write(resp.content)
        print(f"Сохранено {i}.png")
    else:
        print("Сессия не подтверждена: сервер вернул не изображение, а:", content_type)
        print("URL:", safe_url(resp.url))
        if resp.history:
            print("Последний редирект:", safe_url(resp.history[-1].headers.get("Location", "")))