#!/bin/bash
# $1 - the size of the grid - n
# $2 - the maximum number of steps - T

# Generates the input according to the constraints - spawns a SAT input
python3 generator.py $1 $2 unsat input.txt

# Runs the SAT solver
python3 210070014_210050091_210051001_tile_loop.py input.txt
