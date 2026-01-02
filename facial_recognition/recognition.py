"""Face recognition engine built on the face_recognition library."""

from __future__ import annotations

from pathlib import Path
import pickle
import time
from typing import Any

import cv2
import face_recognition
from imutils.video import VideoStream

from facial_recognition import constants


class FaceRecognitionEngine:
    """Handle face detection, recognition, and visualization."""

    def __init__(
        self,
        encodings_path: str | Path = constants.ENCODINGS_PATH,
        video_source: int = 2,
        use_pi_camera: bool = True,
        warmup_seconds: float = 2.0,
        match_threshold: float = constants.MATCH_THRESHOLD,
    ) -> None:
        """Load encodings and initialize the video stream."""
        self.data = self._load_encodings(encodings_path)
        self.match_threshold = match_threshold
        if use_pi_camera:
            self.vs = VideoStream(usePiCamera=True, framerate=10).start()
        else:
            self.vs = VideoStream(src=video_source, framerate=10).start()
        time.sleep(warmup_seconds)

    def _load_encodings(self, encodings_path: str | Path) -> dict[str, list[Any]]:
        """Read serialized facial encodings from disk."""
        path = Path(encodings_path)
        with path.open("rb") as file:
            return pickle.loads(file.read())

    def locate_faces(self, rgb_frame: Any) -> list[tuple[int, int, int, int]]:
        """Detect faces in an RGB frame and return bounding boxes."""
        return face_recognition.face_locations(rgb_frame)

    def recognize_all_faces(
        self, rgb_frame: Any, boxes: list[tuple[int, int, int, int]]
    ) -> tuple[list[str], list[float]]:
        """Compute names and distances for each detected face."""
        encodings = face_recognition.face_encodings(rgb_frame, boxes)
        names: list[str] = []
        distances: list[float] = []
        for encoding in encodings:
            name, distance = self.recognize_face(encoding)
            names.append(name)
            distances.append(distance)
        return names, distances

    def recognize_face(self, encoding: Any) -> tuple[str, float]:
        """Return the name and distance for a recognized face."""
        distances = face_recognition.face_distance(self.data["encodings"], encoding)
        if len(distances) == 0:
            return constants.UNKNOWN, float("inf")

        best_index = int(distances.argmin())
        best_distance = float(distances[best_index])
        if best_distance <= self.match_threshold:
            name = self.data["names"][best_index]
        else:
            name = constants.UNKNOWN
        return name, best_distance

    def plot_face_location(
        self, boxes: list[tuple[int, int, int, int]], names: list[str], frame: Any
    ) -> None:
        """Draw detections and labels onto the provided frame."""
        for ((top, right, bottom, left), name) in zip(boxes, names):
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 225), 2)
            y_coord = top - 15 if top - 15 > 15 else top + 15
            cv2.putText(
                frame, name, (left, y_coord), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2
            )

        cv2.imshow("Facial Recognition is Running", frame)

    def stop_engine(self) -> None:
        """Release resources for the video stream."""
        cv2.destroyAllWindows()
        self.vs.stop()
