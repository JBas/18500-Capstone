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
    error = None

    I1 = getRPIArray(rpi_cam)
    I2 = getUARTArray(uart_cam)

    edge_result = _____()

    hasError = activate(edge_result)

    return hasError

def getRPIArray(camera):
    with picamera.array.PiRGBArray(camera) as output:
        camera.capture(output, "rgb")

    return output.array

def getUARTArray(camera):
    pass


