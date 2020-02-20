import pickle
import numpy as np
from lib import getCameraLocals

def getOptions():
    size = 5
    dimensions = 100

    x = np.arange(0, dimensions+1, size)
    y = np.arange(0, dimensions+1, size)
    z = np.arange(0, dimensions+1, size)

    phis = np.deg2rad(np.arange(0, 360, 25)).tolist()
    psis = np.deg2rad(np.arange(0, 360, 25)).tolist()

    t1 = np.deg2rad(80)
    t2 = np.deg2rad(80)
    T = 60

    types = [(t1, t2, T)]

    pos = getCameraLocals(x, y).tolist()

    xx, yy = np.meshgrid(x, y)
    tpos = list(zip(xx.flatten(), yy.flatten()))

    options = {
        "size": size,
        "pos": pos,
        "phis": phis,
        "psis": psis,
        "heights": z.tolist(),
        "types": types,
        "tpos": tpos,
        "CVR": 1
    }

    options["N_C"] = len(options["pos"])
    options["N_hD"] = len(options["phis"])
    options["N_vD"] = len(options["psis"])
    options["N_E"] = len(options["heights"])
    options["N_A"] = len(options["types"])
    options["N_T"] = len(options["tpos"])

    return options
