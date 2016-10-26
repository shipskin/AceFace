import sys
import os
import subprocess
import json
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
				dataset_param = '/Users/Stephen/faceimagesDB/histodb')
			yield [vid,nametags]



def gener_db(vid_dir_path):
	VIDDB = {}
	nametags = vid_parse(vid_dir_path)
	for vid,tags in nametags:
		VIDDB[vid] = tags
	print VIDDB


gener_db('/Users/Stephen/Movies/crossfit')

testata = {'annie_thorisdottir\n': {'hits': 19, 'time': 22}, 'mat_fraser\n': {'hits': 4, 'time': 21}, 'katrin_davidsdottir\n': {'hits': 6, 'time': 25}, 'rich_froning\n': {'hits': 6, 'time': 27}, 'samantha_briggs\n': {'hits': 36, 'time': 33}, 'emily_bridgers': {'hits': 7, 'time': 22}}

'''
initiate_vid(
	model_param = 'model.pkl',
	vidpath_param = '/Users/kage/xvids/test/annie.mp4',
	dataset_param = '/Users/kage/faceimagesDB/facedb')
'''
