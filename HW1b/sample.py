import copy

# Function to establish the area to survey
# Input is the map dimension (assumed square map)
# Output is a map as a list of lists (default valued 0)
def getMap(dimMap):
    # Set up the surveying area
    map = [0] * dimMap
    for idx in range(dimMap):
        map[idx] = [0]*dimMap
    return map

    # map = [[0] * dimMap]
    # for i in range(dimMap - 1):
    #     map.append([0] * dimMap)
    # return map

# to print all valid placements of police officers
def printMap(maps, dimMap):
    for map in maps:
        for row in map:
            print(row)
        # for i in range(dimMap):
        #     for j in range(dimMap):
        #         print map[i][j],
        #     print
        print ""

# A function to check if a police officer can
# be placed on area[row][col]. Note that this
# function is called when "col" police officers are
# already placed in columns from 0 to "col-1".
# So we need to check only left side for conflicting positions
def isPosValid(map, row, col,dimMap):
    # Check this row on left side
    for i in range(col):
        if map[row][i] == 1:
            return False

    # Check upper diagonal on left side
    # zip is to match variables of similar indexes in different lists
    for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
        if map[i][j] == 1:
            return False

    # Check lower diagonal on left side
    for i, j in zip(range(row, dimMap, 1), range(col, -1, -1)):
        if map[i][j] == 1:
            return False
    # jx, jy = row, col
    # while jx < dimMap and jy >= 0:
    #     if map[jx][jy] == 1:
    #         return False
    #     jx += 1
    #     jy -= 1

    # no need to check the right side because no officer has been placed there yet
    return True


# Function to add new solution to current set of solutions
def addMap(map):
    global maps
    saved_map = copy.deepcopy(map)
    maps.append(saved_map)


# Function to solve HW1 recursively by placing officer one by one from leftmost column
# It returns false if queens cannot be placed, otherwise return true and
# placement of queens in the form of 1s.
def hw1Solver(map, col, dimMap):
    # base case: If all officers are placed then return true
    if col >= numPol:
        return True

    # Consider this column and try placing this officer in all rows one by one
    for i in range(dimMap):
        if isPosValid(map, i, col,dimMap):
            # Place this officer in board[i][col]
            map[i][col] = 1
            if col == dimMap - 1:
                addMap(map)
                map[i][col] = 0 # reset the solution / clean the map
                return True

            # recursively place rest of the police officers
            hw1Solver(map, col + 1, dimMap)

            # If placing an officer in area[i][col] doesn't lead to a solution, then remove
            # officer from area[i][col]
            map[i][col] = 0






global numPol, dimMap
numPol = 5  # number of police officers
dimMap = 5  # dimension of the area

# Establish the survey area
map = getMap(dimMap)

# Recursively solve for solution
if hw1Solver(map, 0, dimMap):
    printMap(maps, dimMap)
else:
    print "Solution does not exist"

print("Total solutions = {}".format(len(maps)))

