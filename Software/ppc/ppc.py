
"""OctoPlus Print Point Cloud Generation

This program implements the print cloud generation for OctoPlus, a 3D printing
error detection system.
@author     Joshua Bas (jnbas@andrew.cmu.edu)
@date       3/2/202

"""

import numpy as np

IMAGE_WIDTH     = 860
IMAGE_HEIGHT    = 400

def ppc(I1, I2, C1, C2):
    """
    inputs  I1, I2: MxNx3 images
    inputs  C1, C2: 3x4 camera matrices
    outputs pt_cloud: Px2 point cloud
    """
    assert(I1.shape == (IMAGE_WIDTH, IMAGE_HEIGT, 3)), "I1 shape not %d x %d x 3" % (IMAGE_WIDTH, IMAGE_HEIGHT)
    assert(I2.shape == (IMAGE_WIDTH, IMAGE_HEIGT, 3)), "I2 shape not %d x %d x 3" % (IMAGE_WIDTH, IMAGE_HEIGHT)
    assert(C1.shape == (3, 4)), "C1 shape not 3 x 4"
    assert(C2.shape == (3, 4)), "C2 shape not 3 x 4"

    F = computeF()
    L_ = F @ x

    assert(pt_cloud.shape[1] == 2), "pt_cloud shape not P x 2"
    return pt_cloud
