from voice_generator import *
from  facial_req import *
import constants
import imutils
import logging
import datetime

def main():
    # Initialize the engine for face recognition
    face_recogn = face_recogn_engine(constants.ENCODINGP)

    # Initialize the voice generator
    voice_gen = voice_generator()

    # List of poeple greeted
    greeted_people = []

    # Set up the logging configuration
    logging.basicConfig(filename='face_recognition.log', level=logging.INFO, format='%(asctime)s %(message)s')

    # loop over frames from the video file stream
    while True:
        # grab the frame from the threaded video stream and resize it to 500px (to speedup processing)
        frame = face_recogn.vs.read()
        frame = imutils.resize(frame, width=500)

        boxes = face_recogn.locate_faces(frame)
        names = face_recogn.recognize_all_faces(frame, boxes)

        face_recogn.plot_face_location(boxes, names, frame)

        # Get the current date and time
        time = datetime.datetime.now()

        for name in names:
            if not name in greeted_people and name != constants.UNKNWON:
                voice_gen.greet(name)
                greeted_people.append(name)

                # Log the date, time, and name (or 'unknown')
                logging.info(f"{time.strftime('%Y-%m-%d %H:%M:%S')} {name}")

        key = cv2.waitKey(1) & 0xFF
        # quit when 'q' key is pressed
        if key == ord("q"):
            print('Goodbye!')
            break

if __name__ == "__main__":
    print('Starting...')
    main()