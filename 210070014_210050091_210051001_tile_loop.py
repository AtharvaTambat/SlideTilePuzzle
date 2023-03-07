### TEAM MEMBERS
## MEMBER 1: 210070014
## MEMBER 2: 210050091
## MEMBER 3: 210051001


from z3 import *
import sys

'''Creates the clauses for the Pseudo Boolean Constarints for p_1 + p2_ ... p_n = k'''
def sum_eq_one(vars):
    return PbEq(tuple([(i,1) for i in vars]), 1)

'''Creates clauses for constraining the valid moves at each step'''
def move_constraints(grid,moves, N, max_steps):
    constraints = []

    # Adds the constraints sum right_i_step + left_i_step + up_i_step + dpown_i_n = 1 => only one step moving one row/ column left/right/up/down should be done in a move
    for i in range(max_steps):
        constraints.append(sum_eq_one(moves[i]))

    # Enforcing move constraints between step 0 (initial state) and the first state (after one operation)

    # Adding constraints for if a move is chosen from amoung right, left .. - ensuring the validity of the next state
    for step in moves: # Skip the last step - No move possible from the last step
        for move in step:
            actual_move = []
            if str(move).split("_")[0] == 'right':
                for row in range(N):
                    for column in range(N):
                        if str(row) == str(move).split("_")[1]:
                            actual_move.append(grid[row][column][int(str(move).split("_")[2])-1] == grid[row][(column+1)%N][int(str(move).split("_")[2])])
                        else:
                            actual_move.append(grid[row][column][int(str(move).split("_")[2])-1] == grid[row][column][int(str(move).split("_")[2])])
            elif str(move).split("_")[0] == 'left':
                for row in range(N):
                    for column in range(N):
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


'''Adds the set of constraints that are to be satisfied at the end'''
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

# Input file name
file = sys.argv[1]

with open(file) as f:
	n,T = [int(x) for x in next(f).split()]
	grid = [ [ [ Int('p_'+str(row) + '_' + str(col) +  '_' + str(step)) for step in range(T+1)] for col in range(n) ] for row in range(n)]
	move = []
	for move_count in range(1,T+1):
		row = []
		for i in range(n):
			row.append(Bool('right_'+str(i) + '_' + str(move_count)))
			row.append(Bool('left_'+str(i) + '_' + str(move_count)))	
			row.append(Bool('up_'+str(i) + '_' + str(move_count)))	
			row.append(Bool('down_'+str(i) + '_' + str(move_count)))
		move.append(row)	

	constraints = []

	row_count = 0
	for line in f:
		entry = [int(x) for x in line.split()]
		for col_count in range(n):
			constraints.append(grid[row_count][col_count][0] == entry[col_count]) # Adding the initial constraints 
		row_count+=1

	# # Adding constraints for valid moves
	constraints.append(move_constraints(grid, move, n, T))

	# Adding goal constarints 
	constraints.append(goal_constraints(grid,n,T))	
 
# Set s to the required formula
s = Solver()
s.add(And(constraints))
x = s.check()

print(x)
if x == sat:
	m = s.model()
	# Output the moves
	step_counter = 0
	for individual_move_set in move:
		if m[Bool("finished_at_" + str(step_counter))]:
			break
		for individual_move in individual_move_set:
			if m[individual_move]:
				print(str(individual_move).split("_")[1] + str(individual_move)[0])
		step_counter+=1