

import picamera

I1_FILEPATH = "I1.png"
I2_FILEPATH = "I2.png"

def getI1():
   """ 
    camera = PiCamera(sensor_mode= ___,
                      resolution=___,
                      framerate=___,
                      framerate_range=___,
                      clock_mode=___)
    """
    with PiCamera() as camera:
        with picamera.array.PiRGBArray(camera) as output:
            camera.capture(output, "rgb")
            print("I1 is a %d by %d image!", {output.array.shape[1], output.array.shape[0]})
    return output.array

def getI2():
    pass


