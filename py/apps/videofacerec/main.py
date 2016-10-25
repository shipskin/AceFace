import sys
import os
import subprocess
import json
import pickle
from videofacerec import *

def initiate_vid(**kwargs):
	vid_args = {}
	PARAMETERS = ['model_param','dataset_param','cascade_param','vidpath_param','resize_param']
	for key in PARAMETERS:
		try:
			vid_args[key]= kwargs[key]
		except KeyError:
			vid_args[key]= None
			pass
	return vid_run_main(**vid_args)


def vid_parse(vid_dir_path):
	nametags = {}
	for vid in os.listdir(vid_dir_path):
		if not vid.startswith('.') and not vid.startswith('$'):
			print "Tagging video..."
			nametags = initiate_vid(
				model_param = 'model.pkl',
				vidpath_param = vid_dir_path+'/'+vid,
				dataset_param = '/Users/kage/faceimagesDB/facedb')
			yield [vid,nametags]



def gener_db(vid_dir_path):
	VIDDB = {}
	nametags = vid_parse(vid_dir_path)
	for vid,tags in nametags:
		VIDDB[vid] = tags
	with open('vidtags.pickle', 'rb') as f:
	  db = pickle.load(f)
	  for datum in VIDDB:
		  db[datum] = VIDDB[vid]

	with open('vidtags.pickle', 'wb') as f:
		pickle.dump(db, f)



gener_db('/Users/kage/xvids/test/')

testdata = {'annie.mp4': {'sara_sigmundsdottir': {'hits': 14, 'time': 47}, 'annie_thorisdottir': {'hits': 49, 'time': 25}, 'mat_fraser': {'hits': 10, 'time': 21}, 'rich_froning': {'hits': 5, 'time': 21}, 'samantha_briggs': {'hits': 0, 'time': 22}}}



'''
initiate_vid(
	model_param = 'model.pkl',
	vidpath_param = '/Users/kage/xvids/test/annie.mp4',
	dataset_param = '/Users/kage/faceimagesDB/facedb')
'''
