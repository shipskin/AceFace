import sys
import os
import subprocess
import json

main_path = '/Users/kage/aceface/Aceface/'
os.chdir(main_path+'/py/apps/videofacerec/')
vid_dir_path = sys.argv[1]


def vid_parse(vid_dir_path):

	for vid in os.listdir(vid_dir_path):
		if not vid.startswith('.') and not vid.startswith('$'):
			cmd = ['python',
				main_path+'py/apps/videofacerec/videofacerec.py',
				main_path+'py/apps/videofacerec/model.pkl',
				'-f',
				os.path.join(vid_dir_path, vid)]
			proc = subprocess.check_output(cmd)
			print proc
			return vid,proc
			#return json.loads(json_line)


def gener_db():
	vid,nametag = vid_parse(vid_dir_path)
	for name in nametag:
		print name['hits']
		print vid


testata = {'annie_thorisdottir\n': {'hits': 19, 'time': 22}, 'mat_fraser\n': {'hits': 4, 'time': 21}, 'katrin_davidsdottir\n': {'hits': 6, 'time': 25}, 'rich_froning\n': {'hits': 6, 'time': 27}, 'samantha_briggs\n': {'hits': 36, 'time': 33}, 'emily_bridgers': {'hits': 7, 'time': 22}}


gener_db()
