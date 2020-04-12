# just get the faces 
# https://stackoverflow.com/questions/8535650/how-to-change-saturation-values-with-opencv

import cv2
import glob
import os
import numpy as np
from shutil import copyfile

face_det = cv2.CascadeClassifier("OpenCV_FaceCascade\lbpcascade_animeface.xml")

#face_det = cv2.CascadeClassifier("OpenCV_FaceCascade\haarcascade_frontalface_default.xml")
#face_det2 = cv2.CascadeClassifier("OpenCV_FaceCascade\haarcascade_frontalface_alt2.xml")
#face_det3 = cv2.CascadeClassifier("OpenCV_FaceCascade\haarcascade_frontalface_alt.xml")
#face_det4 = cv2.CascadeClassifier("OpenCV_FaceCascade\haarcascade_frontalface_alt_tree.xml")

this_dir = os.path.dirname(os.path.abspath(__file__))
	

def extract_anime_faces(directory):
	images = glob.glob(f"{directory}\\*")

	for img in images:
		file_name = img[img.rindex("\\")+1:]
		
		# convert image to grayscale
		frame = cv2.imread(img, cv2.IMREAD_COLOR)
		
		grayscale_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		#grayscale_img = cv2.equalizeHist(grayscale_img)
		

		# detect the face using the 4 classifiers
		faces = face_det.detectMultiScale(grayscale_img, scaleFactor=1.05, minNeighbors=6, minSize=(30,30))
		
		# find and save face
		for (x, y, w, h) in faces:
			print(f"got face for: {file_name}")
			grayscale_img = grayscale_img[y:y+h, x:x+w]
			try:
				dest = f"{directory}_extracted_dataset"
				if not os.path.exists(dest):
					os.makedirs(dest)
					print(f"created: {dest}")
				
				out = cv2.resize(grayscale_img, (350, 350))
				cv2.imwrite(f"{dest}\{file_name}", out)
			except:
				print(f"failure for img: {file_name}")
		
		
extract_anime_faces("anime_faces")