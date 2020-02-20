import sys
import numpy as np
import cplex
from cplex.exceptions import CplexSolverError

# # # # # # # # # # # # # # # # # # # # # # # # # #
# PHASE 1: find min camera count given conditions #
# # # # # # # # # # # # # # # # # # # # # # # # # #
def minimizeCamCount(data):
    xdata = data["xdata"]
    ydata = data["ydata"]
    vdata = data["vdata"]

    x = xdata.flatten().tolist()

    y = ydata[0]
    y_constr = ydata[1]

    v = vdata[0].flatten().tolist()
    vvals_eq = vdata[1].flatten().tolist()
    v_eq_constr = vdata[2].flatten().tolist()

    options = data["options"]

    N_C = options["N_C"]
    N_hD = options["N_hD"]
    N_vD = options["N_vD"]
    N_E = options["N_E"]
    N_A = options["N_A"]
    N_T = options["N_T"]
    CVR = options["CVR"]

    problem = cplex.Cplex()

    problem.objective.set_sense(problem.objective.sense.minimize)
    problem.objective.set_name("Camera Count")

    print("\tAdding x to problem...", end=" ")
    # add x to problem
    problem.variables.add(obj = [1]*len(x),
                          names = x,
                          lb = [0]*len(x),
                          ub = [1]*len(x),
                          types = ["B"]*len(x))
    print("Done")
    print("\tAdding y to problem...", end=" ")
    # add y to problem
    problem.variables.add(obj = [0]*len(y),
                          names = y,
                          lb = [0]*len(y),
                          ub = [1]*len(y),
                          types = ["B"]*len(y))
    
    print("Done")
    print("\tAdding v to problem...", end=" ")
    # add v to problem
    problem.variables.add(obj = [0]*len(v),
                          names = v,
                          lb = [0]*len(v),
                          ub = [1]*len(v),
                          types = ["B"]*len(v))

    print("Done")
    print("\tAdding linear constraints to problem...", end=" ")
    problem.linear_constraints.add(lin_expr=y_constr,
                                   senses=["E"]*len(y_constr),
                                   rhs=[1]*len(y_constr))
    problem.linear_constraints.add(lin_expr=[cplex.SparsePair(y, [1]*len(y))],
                                   senses=["G"],
                                   rhs=[N_T*CVR])
    problem.linear_constraints.add(lin_expr=v_eq_constr,
                                   senses=["E"]*len(v_eq_constr),
                                   rhs=vvals_eq)
    print("Done")
    print("\tAdding quadratic constraints to problem...", end=" ")
    for k in range(N_T):
        Q = cplex.SparseTriple(vdata[0][k, :, :, :, :, :].flatten().tolist(), x, [1]*len(x))
        L1 = cplex.SparsePair([y[k]], [-1])
        L2 = cplex.SparsePair([y[k]], [-N_C])
        problem.quadratic_constraints.add(lin_expr=L1,
                                          quad_expr=Q,
                                          sense="G",
                                          rhs=0)
        problem.quadratic_constraints.add(lin_expr=L2,
                                          quad_expr=Q,
                                          sense="L",
                                          rhs=0)
    problem.write("data/model.lp")
    print("Done")
    print("\tSolving problem...")
    problem.solve()
    status = problem.solution.get_status()
    print("\n\n\tSolution status: ", status)

    if (status != 103):
        solution = problem.solution.get_objective_value()
        print("\tSolution value: ", solution)

    return

# # # # # # # # # # # # # # # # # # # # # # # # # # #
# PHASE 2: find camera parameter given camera count #
# # # # # # # # # # # # # # # # # # # # # # # # # # #
