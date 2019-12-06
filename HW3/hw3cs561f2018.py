# Minh Tran
# CSCI 561 Fall 2018
# Assignment 3
# tranmt@usc.edu
# Description: Optimize path-finding car to reach finisning point

""" Ideas:
- With initial locations of obstacles and start/finish locations of each car, create an initial utility grid
- Iterate to obtain the converged final utility grid
- Use the final utility grid to obtain the policy grid (which optimal direction to take in each cell)
- Need to calculate the expected utility grid in each direction before deciding on the optimal move to make
- Use a function to randomize move at each location based on given probability: 0.7 - 0.1 - 0.1 - 0.1
- Calculate the path cost at the end
- Use 10 different seeds to make 10 different simulations for each car
"""


from __future__ import print_function
import time
# import matplotlib.pyplot as plt
import numpy as np
import math

"""Function to read input file"""
def readFiles(fileIn):
    # read all lines
    lines = fileIn.readlines()

    # Extract data in specific lines
    count = 0
    # First line: positive integer s: size of Grid s*s
    gridSize = int(lines[count])
    print("The size of the Grid is " + str(gridSize))
    count += 1

    # Second line: positive integer n: number of cars
    numCar = int(lines[count])
    print("The number of cars is " + str(numCar))
    count += 1

    # Third line: positive integer o: number of obstacles
    numObs = int(lines[count])
    print("The number of obstacle is " + str(numObs))
    count += 1

    # Obstacle position
    obs = set()
    for iter in range(0, numObs):
        line = lines[count].strip()
        line = line.split(',')
        # add obstacles location by (col,row)
        obs.add((int(line[0]), int(line[1])))
        count += 1
    print("The position of all obstacles are ", obs)

    # Establish all cars as a dictionary
    allCars = {}
    for iter in range(0, numCar):
        # add each car by setting its start and finish
        car = Car()
        line = lines[count].strip()
        line = line.split(',')
        # add car location by (col,row)
        car.setStart((int(line[0]), int(line[1])))
        # set a key for each car in allCars dict as a numeric value
        allCars[iter] = car
        count += 1
        # print (car.getStart())

    print("Keys of all cars: ", allCars.keys())
    print("Each car start and finish locations: ")
    # Car finishing position
    for iter in range(0, numCar):
        # get the car in the dict to add finish location
        car = allCars[iter]
        line = lines[count].strip()
        line = line.split(',')
        # add car location by (col,row)
        car.setFinish((int(line[0]), int(line[1])))
        print(car)
        count += 1
        # print(car.getFinish())

    return gridSize, numCar, numObs, obs, allCars

"""class of A* graph search with input start, end"""
class AStarGraph(object):
    # Define a class board like grid with two barriers
    def __init__(self,width,height):
        # barriers are costly to encounter
        self.barriers = []
        self.width = width
        self.height = height

    def heuristic(self, start, goal):
        # Use Manhattan distance heuristic if we can move one square adjacent
        dx = abs(start[0] - goal[0])
        dy = abs(start[1] - goal[1])
        return dx+dy

    # get the neighboring vertices
    def get_vertex_neighbours(self, pos, width, height):
        n = []
        # Moves allow link a chess king except diagonally
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            x2 = pos[0] + dx
            y2 = pos[1] + dy
            # check if move exceeds boundary
            if x2 < 0 or x2 > width or y2 < 0 or y2 > height:
                # exclude these beyond-boundary neighbors
                continue
            # add that to answer
            n.append((x2, y2))
        return n

    def move_cost(self, a, b, goal):
        # losing 1 unit because of gas but get rewarded 100 units because of reaching goal
        for barrier in self.barriers:
            if b in barrier:
                return 101.0  # Extremely high cost to enter barrier squares
        return 1.0  # Normal movement cost

"""function of A* graph search with input start, end and the graph itself"""
def AStarSearch(start, end, graph):
    G = {}  # Actual movement cost to each position from the start position
    F = {}  # Estimated movement cost of start to end going via this position

    # Initialize starting values
    G[start] = 0.0
    F[start] = graph.heuristic(start, end)

    # Maintain these sets to keep track of visited vertices, open vertices and originality:
    closedVertices = set()
    openVertices = set([start])
    cameFrom = {}

    # loop as long as there are still available vertices to visit
    while len(openVertices) > 0:
        # Get the vertex in the open list with the lowest F score (lowest cost)
        current = None
        currentFscore = None
        for pos in openVertices:
            if current is None or F[pos] < currentFscore:
                currentFscore = F[pos]
                current = pos

        # Check if we have reached the goal
        if current == end:
            # Retrace our route backward
            path = [current]
            while current in cameFrom:
                current = cameFrom[current]
                path.append(current)
            path.reverse()
            return path  # Done!

        # Mark the current vertex as closed
        openVertices.remove(current)
        closedVertices.add(current)

        # Update scores for vertices near the current position
        for neighbour in graph.get_vertex_neighbours(current, graph.width, graph.height):
            if neighbour in closedVertices:
                continue  # We have already processed this node exhaustively
            candidateG = G[current] + graph.move_cost(current, neighbour, end)

            if neighbour not in openVertices:
                openVertices.add(neighbour)  # Discovered a new vertex
            elif candidateG >= G[neighbour]:
                continue  # This G score is worse than previously found

            # Adopt this G score
            cameFrom[neighbour] = current
            G[neighbour] = candidateG
            H = graph.heuristic(neighbour, end)
            F[neighbour] = G[neighbour] + H

    raise RuntimeError("A* failed to find a solution")

"""" OBJECT"""
""" General object Car: 2 methods to set the start and finish points of car"""
class Car():
    # def __init__(self, startLoc = 0, finishLoc = 0):
    #     self.startLoc = startLoc
    #     self.finishLoc = finishLoc

    def setStart(self, loc):
        self.startLoc = loc

    def setFinish(self, loc):
        self.finishLoc = loc

    def getStart(self):
        return self.startLoc

    def getFinish(self):
        return self.finishLoc

    def __str__(self):
        return "Start: " + str(self.startLoc) + " and finish: " + str(self.finishLoc)

"""function to represent deviation from optimal direction, apply once to swerve 90 degree counter clockwise"""
def turnLeft(move):
    if move == "N":
        return "W"
    elif move == "W":
        return "S"
    elif move == "S":
        return "E"
    elif move == "E":
        return "N"


def turnRight(move):
    if move == "N":
        return "E"
    elif move == "E":
        return "S"
    elif move == "S":
        return "W"
    elif move == "W":
        return "N"

""" returns a direction (N, S, E , W)
# 70% chance of going in the right direction
# 10% chance of going swervy to a wrong direction"""
def getRandomMove(optimalMove, swerve, k):
    swerveValue = swerve[k]
    if swerveValue > 0.7:
        if swerveValue > 0.8:
            if swerveValue > 0.9:
                actualMove = turnRight(turnRight(optimalMove))
                # print("swerve_val: " + str(swerveValue ) + " desired: " + optimalMove + " actual: " + actualMove + " k: " + str(k) + "\n")
                return actualMove
            else:
                actualMove = turnRight(optimalMove)
                # print("swerve_val: " + str(swerveValue) + " desired: " + optimalMove + " actual: " + actualMove + " k: " + str(k) + "\n")
                return actualMove
        else:
            actualMove = turnLeft(optimalMove)
            # print("swerve_val: " + str(swerveValue) + " desired: " + optimalMove + " actual: " + actualMove + " k: " + str(k) + "\n")
            return actualMove

    # print("swerve_val: " + str(swerveValue) + " desired: " + optimalMove + " actual: " + optimalMove + " k: " + str(k) + "\n")
    return optimalMove

"""function to update position and score when appling a move to a starting position"""
def updatePosition(gridSize, currentLoc, actualMove):
    # based on the given actual move, find out the step move in x and y direction
    stepMove = getStepMove(actualMove)

    # update the location
    newLoc = (currentLoc[0] + stepMove[0], currentLoc[1] + stepMove[1])

    # check if the new location reaches beyond boundary
    if isValidLocation(newLoc, gridSize):
        return newLoc
    else:
        return currentLoc

# Returns a boolean indicating whether the location is a valid position inside the grid.
def isValidLocation(loc, gridSize):
    if loc[0] < 0 or loc[0] >= gridSize:
        return False
    if loc[1] < 0 or loc[1] >= gridSize:
        return False
    return True

# returns necessary steps in x, y direction to complete the move
def getStepMove(move):
    if move == "N":
        return (0, -1)
    elif move == "S":
        return (0, 1)
    elif move == "W":
        return (-1, 0)
    elif move == "E":
        return (1, 0)

# returns true if direction1 is higher priority/preferred than direction2
def isPreferred(direction1, direction2):
    # order of preferrence of directions
    directions = ["N", "S", "E", "W"]

    # return true if index of direction 1 is smaller than index of direction 2 in the above list
    return directions.index(direction1) < directions.index(direction2)


""" Function to gets best move given the expected cost grid"""
def getOptimalMove(col, row, utilGrid, gridSize):
    directions = ["W", "E", "S", "N"]
    optimalMove = ""
    maxExpUtil = None

    # Calculate utility in each direction
    nUtil, sUtil, eUtil, wUtil = calculateUtil(col, row, utilGrid, gridSize)

    for direction in directions:
        util = None
        # calculate expected utility in each direciton
        if direction == "N":
            util = 0.7 * nUtil + 0.1 * wUtil + 0.1 * eUtil + 0.1 * sUtil
        elif direction == "S":
            util = 0.1 * nUtil + 0.1 * wUtil + 0.1 * eUtil + 0.7 * sUtil
        elif direction == "E":
            util = 0.1 * nUtil + 0.1 * wUtil + 0.7 * eUtil + 0.1 * sUtil
        elif direction == "W":
            util = 0.1 * nUtil + 0.7 * wUtil + 0.1 * eUtil + 0.1 * sUtil

        # update maximum expected utility and corresponding direction
        if maxExpUtil == None or util > maxExpUtil:
            maxExpUtil = util
            optimalMove = direction

        # update the preferred direction if a tie is happen
        # (the directions are sorted in increasing preference)
        elif util == maxExpUtil:
            optimalMove = direction

    return optimalMove



"""MONEY CALCULATION """
"""Function to get average money earned for each car
This will be the average of 10 simulations of different seed"""
def getAvgMoney(car, gridSize, obs):
    # initiate total money Earned for each car after 10 simulation runs
    totalMoneyEarned10Runs = 0.0
    moneyEarnedEachRun = []

    # Get the grid of expected utility
    expUtilGrid = getUtilGrid(car, gridSize, obs)

    # Obtain the grid of optimal movement/policy based on the expected utility grid
    policyGrid = getPolicyGrid(gridSize, expUtilGrid)

    # print the final policy grid
    # print("Final Policy Grid:")
    # for row in range(0, gridSize):
    #    for col in range(0, gridSize):
    #        print(str(policyGrid[col][row]),end="   ")
    #    print("\n")

    # print(policyGrid[0][1])

    # Randomize the seed from 1 to 10
    for seed in range(0, 10):
        # calculate the money earned in each simulation run
        moneyEarnedEachRun.append(calculateMoney(car, gridSize, obs, policyGrid, seed))
        totalMoneyEarned10Runs += calculateMoney(car, gridSize, obs, policyGrid, seed)

    # The answer is the average of the ten simulation runs for each car, with the floor opeartion to round it up
    print("money earned each run", moneyEarnedEachRun)
    print("average", totalMoneyEarned10Runs / 10.0)
    return int(math.floor(totalMoneyEarned10Runs / 10.0))

"""Function to calculate the money earned in each simulation run 
(based on different seeds) for each car"""
def calculateMoney(car, gridSize, obs, policyGrid, seed):
    # initiate current location to be the starting location of the car
    currentLoc = car.startLoc
    # print(currentLoc)

    # if we start at the finishing location, then return reward $100-$1 gas
    if currentLoc == car.finishLoc:
        return 99.0

    # print("seed: ", seed)
    # initiate answer with prescribed decision
    money = 0.0

    # constrain randomness by the given seed
    np.random.seed(seed)

    # Return random floats in the half-open interval [0.0, 1.0)
    # from a uniform distribution in that interval
    swerve = np.random.random_sample(1000000)

    # pick a starting index to choose from swerve list
    k = 0

    # loop until current location coincides with end location
    while currentLoc != car.finishLoc:
        # print("curr: " + str(currentLoc) + " money: " + str(money) +  "\n")
        # print(swerve[k])
        # use index 0 for col, and index 1 for row.
        # extract the optimal move from the policy grid
        optimalMove = policyGrid[currentLoc[0]][currentLoc[1]]
        # print(optimalMove)

        # due to uncertainty (faulty turning mechanism): optimal move is randomized
        actualMove = getRandomMove(optimalMove, swerve, k)
        # print(actualMove)

        #check precision of simulation
        # print(np.finfo(type(swerve[k])))

        # update location
        currentLoc = updatePosition(gridSize, currentLoc, actualMove)

        # pay 1$ for gas no matter what (standing still, run into obstacles or make optimal move)
        money -= 1.0

        # pay 100$ for running into obstacle
        if currentLoc in obs:
            money -= 100.0

        # update index to choose a new random swerve
        k += 1

    # print(multiplier)
    # Reaching goal:
    money += 100.0


    # print("Final money earned: ", money)
    return money


"""GRID METHODS"""
"""Function to obtain the grid of optimal move: NWES"""
def getPolicyGrid(gridSize, expUtilGrid):
    # initialize policy grid for each car
    policyGrid = []
    for i in range(0, gridSize):
        row = [0] * gridSize
        policyGrid.append(row)

    for row in range(0, gridSize):
        for col in range(0, gridSize):
            # for each location, obtain the optimal move based on the expected utility grid
            policyGrid[col][row] = getOptimalMove(col, row, expUtilGrid, gridSize)


    # for i in range(0, gridSize):
    #     column2 = [None] * gridSize
    #     optimalMoveGrid.append(column2)

    """ ALGORITHM TO DECIDE THE NEXT BEST MOVE:
    A STAR SEARCH WITH MANHATTAN DISTANCE AS HEURISTIC """
    # create a A-Star graph object
    # graph = AStarGraph(gridSize, gridSize)
    # graph.barriers.append(obs)
    #
    # for col in range(0, gridSize):
    #     for row in range(0, gridSize):
    #         pseudoStart = (row, col)
    #         # print(pseudoStart)
    #         # print(car.finishLoc)
    #         path = AStarSearch(pseudoStart, car.finishLoc, graph)
    #         # print(path)
    #         if pseudoStart != car.finishLoc:
    #             optimalMoveGrid[col][row] = path[1]
    #             if path[1][0] - pseudoStart[0] == 1:
    #                 policyGrid[col][row]= 'E'
    #             elif path[1][0] - pseudoStart[0] == -1:
    #                 policyGrid[col][row]= 'W'
    #             elif path[1][1] - pseudoStart[1] == -1:
    #                 policyGrid[col][row]= 'N'
    #             elif path[1][1] - pseudoStart[1] == 1:
    #                 policyGrid[col][row]= 'S'
    #         else:
    #             optimalMoveGrid[col][row] = path[0]
    #             policyGrid[col][row] = "F"
    # print(optimalMoveGrid)
    # print(policyGrid)
    return policyGrid

""" Function to get the grid of expected utility based on start-finish and obstacles' locations"""
def getUtilGrid(car, gridSize, obs):
    # Initialize a gridSize*gridSize utility grid
    # starting with -1 at every grid cell (representing gas money loss)
    utilGrid = []
    for i in range(0, gridSize):
        row = [-1.0] * gridSize
        utilGrid.append(row)

    # for row in range(0, gridSize):
    #     for col in range(0, gridSize):
    #         print(utilGrid[row][col], end =" ")
    #     print("\n")

    # update utility for obstacle locations
    for loc in obs:
        utilGrid[loc[0]][loc[1]] -= 100.0

    # update utility for finishing location
    utilGrid[car.finishLoc[0]][car.finishLoc[1]] += 100.0

    # recursively iterate to get the expected utility grid
    return iterateUtilGrid(car, utilGrid, obs, gridSize)




""" UTILITY"""
"""Function to recursively iterate the initial utility grid to obtain final expected util Grid"""
def iterateUtilGrid(car, utilGrid, obs, gridSize):

    while True:
        # initiate a temporary grid with util 0
        tempGrid = []
        for i in range(0, gridSize):
            column = [0.0] * gridSize
            tempGrid.append(column)

        # maximum threshold allowed for difference from optimal value
        maxDelta = 0.0

        # loop through grid for each location
        for row in range(0, gridSize):
            for col in range(0, gridSize):
                # if loc coincides with the finishing location
                if (col, row) == car.finishLoc:
                    tempGrid[col][row] = 99.0
                    continue

                # recursively find the maximum expected utility at that location by iteration
                maxExpUtil = getMaxExpUtil(col, row, utilGrid, gridSize)

                # get the reward based on current location, car location and obstacle
                bonus = getBonusUtil((col, row), car, obs)

                # update the utility with a discounted multiplier 0.9 for future move
                updatedUtil = bonus + 0.9 * maxExpUtil
                tempGrid[col][row] = updatedUtil

                # calculate current difference from new updated result and old result to check for convergence
                currentDelta = abs(updatedUtil - utilGrid[col][row])
                if currentDelta > maxDelta:
                    maxDelta = currentDelta

        # for row in range(0, gridSize):
        #     for col in range(0, gridSize):
        #         print(str(utilGrid[col][row]), end="   ")
        #     print("\n")

        # check for convergence again:
        if maxDelta < 0.1:
            break


        # after convergence, update the final utility grid
        utilGrid = tempGrid

    # print the final converged utility grid
    # print("Final converged utility grid:")
    # for row in range(0, gridSize):
    #     for col in range(0, gridSize):
    #         print(str(utilGrid[col][row]), end="   ")
    #     print("\n")

    return utilGrid

""" Function to get maximum expected utility based on all options presented: 4 directions"""
def getMaxExpUtil(col, row, utilGrid, gridSize):
    # north utility
    nUtil, sUtil, eUtil, wUtil = calculateUtil(col, row, utilGrid, gridSize)

    # choice of the next move is P(move)*Util(move)
    nExpUtil = 0.7 * nUtil + 0.1 * wUtil + 0.1 * eUtil + 0.1 * sUtil
    sExpUtil = 0.1 * nUtil + 0.1 * wUtil + 0.1 * eUtil + 0.7 * sUtil
    eExpUtil = 0.1 * nUtil + 0.1 * wUtil + 0.7 * eUtil + 0.1 * sUtil
    wExpUtil = 0.1 * nUtil + 0.7 * wUtil + 0.1 * eUtil + 0.1 * sUtil

    return max([nExpUtil, eExpUtil, sExpUtil, wExpUtil])

""" Function to determine possible bonuses/penalties to finish/run into obstacles"""
def getBonusUtil(loc, car, obs):
    # if location is obstacle
    if loc in obs:
        return -101.0
    # if location is finishing point
    elif loc == car.finishLoc:
        return 99.0
    else: # just gas money
        return -1.0

# Function to calculate utility if moving in either of 4 directions given a utility grid
def calculateUtil(col, row, utilGrid, gridSize):
    # check if north of that location is valid
    if isValidLocation((col, row - 1), gridSize):
        nUtil = utilGrid[col][row - 1]
    else:
        nUtil = utilGrid[col][row]

    # check if north of that location is valid
    if isValidLocation((col, row + 1), gridSize):
        sUtil = utilGrid[col][row + 1]
    else:
        sUtil = utilGrid[col][row]

    # check if north of that location is valid
    if isValidLocation((col+1, row), gridSize):
        eUtil = utilGrid[col+1][row]
    else:
        eUtil = utilGrid[col][row]

    # check if north of that location is valid
    if isValidLocation((col-1, row), gridSize):
        wUtil = utilGrid[col-1][row]
    else:
        wUtil = utilGrid[col][row]

    return nUtil, sUtil, eUtil, wUtil

"""MAIN"""
if __name__ == "__main__":
    # measure time:
    start_time = time.time()

    """ PROVIDE INPUT """
    # import input.txt file to read
    fileIn = open("input.txt", "r")

    # Extract needed information
    gridSize, numCar, numObs, obs, allCars = readFiles(fileIn)

    width = gridSize
    height = gridSize

    # initiate answers of average money earned by each car:
    avgMoneyAllCars = []
    for idx in range(0, numCar):
        car = allCars[idx]
        # call function to calculate average money each car earn
        avgMoneyEachCar = getAvgMoney(car, gridSize, obs)
        # print("Car number "+ str(idx) + " earned $" + str(avgMoneyEachCar)+ " on average" )
        avgMoneyAllCars.append(avgMoneyEachCar)

    """ ALGORITHM TO DECIDE THE NEXT BEST MOVE:
    A STAR SEARCH WITH MANHATTAN DISTANCE AS HEURISTIC """
    # create a A-Star graph object
    # graph = AStarGraph(width, height)
    # graph.barriers.append(obs)

    # GIVEN SAMPLE CODE TO DETERMINE CAR TURN IN A SIMULATION
    # for i in range(numCar):
    #     car = allCars[i]
    #     start = car.getStart()
    #     end = car.getFinish()
    #     path = AStarSearch(start, end, graph)
    #
    #     # Print result
    #     print("final route", path)
    #
    #     # Plot result as cross plt
    #     plt.plot([v[0] for v in path], [v[1] for v in path])
    #     for barrier in graph.barriers:
    #         plt.plot([v[0] for v in barrier], [v[1] for v in barrier], 'ro', alpha=0.1)
    #     plt.xlim(-1, width + 1)
    #     plt.ylim(height + 1, -1)
    #
    # print("money earned", avgMoneyAllCars)

    # Close the file
    fileIn.close()

    # WRITTING OUTPUT FILE ###
    fileOut = open("output.txt", "w")
    idx = 0
    for avgMoneyEachCar in avgMoneyAllCars:
        # print("Car number " + str(idx) + " earned $" + str(avgMoneyEachCar) + " on average")
        idx += 1
        fileOut.write("%s\n" % avgMoneyEachCar)

    # Close the file
    fileOut.close()

    # Plotting:
    # plt.show()

    # measure time:
    end_time = time.time()
    print("Lapsed time in seconds: ", end_time-start_time)

    #check precision parameters
    # print(np.finfo(float))