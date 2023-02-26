from z3 import *

'''Returns clauses for ensuring internal contraints of the grid'''
def consistency(grid, N, max_steps):
    constraints = []

    # P_i,j,k,n - is a propositional variable which represents whether cell (i,j) is occupied by number k at teh n^{th} step
    # P is represented by grid[][][][]

    for step in range(max_steps+1):
        # Checks (for every step n, for every entry k, sum P_i,j,k,n = 1 => each entry occurs somewhere on the board exactly once)
        for entry in range(N*N):
            constraints.append(sum_eq_one([grid[i][j][entry][step] for i in range(N) for j in range(N)]))

        # Checks (for every step n, for every cell in the grid (row,column), sum P_row,column,k,n = 1 => only one entry occurs at each position (i,j) in every step)
        for row in range(N):
            for column in range(N):
                constraints.append(sum_eq_one(grid[row][column][entry][step] for entry in range(N*N)))
    
    # print(constraints)
    return And(constraints)

'''Creates the clauses for the Pseudo Boolean Constarints for p_1 + p2_ ... p_n = k'''
def sum_eq_one(vars):
    return PbEq(tuple([(i,1) for i in vars]), 1)

'''Creates clauses for constraining the valid moves at each step'''
def move_constraints(grid,moves, N, max_steps):
    constraints = []

    # Adds the constraints sum right_i_step + left_i_step + up_i_step + dpown_i_n = 1 => only one step moving one row/ column left/right/up/down should be done in a move
    for i in range(max_steps):
        constraints.append(sum_eq_one(moves[i]))
    # print(constraints)

    # Enforcing move constraints between step 0 (initial state) and the first state (after one operation)

    # Adding constraints for if a move is chosen from amoung right, left .. - ensuring the validity of the next state
    for step in moves: # Skip the last step - No move possible from the last step
        for move in step:
            actual_move = []
            if str(move).split("_")[0] == 'right':
                for column in range(N):
                    for element in range(N*N):
                        for row in range(N):
                            if str(row) == str(move).split("_")[1]:
                                actual_move.append(Implies(grid[row][column][element][int(str(move).split("_")[2])-1], grid[row][(column+1)%N][element][int(str(move).split("_")[2])]))
                            else:
                                actual_move.append(grid[row][column][element][int(str(move).split("_")[2])-1] == grid[row][column][element][int(str(move).split("_")[2])])
            elif str(move).split("_")[0] == 'left':
                for column in range(N):
                    for element in range(N*N):
                        for row in range(N):
                            if str(row) == str(move).split("_")[1]:
                                actual_move.append(Implies(grid[row][column][element][int(str(move).split("_")[2])-1], grid[row][(column-1)%N][element][int(str(move).split("_")[2])]))
                            else:
                                actual_move.append(grid[row][column][element][int(str(move).split("_")[2])-1] == grid[row][column][element][int(str(move).split("_")[2])])
            elif str(move).split("_")[0] == 'up':
                for row in range(N):
                    for element in range(N*N):
                        for column in range(N):
                            if str(column) == str(move).split("_")[1]:
                                actual_move.append(Implies(grid[row][column][element][int(str(move).split("_")[2])-1], grid[(row+1)%N][column][element][int(str(move).split("_")[2])]))
                            else:
                                actual_move.append(grid[row][column][element][int(str(move).split("_")[2])-1] == grid[row][column][element][int(str(move).split("_")[2])])
            elif str(move).split("_")[0] == 'down':
                for row in range(N):
                    for element in range(N*N):
                        for column in range(N):
                            if str(column) == str(move).split("_")[1]:
                                actual_move.append(Implies(grid[row][column][element][int(str(move).split("_")[2])-1], grid[(row-1)%N][column][element][int(str(move).split("_")[2])]))
                            else:
                                actual_move.append(grid[row][column][element][int(str(move).split("_")[2])-1] == grid[row][column][element][int(str(move).split("_")[2])])
            # Taking an AND of all the conditions to be taken care of in ONE MOVE
            constraints.append(Implies(move,And(actual_move)))
    return (And(constraints))

def goal_constraints(grid, N, max_steps):
    constraints = []
    finished_stages = []

    for step_count in range(max_steps+1): # step_count also includes 0 => the starting configuration is correct
        finish_at_step_i = []
        element = 0
        # Checks whether, at a certain step, the correct configuration is met - 1 is at (0,0), 2 is at (0,1) ...
        for row in range(N):
            for column in range(N):
                finish_at_step_i.append(grid[row][column][element][step_count])
                element+=1

        finished_stage = Bool('finished_at_' + str(step_count))
        finished_stages.append(finished_stage)

        constraints.append(finished_stage == And(finish_at_step_i))

    return(And(And(constraints),Or(finished_stages))) # Extra n Vars added to help check at the end, which is the lowest stage where the search was successful
