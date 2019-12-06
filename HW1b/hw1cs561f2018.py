# Minh Tran
# CSCI 561 Fall 2018
# Assignment 1b
# tranmt@usc.edu
# Description: Scooter Monitoring LADOT

import time
import re
import copy

import cProfile
import numpy as np

"""Function to read input file
   Output map dimension, map grids with score
    number of police and number of scooter"""
def readFiles(fileIn):
    ### READING INPUT FILE ###
    # read all lines
    lines = fileIn.readlines()

    # Extract data in specific lines
    # Dimension of city area:
    dimMap = int(lines[0])
    print("The dimension of the city area are " + str(dimMap))

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
    scoreMap = getMap(dimMap)
    for idx in range(len(row)):
        for i in range(dimMap):
            for j in range(dimMap):
                if row[idx] == i and col[idx] == j:
                    scoreMap[i][j] += 1

    # Test
    if sum(sum(scoreMap, [])) == numSco*12:
        print "Sum of grid score equals number of scooter movements"
    return scoreMap, dimMap, numPol, numSco


"""Function to establish the area to survey
    Input is the map dimension (assumed square map)
    Output is a map as a list of lists (default valued 0)"""
def getMap(dimMap):
    map = [0] * dimMap
    for idx in range(dimMap):
        map[idx] = [0] * dimMap
    return map

"""Function to print a single solution"""
def printMap(map):
    for row in map:
        for column in row:
            print(column),
        print

# Function to print all valid placements of police officers
def printMaps(maps):
    idx = 1
    for map in maps:
        print("Solution " + str(idx))
        for row in map:
            print(row)
        print
        idx += 1

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

"""Function to create a list of row-col coordinates of all positions
    Input is the map dimension (assumed square map)
    Output is all position coordinate as a list of lists (default valued 0)"""
def getCoord(dimMap):
    allPos = []
    for row in range(dimMap):
        for col in range(dimMap):
            allPos.append([row, col])
    return allPos

"""Function to find available positions 
    in Current map left after placing current queens
    Input is current queen positions currentQ(list of lists)
    Output is a availPos(list of lists) """
def findAvail(dimMap, currentPol):
    # Create a full map with all available coordinate
    allAvailPos = getCoord(dimMap)

    # Loop through each police position to remove clashing positions
    for pol in currentPol:
        # print queen
        row = pol[0]
        col = pol[1]
        for i in range(dimMap):
            for j in range(dimMap):
                if i == row or j == col or (i+j) == (row+col) or (j-i) == (col-row):
                    try:
                        allAvailPos.remove([i, j])
                    except ValueError:
                        pass  # do nothing!
    return allAvailPos

"""Function to add new solution to current set of solutions"""
def addSolution(solution):
    """Saves the board state to the global variable 'solutions'"""
    global solutions
    saved_solution = copy.deepcopy(solution)
    solutions.append(saved_solution)

"""Function to add new best score to current set of best score"""
def addScore(score):
    """Saves the board state to the global variable 'solutions'"""
    global scores
    saved_score = copy.deepcopy(score)
    scores.append(saved_score)

"""Function to calculate score"""
def calScore(scoreMap, solution):
    score = 0
    for idx in range(len(solution)):
        score += scoreMap[solution[idx][0]][solution[idx][1]]
    return score


def removeBadStart(allPos, scoreMap):
    dimMap = len(scoreMap)
    for row in range(dimMap):
        for col in range(dimMap):
            if scoreMap[row][col] < 1:
                try:
                    allPos.remove([row, col])
                except ValueError:
                    pass  # do nothing!

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

"""Function to find solutions to place police 
    in Current map left after placing current queens
    Input is current queen positions currentQ(list of lists)
    Output is a availPos(list of lists) """
def findSol(currentPol, numPol, dimMap,scoreMap):
    # At any point, if all officers have been placed, return the solution
    if len(currentPol) == numPol:
        score = calScore(scoreMap, currentPol)
        addScore(score)
        addSolution(currentPol)

    # Find out all available positions to place officers:
    allAvailPos = findAvail(dimMap, currentPol)
    # print allAvailPos

    # Remove bad starting point
    removeBadStart(allAvailPos, scoreMap)

    # Loop through each position to find all solutions
    for pos in allAvailPos:
        # Update the current list
        currentPol.append(pos)
        # print currentPol
        if len(currentPol) == numPol:
            score = calScore(scoreMap, currentPol)
            addScore(score)
            addSolution(currentPol)

        else:
            # recursively call the findSolutions
            findSol(currentPol, numPol, dimMap, scoreMap)

        # Back track if no solution is found
        del currentPol[-1]

    # return scores
    return scores, solutions


"""MAIN"""
def main():
    # start_time = time.time()
    global solutions, scores, maps
    solutions = []
    scores = []
    maps = []


    # import input.txt file to read
    fileIn = open("input.txt", "r")
    scoreMap, dimMap, numPol, numSco = readFiles(fileIn)

    # Print the map with grid score
    print("Map with grid score")
    printMap(scoreMap)
    print

    if numPol == dimMap:
        # SECONDARY SOLVER
        map = getMap(dimMap)

        # Solve: similar to N-queen problem
        solver(map, 0, dimMap, numPol)

        # maximum score
        scores = 0
        # printMaps(maps)

        # Loop through all solutions and find the max
        idxSol = 0
        for idx in range(len(maps)):
            score = 0
            for row in range(dimMap):
                for col in range(dimMap):
                    if maps[idx][row][col] == 1:
                        score += scoreMap[row][col]
            if score > scores:
                scores = score
                idxSol = idx

        print "The maximum activity point is ", scores
        print "The placement of police officer is: "
        printMap(maps[idxSol])

    else:
        #  MAIN SOLVER:
        # obtain all possible starting positions
        allPos = getCoord(dimMap)
        removeBadStart(allPos, scoreMap)

        for startPos in allPos:
            # Initiate solution:
            currentPol = [startPos]

            # Recursively find all solutions
            scores, solutions = findSol(currentPol, numPol, dimMap, scoreMap)

        # cProfile.run('re.compile("foo|bar")')

        # print "The officers' position are ",
        # print bestSolution,  "!"
        # print

        if scores:
            bestSolutions = solutions[np.argmax(scores)]
            scores = max(scores)
            print "The maximum activity point is " + str(scores)
            print "The placement of police officer is: [row, col]:", bestSolutions
        else:
            print "No solution found"


        # print("--- %s seconds ---" % (time.time() - start_time))

    # Close the file
    fileIn.close()

    # WRITTING OUTPUT FILE ###
    fileOut = open("output.txt", "w")
    fileOut.write(str(scores))
    # Close the file
    fileOut.close()

main()