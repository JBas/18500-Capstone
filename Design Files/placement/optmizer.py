import numpy as np
import cplex
from cplex.exceptions import CplexSolverError
import matplotlib.path as mplPath


# specifies that cameras can only be at
# locations forming the border of a square
def getCameraLocals(x_ticks, y_ticks):
    side_1 = zip(
        np.zeros(y_ticks.shape[0]),
        y_ticks)
    side_1 = list(side_1)

    side_2 = zip(
        x_ticks,
        np.zeros(x_ticks.shape[0]))
    side_2 = list(side_2)

    side_3 = zip(
        np.full(y_ticks.shape, x_ticks[-1]),
        y_ticks)
    side_3 = list(side_3)

    side_4 = zip(
        x_ticks,
        np.full(x_ticks.shape, y_ticks[-1]))
    side_4 = list(side_4)

    return np.vstack((side_1, side_2, side_3, side_4))


# # # # # # # # # # # # # # # # # # # # # # # # # #
# visibility poly: caculate 3D FOV                #
# # # # # # # # # # # # # # # # # # # # # # # # # #
def calcTrapezoidalFOV(camera_params):
    p0  = camera_params["p0"]
    e   = camera_params["e"]
    phi = camera_params["phi"]
    psi = camera_params["psi"]
    t1 = camera_params["t1"]
    t2 = camera_params["t2"]
    T = camera_params["T"]

    #print("Camera Parameters: ", camera_params)

    tau = e / np.cos(t2 + psi)
    #print("Tau: ", tau)

    if ((np.rad2deg(t2 + psi) < 90) or (tau > T)):
        #print("FOV with such conditions does not exist!")
        return None

    h = 1 # h is not defined in the paper, so this is a guess! big sad

    # get trapezoid vertices assuming (x0, y0) == (0, 0) and phi == 0
    trapezoid = np.array([
                         [h*np.tan(psi)],
                         [(h / np.cos(psi))*np.abs(t1/2)],
                         [h*np.tan(psi)],
                         [(h / np.cos(psi))*-np.abs(t1/2)],
                         [h*np.tan(psi + t2)],
                         [(h / np.cos(psi + t2))*np.abs(t1/2)],
                         [h*np.tan(psi + t2)],
                         [(h / np.cos(psi + t2))*-np.abs(t1/2)]
                         ])
    # caculate trapezoid vertex by rotating by phi
    M = np.array([
                 [np.cos(phi), -np.sin(phi), 0, 0, 0, 0, 0, 0],
                 [np.sin(phi), np.cos(phi), 0, 0, 0, 0, 0, 0],
                 [0, 0, np.cos(phi), -np.sin(phi), 0, 0, 0, 0],
                 [0, 0, np.sin(phi), np.cos(phi), 0, 0, 0, 0],
                 [0, 0, 0, 0, np.cos(phi), -np.sin(phi), 0, 0],
                 [0, 0, 0, 0, np.sin(phi), np.cos(phi), 0, 0],
                 [0, 0, 0, 0, 0, 0, np.cos(phi), -np.sin(phi)],
                 [0, 0, 0, 0, 0, 0, np.sin(phi), np.cos(phi)]
                ])

    trapezoid = M @ trapezoid

    # add actual installment information
    trapezoid = trapezoid + np.vstack((p0[0], p0[1], p0[0], p0[1], p0[0], p0[1], p0[0], p0[1]))
    return trapezoid.reshape((4, 2))


def isCellCovered(cell_i, trapezoid, cell_size):
    cell_pos = cell_i*cell_size + cell_size/2

    # from stackOverflow, <3:
    bb = mplPath.Path(trapezoid)
    return bb.contains_point(cell_pos)

def setupV(data, x_shape):
    cell_size = data["cell_size"] 
    camera_locations = data["camera_locations"] 
    horiz_orientations = data["horiz_orientations"]
    vert_orientations = data["vert_orientations"]
    camera_heights = data["camera_heights"]
    camera_types = data["camera_types"]
    target_locations = data["target_locations"]
    CVR = data["CVR"] 
    
    N_C = camera_locations.shape[0] 
    N_hD = horiz_orientations.shape[0]
    N_vD = vert_orientations.shape[0]
    N_E = camera_heights.shape[0]
    N_A = camera_types.shape[0]
    N_T = target_locations.shape[0]
    
    v_names = []
    v_vals = []
    for k in range(N_T):
        break_away = False
        target = target_locations[k]
        v_names.append([])
        v_vals.append([])
        for i in range(N_C):
            if (break_away): break
            for j in range(N_hD):
                if (break_away): break
                for d in range(N_vD):
                    if (break_away): break
                    for e in range(N_E):
                        if (break_away): break
                        for t in range(N_A):
                            camera_params = {
                                "p0": camera_locations[i],
                                "e": camera_heights[e],
                                "phi": horiz_orientations[j],
                                "psi": vert_orientations[d],
                                "t1": camera_types[t, 0],
                                "t2": camera_types[t, 1],
                                "T": camera_types[t, 2]
                            }
                            vis_poly = calcTrapezoidalFOV(camera_params)
                            varname = "v(" + str(i) + "_" + str(j) + "_" + str(d) + "_" + str(e) + "_" + str(t) + str(k) + ")"
                            v_names[k].append(varname)

                            if (vis_poly is None):
                                v_vals[k] = list(np.zeros((x_shape,)))
                                break_away = True
                                break

                            v_vals[k].append(isCellCovered(target, vis_poly, cell_size))

    return (v_names, v_vals)


def setupX(problem, data):
    camera_locations = data["camera_locations"] 
    horiz_orientations = data["horiz_orientations"]
    vert_orientations = data["vert_orientations"]
    camera_heights = data["camera_heights"]
    camera_types = data["camera_types"]
    target_locations = data["target_locations"]
    
    N_C = camera_locations.shape[0] 
    N_hD = horiz_orientations.shape[0]
    N_vD = vert_orientations.shape[0]
    N_E = camera_heights.shape[0]
    N_A = camera_types.shape[0]
    N_T = target_locations.shape[0]

    """
    x_ijdet is 1 if there exists a camera at position i
            with horizontal orientation j, vertical orientation d, 
            height e, and angle of view t
    """
    x = []
    for i in range(N_C):
        for j in range(N_hD):
            for d in range(N_vD):
                for e in range(N_E):
                    for t in range(N_A):
                        varname = "x(" + str(i) + "_" + str(j) + "_" + str(d) + "_" + str(e) + "_" + str(t) + ")"
                        x.append(varname)
    
    problem.variables.add(obj = [1]*len(x),
                          names = x,
                          lb = [0]*len(x),
                          ub = [1]*len(x),
                          types = ["B"]*len(x))
    return x


def setupY(problem, data):
    target_locations = data["target_locations"]
    N_T = target_locations.shape[0]
    
    y = []
    for k in range(N_T):
        varname = "y(" + str(k) + ")"
        y.append(varname)
    problem.variables.add(names = y,
                          lb = [0]*len(y),
                          ub = [1]*len(y),
                          types = ["B"]*len(y))
    return y

# # # # # # # # # # # # # # # # # # # # # # # # # #
# PHASE 1: find min camera count given conditions #
# # # # # # # # # # # # # # # # # # # # # # # # # #
def minimizeCamCount(data):
    target_locations = data["target_locations"]
    N_T = target_locations.shape[0]
    
    
    problem = cplex.Cplex()

    problem.objective.set_sense(problem.objective.sense.minimize)
    problem.objective.set_name("Camera Count")

    x = setupX(problem, data)
    y = setupY(problem, data)
    (v_names, v_vals) = setupV(data, len(x))

    lhs = [sum(map(lambda x_, v: x_*v, x, v_vals[k])) for k in range(data["target_locations"].shape[0])]
    rhs = y

    print(len(lhs))
    print(len(rhs))

    problem.linear_constraints.add(lin_expr=lhs,
                                   senses="G",
                                   rhs=rhs)

    problem.write("model.lp")
