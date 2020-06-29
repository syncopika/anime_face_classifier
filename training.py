"""
get_images, 
make_sets and 
run_recognizer functions came from Paul van Gent's tutorial:

van Gent, P. (2016). Emotion Recognition With Python, OpenCV and a Face Dataset. A tech blog about fun things with Python and embedded electronics. Retrieved from:
http://www.paulvangent.com/2016/04/01/emotion-recognition-with-python-opencv-and-a-face-dataset/

"""

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
import random
import numpy as np
from extract_animefaces import *
from shutil import copyfile

this_dir = os.path.dirname(os.path.abspath(__file__))

emotions = ['happy','sad','surprised','angry','scared','worried','neutral']

fisher_face = cv2.face.FisherFaceRecognizer_create()

	
def get_images(emotion):
	images = glob.glob(f"emotions_dataset\{emotion}\*.png")
	random.shuffle(images)
	training = images[:int(len(images) * 0.8)]
	prediction = images[-int(len(images) * 0.2):]
	return training, prediction

def make_sets():
	training_data = []
	training_labels = []
	prediction_data = []
	prediction_labels = []
	
	for emotion in emotions:
		training, prediction = get_images(emotion)
		
		for item in training:
			image = cv2.imread(item)
			grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
			training_data.append(grayscale)
			training_labels.append(emotions.index(emotion))
		
		for item in prediction:
			image = cv2.imread(item)
			grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
			prediction_data.append(grayscale)
			prediction_labels.append(emotions.index(emotion))
			
	return training_data, training_labels, prediction_data, prediction_labels
		
def run_recognizer():
	training_data, training_labels, prediction_data, prediction_labels = make_sets()
	print("training fisher face classifier...")
	print(f"size of training set is: {len(training_labels)} images")
	fisher_face.train(training_data, np.asarray(training_labels))
	
	print("predicting classification set...")
	count = 0
	correct = 0
	incorrect = 0
	for image in prediction_data:
		pred, conf = fisher_face.predict(image)
		if pred == prediction_labels[count]:
			correct += 1
		else:
			incorrect += 1
		count += 1
	return ((100*correct)/(correct + incorrect))
	

######## do the training for the recognizer 
metascore = []
for i in range(0,20):
	print(f"training recognizer: stage {i}")
	correct = run_recognizer()
	print(f"run {i+1}: got {correct}% correct!")
	metascore.append(correct)



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
		# based on pred, put image in folder (a copy of the original image!)
		print(f"classifying {file_name} as {emotions[pred]}!") 
		copyfile(image, f"{this_dir}\{folder_name}_sorted\{emotions[pred]}\{file_name}")

	print("done!")
	
	
	
####### try out the recognizer on new data
sort_images_by_emotion("test_data\\", emotions, fisher_face)