#!/bin/python

# Solution for AI HW1

import time
from random import randint
from random import uniform
from math import exp
from math import ceil
from math import log
import copy

lizPositions = []
treePositions = []
treePosCol = {}
treePosRow = {}
nurseryMatrix = []
"""
Abstract representation of a position in the nursery
"""
class Position:
    row = None
    col = None
    def __init__(self, row, col):
        self.row = row
        self.col = col
"""
A state refers to an arrangement of lizards on the nursery.
This is used to keep track of possible arrangements in BFS.
"""
class State:
    lizPos = None
    def __init__(self, lizPos):
        self.lizPos = lizPos

"""Driver function"""
def main():
    inputFile = open("input.txt", "r")
    method = inputFile.readline().strip()
    N = int(inputFile.readline())
    P = int(inputFile.readline())
    for i in xrange(0, N):
        nurseryMatrix.append([])

    for i in xrange(0, N):
        curLine = inputFile.readline()
        for j in xrange(0, N):
            nurseryMatrix[i].append(curLine[j])

    for i in xrange(0, N):
        treePosCol[i] = -1
        treePosRow[i] = -1

    hasTrees = False
    for i in xrange(0, N):
        for j in xrange(0, N):
            if nurseryMatrix[i][j] == "2":
                hasTrees = True
                treePositions.append(Position(i, j))
                if treePosCol[j] == -1:
                    treePosCol[j] = i
                if treePosRow[i] == -1:
                    treePosRow[i] = i

    if method == "DFS":
        initDFS(N, P, hasTrees)
    elif method == "BFS":
        initBFS(N, P)
    elif method == "SA":
        initSA(N, P, nurseryMatrix)

"""Function call and file write for DFS"""
def initDFS(N, P, hasTrees):
    outputFile = open("output.txt", "w")
    foundSolution = False
    callLimit = 1
    timer = time.time() - start_time
    if hasTrees:
        callLimit = N
    for col in xrange(0, callLimit):
        if solveLizPlacementDFS(N, P, -1, col, timer):
            outputFile.write("OK")
            for pos in lizPositions:
                nurseryMatrix[pos.row][pos.col] = "1"
                print pos.row, pos.col
            for i in xrange(0, N):
                curLine = "".join(nurseryMatrix[i])
                outputFile.write("\n")
                outputFile.write(curLine)
            foundSolution = True
            break
    if not foundSolution:
        outputFile.write("FAIL")

"""Function call and file write for BFS"""
def initBFS(N, P):
    outputFile = open("output.txt", "w")
    stateQueue = []
    lizPos = []
    initState = State(lizPos)
    stateQueue.append(initState)
    resPos = solveLizPlacementBFS(N, P, stateQueue)
    if resPos == None:
        outputFile.write("FAIL")
    else:
        outputFile.write("OK")
        for pos in resPos:
            nurseryMatrix[pos.row][pos.col] = "1"
        for i in xrange(0, N):
            curLine = "".join(nurseryMatrix[i])
            outputFile.write("\n")
            outputFile.write(curLine)

"""Function call and file write for SA"""
def initSA(N, P, nurseryMatrix):
    outputFile = open("output.txt", "w")
    nurseryMatrix = solveLizPlacementSA(N, P, nurseryMatrix)
    if nurseryMatrix == None:
        outputFile.write("FAIL")
    else:
        outputFile.write("OK")
        for i in xrange(0, N):
            curLine = "".join(nurseryMatrix[i])
            outputFile.write("\n")
            outputFile.write(curLine)

"""
Method used by DFS and BFS to determine if cell (row, col) is
a safe location to place a lizard considering other lizards and trees.
lizPositions: List containing Position objects representing lizards.
treePositions: List containing Position objects representing trees.
"""
def isSafe(row, col, lizPositions, treePositions):
    if nurseryMatrix[row][col] == "2":
        return False

    for pos in lizPositions:
        posSafe = False
        if pos.row == row:
            colMin = min(pos.col, col)
            colMax = max(pos.col, col)
            for tree in treePositions:
                if tree.row == row and colMin < tree.col < colMax:
                    posSafe = True
            if posSafe == False:
                return False

        if pos.col == col:
            rowMin = min(pos.row, row)
            rowMax = max(pos.row, row)
            for tree in treePositions:
                if tree.col == col and rowMin < tree.row < rowMax:
                    posSafe = True
            if posSafe == False:
                return False

        if (pos.row + pos.col) == row + col:
            diff1 = pos.row - pos.col
            diff2 = row - col
            minDiff = min(diff1, diff2)
            maxDiff = max(diff1, diff2)
            for tree in treePositions:
                treeDiff = tree.row - tree.col
                if (tree.row + tree.col) == row + col and minDiff < treeDiff < maxDiff:
                    posSafe = True
            if posSafe == False:
                return False

        if (pos.row - pos.col) == row - col:
            sum1 = pos.row + pos.col
            sum2 = row + col
            minSum = min(sum1, sum2)
            maxSum = max(sum1, sum2)
            for tree in treePositions:
                treeSum = tree.row + tree.col
                if (tree.row - tree.col) == row - col and minSum < treeSum < maxSum:
                    posSafe = True
            if posSafe == False:
                return False
    return True

"""
Method used by DFS and BFS to add a lizard to cell (row, col).
"""
def addLizard(lizPostions, row, col):
    newPos = Position(row, col)
    lizPostions.append(newPos)

"""
Recursive implementation of DFS to find a valid solution.
The depth wise increase in this case is column wise. 
Within each column I make multiple recursive calls for each row if a tree is present.
This is to cover all possible cases of lizard placement.
Note : Python's maximum recursion limit ~ 1000 limits N to 400-500 at best.
"""
def solveLizPlacementDFS(n, p, row, col, timer):
    global lizPositions
    global treePositions
    global treePosCol
    if p == 0:
        return True
    if col >= n or timer >= 280:
        return False
    for i in xrange(row+1, n):
        if isSafe(i, col, lizPositions, treePositions):
            addLizard(lizPositions, i, col)
            if treePosCol[col] != -1 and solveLizPlacementDFS(n, p-1, i, col, start_time - time.time()):
                return True
            j = 1
            while col + j <= n:
                if solveLizPlacementDFS(n, p-1, -1, col + j, time.time() - start_time):
                    return True
                j += 1
            lizPositions = lizPositions[:-1]

"""
Iterative implementation of BFS to find a valid solution.
The algorithm makes use of State objects which contain a list for lizard positions.
It also makes use of a state queue as a frontier set to explore.
If a state contains P lizards, it is returned as a valid solution.
"""
def solveLizPlacementBFS(N, P, stateQueue):
    i = 0
    stateCount = 0
    prevStateCount = 1
    statesPopped = 0
    timer = time.time() - start_time
    while stateQueue and i < N and timer < 280:
        curState = stateQueue.pop(0)
        statesPopped += 1
        curStateCount = 0
        for j in xrange(0, N):
            tempPos = list(curState.lizPos)
            if time.time() - start_time > 280:
                break
            if isSafe(i, j, tempPos, treePositions):
                tempPos.append(Position(i, j))
                stateQueue.append(State(tempPos))
                stateCount += 1
                curStateCount += 1
                if len(tempPos) == P:
                    return tempPos
                # From first safe to N, we now iterate over all columns of the current row
                # and for the current state and consider all possible combinations
                # If we find a safe location say x.
                # Add jx to the queue
                # Add x to queue in combination with all elements in "found"
                # Add x to found
                # Repeat until N
                found = []
                if treePosRow[i] != -1:
                    for x in xrange(j+2, N):
                        curTempPos = list(tempPos)
                        if isSafe(i, x, tempPos, treePositions):
                            curPos = Position(i, x)
                            curTempPos.append(curPos)
                            if len(curTempPos) == P:
                                return curTempPos
                            for pos in found:
                                if isSafe(i, x, pos, treePositions):
                                    newPos = list(pos)
                                    newPos.append(curPos)
                                    if len(newPos) == P:
                                        return newPos
                                    found.append(newPos)
                            found.append(curTempPos)
                for pos in found:
                    stateQueue.append(State(pos))
                    stateCount += 1
                    curStateCount += 1
        if stateCount == 0 or curStateCount == 0:
            stateQueue.append(curState)
            stateCount += 1

        if statesPopped == prevStateCount:
            i += 1
            if len(stateQueue[0].lizPos) != 0:
                stateQueue.insert(0, State([]))
                stateCount += 1
            if stateCount != 0:
                prevStateCount = stateCount
            stateCount = 0

            statesPopped = 0
    return None

"""
Used to generate the initial random nursery for Simulated Annealing.
"""
def generateRandomArrangement(N, P, nurseryMatrix, curLizPos):
    for i in xrange(0, P):
        row = randint(0, N - 1)
        col = randint(0, N - 1)
        while nurseryMatrix[row][col] == "1" or nurseryMatrix[row][col] == "2":
            row = randint(0, N-1)
            col = randint(0, N-1)
        nurseryMatrix[row][col] = "1"
        curLizPos.append(Position(row, col))
    return nurseryMatrix

"""
Generates the neighboring state for Simulated Annealing.
This is done by selecting a lizard at random at moving it to a random
location on the board provided there is no tree or lizard there.
"""
def generateNextStep(N, P, lizPos, nurseryMatrix):
    randomLizIdx = randint(0, P-1)
    randomLiz = lizPos[randomLizIdx]
    tempMatrix = copy.deepcopy(nurseryMatrix)
    row = randint(0, N-1)
    col = randint(0, N-1)
    cellsCovered = 1
    while tempMatrix[row][col] == "1" or tempMatrix[row][col] == "2":
        row = randint(0, N-1)
        col = randint(0, N-1)
        cellsCovered += 1
        if cellsCovered >= N**2-1:
            return tempMatrix
    tempMatrix[row][col] = "1"
    tempMatrix[randomLiz.row][randomLiz.col] = "0"
    del lizPos[randomLizIdx]
    lizPos.append(Position(row, col))
    return tempMatrix

"""
Calculates the number of attacks in total. 
For each lizard, 8 directions are traversed on the board to assess conflicts.
"""
def calculateAttacks(lizPos, nurseryMatrix, N):
    attackCount = 0
    for pos in lizPos:
        x = pos.row - 1
        y = pos.col
        while x >= 0:
            if nurseryMatrix[x][y] == "1":
                attackCount += 1
            elif nurseryMatrix[x][y] == "2":
                break
            x -= 1

        x = pos.row + 1
        y = pos.col
        while x < N:
            if nurseryMatrix[x][y] == "1":
                attackCount += 1
            elif nurseryMatrix[x][y] == "2":
                break
            x += 1

        x = pos.row
        y = pos.col - 1
        while y >= 0:
            if nurseryMatrix[x][y] == "1":
                attackCount += 1
            elif nurseryMatrix[x][y] == "2":
                break
            y -= 1

        x = pos.row
        y = pos.col + 1
        while y < N:
            if nurseryMatrix[x][y] == "1":
                attackCount += 1
            elif nurseryMatrix[x][y] == "2":
                break
            y += 1

        x = pos.row - 1
        y = pos.col - 1
        while x >= 0 and y >= 0:
            if nurseryMatrix[x][y] == "1":
                attackCount += 1
            elif nurseryMatrix[x][y] == "2":
                break
            x -= 1
            y -= 1

        x = pos.row + 1
        y = pos.col + 1
        while x < N and y < N:
            if nurseryMatrix[x][y] == "1":
                attackCount += 1
            elif nurseryMatrix[x][y] == "2":
                break
            x += 1
            y += 1

        x = pos.row + 1
        y = pos.col - 1
        while x < N and y >= 0:
            if nurseryMatrix[x][y] == "1":
                attackCount += 1
            elif nurseryMatrix[x][y] == "2":
                break
            x += 1
            y -= 1

        x = pos.row - 1
        y = pos.col + 1
        while x >= 0 and y < N:
            if nurseryMatrix[x][y] == "1":
                attackCount += 1
            elif nurseryMatrix[x][y] == "2":
                break
            x -= 1
            y += 1

    if attackCount == 0:
        print "FOUND"
        for pos in lizPos:
            print pos.row, pos.col
    return attackCount

"""
Probability function to select a worse state for Simulated Annealing.
"""
def selectNextWithChance(deltaE, T):
    randFloat = uniform(0, 1)
    fn = exp(-deltaE/T)
    if randFloat < fn:
        return True
    else:
        return False

"""
Implementation of Simulated Annealing with a logarithmic temperature schedule.
I've added a stabilizing loop within to allow the system to choose a better state
at any given temperature before cooling further.
"""
def solveLizPlacementSA(N, P, nurseryMatrix):
    currentTemperature = 1.0 * 30**1
    freezingTemperature = 0
    stabilizer = 50
    stabilizingFactor = 1.0005
    curLizPos = []
    start_time = time.time()
    timer = start_time - time.time()
    currentArrangement = generateRandomArrangement(N, P, nurseryMatrix, curLizPos)
    while currentTemperature > freezingTemperature and timer < 280:
        for i in xrange(0, stabilizer):
            timer = time.time() - start_time
            newLizPos = list(curLizPos)
            nextStep = generateNextStep(N, P, newLizPos, currentArrangement)
            curAttacks = calculateAttacks(curLizPos, currentArrangement, N)
            nextAttacks = calculateAttacks(newLizPos, nextStep, N)
            if curAttacks == 0:
                return currentArrangement
            if nextAttacks == 0:
                return nextStep
            deltaE = nextAttacks - curAttacks
            if deltaE < 0:
                currentArrangement = nextStep
                curLizPos = list(newLizPos)
            elif selectNextWithChance(deltaE, currentTemperature):
                currentArrangement = nextStep
                curLizPos = list(newLizPos)
        currentTemperature /= log(4 + 3)
        stabilizer = int(ceil(stabilizer * stabilizingFactor))
    return None

if __name__ == '__main__':
    start_time = time.time()
    main()
    print "--- %s seconds ---" % (time.time() - start_time)