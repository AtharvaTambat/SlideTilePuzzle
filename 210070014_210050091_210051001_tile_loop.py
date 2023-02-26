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
	# print(grid)

	constraints = []

	row_count = 0
	for line in f:
		row = [int(x) for x in line.split()]
		for col_count in range(n):
			constraints.append(grid[row_count][col_count][row[col_count]-1][0]) # Adding the initial constraints 
		row_count+=1

	print(constraints)
	# Adding consistency constraints for T steps
	constraints.append(consistency(grid,n,T))

# Set s to the required formula
s = Solver()
s.add(And(constraints))


x = s.check()
print(x)
if x == sat:
	m = s.model()
	
	# Output the moves