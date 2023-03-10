#! /usr/bin/python

# import the necessary packages
from imutils.video import VideoStream
from imutils.video import FPS
import face_recognition
import pickle
import time
import cv2
import constants

# load the known faces and embeddings along with OpenCV's Haar
# cascade for face detection
print("[INFO] loading encodings + face detector...")
data = pickle.loads(open(constants.ENCODINGP, "rb").read())

# start the FPS counter
fps = FPS().start()

class face_recogn_engine:

	def __init__(self, encodinsP: str):
		# Determine faces from encodings.pickle file model created from train_model.py
		self.encodingsP = encodinsP
		# initialize the video stream and allow the camera sensor to warm up
		# Set the ser to the followng
		# src = 0 : for the build in single web cam, could be your laptop webcam
		# src = 2 : I had to set it to 2 inorder to use the USB webcam attached to my laptop
		self.vs = VideoStream(src=2,framerate=10).start()
		self.vs = VideoStream(usePiCamera=True).start()
		time.sleep(2.0)

	# Detect faces in a frame and return the facial embeddings
	def locate_faces(self, frame):
		boxes = face_recognition.face_locations(frame)
		return boxes
	
	# compute the facial embeddings for each face bounding box
	def recognize_all_faces(self, frame, boxes):
		encodings = face_recognition.face_encodings(frame, boxes)
		names = []
		for encoding in encodings:
			names.append(self.recognize_face(encoding))
		return names

	# Return the name of the face if recognize, otherwise "Unknown"
	def recognize_face(self, encoding):
		# attempt to match each face in the input image to our known
		# encodings
		matches = face_recognition.compare_faces(data["encodings"],
			encoding)
		name = constants.UNKNWON 

		# check to see if we have found a match
		if True in matches:
			# find the indexes of all matched faces then initialize a
			# dictionary to count the total number of times each face
			# was matched
			matchedIdxs = [i for (i, b) in enumerate(matches) if b]
			counts = {}

			# loop over the matched indexes and maintain a count for
			# each recognized face face
			for i in matchedIdxs:
				name = data["names"][i]
				counts[name] = counts.get(name, 0) + 1

			# determine the recognized face with the largest number
			# of votes (note: in the event of an unlikely tie Python
			# will select first entry in the dictionary)
			name = max(counts, key=counts.get)
		return name
	
	def plot_face_location(self, boxes, names, frame):
		# loop over the recognized faces
		for ((top, right, bottom, left), name) in zip(boxes, names):
			# draw the predicted face name on the image - color is in BGR
			cv2.rectangle(frame, (left, top), (right, bottom),
				(0, 255, 225), 2)
			y = top - 15 if top - 15 > 15 else top + 15
			cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
				.8, (0, 255, 255), 2)

		# display the image to our screen
		cv2.imshow("Facial Recognition is Running", frame)
	
	def stop_engine(self):
		cv2.destroyAllWindows()
		self.vs.stop()
