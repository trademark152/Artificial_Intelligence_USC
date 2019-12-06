# Minh Tran
# CSCI 561 Fall 2018
# Assignment 1
# tranmt@usc.edu
# Description: Vacuum Cleaner Agent

def main():

    ### READING INPUT FILE ###
    # Read input.txt file and import as a tuple of tuple
    locStatusList = [[] for _ in range(4)]
    #print(locStatusList)

    # import input.txt file to read
    fileIn = open("input.txt", "r")
    idx = 0

    # import line by line
    for line in fileIn:
        # Stripping unnecessary spaces encompassing each line
        line = line.strip()
        #print(line)

        # Splitting line into words and store each location and status as list
        locStats = line.split(',')
        for locStat in locStats:
            # Stripping unnecessary spaces inside each word inside each line
            locStat = locStat.strip()
            #print(locStat)
            locStatusList[idx].append(locStat)

        # update index to the next Location/Status
        idx += 1

    # QC output
    # print(locStatusList)

    # Close the file
    fileIn.close()

    ### WRITTING OUTPUT FILE ###
    # Specify to write on chosen userFileOut
    fileOut = open("output.txt", "w")
    for environment in locStatusList:
        if environment[1].lower() == "dirty":
            fileOut.write("Suck" + "\n")
        elif environment[0].lower() == "a":
            fileOut.write("Right" + "\n")
        elif environment[0].lower() == "b":
            fileOut.write("Left" + "\n")
        else:
            fileOut.write("Unspecified Environment" + "\n")

    # Close the file
    fileOut.close()

    ### READING OUTPUT FILE ###
    # Read output.txt file and print on screen
    file = open("output.txt", "r")

    # import line by line
    for action in file:
        # Stripping unnecessary spaces encompassing each line
        action = action.strip()
        print(action)

main()
