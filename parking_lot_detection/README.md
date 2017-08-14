# Parking lot Vacancy Detection using Deep Learning

Using images from CCTV camera, classify whether a parking spot is vacant or not.

## Dataset

We used the PKLot dataset, which can be found [here](9). This database contains 12,417 images (1280X720) captured 
from two different parking lots (parking1 and parking2) in sunny, cloudy and rainy days. On using the annotations to get the
image of each parking lot, we end up with ~ 695600 images of size 54x32.

## Model Architecture

We choose to fine-tune the pre-trained VGGNet (specifically its F-variant). The pre-trained weights can be obtained from [here](10).
We fix the convolutional layers, i.e., we don't fine-tune the convolutional layers, only the dense layers above it. You can download
checkpoint for testing the image directly from [here](11), or you can train it from scratch yourself using the pre-trained ImageNet 
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

- [Keras](1)
- [scipy](2)
- [matplotlib](3)
- [numpy](4)
- [sklearn](5)
- [PIL](6)
- [OpenCV](7)

Use [pip](8) to install them.

[1]: http://keras.io/
[2]: https://www.scipy.org/
[3]: https://matplotlib.org/
[4]: www.numpy.org/
[5]: http://scikit-learn.org/
[6]: www.pythonware.com/products/pil/
[7]: http://opencv.org/
[8]: https://pypi.python.org/pypi/pip
[9]: http://www.inf.ufpr.br/lesoliveira/download/pklot-readme.pdf
[10]: http://www.vlfeat.org/matconvnet/models/imagenet-vgg-f.mat
[11]: https://drive.google.com/open?id=0B76BuJcKjuxqYXRmSzd2R3U4S2c
