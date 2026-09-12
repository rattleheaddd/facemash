from pathlib import Path
import shutil

import numpy as np
import onnxruntime as ort
from PIL import Image, ImageOps


BASE_DIR = Path(__file__).resolve().parent
INPUT_DIR = BASE_DIR / "pics"
WOMEN_DIR = BASE_DIR / "women"
MEN_DIR = BASE_DIR / "men"
MODEL_PATH = BASE_DIR / "models" / "resnet152_optimized.onnx"
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
IMAGE_SIZE = (224, 224)
WOMAN_THRESHOLD = 0.5


def prepare_image(image_path: Path) -> np.ndarray:
    with Image.open(image_path) as image:
        image = ImageOps.exif_transpose(image).convert("RGB")
        image = image.resize(IMAGE_SIZE, Image.Resampling.BILINEAR)
        image_array = np.asarray(image, dtype=np.float32)

    # ResNetV2 preprocessing: convert RGB values from [0, 255] to [-1, 1].
    image_array = image_array / 127.5 - 1.0
    return np.expand_dims(image_array, axis=0)


def unique_destination(directory: Path, filename: str) -> Path:
    destination = directory / filename
    if not destination.exists():
        return destination

    stem = Path(filename).stem
    suffix = Path(filename).suffix
    counter = 1
    while True:
        destination = directory / f"{stem}_{counter}{suffix}"
        if not destination.exists():
            return destination
        counter += 1


def main() -> None:
    if not INPUT_DIR.exists():
        raise FileNotFoundError(f"Папка не найдена: {INPUT_DIR}")
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Модель не найдена: {MODEL_PATH}")

    WOMEN_DIR.mkdir(exist_ok=True)
    MEN_DIR.mkdir(exist_ok=True)

    session = ort.InferenceSession(
        str(MODEL_PATH),
        providers=["CPUExecutionProvider"],
    )
    input_name = session.get_inputs()[0].name
    image_paths = sorted(
        path
        for path in INPUT_DIR.iterdir()
        if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS
    )

    processed = 0
    failed = 0
    for image_path in image_paths:
        try:
            prediction = float(session.run(None, {input_name: prepare_image(image_path)})[0][0][0])
            target_dir = WOMEN_DIR if prediction >= WOMAN_THRESHOLD else MEN_DIR
            destination = unique_destination(target_dir, image_path.name)
            shutil.move(str(image_path), str(destination))
            label = "women" if target_dir == WOMEN_DIR else "men"
            print(f"{image_path.name}: {prediction:.4f} -> {label}")
            processed += 1
        except Exception as error:
            failed += 1
            print(f"Ошибка обработки {image_path.name}: {error}")

    print(f"Готово. Обработано: {processed}, ошибок: {failed}")


if __name__ == "__main__":
    main()