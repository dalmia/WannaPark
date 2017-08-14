# Parking lot Vacancy Detection using Deep Learning

Using images from CCTV camera, classify whether a parking spot is vacant or not.

## Dataset

We used the PKLot dataset, which can be found [here](http://www.inf.ufpr.br/lesoliveira/download/pklot-readme.pdf). This database contains 12,417 images (1280X720) captured 
from two different parking lots (parking1 and parking2) in sunny, cloudy and rainy days. On using the annotations to get the
image of each parking lot, we end up with ~ 695600 images of size 54x32.

## Model Architecture

We choose to fine-tune the pre-trained VGGNet (specifically its F-variant). The pre-trained weights can be obtained from [here](http://www.vlfeat.org/matconvnet/models/imagenet-vgg-f.mat).
We fix the convolutional layers, i.e., we don't fine-tune the convolutional layers, only the dense layers above it. You can download
checkpoint for testing the image directly from [here](https://drive.google.com/open?id=0B76BuJcKjuxqYXRmSzd2R3U4S2c), or you can train it from scratch yourself using the pre-trained ImageNet 
weights linked earlier. The below is our model architecture: <br>
<p align="center">
<img alt="Architecture" src="https://github.com/dalmia/WannaPark/blob/master/images/model.png"/>
</p>

## Running the code

For training the model:

```
python train_detection.py`
```

For testing the model:

```
python test_images.py`
```

## Results

The green boxes signify the vacant spots.

<p align = "center">
 <b> Input</b>
 &nbsp; &nbsp; &nbsp;
 <b>Output</b>
 </p>
 <p align = "center">
 <img src = 'images/results/original_detection.jpg'/>
 &nbsp; &nbsp; &nbsp;
 <img src = 'images/results/parking_lot_detection.png'/>
 </p>
 
## Dependencies

- [Keras](http://keras.io/)
- [scipy](https://www.scipy.org/)
- [matplotlib](https://matplotlib.org/)
- [numpy](www.numpy.org/)
- [sklearn](http://scikit-learn.org/)
- [PIL](www.pythonware.com/products/pil/)
- [OpenCV](http://opencv.org/)

Use [pip](https://pypi.python.org/pypi/pip) to install them.
