# Minh Tran
# CSCI 561 Fall 2018
# Assignment 1b
# tranmt@usc.edu
# Description: Scooter Monitoring LADOT

import copy
import numpy as np

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

# Function to print 1 placement of police officers
def printMap(map):
    for row in map:
        for grid in row:
            print(grid),
        print

# Function to add new solution to current set of solutions
def addMap(map):
    """Saves the board state to the global variable 'solutions'"""
    global maps
    saved_map = copy.deepcopy(map)
    maps.append(saved_map)

# Function to read input file and output map with grid score and other parameters
def readFiles(fileIn):
    ### READING INPUT FILE ###
    # read all lines
    lines = fileIn.readlines()

    # Extract data in specific lines
    # Width and Height of city area:
    dimMap = int(lines[0])
    print("The width and height of the city area are " + str(dimMap))

    # Number of police officers
    numPol = int(lines[1])
    print("The number of police is " + str(numPol))

    # Number of scooters:
    numSco = int(lines[2])
    print("The number of scooters is " + str(numSco))

    # Extract the rest of the data: numSco*12 for each Scooter
    row = []
    col = []
    remLines = lines[3:]
    for line in remLines:
        line = line.strip()
        line = line.split(',')
        row.append(int(line[0]))
        col.append(int(line[1]))

    # Create an empty map
    map = getMap(dimMap)
    for idx in range(len(row)):
        for i in range(dimMap):
            for j in range(dimMap):
                if row[idx] == i and col[idx] == j:
                    map[i][j] += 1

    # Test
    if sum(sum(map, [])) == numSco*12:
        print "Sum of grid score equals number of scooter movements"
    return map, dimMap, numPol, numSco

# This function is to calculate the potential "lost" score if a position is picked
def evalFunc(map):
    dimMap = len(map)
    valMap = getMap(dimMap)
    mapArray = np.asarray(map)

    for row in range(dimMap):
        for col in range(dimMap):
            # Calculate lost opportunity in row and col
            sumRow = np.sum(mapArray,axis=1)[row] - map[row][col]
            sumCol = np.sum(mapArray,axis=0)[col] - map[row][col]

            # Calculate lost opportunity in diagonal
            diagonal = np.diag(mapArray, col - row)
            antidiagonal = np.diag(np.fliplr(mapArray), dimMap - col - 1 - row)

            sumDiagonal = np.sum(diagonal) - map[row][col]
            sumAntidiagonal = np.sum(antidiagonal) - map[row][col]

            # this value needs to underline the LOST opportunity
            valMap[row][col] = sumRow + sumCol + sumDiagonal + sumAntidiagonal
    return valMap

# This function is to find the best remaining place with highest grid score
def findBestLoc(map):
    # pass the input to an array
    mapArray = np.asarray(map)

    # find the max value of this 2D array
    maxVal = max(mapArray.flatten())

    # sort the grid score value of this 2D array
    sortedVal = mapArray.flatten()[np.argsort(mapArray.flatten())]
    sortedValUnique = np.unique(sortedVal)

    # Find the maximum available spot to place the officer
    locBest = zip(*np.where(mapArray == maxVal))

    # Find all available spots to place the officer in the order of decreasing score
    locSort = []
    for idx in range(len(sortedValUnique)):
        locSort.append(zip(*np.where(mapArray == sortedValUnique[idx])))

    # Reverse for highest score grid first
    locSort.reverse()
    locSortFlat = [item for sublist in locSort for item in sublist]
    return locBest, locSortFlat

# This function is to check if the position to place an officer is valid
def isPosValid(map, row, col, dimMap):
    """Check if it's valid to place an officer at map[x][y]"""

    # Check this row on left side
    for j in range(col):
        if map[row][j] == 1:
            return False

    # Check this row on right side
    for j in range(col + 1, dimMap, 1):
        if map[row][j] == 1:
            return False

    # Check this column on top side
    for i in range(row):
        if map[i][col] == 1:
            return False

    # Check this column on bottom side
    for i in range(row + 1, dimMap, 1):
        if map[i][col] == 1:
            return False

    # Check upper diagonal on left side
    # zip is to match variables of similar indexes in different lists
    for i, j in zip(range(row-1, -1, -1), range(col-1, -1, -1)):
        if map[i][j] == 1:
            return False

    # Check upper diagonal on right side
    # zip is to match variables of similar indexes in different lists
    for i, j in zip(range(row + 1, dimMap, 1), range(col+1, dimMap, 1)):
        if map[i][j] == 1:
            return False

    # Check lower diagonal on left side
    for i, j in zip(range(row+1, dimMap, 1), range(col-1, -1, -1)):
        if map[i][j] == 1:
            return False

    # Check lower diagonal on right side
    for i, j in zip(range(row-1, -1, -1), range(col+1, dimMap, 1)):
        if map[i][j] == 1:
            return False

    return True


# This function update the map of grid score after each placement of officer @ [row][col]
def updateMap(map, row, col):
    dimMap = len(map)
    # Remove that point
    map[row][col] = 0

    # Check this row on left side
    for j in range(col):
        map[row][j] = 0

    # Check this row on right side
    for j in range(col + 1, dimMap, 1):
        map[row][j] = 0

    # Check this column on top side
    for i in range(row):
        map[i][col] = 0

    # Check this column on bottom side
    for i in range(row + 1, dimMap, 1):
        map[i][col] = 0

    # Check upper diagonal on left side
    # zip is to match variables of similar indexes in different lists
    for i, j in zip(range(row-1, -1, -1), range(col-1, -1, -1)):
        map[i][j] = 0

    # Check upper diagonal on right side
    # zip is to match variables of similar indexes in different lists
    for i, j in zip(range(row + 1, dimMap, 1), range(col+1, dimMap, 1)):
        map[i][j] = 0

    # Check lower diagonal on left side
    for i, j in zip(range(row+1, dimMap, 1), range(col-1, -1, -1)):
        map[i][j] = 0

    # Check lower diagonal on right side
    for i, j in zip(range(row-1, -1, -1), range(col+1, dimMap, 1)):
        map[i][j] = 0

    return map

# Function to solve HW1 recursively by placing officer one by one from leftmost column
# It returns false if queens cannot be placed, otherwise return true and
# placement of queens in the form of 1s.
def solver2(map, col, dimMap, numPol):
    """Use backtracking to find all solutions"""
    # base case: If all officers are placed then return true
    if col >= numPol:
        return True

    # The possibility of placing the first officer is first column to the dimMap-numPol column
    # for j in range(0, dimMap-numPol+1, 1):
        # Consider this column and try placing this officer in all rows one by one
    for i in range(0,dimMap,1):
        if isPosValid(map, i, col, dimMap):
            # Place this officer in board[i][col]
            map[i][col] = 1
            # Check if the last officer has been successfully placed or not
            if col == numPol - 1:
                addMap(map)  # add solution to the set
                map[i][col] = 0  # reset the solution / clean the map
                return True

            # recursively place rest of the police officers
            else:
                solver2(map, col + 1, dimMap,numPol)
            # backtrack
            map[i][col] = 0


# This function implements a greedy heuristic to solve for
# the best placement of officer in the grid map to obtain the highest score
def solver(map, numPol):
    # Keep track of activity point and number of police officers properly placed
    point = 0
    polPlace = 0

    # base case: If all officers are placed then return true
    if polPlace == numPol:
        return True

    # Create a parallel map to keep track of police officer's posiiton
    locMap = getMap(len(map))

    # Loop through each police officer to place him/her
    for pol in range(numPol):
        # Find location to place the officer
        locsBest, locsSorted = findBestLoc(map)

        # Pick the best available location based on the guided eval function
        loc = locsSorted[0]
        print loc

        if isPosValid(locMap, loc[0], loc[1], len(map))==False:
            print "This officer is not properly placed"
            break

        # Pick the best available location based on the guided eval function
        # place the officer here and update point
        point += map[loc[0]][loc[1]]
        polPlace += 1

        # update the corresponding location map (map that only has 1s for officer location and 0s elsewhere)
        locMap[loc[0]][loc[1]] = 1

        # update map
        updateMap(map, loc[0], loc[1])

    if polPlace == numPol:
        print "All police officers have been placed"
    if polPlace < numPol:
        print "Not all police officers have been placed"
    return point


# MAIN
def main():
    global maps
    maps = []

    # import input.txt file to read
    fileIn = open("input3.txt", "r")
    map, dimMap, numPol, numSco = readFiles(fileIn)

    # Print the map with grid score
    print("Map with grid score")
    printMap(map)
    print

    # Establish an eval function of LOST score
    # valMap = evalFunc(map)
    # print("Evaluation Function with grid score")
    # printMap(valMap)

    # Solve
    point = solver(map, numPol)
    print "Greedy Point is " + str(point)

    # Close the file
    fileIn.close()


    # WRITTING OUTPUT FILE ###
    fileOut = open("output.txt", "w")
    fileOut.write(str(point))
    # Close the file
    fileOut.close()
main()