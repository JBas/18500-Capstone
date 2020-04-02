"""@package docstring
Documentation for the edge file.
Right now it only has edge detection and 
edge error functions.
"""

import skimage.feature
from skimage.color import rgb2hsv, rgb2grey
from scipy.spatial.distance import directed_hausdorff
import numpy as np

def maskImage(image, params: dict):
    HSV = params["HSV"]
    HSV_tolerance = params["HSV_tolerance"]

    hsv_image = rgb2hsv(image)

    hue = hsv_image[:, :, 0]
    sat = hsv_image[:, :, 1]
    val = hsv_image[:, :, 2]

    mask = (((hue <= (1.0 + HSV_tolerance)*HSV[0]) & (hue >= (1.0 - HSV_tolerance)*HSV[0])) |
            ((sat <= (1.0 + HSV_tolerance)*HSV[1]) & (sat >= (1.0 - HSV_tolerance)*HSV[1])) |
            ((val <= (1.0 + HSV_tolerance)*HSV[2]) & (val >= (1.0 - HSV_tolerance)*HSV[2])))
    grey = rgb2grey(image)
    masked = grey*mask
    return masked

def edgeDetect(image, params: dict):
    """edgeDetect.
    This function receives and image and a dictionary
    of params. An image mask is created based on HSV
    tolerances, and an edge image is created.
    """
    masked = maskImage(image, params)

    edge = skimage.feature.canny(rgb2grey(image), sigma=3)
    return edge

def edgeError(edge, trace, params: dict) -> bool:
    H = np.max(directed_hausdorrf(trace, edge)[0], directed_hausdorff(edge, trace)[0])
    return error

if __name__=="__main__":
    from skimage.io import imread, imshow, show
    import matplotlib.pyplot as plt

    image = imread("data/image_0.jpg")

    params = {"HSV": (60.0, 0.021, 0.549),
              "HSV_tolerance": 0.10
             }
    edge = edgeDetect(image, params)

    imshow(edge)

    show()
