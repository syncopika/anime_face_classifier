import glob

def get_image_list(directory, output):
	images = glob.glob(f"{directory}\\*")
	f = open(f"{output}.txt", "w")

	for img in images:
		f.write(img+"\n")
		
get_image_list("negative_images", "negative_image_list")
get_image_list("positive_images2", "positive_image_list")