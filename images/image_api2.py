

# import the necessary packages
import requests
import cv2
import urllib
import sys
import os


# import the necessary packages
import numpy as np
import json


def detect(url):
	# define the path to the face detector

	FACE_DETECTOR_PATH = "{base_path}/cascades/haarcascade_frontalface_alt2.xml".format(
		base_path=os.path.abspath(os.path.dirname(__file__)))
	# load the image and convert
	image = _grab_image(url=url)

	# convert the image to grayscale, load the face cascade detector,
	# and detect faces in the image
	#image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	detector = cv2.CascadeClassifier(FACE_DETECTOR_PATH)
	# Try to get bounding coords around faces
	try:
		rects = detector.detectMultiScale(
			image,
			scaleFactor=1.1,
			minNeighbors=5,
			minSize=(30, 30),
			flags=cv2.cv.CV_HAAR_SCALE_IMAGE

		)
	# Except OpenCV error..?
	except:
		return None

	# construct a list of bounding boxes from the detection
	rects = [(int(x), int(y), int(x + w), int(y + h)) for (x, y, w, h) in rects]

	# update the data dictionary with the faces detected
	data = {"num_faces": len(rects), "faces": rects, "success": True}

	# return a JSON response
	return data

def _grab_image(path=None, stream=None, url=None):
	# if the path is not None, then load the image from disk
	if path is not None:
		image = cv2.imread(path)

	# otherwise, the image does not reside on disk
	else:
		# if the URL is not None, then download the image
		if url is not None:
			resp = urllib.urlopen(url)
			data = resp.read()

		# if the stream is not None, then the image has been uploaded
		elif stream is not None:
			data = stream.read()

		# convert the image to a NumPy array and then read it into
		# OpenCV format
		image = np.asarray(bytearray(data), dtype="uint8")
		image = cv2.imdecode(image, cv2.IMREAD_COLOR)

	# return the image
	return image






'''FOR URL DOWNLOADS ONLY'''

# url of image to be analyzed LIST OF URLS OF IMAGES TO BE CROPPED AND SAVED
def urldownload(folder_name,url):
	# define the URL to our face detection API

	folder_name = folder_name
	url = url

	try:
		# download image to local
		urllib.urlretrieve(url, "pic.jpg")
		# read image to cv2 for processing
		image = cv2.imread("pic.jpg", 0)
		# send image to facedetector, which detects faces and returns box coords

		r = detect(url)
		if r != None:
			print 'Data returned -'
			print "faces.jpg: {}".format(r)

			# loop over the faces and draw them on the image
			for (startX, startY, endX, endY) in r["faces"]:
				cv2.rectangle(image, (startX, startY), (endX, endY), (0, 255, 0), 2)
				# crops image to face for analyzing
				crop_img = image[startY:endY, startX:endX] # Crop from x, y, w, h -> 100, 200, 300, 400
				# WRITES IMAGE TO FOLDER () CHANGE ACCORDINGLY
				count = len(os.listdir("facedb/{}".format(folder_name)))
				cv2.imwrite("facedb/{}/{}.pgm".format(folder_name,count+1), crop_img)
	except ValueError:
		pass
