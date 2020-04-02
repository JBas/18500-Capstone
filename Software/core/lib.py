import picamera
import picamera.array

I1_FILEPATH = "I1.png"
I2_FILEPATH = "I2.png"

MAX_ERROR_CHECK = 5

def activate(edge_result) -> bool:
    edge_weighting = 1.0
    return bool(edge_result*edge_weight)
    
def run(rpi_cam, uart_cam, params: dict) -> bool:
    hasError = False

    I1 = getRPIArray(rpi_cam)
    e1 = edgeDetect(I1, params)

    err = blobError(e1, trace, params)

    hasError = activate(err)

    return hasError

def getRPIArray(camera):
    with picamera.array.PiRGBArray(camera) as output:
        camera.capture(output, "hsv")

    return output.array

def getUARTArray(camera):
    pass


