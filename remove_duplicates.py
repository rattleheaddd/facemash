from pathlib import Path
import hashlib

folder = Path("pics")
seen = {}

for file_path in folder.iterdir():
    if not file_path.is_file():
        continue

    file_hash = hashlib.sha256(file_path.read_bytes()).hexdigest()

    if file_hash in seen:
        print(f"Удаляю дубликат: {file_path} == {seen[file_hash]}")
        file_path.unlink()
    else:
        seen[file_hash] = file_path