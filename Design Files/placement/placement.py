import sys
import pickle
import numpy as np

from lib import setupX, setupY, setupV
from defaults import getOptions
from optimizer import minimizeCamCount


def solve(data):
    print("Minimizing camera count...")
    minimizeCamCount(data)
    print("Done")
    sys.exit()
    return

def show(params):
    #fig, ax = plt.subplots()
    #ax.set_xticks()
    #ax.set_yticks()
    #ax.fill(trapezoid[:, 0], trapezoid[:, 1], fill=False)
    #ax.set(xlabel='x direction', ylabel='y direction',
    #       title='FOV')
    #ax.grid()
    #plt.show()
    pass

if __name__=="__main__":
    data = None
    vdata = None
    xdata = None
    ydata = None
    options = None

    # try reading from data.pkl file
    try:
        print("Reading data.pkl...", end= " ")
        with open("data/data.pkl", "rb") as f:
            data = pickle.load(f)
        print("Done")
    except FileNotFoundError:
        # create options
        print("\nNo data.pkl! Using defaults...", end= " ")
        options = getOptions()
        print("Done")

        # create vdata
        print("Creating vdata...", end= " ")
        vdata = setupV(options)
        print("Done")

        # create xdata
        print("Creating xdata...", end= " ")
        xdata = setupX(options)
        print("Done")

        # create ydata 
        print("Creating ydata...", end= " ")
        ydata = setupY(options["N_T"])
        print("Done")

        data = {
            "options": options,
            "vdata": vdata,
            "xdata": xdata,
            "ydata": ydata
        }

        print("Writing data.pkl...", end= " ")
        with open("data/data.pkl", "wb") as f:
            pickle.dump(data, f)
        print("Done")

    assert(data is not None)
    assert(data["vdata"] is not None)
    assert(data["xdata"] is not None)
    assert(data["ydata"] is not None)
    assert(data["options"] is not None)

    solve(data)
    # show(params)
