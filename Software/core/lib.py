

import picamera

I1_FILEPATH = "I1.png"
I2_FILEPATH = "I2.png"

def check():
   """ 
    camera = PiCamera(sensor_mode= ___,
                      resolution=___,
                      framerate=___,
                      framerate_range=___,
                      clock_mode=___)
    """
    camera = PiCamera()
    try:
        # get I1
        try
        camera.capture(ouput=I1_FILEPATH,
                       format="png",
                       use_video_port=True,
                       resize=None,
                       splitter_port=0,
                       bayer=False,
                       options=None)
        # get I2

    except PiCameraError:
        print("The camera is messed up!")
    finally:
        camera.close()

    pass


if __name__=="__main__":
    check()
