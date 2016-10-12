# import the necessary packages
import requests
import cv2
import urllib
import sys
import os
# define the URL to our face detection API
url = "http://192.168.1.118:8000/face_detection/detect/"



# use our face detection API to find faces in images via image URL
### image = cv2.imread("hot.jpg")


'''FOR URL DOWNLOADS ONLY

# url of image to be analyzed LIST OF URLS OF IMAGES TO BE CROPPED AND SAVED

imgurl = [
"https://scontent.fsnc1-1.fna.fbcdn.net/v/t1.0-9/58106_1642476788787_6976300_n.jpg?oh=e381fc8709f3a29abeb040d4216c2b0a&oe=5862CF1B",
"https://scontent.fsnc1-1.fna.fbcdn.net/v/t1.0-9/14370296_10206783546400541_7953299272349599526_n.jpg?oh=e773e1c2bd54750c5a34f643ee8ad515&oe=5866AF0D",
"https://scontent.fsnc1-1.fna.fbcdn.net/v/t1.0-0/p206x206/5822_4952575085475_1929426619_n.jpg?oh=24e55185fe7d9a9459a13033336fc7f4&oe=587C4868",
"https://scontent.fsnc1-1.fna.fbcdn.net/v/t1.0-0/p206x206/10351390_10101321725977408_8843871840151303616_n.jpg?oh=26e6dc498e303b5d070abe56ca154f63&oe=58756E45",
"https://scontent.fsnc1-1.fna.fbcdn.net/v/t1.0-0/p206x206/10367804_10202609394769359_6438287991568483563_n.jpg?oh=3ece6ba3b50a7adf279ea35555df5fb8&oe=587BBC67",
"https://scontent.fsnc1-1.fna.fbcdn.net/v/t1.0-0/p206x206/936412_4943877308036_2000255560_n.jpg?oh=dd8f3cf3c6f5771907be3fa63b6b0941&oe=586FF191"
]


for imag in range(len(imgurl)):
# download image to local
urllib.urlretrieve(imgurl[imag], "pic.jpg")
# read image to cv2 for processing
image = cv2.imread("pic.jpg", 0)
# send image to facedetector server, which detects faces and returns box coords
payload = {"url": imgurl[imag]}
r = requests.post(url, data=payload).json()
print "faces.jpg: {}".format(r)

# loop over the faces and draw them on the image
for (startX, startY, endX, endY) in r["faces"]:
cv2.rectangle(image, (startX, startY), (endX, endY), (0, 255, 0), 2)


# crops image to face for analyzing
crop_img = image[startY:endY, startX:endX] # Crop from x, y, w, h -> 100, 200, 300, 400

# WRITES IMAGE TO FOLDER (PH) CHANGE ACCORDINGLY
cv2.imwrite("/Users/kage/facerec/data/images/ph/%d.pgm" % imag, crop_img)


# NOTE: its img[y: y + h, x: x + w] and *not* img[x: x + w, y: y + h]

'''



# load our image and now use the face detection API to find faces in
# images by uploading an image directly

imags = [
"annie-thorisdottir1.jpg",
"annie-thorisdottir2.jpg",
"annie-thorisdottir3.jpg",
"annie-thorisdottir4.jpg",
"annie-thorisdottir5.jpg"
]

for imag in range(len(imags)):
	image = cv2.imread(imags[imag], 0)
	payload = {"image": open(imags[imag], "rb")}
	r = requests.post(url, files=payload).json()
	print "{}".format(r)
	# loop over the faces and draw them on the image
	for (startX, startY, endX, endY) in r["faces"]:
		cv2.rectangle(image, (startX, startY), (endX, endY), (0, 255, 0), 2)

		# crops image to face
		crop_img = image[startY:endY, startX:endX]

		# RESIZE IMAGE TO 10KB
		r = 100.0 / crop_img.shape[1]
		dim = (100, int(crop_img.shape[0] * r))
		resized = cv2.resize(crop_img, dim, interpolation = cv2.INTER_AREA)

		# WRITES IMAGES TO FOLDER (PH) CHANGE ACCORDINGLY
		cv2.imwrite("/Users/Stephen/facerec/orl_faces/annie-thorisdottir/%d.pgm" % imag, resized)



		'''
		# NOTE: its img[y: y + h, x: x + w] and *not* img[x: x + w, y: y + h]
		# show the output image
		cv2.imshow("seattle4.jpg", image)
		cv2.waitKey(0)
		'''
