"""Train a facial recognition model and serialize encodings."""

from __future__ import annotations

from pathlib import Path
import pickle
from typing import Any

import cv2
import face_recognition
from imutils import paths


def train_model(dataset_dir: str = "dataset") -> dict[str, list[Any]]:
    """Generate facial encodings from the dataset."""
    image_paths = list(paths.list_images(dataset_dir))
    print("[INFO] start processing faces...")

    known_encodings: list[Any] = []
    known_names: list[str] = []

    for index, image_path in enumerate(image_paths, start=1):
        print(f"[INFO] processing image {index}/{len(image_paths)}")
        name = Path(image_path).parent.name

        image = cv2.imread(image_path)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        boxes = face_recognition.face_locations(rgb, model="hog")

        encodings = face_recognition.face_encodings(rgb, boxes)
        known_encodings.extend(encodings)
        known_names.extend([name] * len(encodings))

    return {"encodings": known_encodings, "names": known_names}


def save_encodings(data: dict[str, list[Any]], output_path: str = "encodings.pickle") -> None:
    """Serialize encodings to disk."""
    print("[INFO] serializing encodings...")
    with open(output_path, "wb") as file:
        file.write(pickle.dumps(data))


def main() -> None:
    """Run the training pipeline."""
    encodings = train_model()
    save_encodings(encodings)


if __name__ == "__main__":
    main()
