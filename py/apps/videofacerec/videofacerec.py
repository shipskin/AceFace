#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) Philipp Wagner. All rights reserved.
# Licensed under the BSD license. See LICENSE file in the project root for full license information.

import logging
# cv2 and helper:
import cv2
from helper.common import *
from helper.video import *
# add facerec to system path
import sys
sys.path.append("../..")
# facerec imports
from facerec.model import PredictableModel
from facerec.preprocessing import TanTriggsPreprocessing
from facerec.operators import ChainOperator
from facerec.feature import Fisherfaces
from facerec.distance import EuclideanDistance
from facerec.classifier import NearestNeighbor
from facerec.validation import KFoldCrossValidation
from facerec.serialization import save_model, load_model
from facerec.tagger import TagGenerator
# for face detection (you can also use OpenCV2 directly):
from facedet.detector import CascadedDetector


class ExtendedPredictableModel(PredictableModel):
	""" Subclasses the PredictableModel to store some more
		information, so we don't need to pass the dataset
		on each program call...
	"""

	def __init__(self, feature, classifier, image_size, subject_names):
		PredictableModel.__init__(self, feature=feature, classifier=classifier)
		self.image_size = image_size
		self.subject_names = subject_names

def get_model(image_size, subject_names):
	""" This method returns the PredictableModel which is used to learn a model
		for possible further usage. If you want to define your own model, this
		is the method to return it from!
	"""
	# Define the Fisherfaces Method as Feature Extraction method:
	feature = ChainOperator(TanTriggsPreprocessing(), Fisherfaces())
	# Define a 1-NN classifier with Euclidean Distance:
	classifier = NearestNeighbor(dist_metric=EuclideanDistance(), k=1)
	# Return the model as the combination:
	return ExtendedPredictableModel(feature=feature, classifier=classifier, image_size=image_size, subject_names=subject_names)

def read_subject_names(path):
	"""Reads the folders of a given directory, which are used to display some
		meaningful name instead of simply displaying a number.

	Args:
		path: Path to a folder with subfolders representing the subjects (persons).

	Returns:
		folder_names: The names of the folder, so you can display it in a prediction.
	"""
	folder_names = []
	for dirname, dirnames, filenames in os.walk(path):
		for subdirname in dirnames:
			folder_names.append(subdirname)
	return folder_names

def read_images(path, image_size=None):
	"""Reads the images in a given folder, resizes images on the fly if size is given.

	Args:
		path: Path to a folder with subfolders representing the subjects (persons).
		sz: A tuple with the size Resizes

	Returns:
		A list [X, y, folder_names]

			X: The images, which is a Python list of numpy arrays.
			y: The corresponding labels (the unique number of the subject, person) in a Python list.
			folder_names: The names of the folder, so you can display it in a prediction.
	"""
	c = 0
	X = []
	y = []
	folder_names = []
	for dirname, dirnames, filenames in os.walk(path):
		for subdirname in dirnames:
			folder_names.append(subdirname)
			subject_path = os.path.join(dirname, subdirname)
			for filename in os.listdir(subject_path):
				try:
					im = cv2.imread(os.path.join(subject_path, filename), cv2.IMREAD_GRAYSCALE)
					# resize to given size (if given)
					if (image_size is not None):
						im = cv2.resize(im, image_size)
					X.append(np.asarray(im, dtype=np.uint8))
					y.append(c)
				except IOError, (errno, strerror):
					print "I/O error({0}): {1}".format(errno, strerror)
				except:
					print "Unexpected error:", sys.exc_info()[0]
					raise
			c = c+1
	return [X,y,folder_names]


class App(object):
	def __init__(self, model, camera_id, cascade_filename, video_file):
		self.model = model
		self.detector = CascadedDetector(cascade_fn=cascade_filename, minNeighbors=5, scaleFactor=1.1)
		self.TagGenerator = TagGenerator()
		self.video_file = video_file
		#self.cam = create_capture(camera_id)

	def run(self):
		# Path to video filenames
		vidcap = cv2.VideoCapture(self.video_file)
		frames = vidcap.get(7)

		frame_count = 0
		while frame_count <= frames-100:
			# Skip 10 frames at a time
			for i in xrange(10):
				vidcap.grab()
			# Retrieve frame for detection
			ret, frame =  vidcap.read()
			# Resize the frame to half the original size for speeding up the detection process:
			img = cv2.resize(frame, (frame.shape[1]/2, frame.shape[0]/2), interpolation = cv2.INTER_CUBIC)
			imgout = img.copy()
			for i,r in enumerate(self.detector.detect(img)):
				x0,y0,x1,y1 = r
				# (1) Get face, (2) Convert to grayscale & (3) resize to image_size:
				face = img[y0:y1, x0:x1]
				face = cv2.cvtColor(face,cv2.COLOR_BGR2GRAY)
				face = cv2.resize(face, self.model.image_size, interpolation = cv2.INTER_CUBIC)
				# Get a prediction from the model:
				prediction = self.model.predict(face)[0]
				predict_distance = self.model.predict(face)[1]['distances']

				# Drop detection if threshold "distance" above value
				if predict_distance < 1200:
					#print predict_distance
					# Draw the face area in image:
					cv2.rectangle(imgout, (x0,y0),(x1,y1),(0,255,0),2)
					# Draw the predicted name (folder name...):
					draw_str(imgout, (x0-20,y0-20), self.model.subject_names[prediction])
					self.TagGenerator.addAthlete(self.model.subject_names[prediction], vidcap.get(0)/1000)
			print frame_count
			# Show image & exit on escape:
			ch = cv2.waitKey(10)
			if ch == 27:
				break
			# End program at end of video
			frame_count += 100
			#if vidcap.get(2) >= 0.90:
		return self.TagGenerator.namedb


def vid_run_main(**kwargs):

	# KEYS: model_param,dataset_param,cascade_param,vidpath_param,resize_param

	PARAMETERS = {'model_param': None,'dataset_param':None,'cascade_param':None,'vidpath_param':None,'resize_param':None}
	for key in PARAMETERS:
		print 'initializing {}...'.format(key)

		try:
			if kwargs[key]:
				PARAMETERS[key] = kwargs[key]
				print 'initialized {} = {}'.format(key,kwargs[key])
			else:
				print "No parameter - {} - will be set to default".format(key)
		except KeyError:
			pass


	# model.pkl is a pickled (hopefully trained) PredictableModel, which is
	# used to make predictions. You can learn a model yourself by passing the
	# parameter -d (or --dataset) to learn the model from a given dataset.
	# Add options for training, resizing, validation and setting the camera id:

	if PARAMETERS['model_param'] != None:
		model_filename = PARAMETERS['model_param']
		print "Model = {}".format(model_filename)
	else:
		print "[Error] No prediction model was given."
		sys.exit

	# This model will be used (or created if the training parameter (-t, --train) exists:
	# Check if the given model exists, if no dataset was passed:
	if (PARAMETERS['dataset_param'] is None) and (not os.path.exists(model_filename)):
		print "[Error] No prediction model found at {}.".format(model_filename)
		sys.exit()

	# Check if the given (or default) cascade file exists:
	if PARAMETERS['cascade_param'] != None:
		cascade_filename = PARAMETERS['cascade_param']
	else: # Set default
		cascade_filename = "haarcascade_frontalface_alt2.xml"
	if not os.path.exists(cascade_filename):
		print "[Error] No Cascade File found at {}.".format(cascade_filename)
		sys.exit()

	# Check if video filename given
	if PARAMETERS['vidpath_param'] != None:
		vid_filename = PARAMETERS['vidpath_param']
	else: # Set default for testing
		vid_filename = '/Users/kage/xvids/test/annie.mp4'
	if not os.path.exists(vid_filename):
		print "[Error] No video filename found at '{}'".format(vid_filename)
	# We are resizing the images to a fixed size, as this is neccessary for some of
	# the algorithms, some algorithms like LBPH don't have this requirement. To
	# prevent problems from popping up, we resize them with a default value if none
	# was given:
	if PARAMETERS['resize_param'] != None:
		size = PARAMETERS['resize_param']
	else: # Set default value
		size = "100x100"
	try:
		image_size = (int(size.split("x")[0]), int(size.split("x")[1]))
	except:
		print "[Error] Unable to parse the given image size '%s'. Please pass it in the format [width]x[height]!" % options.size
		sys.exit()

	# We have got a dataset to learn a new model from:
	dataset = PARAMETERS['dataset_param']
	if dataset:
		# Check if the given dataset exists:
		if not os.path.exists(dataset):
			print "[Error] No dataset found at '%s'." % dataset
			sys.exit()
		# Reads the images, labels and folder_names from a given dataset. Images
		# are resized to given size on the fly:
		print "Loading dataset..."
		[images, labels, subject_names] = read_images(dataset, image_size)
		# Zip us a {label, name} dict from the given data:
		list_of_labels = list(xrange(max(labels)+1))
		subject_dictionary = dict(zip(list_of_labels, subject_names))
		# Get the model we want to compute:
		model = get_model(image_size=image_size, subject_names=subject_dictionary)

		# Sometimes you want to know how good the model may perform on the data
		# given, the script allows you to perform a k-fold Cross Validation before
		# the Detection & Recognition part starts:
		'''
		if numfolds:
			print "Validating model with %s folds..." % options.numfolds
			# We want to have some log output, so set up a new logging handler
			# and point it to stdout:
			handler = logging.StreamHandler(sys.stdout)
			formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
			handler.setFormatter(formatter)
			# Add a handler to facerec modules, so we see what's going on inside:
			logger = logging.getLogger("facerec")
			logger.addHandler(handler)
			logger.setLevel(logging.DEBUG)
			# Perform the validation & print results:
			crossval = KFoldCrossValidation(model, k=numfolds)
			crossval.validate(images, labels)
			crossval.print_results()
		'''
		# Compute the model:
		print "Computing the model..."
		model.compute(images, labels)
		# And save the model, which uses Pythons pickle module:
		print "Saving the model..."
		save_model(model_filename, model)
	else:
		#print "Loading the model..."
		model = load_model(model_filename)
	# We operate on an ExtendedPredictableModel. Quit the application if this
	# isn't what we expect it to be:
	if not isinstance(model, ExtendedPredictableModel):
		#print "[Error] The given model is not of type '%s'." % "ExtendedPredictableModel"
		sys.exit()
	# Now it's time to finally start the Application! It simply get's the model
	# and the image size the incoming webcam or video images are resized to:
	print "Starting application..."
	nametags = App(model=model,
				camera_id=0,
				cascade_filename=cascade_filename,
				video_file=vid_filename).run()
	return nametags
