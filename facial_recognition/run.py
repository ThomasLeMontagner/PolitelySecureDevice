from voice_generator import *
from  facial_req import *
import constants
import imutils

def main():
    # Initialize the engine for face recognition
    face_recogn_engine = face_recogn_engine(constants.ENCODINGP)

    # Initialize the voice generator
    voice_generator = voice_generator()

    # List of poeple greeted
    greeted_people = []

    # loop over frames from the video file stream
    while True:
        # grab the frame from the threaded video stream and resize it
        # to 500px (to speedup processing)
        frame = face_recogn_engine.vs.read()
        frame = imutils.resize(frame, width=500)

        boxes = face_recogn_engine.locate_faces(frame)
        names = face_recogn_engine.recognize_all_faces(frame, boxes)

        for name in names:
            if not name in greeted_people and name != constants.UNKNWON:
                voice_generator.greet(name)

        key = cv2.waitKey(1) & 0xFF
        # quit when 'q' key is pressed
        if key == ord("q"):
            break

if __name__ == "__main__":
    main()