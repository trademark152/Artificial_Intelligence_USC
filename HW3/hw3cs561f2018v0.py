# Minh Tran
# CSCI 561 Fall 2018
# Assignment 2
# tranmt@usc.edu
# Description: Sleeping accommodation for homeless people

""" Ideas:
"""


"""Function to read input file
   Output numBed, numPark, numApp..."""
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
    obs = []
    for iter in range(0, numObs):
        line = lines[count].strip()
        line = line.split(',')
        obs.append((int(line[0]), int(line[1])))
        # locObs.append(lines[count])
        count += 1
    print("The position of all obstacles are ", obs)

    # Car starting position
    carsStart = []
    for iter in range(0, numCar):
        line = lines[count].strip()
        line = line.split(',')
        carsStart.append((int(line[0]), int(line[1])))
        # locObs.append(lines[count])
        count += 1
    print("The starting position of all cars are ", carsStart)

    # Car starting position
    carsFinish = []
    for iter in range(0, numCar):
        line = lines[count].strip()
        line = line.split(',')
        carsFinish.append((int(line[0]), int(line[1])))
        # locObs.append(lines[count])
        count += 1
    print("The finishing position of all cars are ", carsFinish)

    return gridSize, numCar, numObs , obs, carsStart, carsFinish

def main():
    # import input.txt file to read
    fileIn = open("input0.txt", "r")
    gridSize, numCar, numObs, obs, carsStart, carsFinish= readFiles(fileIn)

    # GIVEN SAMPLE CODE TO DETERMINE CAR TURN IN A SIMULATION
    # for i in range(len(cars)):
    #     for j in range(10):
    #         pos = cars[i]
    # np.random.seed(j)
    # swerve = np.random.random_sample(1000000)
    # k = 0
    # while pos != ends[i]:
    #     move = policies[i][pos]
    # if swerve[k] > 0.7:
    #     if swerve[k] > 0.8:
    #         if swerve[k] > 0.9:
    #         move = turn_left(turn_left(move))
    # else:
    #     move = turn_left(move)
    # else:
    # move = turn_right(move)


    # Close the file
    fileIn.close()

    # WRITTING OUTPUT FILE ###
    fileOut = open("output.txt", "w")

    # fileOut.write('hello' + "\n")
    fileOut.write("\n")
    # Close the file
    fileOut.close()

# methods
# function to find the next optimal SPLA applicant to choose from

main()