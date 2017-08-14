# Face Similarity Comparison

Compute the similarity between the images of two faces.

## Steps
Refer [this](1) for a detailed explanation. 'Entry' and 'Exit' below refer to entering into and exiting from 
a parking lot.

<p align = "center">
 <b> Input Entry</b>
 &nbsp; &nbsp; &nbsp;
 <b>Input Exit</b>
 </p>
 <p align = "center">
 <img alt = 'Entry Image' src = 'images/final_entry/image.jpg'/>
 &nbsp; &nbsp; &nbsp;
 <img alt = 'Exit Image 1' src = 'images/final_exit/image.jpg'/>
</p>

### 1. Finding all the faces (Histogram of Gradients)

<p align = "center">
<b>Entry Face</b>
&nbsp; &nbsp; &nbsp;
<b>Exit Face</b>
</p>
<p align = "center">
<img alt = 'Output Entry Image' src = 'images/results/face_entry.png'/>
&nbsp; &nbsp; &nbsp;
<img alt = 'Output Exit Image 1' src = 'images/results/face_exit.png'/>
</p>

### 2. Posing and Projecting Faces (Face Landmark Estimation)
<p align = "center">
<b> Entry Face Aligned</b>
&nbsp; &nbsp; &nbsp;
<b>Exit Face Aligned</b>
</p>
<p align = "center">
<img alt = 'Output Entry Aligned Image' src = 'images/results/face_aligned_entry.jpg' width="200" height="200"/>
&nbsp; &nbsp; &nbsp;
<img alt = 'Output Exit Aligned Image 1' src = 'images/results/face_aligned_exit.jpg' width="200" height="200"/>
</p>

### 3. Neural Network as feature extractor (Convolutional Neural Networks)

Compute the euclidean distance between the features computed by the VGGNet using the pre-trained ImageNet weights.
```python
Distance: 11.616581
```
<img alt = 'Architecture' src = 'http://www.vlfeat.org/matconvnet/models/imagenet-vgg-f.svg' width="800" height="800"/>

## Running the code

```
python compare_similarity.py
```

## Dependencies
- [PIL](3)
- [skimage](4)
- [numpy](5)
- [keras](6)
- [OpenCV](7)
- [dlib](8)

Use [pip](9) to install them (except for dlib).

[1]: https://medium.com/@ageitgey/machine-learning-is-fun-part-4-modern-face-recognition-with-deep-learning-c3cffc121d78
[2]: http://www.vlfeat.org/matconvnet/models/imagenet-vgg-f.svg
[3]: www.pythonware.com/products/pil/
[4]: http://scikit-image.org/docs/dev/api/skimage.html
[5]: www.numpy.org/
[6]: http://keras.io/
[7]: http://opencv.org/
[8]: http://dlib.net/
[9]: https://pypi.python.org/pypi/pip
