"""Entry point for running face recognition and greetings."""

from __future__ import annotations

import logging

import cv2
import imutils

from facial_recognition import constants
from facial_recognition.recognition import FaceRecognitionEngine
from facial_recognition.speech import VoiceGenerator


def main() -> None:
    """Start the recognition loop and greet recognized faces."""
    face_recognizer = FaceRecognitionEngine()
    voice_gen = VoiceGenerator()
    greeted_people: list[str] = []

    logging.basicConfig(
        filename="face_recognition.log",
        level=logging.INFO,
        format="%(asctime)s %(message)s",
    )

    while True:
        frame = face_recognizer.vs.read()
        frame = imutils.resize(frame, width=500)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        boxes = face_recognizer.locate_faces(rgb_frame)
        names, distances = face_recognizer.recognize_all_faces(rgb_frame, boxes)
        face_recognizer.plot_face_location(boxes, names, frame)

        for name, distance in zip(names, distances):
            logging.info(
                "name=%s distance=%.3f threshold=%.3f",
                name,
                distance,
                face_recognizer.match_threshold,
            )

            if name not in greeted_people and name != constants.UNKNOWN:
                voice_gen.greet(name)
                greeted_people.append(name)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            print("Goodbye!")
            break

    face_recognizer.stop_engine()


if __name__ == "__main__":
    print("Starting...")
    main()
