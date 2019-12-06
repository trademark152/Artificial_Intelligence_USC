import copy
import time

# Function to establish the area to survey
# Input is the map dimension (assumed square map)
# Output is a map as a list of lists (default valued 0)
def getMap(dimMap):
    map = [0] * dimMap
    for idx in range(dimMap):
        map[idx] = [0] * dimMap
    return map

# Function to print all valid placements of police officers
def printMaps(maps):
    idx = 1
    for map in maps:
        print("Solution " + str(idx))
        for row in map:
            print(row)
        print
        idx += 1

def isPosValid(map, row, col, dimMap):
    """Check if it's valid to place an officer at map[x][y]"""

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

    # no need to check the right side because no officer has been placed there yet
    return True


# Function to add new solution to current set of solutions
def addMap(map):
    """Saves the board state to the global variable 'solutions'"""
    global maps
    saved_map = copy.deepcopy(map)
    maps.append(saved_map)


# Function to solve HW1 recursively by placing officer one by one from leftmost column
# It returns false if queens cannot be placed, otherwise return true and
# placement of queens in the form of 1s.
def solver(map, col, dimMap, numPol):
    """Use backtracking to find all solutions"""
    # base case: If all officers are placed then return true
    if col >= numPol:
        return True

    # # The possibility of placing the first officer is first column to the dimMap-numPol column
    # for j in range(0, dimMap-numPol, 1):
    # Consider this column and try placing this officer in all rows one by one
    for i in range(dimMap-numPol, dimMap, 1):
        if isPosValid(map, i, col, dimMap):
            # Place this officer in board[i][col]
            map[i][col] = 1
            # Check if the last officer has been successfully placed or not
            if col == numPol - 1:
                addMap(map)  # add solution to the set
                map[i][col] = 0  #
                return True

            # recursively place rest of the police officers
            else:
                solver(map, col + 1, dimMap, numPol)
            # backtrack
            map[i][col] = 0

def main():
    start = time.clock()
    global maps
    dimMap = 9
    numPol = 9
    map = getMap(dimMap)
    maps = []

    solver(map, 0, dimMap, numPol)

    printMaps(maps)

    print("Total solutions = {}".format(len(maps)))

    print("Time elapsed: "+ str(time.clock()-start) + " s")
main()