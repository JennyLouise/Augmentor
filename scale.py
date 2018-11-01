import math
from cv2 import imread, imwrite
import csv
from PIL import Image
import numpy as np

vertical_opening_angle=52.1
horizontal_opening_angle=60.4

def rescale_image(image_directory, image_name, target_pixel_size, data_filename):
	altitude = get_altitude(image_name.strip(), data_filename)
	print(image_directory+image_name)
	image = imread(image_directory + image_name.strip())
	print(image)
	shape=image.shape
	image_width=shape[0]
	image_height=shape[1]
	pixel_height = get_pixel_height(altitude, image_height)
	print(pixel_height)
	pixel_width = get_pixel_width(altitude, image_width)
	print(pixel_width)
	vertical_rescale=pixel_height/target_pixel_size
	horizontal_rescale=pixel_width/target_pixel_size
	size=(int(image_width*horizontal_rescale), int(image_height*vertical_rescale))
	print(size)
	image = Image.fromarray(image.astype('uint8'), 'RGB')
	image= image.resize(size, Image.NEAREST)
	print(np.array(image).shape)
	return np.array(image)

#pulls altitude of given image out of datafile and returns it
def get_altitude(image_name, data_filename):
	data_file = open(data_filename, 'r')
	reader = csv.reader(data_file, delimiter='	')
	image_number='_'.join(image_name.split('_')[2:3])
	matched_lines = [line for line in data_file.readlines() if image_number in line]
	print(matched_lines)
	if(matched_lines == []):
		print("ERROR: image name not found in data file")
		exit()
	altitude=matched_lines[0].split('	')[12]
	print(altitude)
	return altitude

#uses given vertical opening angle of camera and the altitude parameter to determine the pixel height
def get_pixel_height(altitude, image_height):
	image_spatial_height=2*float(altitude)*float(math.tan(math.radians(vertical_opening_angle/2)))
	pixel_height=image_spatial_height/image_height
	return pixel_height

#uses given horizontal opening angle of camera and the altitude parameter to determine the pixel width
def get_pixel_width(altitude, image_width):
	image_spatial_width=2*float(altitude)*float(math.tan(math.radians(horizontal_opening_angle/2)))
	pixel_width=image_spatial_width/image_width
	return pixel_width

def rescale_many_images(image_directory, image_list_filename, target_pixel_size, data_filename, output_directory):
	image_list = open(image_list_filename, 'r')
	for image_name in image_list.readlines():
		image_file = open(output_directory+image_name.strip(), 'w')
		imwrite(output_directory+image_name.strip(), rescale_image(image_directory, image_name, target_pixel_size, data_filename))


rescale_many_images("/scratch/jw22g14/Joetsu/images/", "list.txt", 0.01, "./stereo_pose_est.data", "/scratch/jw22g14/Joetsu/rescaled/")
