"""Capture headshots from the PiCamera into the dataset directory."""

from __future__ import annotations

from pathlib import Path

import cv2
from picamera import PiCamera
from picamera.array import PiRGBArray


def capture_headshots(
    person_name: str,
    output_dir: str = "dataset",
    resolution: tuple[int, int] = (512, 304),
    framerate: int = 10,
) -> None:
    """Save headshots for the provided person until ESC is pressed."""
    output_path = Path(output_dir) / person_name
    output_path.mkdir(parents=True, exist_ok=True)

    camera = PiCamera()
    camera.resolution = resolution
    camera.framerate = framerate
    raw_capture = PiRGBArray(camera, size=resolution)

    img_counter = 0
    for frame in camera.capture_continuous(
        raw_capture, format="bgr", use_video_port=True
    ):
        image = frame.array
        cv2.imshow("Press Space to take a photo", image)
        raw_capture.truncate(0)

        key = cv2.waitKey(1)
        raw_capture.truncate(0)
        if key % 256 == 27:
            print("Escape hit, closing...")
            break
        if key % 256 == 32:
            img_name = output_path / f"image_{img_counter}.jpg"
            cv2.imwrite(str(img_name), image)
            print(f"{img_name} written!")
            img_counter += 1

    cv2.destroyAllWindows()


if __name__ == "__main__":
    capture_headshots("Raquel")
