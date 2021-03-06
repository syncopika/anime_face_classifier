# just get the faces 

import cv2
import glob
import os
import numpy as np
from shutil import copyfile

face_det = cv2.CascadeClassifier("cascade_classifier\cascade.xml")

this_dir = os.path.dirname(os.path.abspath(__file__))


def extract_face(image_path):

	# convert image to grayscale
	frame = cv2.imread(image_path)
	grayscale_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	# detect the face features
	faces = face_det.detectMultiScale(grayscale_img, scaleFactor=1.05, minNeighbors=3, minSize=(30,30))
	
	# find and save face
	out = None
	count = 0
	for (x, y, w, h) in faces:
		feature = grayscale_img[y:y+h, x:x+w]
		try:			
			out = cv2.resize(feature, (350, 350))
		except Exception as err:
			print(f"{err}: failure for img: {image_path}")
		count += 1
		
	print(f"found {count} feature(s) for: {image_path}")
		
	return out # cv2.imwrite(f"{dest}\{file_name}_{count}.png", out)
	

def extract_anime_faces(directory):
	images = glob.glob(f"{directory}\\*")

	hits = 0
	for img in images:
		file_name = img[img.rindex("\\")+1:img.index(".p")] # ASSUMING PNG IMAGES!
		
		# convert image to grayscale
		frame = cv2.imread(img, cv2.IMREAD_COLOR)
		
		grayscale_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		#grayscale_img = cv2.equalizeHist(grayscale_img)

		# detect the face features
		faces = face_det.detectMultiScale(grayscale_img, scaleFactor=1.05, minNeighbors=3, minSize=(30,30))
		
		# find and save face
		count = 0
		for (x, y, w, h) in faces:
			#print(f"dimensions: x->{x}, y->{y}, w->{w}, h->{h}")
			feature = grayscale_img[y:y+h, x:x+w]
			try:
				dest = f"{directory}_extracted_dataset2"
				if not os.path.exists(dest):
					os.makedirs(dest)
					print(f"created: {dest}")
				
				out = cv2.resize(feature, (350, 350))
				cv2.imwrite(f"{dest}\{file_name}_{count}.png", out)
			except Exception as err:
				print(f"{err}: failure for img: {file_name}")
			count += 1
			
		if count > 0:
			hits += 1
			
		print(f"found {count} feature(s) for: {file_name}")
		
	print(f"found faces for {hits} images out of {len(images)}")
		
		
#extract_anime_faces("anime_faces")