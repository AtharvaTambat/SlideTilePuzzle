from z3 import *

# '''Returns clauses for ensuring internal contraints of the grid'''
# def consistency(grid, N, max_steps):
#     constraints = []

#     # P_i,j,n - is a integer variable which represents whether cell (i,j) is occupied by number k at teh n^{th} step
#     # P is represented by grid[][][]
#     for step in range(max_steps+1):
#         # Checks whether each entry occurs somewhere on the board exactly once
#         for entry in range(1,N*N+1):
#             constraints.append(sum_eq_one([(grid[i][j][step] ==  entry) for i in range(N) for j in range(N)]))
    
#         # Checks (for every step n, for every cell in the grid (row,column), sum P_row,column,k,n = 1 => only one entry occurs at each position (i,j) in every step)
#         for row in range(N):
#             for column in range(N):
#                 constraints.append(sum_eq_one((grid[row][column][step] == entry) for entry in range(1,N*N+1)))

#     # print(constraints)
#     return And(constraints)

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
    # print('moves array',moves)
    for step in moves: # Skip the last step - No move possible from the last step
        for move in step:
            actual_move = []
            if str(move).split("_")[0] == 'right':
                for column in range(N):
                    for row in range(N):
                        if str(row) == str(move).split("_")[1]:
                            actual_move.append(grid[row][column][int(str(move).split("_")[2])-1] == grid[row][(column+1)%N][int(str(move).split("_")[2])])
                        else:
                            actual_move.append(grid[row][column][int(str(move).split("_")[2])-1] == grid[row][column][int(str(move).split("_")[2])])
            elif str(move).split("_")[0] == 'left':
                for column in range(N):
                    for row in range(N):
                        if str(row) == str(move).split("_")[1]:
                            actual_move.append(grid[row][column][int(str(move).split("_")[2])-1] == grid[row][(column-1)%N][int(str(move).split("_")[2])])
                        else:
                            actual_move.append(grid[row][column][int(str(move).split("_")[2])-1] == grid[row][column][int(str(move).split("_")[2])])
            elif str(move).split("_")[0] == 'up':
                for row in range(N):
                    for column in range(N):
                        if str(column) == str(move).split("_")[1]:
                            actual_move.append(grid[row][column][int(str(move).split("_")[2])-1] == grid[(row-1)%N][column][int(str(move).split("_")[2])])
                        else:
                            actual_move.append(grid[row][column][int(str(move).split("_")[2])-1] == grid[row][column][int(str(move).split("_")[2])])
            elif str(move).split("_")[0] == 'down':
                for row in range(N):
                    for column in range(N):
                        if str(column) == str(move).split("_")[1]:
                            actual_move.append(grid[row][column][int(str(move).split("_")[2])-1] == grid[(row+1)%N][column][int(str(move).split("_")[2])])
                        else:
                            actual_move.append(grid[row][column][int(str(move).split("_")[2])-1] == grid[row][column][int(str(move).split("_")[2])])
            # Taking an AND of all the conditions to be taken care of in ONE MOVE
            constraints.append(Implies(move,And(actual_move)))


    # Optimization - Right at step i will not cause left at step i+1 - of the same row, column ...
    for step_num in range(len(moves)-1): # Skip the last step - No move possible from the last step
        for move_num in range(4*N):
            if str(moves[step_num][move_num]).split("_")[0] == 'right':
                constraints.append(Implies(moves[step_num][move_num],Not(Bool('left_' + str(moves[step_num][move_num]).split('_')[1]+ '_' + str(step_num + 2)))))
            if str(moves[step_num][move_num]).split("_")[0] == 'left':
                constraints.append(Implies(moves[step_num][move_num],Not(Bool('right_' + str(moves[step_num][move_num]).split('_')[1]+ '_' + str(step_num + 2)))))
            if str(moves[step_num][move_num]).split("_")[0] == 'up':
                constraints.append(Implies(moves[step_num][move_num],Not(Bool('down_' + str(moves[step_num][move_num]).split('_')[1]+ '_' + str(step_num + 2)))))
            if str(moves[step_num][move_num]).split("_")[0] == 'down':
                constraints.append(Implies(moves[step_num][move_num],Not(Bool('up_' + str(moves[step_num][move_num]).split('_')[1]+ '_' + str(step_num + 2)))))

    return (And(constraints))



def goal_constraints(grid, N, max_steps):
    constraints = []
    finished_stages = []

    for step_count in range(max_steps+1): # step_count also includes 0 => the starting configuration is correct
        finish_at_step_i = []
        element = 1
        # Checks whether, at a certain step, the correct configuration is met - 1 is at (0,0), 2 is at (0,1) ...
        for row in range(N):
            for column in range(N):
                finish_at_step_i.append(grid[row][column][step_count] == element)
                element+=1

        finished_stage = Bool('finished_at_' + str(step_count))
        finished_stages.append(finished_stage)

        constraints.append(finished_stage == And(finish_at_step_i))

    return(And(And(constraints),Or(finished_stages))) # Extra n Vars added to help check at the end, which is the lowest stage where the search was successful


# def goal_constraints(grid, N, max_steps):
#     constraints = []

#     for step_count in range(max_steps+1): # step_count also includes 0 => the starting configuration is correct
#         finish_at_step_i = []
#         element = 1
#         # Checks whether, at a certain step, the correct configuration is met - 1 is at (0,0), 2 is at (0,1) ...
#         for row in range(N):
#             for column in range(N):
#                 finish_at_step_i.append(grid[row][column][step_count] == element)
#                 element+=1

#         constraints.append(And(finish_at_step_i))

#     return(Or(constraints)) # Extra n Vars added to help check at the end, which is the lowest stage where the search was successful