"""OctoPlus GCODE to 3D Model

@author     Hannah Preston
Implemented the original gcode_to_3d_model and graph_it functions that
operate on x, y, z arrays

@author     Joshua Bas
Changed to operate on one array of (x,y,z) coords

This program implements the 3D viewer for the OctoPlus plugin 
"""
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

def graph_it(xcoords, ycoords, zcoords):
    # open and read the file
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.plot(xcoords, ycoords, zcoords, color='b')

    plt.show()

def graph_it(ref):
    # open and read the file
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.plot(ref[:, 0], ref[:, 1], ref[:, 2], color='b')

    plt.show()

def gcode_to_3d_model(gcode_file):
    # open and read the file
    g_file = open(gcode_file, 'r')
    g_code = g_file.readlines()
    g_file.close()

    x = []
    y = []
    z = []
        
    for g in g_code:
        if ("G1" in g) and ("X" in g) and ("Y" in g) and ("Z" in g) and ("F" in g):
            # locate the place in the string where the coordinates will be given
            # x-coordinate
            x_loc = g.find("X")
            # y-coordinate
            y_loc = g.find("Y")
            # z-coordinate
            z_loc = g.find("Z")
            # end indicator
            f = g.find("F")
            # print("line: %s\n z at %d and f at %d", (g,z_loc,f))

            # get coordinates
            
            tx = float(g[x_loc+1:y_loc-1])
            ty = float(g[y_loc+1:z_loc-1])
            tz = float(g[z_loc+1:f-1])

            # add coordinates to big list of coords
            x.append(tx)
            y.append(ty)
            z.append(tz)

    ref = np.asarray(list(zip(x, y, z)))
    ref = ref[ref[:, 2].argsort()]
    ref = ref[:-1] # remove the last point bc it is just to move extruder to home position

    return ref

if __name__=="__main__":
    filename ="data/gcode" 
    ref = gcode_to_3d_model(filename)
    graph_it(ref)
