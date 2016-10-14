import os as os
import argparse
from pathlib import Path
import shutil

def main(photo_file):
	files=os.listdir(photo_file)
	for file in files:
		print (os.path.abspath(os.path.join(photo_file, file)))
		abs_file=os.path.abspath(os.path.join(photo_file, file)) 
		label_dir = "C:\\BigData\\google\\api\python-docs-samples\\vision\\api\label\\folders\\"+file.split('.')[0]
		try:
			label_dir = os.makedirs(label_dir)
		except OSError:
			pass
		shutil.copy(abs_file,label_dir)

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('image_dir', help='The dir containing images you\'d like to label.')
	args = parser.parse_args()
	main(args.image_dir)