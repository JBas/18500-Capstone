"""@package docstring
Documentation for the blob file.
Right now it only has blob detection and 
blob error functions.
"""

import skimage.feature

def blobDetect(image, params):
    """blobDetect.
    This function receives and image and a dictionary
    of params. An image mask is created based on HSV
    tolerances, and an array of blobs is created.
    Blobs are of the form [row, col, radius].
    """

    HSV = params["HSV"]
    HSV_tolerance = params["HSV_tolerance"]

    mask = (image <= (image + HSV*HSV_tolerance)) & (image >= (image - HSV_tolerace))

    blobs = skimage.feature.blob_log(image*mask, threshold = 0.5)
    blobs[:, 2] = blobs[:, 2] * sqrt(2)
    return blobs

def blobError(blobs, history):
    

    return error
