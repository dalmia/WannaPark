import sys
import dlib
from skimage import io
from PIL import Image
from scipy.misc import imread, imshow, imsave
import cv2
import numpy as np
import openface
from keras.applications.vgg19 import VGG19
#-------------------------------------------------------------------

def get_face(filename):
    # Create a HOG face detector using the built-in dlib class
    predictor_model = "shape_predictor_68_face_landmarks.dat"
    
    face_detector = dlib.get_frontal_face_detector()
    face_pose_predictor = dlib.shape_predictor(predictor_model)
    face_aligner = openface.AlignDlib(predictor_model)

    win = dlib.image_window()

    # Load the image into an array
    image = io.imread(filename)

    # Run the HOG face detector on the image data.
    # The result will be the bounding boxes of the faces in our image.
    detected_faces = face_detector(image, 1)

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
        alignedFace = face_aligner.align(534, image, face_rect, landmarkIndices=openface.AlignDlib.OUTER_EYES_AND_NOSE)

        # Draw the face landmarks on the screen.
        #win.add_overlay(pose_landmarks)
    return face1, alignedFace
#----------------------------------------------------------------------------------------

faces = get_face('../images/final_entry/image.jpg')
imsave('face.jpg', faces[0])