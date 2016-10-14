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

			return proc
			#return json.loads(json_line)


print vid_parse(vid_dir_path)
