
# coding: utf-8

# In[2]:

import keras.backend as K
from keras.layers import Flatten, Dense, Conv2D, MaxPooling2D, Activation, Dropout, Input
from keras.models import Sequential, Model
from keras.callbacks import TensorBoard, ModelCheckpoint
from keras.optimizers import SGD
from keras.layers.core import Lambda

from custom import LocalResponseNormalization

from os import listdir, mkdir
from os.path import join, isdir
from scipy.misc import imread
import numpy as np
from sklearn.utils import shuffle
from scipy.io import loadmat
import h5py
import sys

np.random.RandomState(0)

img_height = 54
img_width = 32
num_channels = 3
num_classes = 2
num_images_train = 207574
num_images_test = 216649

root = 'PKLot/PKLotSegmented/PUC/'

trainX = np.zeros((num_images_train, img_height, img_width, num_channels))
validX  = np.zeros((num_images_test, img_height, img_width, num_channels))

trainY = np.zeros(num_images_train)
validY = np.zeros(num_images_test)

counter_train = 0
counter_test = 0

if not isdir('weights'):
    mkdir('weights')

if not isdir(root):
    print('PKLot dataset folder missing... Exiting!!')
    sys.exit(0)

weathers = [w for w in listdir(root)]

#------------------------------------------------------------- Preparing Data
print('Preparing data...')
for weather in weathers:
    root_ = root + weather + '/'
    print("Inside folder: %s" % root_)
    days = [day for day in listdir(root_)]
    mid = len(days)/2
    train_days = days[:mid]
    test_days = days[mid:]
    
    # add to train data
    for day in train_days:
        _root_ = root_ + day + '/'
        print("Inside folder: %s" % _root_)
        labels = [label for label in listdir(_root_)]
        for i, label in enumerate(labels):
            img_root = _root_ + label + '/'
            img_names = [img for img in listdir(img_root)]
            for j,img_name in enumerate(img_names):
                if (j+1) % 1000 == 0:
                    print("Inside folder: %s, image # %d" % (img_root, j+1))
                img = imread(img_root + img_name)
                img = np.resize(img, (img_height, img_width, num_channels))
                trainX[counter_train] = img
                trainY[counter_train] = 1-i
                counter_train += 1
    
    # add to test data
    for day in test_days:
        _root_ = root_ + day + '/'
        print("Inside folder: %s" % _root_)
        labels = [label for label in listdir(_root_)]
        for i, label in enumerate(labels):
            img_root = _root_ + label + '/'
            img_names = [img for img in listdir(img_root)]
            for j,img_name in enumerate(img_names):
                if (j+1) % 1000 == 0:
                    print("Inside folder: %s, image # %d" % (img_root, j+1))
                img = imread(img_root + img_name)
                img = np.resize(img, (img_height, img_width, num_channels))
                validX[counter_test] = img
                validY[counter_test] = 1-i
                counter_test += 1

print('Done')

trainX, trainY = shuffle(trainX, trainY)
validX, validY = shuffle(validX, validY)

print('Saving to h5py')
data = h5py.File('data.h5', 'w')
data.create_dataset('trainX', data=trainX)
data.create_dataset('trainY', data=trainY)
data.create_dataset('validX', data=validX)
data.create_dataset('validY', data=validY)
print('Done.')

#------------------------------------------------------------- Model

def VGG_16():
    '''Model definition'''

    model = Sequential()
    model.add(Conv2D(64, (11, 11,), padding='valid', strides=(4,4), input_shape=(img_height,img_width,num_channels), name='conv1'))
    model.add(Activation('relu', name='relu1'))
    model.add(LocalResponseNormalization(name='norm1'))
    model.add(MaxPooling2D((2,2), padding='same', name='pool1'))

    model.add(Conv2D(256, (5,5), padding='same', name='conv2'))
    model.add(Activation('relu', name='relu2'))
    model.add(LocalResponseNormalization(name='norm2'))
    model.add(MaxPooling2D((2,2), padding='same', name='pool2'))

    model.add(Conv2D(256, (3, 3), padding='same', name='conv3'))
    model.add(Activation('relu', name='relu3'))
    model.add(Conv2D(256, (3, 3), padding='same', name='conv4'))
    model.add(Activation('relu', name='relu4'))
    model.add(Conv2D(256, (3, 3), padding='same', name='conv5'))
    model.add(Activation('relu', name='relu5'))
    model.add(MaxPooling2D((2,2), padding='same', name='pool5'))

    return model

def copy_mat_to_keras(kmodel, weights_path):
    '''Utility function

    Loads weights from .mat file to keras model
    '''

    kerasnames = [lr.name for lr in kmodel.layers]
    data = loadmat(weights_path, matlab_compatible=False, struct_as_record=False)
    layers = data['layers']
    description = data['meta'][0,0].classes[0,0].description

    prmt = (0,1,2,3)

    for i in range(layers.shape[1]):
        matname = layers[0,i][0,0].name[0]
        if matname in kerasnames:
            kindex = kerasnames.index(matname)
            if len(layers[0,i][0,0].weights) > 0:
                l_weights = layers[0,i][0,0].weights[0,0]
                l_bias = layers[0,i][0,0].weights[0,1]
                f_l_weights = l_weights.transpose(prmt)
                assert (f_l_weights.shape == kmodel.layers[kindex].get_weights()[0].shape)
                assert (l_bias.shape[1] == 1)
                assert (l_bias[:,0].shape == kmodel.layers[kindex].get_weights()[1].shape)
                assert (len(kmodel.layers[kindex].get_weights()) == 2)
                kmodel.layers[kindex].set_weights([f_l_weights, l_bias[:,0]])

model = VGG_16()
# Load pre-trained weights from .mat file
copy_mat_to_keras(model, 'weights/imagenet-vgg-f.mat')

# Freeze the convolutional layers
for layer in model.layers:
    layer.trainable = False

model.add(Flatten())
model.add(Dropout(0.5, name='dropout6'))
model.add(Dense(4096, activation='relu', name='fc6'))
model.add(Dropout(0.5, name='dropout7'))
model.add(Dense(4096, activation='relu', name='fc7'))
model.add(Dropout(0.5, name='dropout8'))
model.add(Dense(1, activation='sigmoid', name='predictions'))

model.summary()

# Hyperparameters
batch_size = 128
epochs = 100
learning_rate = 0.00001
weight_decay = 0.0005
nesterov = True
momentum = 0.99

#------------------------------------------------------------- Training

# optimizer
sgd = SGD(lr=learning_rate, decay=weight_decay, momentum=momentum, nesterov=nesterov)

# Callbacks
tb = TensorBoard(log_dir='./logs', histogram_freq=0, write_graph=True, write_images=False)
checkpointer = ModelCheckpoint(filepath="./weights/checkpoint-{epoch:02d}-{val_loss:.2f}.hdf5", verbose=1)

model.compile(loss='binary_crossentropy', optimizer=sgd, metrics=['accuracy'])

model.fit(trainX, trainY,
          batch_size=batch_size,
          epochs=epochs,
          verbose=1,
          validation_data=(validX, validY),
          callbacks=[checkpointer, tb])

model.save('model.h5')
print('Training complete.')

