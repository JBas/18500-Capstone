
"""OctoPlus Print Point Cloud Generation

@author     Joshua Bas (jnbas@andrew.cmu.edu)
@date       3/2/202

This program implements the print cloud generation for OctoPlus, a 3D printing
error detection system. The OpenCV Python and C++ documentations were helpful.
"""
import cv2 as cv
import numpy as np
import scipy
import pdb
from matplotlib import pyplot as plt

FLANN_INDEX_LSH = 6

class PPC():
    def __init__(self, I1, I2):
        assert(I1.shape == I2.shape), "Image shape mismatched!"
        self.I1 = I1
        self.I2 = I2
        self.cloud = None
        pass

    def generate(self):
        """
        inputs  I1, I2: MxNx3 images
        outputs F: fundamental matrix, just in case
        """

        pts1, pts2, matches = getMatchedPoints(I1, I2)

        F, mask = cv.findFundamentalMat(pts1, pts2,
                                        cv.FM_RANSAC,
                                        ransacReprojThreshold=2,
                                        confidence=.99)
        pts1 = pts1[mask.ravel() == 1]
        pts2 = pts2[mask.ravel() == 1]

        L = cv.computeCorrespondEpilines(pts1, 1, F)
        L_ = cv.computeCorrespondEpilines(pts2, 2, F)

        #self.cloud = _____
        return F

    def analyze(self, rpc, layer=0):
        assert(rpc is not None)
        assert(layer >= 0)

        ref = rpc[:layer]

        # ensure that same number of layers are being compared
        assert(ppc.shape[0] == rpc.shape[0])

        # translate ppc to origin

        # Euclidean similarity



        return


# # # # # # # # # # #
#  Helper Functions #
# # # # # # # # # # #

def getMatchedPoints(I1, I2):
    orb = cv.ORB_create()

    kp1, descr1 = orb.detectAndCompute(I1, None)
    kp2, descr2 = orb.detectAndCompute(I2, None)
    
    index_params = dict(algorithm = FLANN_INDEX_LSH,
                        table_number = 6,
                        key_size = 12,
                        multi_probe_level = 2)
    search_params = dict(checks=50)

    flann = cv.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(descr1, descr2, k=2)
    
    pts1 = []
    pts2 = []

    for m, n in matches:
        if m.distance < 0.75*n.distance:
            pts1.append(kp1[m.queryIdx].pt)
            pts2.append(kp2[m.trainIdx].pt)

    pts1 = np.int32(pts1)
    pts2 = np.int32(pts2)

    return pts1, pts2, matches

if __name__=="__main__":
    #Using 2014 dataset from http://vision.middlebury.edu/stereo/data/
    I1 = cv.imread("MiddEval3/trainingQ/Teddy/im0.png", cv.IMREAD_GRAYSCALE)
    I2 = cv.imread("MiddEval3/trainingQ/Teddy/im1.png", cv.IMREAD_GRAYSCALE)

    cloud = PPC(I1, I2)
    cloud.generate()
