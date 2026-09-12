from pathlib import Path
import re

import matplotlib.pyplot as plt


BASE_DIR = Path(__file__).resolve().parent
WOMEN_DIR = BASE_DIR / "women"
OUTPUT_PATH = BASE_DIR / "women_id_distribution.png"
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


def extract_id(file_path: Path) -> int | None:
    match = re.match(r"^(\d+)(?:_|$)", file_path.stem)
    return int(match.group(1)) if match else None


def calculate_bin_width(ids: list[int]) -> int:
    sorted_ids = sorted(ids)
    quartiles = [
        sorted_ids[int((len(sorted_ids) - 1) * fraction)]
        for fraction in (0.25, 0.75)
    ]
    raw_width = 2 * (quartiles[1] - quartiles[0]) / len(sorted_ids) ** (1 / 3)
    return max(500, round(raw_width / 500) * 500)


def main() -> None:
    image_paths = sorted(
        path
        for path in WOMEN_DIR.iterdir()
        if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS
    )
    ids = [photo_id for path in image_paths if (photo_id := extract_id(path)) is not None]
    skipped = len(image_paths) - len(ids)

    if not ids:
        raise RuntimeError(f"В папке {WOMEN_DIR} нет фотографий с числовым ID")

    bin_width = calculate_bin_width(ids)
    first_bin = min(ids) // bin_width * bin_width
    last_bin = (max(ids) // bin_width + 1) * bin_width
    bin_edges = list(range(first_bin, last_bin + bin_width, bin_width))

    plt.figure(figsize=(16, 7))
    plt.hist(ids, bins=bin_edges, edgecolor="white", linewidth=0.4)
    plt.xlabel("ID фотографии")
    plt.ylabel("Количество фотографий")
    plt.title(f"Распределение фотографий women по ID (шаг {bin_width})")
    plt.xticks(range(first_bin, last_bin + 1, bin_width * 5), rotation=45, ha="right")
    plt.grid(axis="y", alpha=0.25)
    plt.tight_layout()
    plt.savefig(OUTPUT_PATH, dpi=160)
    plt.close()

    print(f"График сохранён: {OUTPUT_PATH}")
    print(f"Автоматически выбранный шаг: {bin_width}")
    print(f"Учтено фотографий: {len(ids)}")
    if skipped:
        print(f"Пропущено файлов без числового ID: {skipped}")


if __name__ == "__main__":
    main()