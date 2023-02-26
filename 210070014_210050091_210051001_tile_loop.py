### TEAM MEMBERS
## MEMBER 1: 210070014
## MEMBER 2: 210050091
## MEMBER 3: 210051001


from z3 import *
import sys

# Input file name
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