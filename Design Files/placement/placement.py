import sys
import numpy as np
import matplotlib.pyplot as plt
from optimizer import getCameraLocals
from optimizer import calcTrapezoidalFOV
from optimizer import isCellCovered
from optimizer import minimizeCamCount


def main():
    cell_size = 5 # 100 mm
    grid_x = 10   # 1000 mm
    grid_y = 10   # 1000 mm
    grid_z = 10   # 1000 mm
    grid_x_tick = np.arange(0, grid_x + 1, cell_size)
    grid_y_tick = np.arange(0, grid_y + 1, cell_size)
    grid_z_tick = np.arange(0, grid_z + 1, cell_size)

    xx, yy = np.meshgrid(grid_x_tick, grid_y_tick)
    target_locations = np.array(list(zip(xx.flatten(), yy.flatten())))

    camera_locations = getCameraLocals(grid_x_tick, grid_y_tick)

    phi = np.deg2rad(np.arange(0, 90, 45)) #np.deg2rad(np.arange(0, 316, 45))         # horizontal orientations
    psi = np.deg2rad(np.arange(1, 30, 15)) #np.deg2rad(np.arange(1, 30, 2))           # vertical orientations
    t1 = np.deg2rad(80)                             # horizontal angles of camera view
    t2 = np.deg2rad(80)                             # vertical angles of camera view
    T = 60                                          # maximum recognition distance

    camera_types = np.array([(t1, t2, T)])

    fig, ax = plt.subplots()

    ax.set_xticks(grid_x_tick)
    ax.set_yticks(grid_y_tick)

    min_params = {
        "cell_size": cell_size,
        "camera_locations": camera_locations,
        "horiz_orientations": phi, 
        "vert_orientations": psi,
        "camera_heights": grid_z_tick,
        "camera_types": camera_types,
        "target_locations": target_locations,
        "CVR": 1
    }

    minimizeCamCount(min_params)

    #ax.fill(trapezoid[:, 0], trapezoid[:, 1], fill=False)
    ax.set(xlabel='x direction', ylabel='y direction',
           title='FOV')

    ax.grid()
    plt.show()


if __name__=="__main__":
    main()
