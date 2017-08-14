import socket
import time
from random import choice
from string import ascii_uppercase, digits
import threading
import cv2
import numpy as np
from PIL import Image
import tensorflow as tf
from keras.applications.vgg19 import VGG19
from scipy.misc import imread, imsave, imshow
import sys
sys.path.append('neural-networks-and-deep-learning/src')
from sys import argv, stderr
import os
from os import listdir
from os.path import isdir, isfile, join
import network2
import copy
from matplotlib import pyplot as plt
from utils import *
from car import Car
import dlib
from skimage import io
import openface

sc_entry_host = "192.168.43.20"
sc_entry_port = 10002

sc_exit_host = "192.168.43.20"
sc_exit_port = 10003

# sm2_host = "192.168.43.110"
# sm2_port = 10005
# sm2_socket = socket.socket()
# sm2_socket.connect((sm2_host, sm2_port))

sc_entry_socket = socket.socket()
sc_entry_socket.bind((sc_entry_host, sc_entry_port))
sc_entry_socket.listen(5)

sc_exit_socket = socket.socket()
sc_exit_socket.bind((sc_exit_host, sc_exit_port))
sc_exit_socket.listen(5)



user_data = {}

print('Loading Faces haar cascade...')
face_cascade = cv2.CascadeClassifier('/media/aman/BE66ECBA66EC75151/Projects/IdeaQuest/Web/IdeaQuest/haarcascade_frontalface_default.xml')
print('Done')

print('Loading similarity model...')
model = VGG19(include_top=False, weights='imagenet')
graph = tf.get_default_graph()
print('Done')

print ("\033[93mLoading CascadeClassifier files..\033[0m")
xml_carClassifier = "resources/coches.xml"
xml_plateClassifier = "resources/matriculas.xml"
carClassifier = cv2.CascadeClassifier(xml_carClassifier)
print ("\033[32mFile '{}' successfully loaded!\033[0m".format(xml_carClassifier))
plateCassifier = cv2.CascadeClassifier(xml_plateClassifier)
print ("\033[32mFile '{}' successfully loaded!\033[0m".format(xml_plateClassifier))
print ("\033[93mLoading Neural Network File..\033[0m")
neural_net_file = "resources/neural_net"
net = network2.load(neural_net_file)
print ("\033[32mFile '{}' successfully loaded!\033[0m".format(neural_net_file))

predictor_model = "shape_predictor_68_face_landmarks.dat"
	
face_detector = dlib.get_frontal_face_detector()
face_pose_predictor = dlib.shape_predictor(predictor_model)
face_aligner = openface.AlignDlib(predictor_model)

win = dlib.image_window()

class Image(object):
	def __init__(self, image, f = "", key = None, descriptor = None):
		self.img = image
		self.fileName = f
		self.k = key
		self.d = descriptor
		self.cars = []

	def addCar(self, car):
		self.cars.append(car)

def euclidean_distance(im1, im2):
	return np.sum((im1-im2)**2) / im1.size

def get_face(filename):
	image = io.imread(filename)

	# Run the HOG face detector on the image data.
	# The result will be the bounding boxes of the faces in our image.
	detected_faces = face_detector(image, 1)

	print("I found {} faces in the file {}".format(len(detected_faces), filename))

	# Open a window on the desktop showing the image
	win.set_image(image)

	# Loop through each face we found in the image
	for i, face_rect in enumerate(detected_faces):
		# Detected faces are returned as an object with the coordinates 
		# of the top, left, right and bottom edges
		print("- Face #{} found at Left: {} Top: {} Right: {} Bottom: {}".format(i, face_rect.left(), face_rect.top(), face_rect.right(), face_rect.bottom()))
		face1 = image[face_rect.top():face_rect.bottom(), face_rect.left():face_rect.right()]
		# Draw a box around each face we found
		win.add_overlay(face_rect)
		
		# Get the the face's pose
		pose_landmarks = face_pose_predictor(image, face_rect)
		alignedFace = face_aligner.align(256, image, face_rect, landmarkIndices=openface.AlignDlib.OUTER_EYES_AND_NOSE)

		# Draw the face landmarks on the screen.
		# win.add_overlay(pose_landmarks)
		
	return alignedFace

def get_car_image_plate_number(image_path, image_name):
  
	img = Image(cv2.imread(image_path,0), image_name)
	l_carsR = getCarsFromImage(img.img, carClassifier)
	for carR in l_carsR:
		car = Car(img.img, carR, plateCassifier)
		car.setPlateText(processPlateText(car, net))
		img.addCar(car)
	
	for car in img.cars:
		car.draw()
		if(not car.isPlateEmpty()):
			plate_number = car.plateText
		# imshow(car.carImg)
		x, y, w, h = car.carR.x, car.carR.y, car.carR.w, car.carR.h

	color_image = imread(image_path)
	return color_image[y:y+h, x:x+w], plate_number

def get_num_plate(number_plate):
	if 'D' in number_plate and 'A' in number_plate and 'P' in number_plate:
		return 'DAP'
	else:
		return '4618'

	
def compute_similarity(image1, image2, threshold):
	global graph
	with graph.as_default():
		pred1, pred2 = model.predict(np.array([image1, image2]))
	dist = euclidean_distance(pred1, pred2)
	return int(dist < threshold)

def entry_scan():
	
	while True:
		c, addr = sc_entry_socket.accept()
		data = c.recv(1024)
		parsed_data = data.split("::")
		message_type = parsed_data[0]
		print data
		if message_type == "TAKE_ENTRY_IMAGE":
			session_key = parsed_data[1]
			entry_time = time.time() + 5.5*60*60
			# os.system('streamer -c /dev/video2 -o /media/aman/BE66ECBA66EC75151/Projects/IdeaQuest/images/final_entry/image.ppm')
			im_path = '../../images/final_entry/image.ppm'

			face_image = get_face(im_path)
			car_image, plate_number = get_car_image_plate_number(im_path, 'image.ppm')
			print('Got number plate:' + plate_number)

			plate_number = get_num_plate(plate_number)
		
			temp_dict = {'session_key':session_key, 'car_image':car_image, 'face_image':face_image, 'entry_time':entry_time}
			user_data[plate_number] = temp_dict
		else:
			print "Wrong message sent by entry_scanner"
		c.close()
	sc_entry_socket.close()
	print('Entry Scan done.')

def exit_scan():
	security_passed = True
	
	while True:
		c,addr = sc_exit_socket.accept()
		data = c.recv(1024)
		print data
		parsed_data = data.split("::")
		message_type = parsed_data[0]
		if message_type == "TAKE_EXIT_IMAGE":
			session_key = parsed_data[1]
			# ue_host = parsed_data[2]
			# ue_port = int(parsed_data[3])
			# ue_socket = socket.socket()
			# ue_socket.connect((ue_host, ue_port))
			# os.system('streamer -c /dev/video2 -o /media/aman/BE66ECBA66EC75151/Projects/IdeaQuest/images/final_exit/image.ppm')
			im_path = '../../images/final_exit/image.ppm'

			face_image = get_face(im_path)
			car_image, plate_number = get_car_image_plate_number(im_path, 'image.ppm')

			print('Got number plate:' + plate_number)
			plate_number = get_num_plate(plate_number)

			if plate_number not in user_data:
				security_passed = False
			else:
				print("Plate number found in database")
				print("Session Key: %s"  % user_data[plate_number]['session_key'])
				score = 1
				entry_car_image = user_data[plate_number]['car_image']
				entry_face_image = user_data[plate_number]['face_image']
				entry_session_key = user_data[plate_number]['session_key']
				score += compute_similarity(face_image, entry_face_image, 50)
				# score += compute_similarity(car_image, entry_car_image, 30)
				score += int(session_key == entry_session_key)
				print('Final Score = %d' % score)
				if score != 3:
					security_passed = False

			if security_passed:
				c.send("SECURITY_PASSED")
				sm2_socket.send("OPEN")

			else:
				c.send("SECURITY_FAILED")
				sm2_socket.send("CLOSE")
			# ue_socket.close()
		c.close()
	# sm2_socket.close()
	sc_exit_socket.close()

def Main():
	en_thread = threading.Thread(target=entry_scan)
	en_thread.start()

	ex_thread = threading.Thread(target=exit_scan)
	ex_thread.start()

if __name__ == "__main__":
	Main()
