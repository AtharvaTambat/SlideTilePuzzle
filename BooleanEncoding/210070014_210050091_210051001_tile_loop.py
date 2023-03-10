### TEAM MEMBERS
## MEMBER 1: 210070014
## MEMBER 2: 210050091
## MEMBER 3: 210051001


from z3 import *
from constraints import *
import sys

# Input file name
file = sys.argv[1]

with open(file) as f:
	n,T = [int(x) for x in next(f).split()]
	grid = [ [ [ [ Bool('p_'+str(row) + '_' + str(col) + '_' + str(entry) + '_' + str(step)) for step in range(T+1)] for entry in range(1,n*n+1) ] for col in range(n) ] for row in range(n)]
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
		row = [int(x) for x in line.split()]
		for col_count in range(n):
			constraints.append(grid[row_count][col_count][row[col_count]-1][0]) # Adding the initial constraints 
		row_count+=1

	# Adding consistency constraints for T steps
	constraints.append(consistency(grid,n,T))

	# Adding constraints for valid moves
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