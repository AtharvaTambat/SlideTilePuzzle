import csv,random,sys

if len(sys.argv) != 5:
    print("Usage: python3 generator.py <N> <T> <sat/unsat> <output_filename>")
    exit(1)

n = int(sys.argv[1])
T = int(sys.argv[2])
type = sys.argv[3].strip()
filename = sys.argv[4]

if type != "sat" and type != "unsat":
    print("Usage: python3 generator.py <N> <T> <sat/unsat> <putput filename>")
    print("3rd argument should be string \"sat\" or \"unsat\"")
    exit(1)

board = []
moves = []

file = open(filename, "w")

number = 1
for n_outer_index in range(0,n):
    row = []
    for n_index in range(0,n):
        row.append(number)
        number = number + 1
    board.append(row)

# print("Board:")
# for row in board:
#     print(row)

for t in range(T):
    dir_rand = random.randint(0,3)
    index_rand = random.randint(0,n-1)

    if dir_rand == 0: #"left":
        temp = board[index_rand][0]
        for j in range(n-1):
            board[index_rand][j] = board[index_rand][j+1]
        board[index_rand][n-1] = temp
        move = str(index_rand)+"r"
        moves.append(move)
    if dir_rand == 1: #"right":
        temp = board[index_rand][n-1]
        for j in reversed(range(n-1)):
            board[index_rand][j+1] = board[index_rand][j]
        board[index_rand][0] = temp
        move = str(index_rand)+"l"
        moves.append(move)
    if dir_rand == 2: #"up":
        temp = board[0][index_rand]
        for j in range(n-1):
            board[j][index_rand] = board[j+1][index_rand]
        board[n-1][index_rand] = temp
        move = str(index_rand)+"d"
        moves.append(move)
    if dir_rand == 3: #"down":
        temp = board[n-1][index_rand]
        for j in reversed(range(n-1)):
            board[j+1][index_rand] = board[j][index_rand]
        board[0][index_rand] = temp
        move = str(index_rand)+"u"
        moves.append(move)


if type == "sat":
    file.write(str(n)+" "+str(T)+"\n")
    for row in board:
        for no in row:
            file.write(str(no)+" ")
        file.write("\n")

    print("One of the solutions to the generated sat problem in " + filename + ":")
    print()
    print("sat")
    for move in reversed(moves):
        print(move)

if type == "unsat":
    # create unsat board by flipping any 2 consecutive numbers
    i_1 = random.randint(0,n-1)
    j_1 = random.randint(0,n-1)
    dir_rand = random.randint(0,3)

    if dir_rand == 0:
        i_2 = i_1
        j_2 = j_1+1
        if j_2 == n:
            j_2 = 0

    if dir_rand == 1:
        i_2 = i_1+1
        j_2 = j_1
        if i_2 == n:
            i_2 = 0

    if dir_rand == 2:
        i_2 = i_1
        j_2 = j_1-1
        if j_2 == 0:
            j_2 = n-1

    if dir_rand == 3:
        i_2 = i_1-1
        j_2 = j_1
        if i_2 == 0:
            i_2 = n-1

    temp = board[i_1][j_1]
    board[i_1][j_1] = board[i_2][j_2]
    board[i_2][j_2] = temp

    file.write(str(n)+" "+str(T)+"\n")
    for row in board:
        for no in row:
            file.write(str(no)+" ")
        file.write("\n")

file.close()