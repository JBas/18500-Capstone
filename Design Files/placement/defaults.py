import pickle
import numpy as np
from optimizer import getCameraLocals

size = 10
dimensions = 100

x = np.arange(0, dimensions+1, size)
y = np.arange(0, dimensions+1, size)
z = np.arange(0, dimensions+1, size)

phis = np.deg2rad(np.arange(0, 360, 45)).tolist()
psis = np.deg2rad(np.arange(0, 360, 45)).tolist()

t1 = np.deg2rad(80)
t2 = np.deg2rad(80)
T = 60

types = [(t1, t2, T)]

pos = getCameraLocals(x, y).tolist()

xx, yy = np.meshgrid(x, y)
tpos = list(zip(xx.flatten(), yy.flatten()))

params = {
    "size": size,
    "pos": pos,
    "phis": phis,
    "psis": psis,
    "heights": z.tolist(),
    "types": types,
    "tpos": tpos,
    "CVR": 1
}

params["N_C"] = len(params["pos"])
params["N_hD"] = len(params["phis"])
params["N_vD"] = len(params["psis"])
params["N_E"] = len(params["heights"])
params["N_A"] = len(params["types"])
params["N_T"] = len(params["tpos"])

import pprint

pp = pprint.PrettyPrinter(indent=2)
pp.pprint(params)

with open("parameters.data", "wb") as f:
    pickle.dump(params, f)
