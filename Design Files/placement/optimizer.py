import sys
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
    cell_pos = np.array(cell_i)*cell_size + cell_size/2

    # from stackOverflow, <3:
    bb = mplPath.Path(trapezoid)
    return bb.contains_point(cell_pos)

def setupV(data):
    cell_size = data["size"] 
    camera_locations = data["pos"] 
    horiz_orientations = data["phis"]
    vert_orientations = data["psis"]
    camera_heights = data["heights"]
    camera_types = data["types"]
    target_locations = data["tpos"]
    CVR = data["CVR"] 
    
    N_C = data["N_C"]
    N_hD = data["N_hD"]
    N_vD = data["N_vD"]
    N_E = data["N_E"]
    N_A = data["N_A"]
    N_T = data["N_T"]
    
    v = np.zeros((N_T, N_C, N_hD, N_vD, N_E, N_A), dtype=int)
    names = np.zeros((N_T, N_C, N_hD, N_vD, N_E, N_A), dtype=object)
    for k in range(N_T):
        target = target_locations[k]
        for i in range(N_C):
            for j in range(N_hD):
                for d in range(N_vD):
                    for e in range(N_E):
                        for t in range(N_A):
                            camera_params = {
                                "p0": camera_locations[i],
                                "e": camera_heights[e],
                                "phi": horiz_orientations[j],
                                "psi": vert_orientations[d],
                                "t1": camera_types[t][0],
                                "t2": camera_types[t][1],
                                "T": camera_types[t][2]
                            }
                            vis_poly = calcTrapezoidalFOV(camera_params)
                            varname = "v(" + str(i) + "_" + str(j) + "_" + str(d) + "_" + str(e) + "_" + str(t) + str(k) + ")"
                            names[k, i, j, d, e, t] = varname

                            if (vis_poly is None):
                                v[k, i, j, d, e, t] = 0
                                continue

                            varval = int(isCellCovered(target, vis_poly, cell_size))
                            v[k, i, j, d, e, t] = varval

    return [v, names]


def setupX(data):
    camera_locations = data["pos"] 
    horiz_orientations = data["phis"]
    vert_orientations = data["psis"]
    camera_heights = data["heights"]
    camera_types = data["types"]
    target_locations = data["tpos"]
    
    N_C = data["N_C"]
    N_hD = data["N_hD"]
    N_vD = data["N_vD"]
    N_E = data["N_E"]
    N_A = data["N_A"]
    N_T = data["N_T"]

    """
    x_ijdet is 1 if there exists a camera at position i
            with horizontal orientation j, vertical orientation d, 
            height e, and angle of view t
    """
    xdata = np.zeros((N_C, N_hD, N_vD, N_E, N_A), dtype=object)
    for i in range(N_C):
        for j in range(N_hD):
            for d in range(N_vD):
                for e in range(N_E):
                    for t in range(N_A):
                        varname = "x(" + str(i) + "_" + str(j) + "_" + str(d) + "_" + str(e) + "_" + str(t) + ")"
                        x[i, j, d, e, t] = varname
    
    return xdata


def setupY(problem, data):
    target_locations = data["tpos"]
    N_T = data["N_T"]
    
    y = []
    for k in range(N_T):
        varname = "y(" + str(k) + ")"
        y.append(varname)
    problem.variables.add(obj = [0]*len(y),
                          names = y,
                          lb = [0]*len(y),
                          ub = [1]*len(y),
                          types = ["B"]*len(y))
    return y

# # # # # # # # # # # # # # # # # # # # # # # # # #
# PHASE 1: find min camera count given conditions #
# # # # # # # # # # # # # # # # # # # # # # # # # #
def minimizeCamCount(params, vdata):
    N_C = params["N_C"]
    N_hD = params["N_hD"]
    N_vD = params["N_vD"]
    N_E = params["N_E"]
    N_A = params["N_A"]
    N_T = params["N_T"]

    v = vdata[0].flatten().tolist()
    vnames = vdata[1].flatten().tolist()

    problem = cplex.Cplex()

    problem.objective.set_sense(problem.objective.sense.minimize)
    problem.objective.set_name("Camera Count")

    # add x to problem
    xdata = setupX(problem, params)
    x = xdata.flatten().tolist()
    problem.variables.add(obj = [1]*len(x),
                          names = x,
                          lb = [0]*len(x),
                          ub = [1]*len(x),
                          types = ["B"]*len(x))
    
    # add y to problem
    y = setupY(problem, params)
    

    # add v to problem
    problem.variables.add(obj = [0]*len(v),
                          names = vnames,
                          lb = [0]*len(v),
                          ub = [1]*len(v),
                          types = ["B"]*len(v))

    for k in range(N_T):
        for i in range(N_C):
            for j in range(N_hD):
                for d in range(N_vD):
                    for e in range(N_E):
                        for t in range(N_A):
                            val = vdata[0][k, i, j, d, e, t]
                            name = vdata[1][k, i, j, d, e, t]
                            problem.linear_constraints.add(lin_expr=[cplex.SparsePair([name], [1])],
                                                           senses=["E"],
                                                           rhs=[val])
    for k in range(N_T):
        for i in range(N_C):
            for j in range(N_hD):
                for d in range(N_vD):
                    for e in range(N_E):
                        for t in range(N_A):
                            problem.quadratic_constraints.add(quad_expr=[cplex.SparseTriple(names[k, i, j, d, e, t], x[t + e], [1])],
                                                           senses=["G"],
                                                           rhs=[y[k]])
    problem.write("model.lp")
"""
    for k in range(N_T):
        for i in range(N_C):
            for j in range(N_hD):
                for d in range(N_vD):
                    for e in range(N_E):
                        for t in range(N_A):
                            problem.quad_constraints.add(lin_expr=[cplex.SparsePair([varname], [1])],
                                senses="G",
                                rhs=[y[k]])
"""    
"""
    problem.linear_constraints.add(lin_expr=lhs,
                                   senses="G",
                                   rhs=rhs)
"""
