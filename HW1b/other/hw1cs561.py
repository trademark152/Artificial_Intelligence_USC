# Minh Tran
# CSCI 561 Fall 2018
# Assignment 1b
# tranmt@usc.edu
# Description: Scooter Monitoring LADOT

import numpy as np
import copy

# Function to establish the area to survey
# Input is the map dimension (assumed square map)
# Output is a map as a list of lists (default valued 0)
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
                solver(map, col + 1, dimMap,numPol)
            # backtrack
            map[i][col] = 0

def sumkLargest(arr, k):
    # Sort the given array arr in reverse order.
    # arr.sort(reverse=True)
    arrSort = sorted(arr, reverse=True)
    sumK = 0
    # Print the first kth largest elements
    for i in range(k):
      sumK += arrSort[i]
    return sumK

def findSolution(map,maps,numPol):
    maxPoint = 0
    for mapLoc in maps:
        mapLocArray = np.asarray(mapLoc)
        mapArray = np.asarray(map)
        pointArr = mapArray.flatten()[mapLocArray.flatten() == 1]
        print pointArr
        point = sumkLargest(pointArr, numPol)
        if point > maxPoint:
            maxPoint = point
    return maxPoint


# MAIN
def main():
    global maps
    maps = []

    # import input.txt file to read
    fileIn = open("input1.txt", "r")
    map, dimMap, numPol, numSco = readFiles(fileIn)

    # Print the map with grid score
    print("Map with grid score")
    printMap(map)
    print

    # Initiate a map with just 0s and 1s (1 means police)
    mapLoc = getMap(dimMap)

    # Solve the problem first with number of police equaling grid size
    solver(mapLoc, 0, dimMap, dimMap)

    # Print all solutions:
    printMaps(maps)
    print("Total solutions = {}".format(len(maps)))

    # Find solutions:
    maxPt = findSolution(map, maps,numPol)
    print maxPt

    # Close the file
    fileIn.close()


    # WRITTING OUTPUT FILE ###
    # fileOut = open("output.txt", "w")
    # fileOut.write(str(point))
    # # Close the file
    # fileOut.close()
main()