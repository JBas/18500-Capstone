
"""OctoPlus Print Point Cloud Generation

This program implements the print cloud generation for OctoPlus, a 3D printing
error detection system.
@author     Joshua Bas (jnbas@andrew.cmu.edu)
@date       3/2/202

"""
import cv2 as cv
import numpy as np
import pdb
from matplotlib import pyplot as plt

#IMAGE_WIDTH     = 860
#IMAGE_HEIGHT    = 400
#M = min(IMAGE_WIDTH, IMAGE_HEIGHT)

def ppc(I1, I2):
    """
    inputs  I1, I2: MxNx3 images
    inputs  C1, C2: 3x4 camera matrices
    outputs pt_cloud: Px2 point cloud
    """
    #assert(I1.shape == (IMAGE_WIDTH, IMAGE_HEIGHT, 3)), "I1 shape not %d x %d x 3" % (IMAGE_WIDTH, IMAGE_HEIGHT)
    #assert(I2.shape == (IMAGE_WIDTH, IMAGE_HEIGHT, 3)), "I2 shape not %d x %d x 3" % (IMAGE_WIDTH, IMAGE_HEIGHT)

    orb = cv.ORB_create()
    kp1, descr1 = orb.detectAndCompute(I1, None)
    
    kp2, descr2 = orb.detectAndCompute(I2, None)
    
    FLANN_INDEX_LSH = 6
    index_params = dict(algorithm = FLANN_INDEX_LSH,
                        table_number = 6,
                        key_size = 12,
                        multi_probe_level = 2)
    search_params = dict(checks=1000)

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

    """
    I3 = cv.drawMatchesKnn(I1, kp1, I2, kp2, matches[:10], None, flags=2)
    plt.imshow(I3)
    plt.show()
    """
    F, mask = cv.findFundamentalMat(pts1,pts2,cv.FM_LMEDS)
    pdb.set_trace()
    return

if __name__=="__main__":
    I1 = cv.imread("MiddEval3/trainingQ/Teddy/im0.png", 0)
    I2 = cv.imread("MiddEval3/trainingQ/Teddy/im1.png", 0)
    ppc(I1, I2)
