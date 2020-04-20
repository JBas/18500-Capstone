"""@package docstring
Documentation for the edge file.
Right now it only has edge detection and 
edge error functions.
"""

import skimage.feature
from skimage.color import rgb2hsv, rgb2grey
from scipy.spatial.distance import directed_hausdorff
import numpy as np
from hausdorff import ModHausdorffDist

def HSVMask(image, params: dict):
    """HSVMask.
    This function receives and image and a dictionary
    of params. Returns an image mask based on HSV
    tolerances.
    """
    HSV = params["HSV"]
    HSV_tolerance = params["HSV_tolerance"]

    hsv_image = rgb2hsv(image)

    hue = hsv_image[:, :, 0]
    sat = hsv_image[:, :, 1]
    val = hsv_image[:, :, 2]

    mask = (((hue <= (1.0 + HSV_tolerance)*HSV[0]) & (hue >= (1.0 - HSV_tolerance)*HSV[0])) |
            ((sat <= (1.0 + HSV_tolerance)*HSV[1]) & (sat >= (1.0 - HSV_tolerance)*HSV[1])) |
            ((val <= (1.0 + HSV_tolerance)*HSV[2]) & (val >= (1.0 - HSV_tolerance)*HSV[2])))
    return mask

def edgeDetect(image, params: dict):
    """edgeDetect.
    This function receives and image and a dictionary
    of params. Returns an edge image of the given image.
    """
    mask = HSVMask(image, params)
    masked = rgb2grey(image)*mask;

    edge = skimage.feature.canny(rgb2grey(image), sigma=params["edge_sigma"])
    return edge

def edgeError(edge, ref, params: dict) -> bool:
    """edgeError.
    This function receives an edge image, an array of edge images, and
    a dictionary of params. Determines if there is an error given the
    edge image and the reference edge image of the current layer, using
    Hausdorrf distance.
    """
    # Assuming that ref has been appropiately tranformed to camera
    # orientation

    trace = ref[0] #ref[0:params["layer"] + 1] # trace is an edge image

    #tau = params["tau"]

    #center_of_rotation = medoid(edge, edge)
    #rk = np.amax(((center_of_rotation - edge)**2).sum(axis=1))
    #dtheta = np.arctan(1/rk)

    #Q = np.zeros(int(2*np.pi/dtheta))
    #for i in range(0, int(2*np.pi/dtheta)):
    #    R = np.array([
    #                 [np.cos(i*dtheta), -np.sin(i*dtheta)],
    #                 [np.sin(i*dtheta), np.cos(i*dtheta)]])
    #    Q[i] = directed_hausdorrf(R @ edge + t, trace)

    # directed_hausdorrf uses Euclidean distance metric, hardcoded
    FHD = directed_hausdorff(np.argwhere(trace != 0), np.argwhere(edge != 0))[0] 
    RHD = directed_hausdorff(np.argwhere(edge != 0), np.argwhere(trace != 0))[0] 
    MHD = np.max(np.array([FHD, RHD]))

    # if there is translation, H can be large because there are pts in
    # A not near any points in B, but M_t can be small because there exists
    # a translation that makes each point of A nearly coincident with some
    # point in B (Huttenlocher)
    return MHD

if __name__=="__main__":
    from skimage.io import imread, imshow, show
    import matplotlib.pyplot as plt

    params = {"HSV": (60.0, 0.021, 0.549),
              "HSV_tolerance": 0.10,
              "edge_sigma":3,
              "tau":3,
              "H_thresh":100
             }
    image = imread("data/image_0.jpg")
    ref = edgeDetect(image, params)
    
    edges = []
    edges.append(ref)
    edges.append(edgeDetect(skimage.filters.gaussian(image, multichannel=True, sigma=3), params))
    edges.append(edgeDetect(imread("data/image_1.jpg"), params))
    edges.append(edgeDetect(imread("data/image_2.jpg"), params))

    f, axarr = plt.subplots(2,2)
    axarr[0,0].imshow(edges[0])
    axarr[0,1].imshow(edges[1])
    axarr[1,0].imshow(edges[2])
    axarr[1,1].imshow(edges[3])

    text = []
    for edge in edges:
        text.append(edgeError(edge, [ref], params))
    
    axarr[0,0].set_title("orig, dist: {:.2f}".format(text[0]))
    axarr[0,1].set_title("orig (blurred), dist: {:.2f}".format(text[1]))
    axarr[1,0].set_title("not-orig 1, dist: {:.2f}".format(text[2]))
    axarr[1,1].set_title("not-orig 2, dist: {:.2f}".format(text[3]))

    show()
