import picamera
import picamera.array

I1_FILEPATH = "I1.png"
I2_FILEPATH = "I2.png"

MAX_ERROR_CHECK = 5

def activate(edge_result):
    edge_weighting = 1.0
    return bool(edge_result*edge_weight)
    
def run(rpi_cam, uart_cam):
    hasError = False

    I1 = getRPIArray(rpi_cam)
    I2 = getUARTArray(uart_cam)

    blobs1 = blobDetect(I1)
    blobs2 = blobDetect(I2)

    blob_result1 = blobError(blobs1, blob_history1)
    blob_result2 = blobError(blobs2, blob_history2)

    hasError = activate(blob_result1, blob_result2)

    return hasError

def getRPIArray(camera):
    with picamera.array.PiRGBArray(camera) as output:
        camera.capture(output, "hsv")

    return output.array

def getUARTArray(camera):
    pass


