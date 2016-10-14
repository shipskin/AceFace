import sys
import os
import subprocess

main_path = '/Users/Stephen/Documents/Code/AceFace/'
os.chdir(main_path+'py/apps/videofacerec/')
vid_dir_path = sys.argv[1]

def vid_parse(vid_dir_path):
	vid_tags = []
	for vid in os.listdir(vid_dir_path):
		if not vid.startswith('.') and not vid.startswith('$'):
			cmd = ['python', main_path+'py/apps/videofacerec/videofacerec.py', main_path+'py/apps/videofacerec/model.pkl', '-f', os.path.join(vid_dir_path, vid)]
			proc = subprocess.check_output(cmd)
			vid_tags.append(proc)
	return vid_tags

print vid_parse(vid_dir_path)
