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
    ) -> None:
        """Load encodings and initialize the video stream."""
        self.data = self._load_encodings(encodings_path)
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

    def locate_faces(self, frame: Any) -> list[tuple[int, int, int, int]]:
        """Detect faces in a frame and return bounding boxes."""
        return face_recognition.face_locations(frame)

    def recognize_all_faces(
        self, frame: Any, boxes: list[tuple[int, int, int, int]]
    ) -> list[str]:
        """Compute names for each detected face."""
        encodings = face_recognition.face_encodings(frame, boxes)
        names: list[str] = []
        for encoding in encodings:
            names.append(self.recognize_face(encoding))
        return names

    def recognize_face(self, encoding: Any) -> str:
        """Return the name of a recognized face or the unknown constant."""
        matches = face_recognition.compare_faces(self.data["encodings"], encoding)
        name = constants.UNKNWON

        if True in matches:
            matched_idxs = [index for (index, match) in enumerate(matches) if match]
            counts: dict[str, int] = {}

            for index in matched_idxs:
                match_name = self.data["names"][index]
                counts[match_name] = counts.get(match_name, 0) + 1

            name = max(counts, key=counts.get)
        return name

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
