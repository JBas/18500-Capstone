import picamera
import picamera.array

I1_FILEPATH = "I1.png"
I2_FILEPATH = "I2.png"

MAX_ERROR_CHECK = 5

def activate(results, weights, thresh) -> bool:
    if np.dot(results, weights) < thresh:
        return 0
    return 1
    


def getRPIArray(camera):
    with picamera.array.PiRGBArray(camera) as output:
        camera.capture(output, "hsv")

    return output.array

def getUARTArray(camera):
    pass


