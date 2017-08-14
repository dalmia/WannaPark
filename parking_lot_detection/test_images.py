import matplotlib.pyplot as plt
from scipy.misc import imread, imshow
import numpy as np
from PIL import Image
from keras.models import load_model
from keras.engine.topology import Layer, InputSpec
from custom import LocalResponseNormalization
import cv2   
import os
from os.path import isfile, join, exists
import socket
import time
import sys

MAGIC = "face600d"

counter = 0
server_host = "192.168.43.20"
server_port = 5000
total_time = 0

IMAGE_DIR = '../images/final_detection/image.ppm'
CHECKPOINT_DIR = 'weights/checkpoint-07-0.07.hdf5'

if not exists(IMAGE_DIR):
    print('Image file missing... Exiting!!')
    sys.exit(0)

if not exists(CHECKPOINT_DIR):
    print('Checkpoint file missing... Exiting!!')
    sys.exit(0)

model = load_model(CHECKPOINT_DIR, custom_objects={'LocalResponseNormalization': LocalResponseNormalization})

while True:

    # os.system('streamer -c /dev/video0 -o /media/aman/BE66ECBA66EC75151/Projects/IdeaQuest/images/final_detection/image.ppm')
    im = imread(IMAGE_DIR)
    imshow(im)

    x_shift = 32
    y_shift = 54
    x_range = [0, 32, 64, 96]
    y_range = [0, 108]

    im = Image.fromarray(im)
    im = im.resize((162, 128))
    im = np.array(im)

    images = []
    for x in x_range:
        for y in y_range:
            im_ = Image.fromarray(im[x+2:x+x_shift-2, y+2:y+y_shift-2])
            im_ = im_.resize((54, 32))
            im_ = np.array(im_)
            im_ = im_.transpose(1,0,2)
            images.append(im_)

    images = np.array(images)

    predictions = model.predict(images, verbose=1)

    predictions = np.hstack(predictions < 0.5).astype(int)

    i = 0
    im_ = np.copy(im)
    for x in x_range:
        for y in y_range:
            im_ = cv2.rectangle(im_,(y,x+2),(y+y_shift,x+x_shift-2),(255*(predictions[i]),255*(1-predictions[i]),0),2)
            i += 1

    imshow(im_)
    break

    # total = str(len(predictions))
    # available = str(len(np.where(predictions == 1)[0]))
    # detail = ''
    # for pred in predictions:
    #     detail += str(pred)

    # data = "magic=" + MAGIC + "::identity=" + identity + "::total=" + total + "::available=" + available + "::detail=" + detail
    # print(data)
    # server_socket = socket.socket()

    # server_socket.connect((server_host, server_port))    
    # server_socket.send(data)
    # server_socket.close()
    # time.sleep(5)



