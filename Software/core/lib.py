
import threading
import picamera

I1_FILEPATH = "I1.png"
I2_FILEPATH = "I2.png"

MAX_ERROR_CHECK = 5

class CheckThread(threading.Thread):
    def __init__(self, rpc, layer, group=None, target=None, name="check",
                 args=(), kwargs=None, verbose=None):
        self.cycles = 0
        self.rpc = rpc
        self.layer = layer
        self.cycleLock = threading.Lock()
        threading.Thread.__init__(self, group=group, tagert=target,
                                  name=name, args=args, kwargs=kwargs,
                                  verbose=verbose)
        pass

    def incrCycles(self):
        self.cycleLock.acquire(blocking=1)
        self.cycles += 1
        self.cycleLock.release()
        pass
    
    def activate(self, ppc_result, edge_result):
        ppc_weighting = 0.0
        edge_weighting = 1.0
        return bool(ppc_result*ppc_weighting + edge_result*edge_weight)

    def run(self):
        hasError = False
        error = None

        I1 = getI1()
        #I2 = getI2()

        #ppc = PPC(I1, I2)
        #ppc.generate()
        #ppc_result = ppc.analyze(self.rpc, self.layer)

        #edge_result = _____()

        hasError = activate(ppc_result, edge_result)

        self.cycleLock.acquire(blocking=1)
        if (self.cycles > MAX_ERROR_CHECK and hasError):
            error = "System did not meet requirements!"
        self.cycleLock.release()
        return

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


