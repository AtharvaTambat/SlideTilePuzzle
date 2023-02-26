import csv,sys

inputFileName = sys.argv[1]
outputFileName = sys.argv[2]

n = 0
T = 0
board = []
moves = []

debug = False # set this variable to True to output the board contents after each move

with open(inputFileName) as input_file:
    firstLineProcessedFlag = False
    for line in input_file:
        tokens = line.strip().split()
        if debug:
            print("processing first line:"+str(tokens))
        if not firstLineProcessedFlag:
            if len(tokens) != 2:
                print("Invalid input file format. Format for first line :<n> <T>")
                exit(0)
            n = int(tokens[0])
            T = int(tokens[1])
            firstLineProcessedFlag = True
        else:
            if len(tokens) != n:
                print("Invalid input file format. Expecting n numbers separated by a single space in each line.")
                exit(0)
            row = []
            for token in tokens:
                row.append(token)
            board.append(row)

with open(outputFileName) as output_file:
    firstLineProcessedFlag = False
    for line in output_file:
        tokens = line.strip().split()
        if debug:
            print("processing first line:"+str(tokens))
        if not firstLineProcessedFlag:
            if len(tokens) != 1 or (tokens[0] != "sat" and tokens[0] != "unsat"):
                print("Invalid input file format. Format for first line :<sat/unsat>")
                exit(0)
            status = tokens[0]
            if status == "unsat":
                print("This verifier is written to verify sat output")
                exit(0)
            firstLineProcessedFlag = True
        else:
            if len(tokens) != 1 or (tokens[0][len(tokens[0])-1] != 'u' and tokens[0][len(tokens[0])-1] != 'd' and tokens[0][len(tokens[0])-1] != 'l' and tokens[0][len(tokens[0])-1] != 'r') :
                print("Invalid input file format. Output format:<k><u/d/l/r>")
                print("(No whitespaces in each line)")
                exit(0)
            if int(tokens[0][0]) >= n:
                print("Given row/col index is greater than or equal to n="+str(n))
                exit(0)
            move = {}
            dir = tokens[0][len(tokens[0])-1]
            if dir == "u":
                move["dir"] = "up"
            elif dir == "d":
                move["dir"] = "down"
            elif dir == "l":
                move["dir"] = "left"
            elif dir == "r":
                move["dir"] = "right"
            else:
                print("error")
                exit(0)

            move["k"] = int(tokens[0][0:len(tokens[0])-1])
            moves.append(move)

print("n:"+str(n))
print("T:"+str(T))
print("Board:")
for row in board:
    print(row)
print("Moves:")
for move in moves:
    row_or_col = "col" if (move["dir"] == "up" or move["dir"] == "down") else "row"
    print("Move " + row_or_col + " at index " + str(move["k"]) + " in direction : "+move["dir"])

if len(moves) > T:
    print("Number of moves exceeds the time step T")
    exit(0)

print("\n")
print("----------------------------------")
print("Evaluating moves on given board...")

for move in moves:
    if debug:
        row_or_col = "col" if (move["dir"] == "up" or move["dir"] == "down") else "row"
        print("Moving " + row_or_col + " at index " + str(move["k"]) + " "+move["dir"])

    if move["dir"]=="left":
        index = move["k"]
        temp = board[index][0]
        for j in range(n-1):
            board[index][j] = board[index][j+1]
        board[index][n-1] = temp
    if move["dir"]=="right":
        index = move["k"]
        temp = board[index][n-1]
        for j in reversed(range(n-1)):
            board[index][j+1] = board[index][j]
        board[index][0] = temp
    if move["dir"] == "up":
        index = move["k"]
        temp = board[0][index]
        for j in range(n-1):
            board[j][index] = board[j+1][index]
        board[n-1][index] = temp
    if move["dir"] == "down":
        index = move["k"]
        temp = board[n-1][index]
        for j in reversed(range(n-1)):
            board[j+1][index] = board[j][index]
        board[0][index] = temp
    
    if debug:
        print("Board:")
        for row in board:
            print(row)

correctnessFlag = True
for row_index in range(n):
    start = 1+(row_index*n)
    end = start+n
    board_row = board[row_index]
    correct_row = range(start,end)
    for i in range(0,n):
        if int(board_row[i]) != int(correct_row[i]):
            correctnessFlag = False
            break;
    if correctnessFlag == False:
        break;

if correctnessFlag:
    print("Given solution is CORRECT")
else:
    print("Given solution is INCORRECT")