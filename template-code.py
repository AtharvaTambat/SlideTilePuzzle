### TEAM MEMBERS
## MEMBER 1: 210070014
## MEMBER 2: 
## MEMBER 3: <roll_number_3>


from z3 import *
import sys

file = sys.argv[1]

with open(file) as f:
	n,T = [int(x) for x in next(f).split()]
	matrix = []
	for line in f:
		matrix.append([int(x) for x in line.split()])

s = Solver()

# Set s to the required formula

x = s.check()
print(x)
if x == sat:
	m = s.model()
	
	# Output the moves