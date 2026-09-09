import requests

# Загрузи cookies из твоего браузера (экспортированные в Netscape-формате)
cookies_path = "cookies.txt"

session = requests.Session()

# Простой парсер netscape cookie file
def load_cookies(session, path):
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split("\t")
            if len(parts) != 7:
                continue
            domain, _, path_, secure, expiry, name, value = parts
            session.cookies.set(name, value, domain=domain, path=path_)

load_cookies(session, cookies_path)

url = "https://lms.mtuci.ru/pluginfile.php/155429/user/icon/mtuci/f3?rev=8856688"

resp = session.get(url, allow_redirects=True)
resp.raise_for_status()

content_type = resp.headers.get("Content-Type", "")
if "image" in content_type:
    if "/theme/image.php/" in resp.url:
        print("Сервер отдал дефолтную фотографию пользователя:", resp.url)
    with open("my_avatar.png", "wb") as f:
        f.write(resp.content)
    print("Сохранено: my_avatar.png")
else:
    print("Сессия не подтверждена: сервер вернул не изображение, а:", content_type)
    print("Конечный URL:", resp.url)
    if resp.history:
        print("Редиректы:", [item.headers.get("Location", "") for item in resp.history])