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

        boxes = face_recognizer.locate_faces(frame)
        names = face_recognizer.recognize_all_faces(frame, boxes)
        face_recognizer.plot_face_location(boxes, names, frame)

        for name in names:
            logging.info("%s", name)  # TODO: add confidence score and debounce greetings

            if name not in greeted_people and name != constants.UNKNWON:
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
