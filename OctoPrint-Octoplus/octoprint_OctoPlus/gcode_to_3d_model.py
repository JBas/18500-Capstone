import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

def run(file, theta):
    [x,y,z] = gcode_to_3d_model(file)

    graph_it(x,y,z,theta)
    

def graph_it(xcoords, ycoords, zcoords,theta):

    # for scaling so it doesn't look wonky 
    max_x = np.amax(xcoords)
    max_y = np.amax(ycoords)
    max_z = np.amax(zcoords)

    max_max = np.amax([max_x, max_y,max_z])

    # set up 3d plot space
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.set_xlim(-max_max/2, max_max/2)
    ax.set_ylim(-max_max/2, max_max/2)
    ax.set_zlim(0, max_max)

    ax.view_init(elev=0.,azim = theta)

    # plot figure
    ax.plot(xcoords, ycoords, zcoords, color='b')

    #save figure
    fig.savefig('test.png', bbox_inches='tight')

    plt.show()

def gcode_to_3d_model(gcode_file):
    # open and read the file
    g_file = open(gcode_file, 'r')
    g_code = g_file.readlines()

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

            # get coordinates
            tx = float(g[x_loc+1:y_loc-1])
            ty = float(g[y_loc+1:z_loc-1])
            tz = float(g[z_loc+1:f-1])

            # add coordinates to big list of coords
            x.append(tx)
            y.append(ty)
            z.append(tz)
            
    g_file.close()

    return (x,y,z)
        
    
