# http://www.paulvangent.com/2016/04/01/emotion-recognition-with-python-opencv-and-a-face-dataset/
# https://stackoverflow.com/questions/47202316/saving-opencv-object-in-memory-in-python
# https://stackoverflow.com/questions/46968477/opencv3-python-3-how-to-train-fisherfacerecognizer-dataset
# https://stackoverflow.com/questions/20801015/recommended-values-for-opencv-detectmultiscale-parameters
# http://www.willberger.org/cascade-haar-explained/
# https://docs.opencv.org/2.4/modules/contrib/doc/facerec/facerec_tutorial.html
# https://docs.opencv.org/3.4/db/d28/tutorial_cascade_classifier.html

# oooooooh: https://github.com/nagadomi/lbpcascade_animeface
# https://freedomofkeima.com/blog/posts/flag-15-image-recognition-for-anime-characters

"""
	step 1: get dataset
		- requires good face extractor first!
		- need to better understand Haar classifiers
	step 2: train recognizer
		- try LBPH? or Fisherface
	step 3: test on input 
	
	- need python script for making the dataset to train on
		- clean up images, get faces 
		- separate by emotion (manual step)
		
		
		
	6/19/20
	let's assume we have a satisfactory (for the most part) face detector/extractor 
	
	so:
	1. make sure you have a sorted face emotion dataset to train on!
		- this can be made easier with your supposed satisfactory face extractor 
		- make sure there's a decent number of samples 
	2. train the dataset 
	3. get a new dataset to test on! these should be just a bunch of new, random images with faces.
	4. using your face extractor, take the face, run against the recognizer we trained, and see if the output is good.
		- we can probably expect a few false positives
	
"""

import cv2
import glob
import os
from shutil import copyfile

# raw dataset needs to be sorted first by emotion 
# then this can be used to create a clean dataset for training
def create_training_set(directory):
	pass

def sort_images_by_emotion(folder_path, emotions, recognizer):
	# but waitttt! the recognizer defines what emotions it can predict
	# just make sure you know the emotions list defined above is what it uses
	# if we pass in fisher_face
	folder_name = folder_path[:folder_path.index("\\")]

	# get all images in folder
	images = glob.glob(f"{folder_path}\*")
	
	# new directory for the output and for each emotion
	for emotion in emotions:
		emotion_folder = f"{this_dir}\{folder_name}_sorted\{emotion}"
		if not os.path.exists(emotion_folder):
			os.makedirs(emotion_folder)
			print(f"created: {emotion_folder}")
					
	# use the recognizer to predict the images
	for image in images:
		print(f"working on: {image}")
		file_name = image[image.rindex("\\")+1:]
		img = extract_face(image)
		if img is None:
			print(f"no face found for: {image}")
			continue
		pred, conf = recognizer.predict(img)
		# based on pred, put image in folder (the original image!)
		copyfile(image, f"{this_dir}\{folder_name}_sorted\{emotions[pred]}\{file_name}")

	print("done!")