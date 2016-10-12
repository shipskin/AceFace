import cv2

def facechop(image, n):
	facedata = "/Users/Stephen/facerec/py/apps/videofacerec/haarcascade_frontalface_alt2.xml"
	cascade = cv2.CascadeClassifier(facedata)

	img = cv2.imread(image)
	#img = cv2.resize(frame, (frame.shape[1]/2, frame.shape[0]/2))
	minisize = (img.shape[1],img.shape[0])
	miniframe = cv2.resize(img, minisize, interpolation = cv2.INTER_AREA)

	faces = cascade.detectMultiScale(miniframe)

	for f in faces:
		x, y, w, h = [ v for v in f ]
		cv2.rectangle(img, (x,y), (x+w,y+h), (255,255,255))

		sub_face = img[y:y+h, x:x+w]
		face_file_name = "/Users/Stephen/facerec/faces/annie-thorisdottir/annie-thorisdottir" + str(n) + ".pgm"
		cv2.imwrite(face_file_name, sub_face)

	cv2.imshow(image, img)

	return

if __name__ == '__main__':
	face_paths = ['/Users/Stephen/facerec/annie.jpg', '/Users/Stephen/facerec/annie2.jpg', '/Users/Stephen/facerec/annie3.png', '/Users/Stephen/facerec/annie4.jpg', '/Users/Stephen/facerec/annie5.jpg', '/Users/Stephen/facerec/annie6.jpg']
	count = 5
	for face in face_paths:
		facechop(face, count)
		count +=1
