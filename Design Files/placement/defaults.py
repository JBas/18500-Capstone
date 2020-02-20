import pickle
import numpy as np
from lib import getCameraLocals

def getOptions():
    # 3D printer bed dimensions
    size = 40
    width = 215
    length = 197
    height = 200

    x = np.arange(0, width+1, size)
    y = np.arange(0, length+1, size)
    z = np.arange(0, height+1, size)

    phis = np.deg2rad(np.arange(0, 360, 25)).tolist()
    psis = np.deg2rad(np.arange(0, 360, 25)).tolist()

    # AOV = 2*arctan(d / (2*f))
    # Arducam NOIR 8MP,
    # TTL Serial JPEG,

    types = [(np.deg2rad(16.81), np.deg2rad(12.64), 200),
             (np.deg2rad(52.88), np.deg2rad(40.97), 10000)]

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
