OVERVIEW
_________________________________________________________________________________________


This exercise is inspired by the popular sliding puzzle:
https://en.wikipedia.org/wiki/Sliding_puzzle

Here is the description of the exercise:
1) There is an n x n grid.
2) The numbers 1 through n^2 are placed in the cells of the grid in some fashion.
3) In each move, a single row (or column) may be slid in either direction, moving all the elements in the row accordinly. In such a shift, the elements are moved cyclically. For example, if we shift the row 1 2 3 to the right, the resulting row is 3 1 2.
4) The goal of the game is to decide whether it is possible to perform shifts such that the grid ends up having the elements 1 through n^2, in order from top to bottom and left to right.

Example:
If we start with the 3 x 3 grid as follows,  
4 2 3
9 5 6
1 7 8
we can shift the first column down to get
1 2 3
4 5 6
9 7 8
then shift the third row left to get
1 2 3
4 5 6
7 8 9
as desired.

This game can also be played online at `https://lalaniket8.github.io/tileloop/`.

_________________________________________________________________________________________

		INPUT FORMAT
_________________________________________________________________________________________


The first line of the input has the dimension of the grid "n", and the maximum number of moves "T"
   -Example: "3 10" means "the 3x3 grid needs to be brought to the ordered position in at most 10 moves"

The remaining n lines describe the initial position of the grid, separated by spaces

For example, the earlier example is input as
3 2
4 2 3
9 5 6
1 7 8
_________________________________________________________________________________________

		SOLUTION
___________________________________________________________________________________________

In this assignment, you encode the above game as a SAT problem and use a SAT solver to find the moves to bring the grid to the desired form within the given limit. 

Write your solution in a file called `<rollnumber1>_<rollnumber2>_<rollnumber3>_tile_looptile_loop.py`.

_________________________________________________________________________________________

		OUTPUT
___________________________________________________________________________________________

Your code must only output to stdout.

- If the goal is not possible, your code should only print "unsat" and exit
	
- If the goal is possible, your code should print "sat" then a sequence of moves, one per line
   * A move is an integer followed by a letter
   * The integer denotes the row/column that the move shifts. This number is output 0-indexed.
   * The letter is one of "r,l,u,d" and denotes whether the row/column corresponding to the integer is shifted right, left, up, or down. 

Example output:

sat
0d
2l

The above sequence of moves solves the example grid.

_________________________________________________________________________________________

		HARNESS CODE
_________________________________________________________________________________________

We provide you with the following python scripts:
1. generator.py : To generate test cases 
2. verifier.py : To verify if your output is correct
3. template-code.py : You may use this as a backbone to start coding
	

Description:
1. generator.py

   To generate inputs for testing, use this file as follows:

   `$ python3 generator.py <N> <T> <sat/unsat> <filename.txt>`

   The above command will produce an "sat" or "unsat" input in file `<filename.txt>` with board size "N" and maximum number of moves "T".

   More description on the third argument:
   1. The 3rd argument determines whether the generated input is "sat" or "unsat".
   2. For "sat", the required input file is written to `<filename.txt>`, this board is solvable, and one on the possible solutions is also printed to stdout for your reference (your solver may get a different output, please keep in mind that there can be multiple solutions (set of moves) to any given input)
   3. For "unsat", the required input file is written to `<filename.txt>`, this board is unsolvable

   You can use the generator to test for "sat" and "unsat" cases.

   NOTE: A "sat" input board can have many set of moves (solutions) to solve it,
   However, an "unsat" board only has one correct output: "unsat".

2. verifier.py

   Please write you code in a single python script.
   We will call your solution using the following command.

   `$ python3 <rollnumber1>_<rollnumber2>_<rollnumber3>_tile_loop.py /path/to/input1.txt > /path/to/output1.txt`


   Finally, we will verify the input-output with our verifier included in this folder. The verifier can verify "sat" input boards only.

   `$ python3 verifier.py input1.txt output1.txt`

   The above script reads the input and output, runs the given moves and tells you if the output for given input is correct or not.
   You can change the variable value "debug = True" on Line 11 of verifier.py to get a more verbose description.

_________________________________________________________________________________________

		SUBMISSION INSTRUCTIONS
_________________________________________________________________________________________

This assignment is to be done in groups of 3 students.

Please write you code in a single python script: `<rollnumber1>_<rollnumber2>_<rollnumber3>_tile_loop.py`
We will call your solution using the following command.

`$ python3 <rollnumber1>_<rollnumber2>_<rollnumber3>_tile_loop.py /path/to/input1.txt > /path/to/output1.txt`

NOTE: Please make sure your code doesnot contain unwanted whitespaces, since we will evaluate your code using an autograder, any mismatch will lead to 0 marks.

NOTE: There is no hard limit on an acceptable running time for the code. It will be graded relative to your peers, so try to come up with a solution that runs in a reasonable time.

NOTE: We will rely on the roll number written in submission file name to grade your assignment.
Please make sure it contains the correct roll number.
Discrepancy in the same cannot be handled later.

NOTE: You are not required to use Z3. You may use any SAT solver available. If you use any other solver, it is your
responsibility to add a script in your submission to install the solver on Ubnuntu 22.03 linux.

Please refer to the course website
(https://www.cse.iitb.ac.in/~akg/courses/2023-logic/)