from z3 import *

'''Returns clauses for ensuring internal contraints of the grid'''
def consistency(grid, N, max_steps):
    constraints = []

    # P_i,j,k,n - is a propositional variable which represents whether cell (i,j) is occupied by number k at teh n^{th} step
    # P is represented by grid[][][][]

    # Checks (for every step n, for every entry k, sum P_i,j,k,n = 1 => each entry occurs somewhere on the board exactly once)
    for step in range(max_steps):
        for entry in range(N*N):
            constraints.append(sum_eq_one([grid[i][j][entry][step] for i in range(N) for j in range(N)]))

    print(constraints)

    # Checks (for every step n, for every cell in the grid (row,column), sum P_row,column,k,n = 1 => only one entry occurs at each position (i,j) in every step)
    # for step in range(max_steps):
    #     for row in range(N):
    #         for column in range(N):
    #             constraints.append(sum_eq_one(grid[row][column][entry][step] for entry in range(N)))

    return And(constraints)

'''Creates the clauses for the Psedo Boolean Constarints for p_1 + p2_ ... p_n = k'''
def sum_eq_one(vars):
    return PbEq(tuple([(i,1) for i in vars]), 1)
