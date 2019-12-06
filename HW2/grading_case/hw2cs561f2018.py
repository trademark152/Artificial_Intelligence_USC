# Minh Tran
# CSCI 561 Fall 2018
# Assignment 2
# tranmt@usc.edu
# Description: Sleeping accommodation for homeless people

import time


""" Ideas:
1) 3 classes: SPLA, HSA and App will be created to represent the filled calendars of
SPLA, LAHSA and all applicants.
2) Maintain two lists of hsaChosen and splaChosen to store the id list of all applicants
that have been chosen
3) Create a game that spla and hsa choose by turn, each trying to maximize its own efficiency
"""

"""Function to read input file
   Output numBed, numPark, numApp..."""
def readFiles(fileIn):
    # read all lines
    lines = fileIn.readlines()

    # Extract data in specific lines
    # First line: positive integer b: number of bed in the shelter
    numBed = int(lines[0])
    print("The number of beds in the shelter is " + str(numBed))

    # Second line: positive integer p: number of spaces in parking lot
    numPark = int(lines[1])
    print("The number of spaces in parking lot is " + str(numPark))

    # Third line: positive integer L: number of applicants chosen by LAHSA so far:
    numHsaChosen = int(lines[2])
    print("The number of applicants already chosen by LAHSA is " + str(numHsaChosen))

    # Extract the next L lines: L number of applicant ID (5 digits)
    hsaChosen = set()
    remLines1 = lines[3:3+numHsaChosen]
    print("All ID of applicants chosen by LAHSA are: "),
    for line in remLines1:
        line = line.strip()
        hsaChosen.add(line)
    print(hsaChosen)

    # Next line: positive integer S: number of applicants chosen by SPLA so far:
    numSplaChosen = int(lines[3+numHsaChosen])
    print("The number of applicants already chosen by SPLA is " + str(numSplaChosen))

    # Extract the next S lines: S number of applicant ID for SPLA (5 digits)
    splaChosen = set()
    remLines2 = lines[3+numHsaChosen+1: 3+numHsaChosen+1+numSplaChosen]
    print("All ID of applicants chosen by SPLA are: "),
    for line in remLines2:
        line = line.strip()
        splaChosen.add(line)
        # print(line),
    print(splaChosen)

    # Next line: positive integer A: total number of applicants:
    numTotalApp = int(lines[3 + numHsaChosen + 1 + numSplaChosen])
    print("The total number of applicants is " + str(numTotalApp))

    # Extract the next A lines: list of A applicant information (full digits)
    appStrings = []
    remLines3 = lines[3 + numHsaChosen + 1 + numSplaChosen+1:]
    # print("All applicants's information are: ")
    for line in remLines3:
        line = line.strip()
        # create an empty dictionary for each applicant
        appStrings.append(line)
        # within each series, first 5 digits is ID:
        # print(line)

    return numBed, numPark, numHsaChosen, hsaChosen, numSplaChosen, splaChosen, numTotalApp, appStrings


"""This class represent each applicant with all provided attributes as well as the need days schedule
Each applicant has function to see if he/she qualifies for any program
"""
class App:
    # constructor: set all attributes available to each applicant
    def __init__(self, ID, gender, age, hasPet, hasMed, hasCar, hasLicense, needDaysSchedule):
        self.ID = ID
        self.gender = gender
        self.age = age
        self.hasPet = hasPet
        self.hasMed = hasMed
        self.hasCar = hasCar
        self.hasLicense = hasLicense

        # initialize needDays attribute
        self.needDays = []
        # set needDays:
        self.setNeedDays(needDaysSchedule)

        # define an attribute to see which program/basket this applicant is at
        # 4 available choices: spla or hsa
        self.programs = []
        self.setPrograms()

    # specify which days this applicant need shelter
    def setNeedDays(self, needDaysSchedule):
        if int(needDaysSchedule[0]) == 1:
            self.needDays.append("mon")
        if int(needDaysSchedule[1]) == 1:
            self.needDays.append("tue")
        if int(needDaysSchedule[2]) == 1:
            self.needDays.append("wed")
        if int(needDaysSchedule[3]) == 1:
            self.needDays.append("thu")
        if int(needDaysSchedule[4]) == 1:
            self.needDays.append("fri")
        if int(needDaysSchedule[5]) == 1:
            self.needDays.append("sat")
        if int(needDaysSchedule[6]) == 1:
            self.needDays.append("sun")

    # See which program this applicant qualifies
    def setPrograms(self):
        # initialize by adding None
        self.programs.append("None")
        # check attribute of each applicant to prove qualification
        # SPLA: has car and license without medical condition
        if self.hasCar == "Y" and self.hasLicense == "Y" and self.hasMed == "N":
            self.programs.append("spla")
        # HSA: female over 17 years old without pet
        if self.gender == "F" and self.age > 17 and self.hasPet == "N":
            self.programs.append("hsa")

    # print applicant ID
    def __repr__(self):
        return self.ID

"""This class represents schedule of SPLA. It has the following attributes:
numPark: number of available park spaces for each day
parkedSpaces: number of occupied space for each day
score: represent number of occupied spot in this schedule ~ efficiency
possibleApp: set of possible applicants to choose from
"""
class SPLA:
    def __init__(self, numPark):
        self.numPark = numPark
        # initialize a dict with 0 values
        self.parkedSpaces = {"mon": 0, "tue": 0, "wed": 0, "thu": 0, "fri": 0, "sat": 0, "sun": 0}
        self.score = 0
        self.possibleApp = set()

    # function to check if an applicant can fit in the current schedule
    def canFit(self, app):
        # check for each day in applicant's needDays to see if the schedule is full that day (exceeding capacity)
        for needDay in app.needDays:
            if self.parkedSpaces[needDay] >= self.numPark:
                return False
        return True

    # function to get the capacity of spla
    def getNumPark(self):
        return self.numPark

    # function to add an applicant to this schedule (ONLY WHEN canFit = true)
    def addApp(self, app):
        for needDay in app.needDays:
            # update the schedule
            self.parkedSpaces[needDay] += 1
            # add corresponding score to update efficiency
            self.score += 1

    # function to remove an applicant out of this schedule
    def deleteApp(self, app):
        for needDay in app.needDays:
            # update the schedule
            self.parkedSpaces[needDay] -= 1
            # add corresponding score to update efficiency
            self.score -= 1

"""This class represents schedule of HSA. It has the following attributes:
numPark: number of available bed spaces for each day
bedSpaces: number of occupied space for each day
score: represent number of occupied spot in this schedule ~ efficiency
possibleApp: set of possible applicants to choose from
"""
class HSA:
    def __init__(self, numBed):
        self.numBed = numBed
        # initialize a dict with 0 values
        self.bedSpaces = {"mon": 0, "tue": 0, "wed": 0, "thu": 0, "fri": 0, "sat": 0, "sun": 0}
        self.score = 0
        self.possibleApp = set()

    # function to check if an applicant can fit in the current schedule
    def canFit(self, app):
        # check for each day in applicant's needDays to see if the schedule is full that day (exceeding capacity)
        for needDay in app.needDays:
            if self.bedSpaces[needDay] >= self.numBed:
                return False
        return True

    # function to get the capacity of spla
    def getNumBed(self):
        return self.numBed

    # function to add an applicant to this schedule (ONLY WHEN canFit = true)
    def addApp(self, app):
        for needDay in app.needDays:
            # update the schedule
            self.bedSpaces[needDay] += 1
            # add corresponding score to update efficiency
            self.score += 1

    # function to remove an applicant out of this schedule
    def deleteApp(self, app):
        for needDay in app.needDays:
            # update the schedule
            self.bedSpaces[needDay] -= 1
            # add corresponding score to update efficiency
            self.score -= 1

# Function to create a new applicant and place it into appropriate categories
# 4 available categories: chosenHsa/chosenSpla or possibleApp of Hsa/Spla
def createApp(splaChosen, spla, hsaChosen, hsa, appString):
    # Get input from appString
    ID = appString[0:5]
    gender = appString[5]
    age = int(appString[6:9])
    hasPet = appString[9]
    hasMed = appString[10]
    hasCar = appString[11]
    hasLicense = appString[12]
    needDaysSchedule = appString[13:]

    # Create an applicant based on the given attribute
    app = App(ID, gender, age, hasPet, hasMed, hasCar, hasLicense, needDaysSchedule)

    # if the applicant has been chosen, add them to the correct program.
    if app.ID in splaChosen:
        spla.addApp(app)
        return app
    elif app.ID in hsaChosen:
        hsa.addApp(app)
        return app

    # if the applicant has not been chosen but they are potential candidates for any program
    # add them to the correct program.
    if "spla" in app.programs:
        spla.possibleApp.add(app)
    if "hsa" in app.programs:
        hsa.possibleApp.add(app)
    return app


# Choose the next best hsa candidate out of possible pool of HSA to maximize HSA efficiency
def getNextAppHsa(spla, hsa):
    # initialize maxScore and bestApp
    maxScore = -1
    bestApp = None

    # loop through all possible applicants in the possible pool of hsa
    # make a copy to avoid tampering original possible pool
    for app in hsa.possibleApp.copy():
        # remove this applicant from hsa
        hsa.possibleApp.remove(app)

        # create boolean statement to keep track if this app is added/removed from schedule
        deletedFromSpla = False
        addedToHsa = False

        # check if hsa can fit this applicant in its schedule
        if hsa.canFit(app):
            # add to hsa
            hsa.addApp(app)
            # update Boolean
            addedToHsa = True

            # check if that applicant in the possible pool of spla
            if app in spla.possibleApp:
                # remove that applicant from the pool
                spla.possibleApp.remove(app)
                # update Boolean
                deletedFromSpla = True

        # Run algorithm to maximize spla score in the following turns with updated schedules
        splaScore, hsaScore = splaMAX(spla, hsa)

        # choose the best score for hsa or break ties by smaller applicant id
        if (hsaScore > maxScore or(hsaScore == maxScore and app.ID < bestApp.ID)):
            maxScore = hsaScore
            bestApp = app

        # revert the changes of schedules to test other applicants before loop close
        # add this applicant from hsa
        hsa.possibleApp.add(app)

        # check tracked Boolean to see if the following actions need to be reverted
        if addedToHsa:
            hsa.deleteApp(app)
        if deletedFromSpla:
            spla.possibleApp.add(app)

    return bestApp

# Choose the next best hsa candidate out of possible pool of SPLA to maximize SPLA efficiency
def getNextAppSpla(spla, hsa):
    # initialize maxScore and bestApp
    maxScore = -1
    bestApp = None

    # loop through all possible applicants in the possible pool of spla
    # make a copy to avoid tampering original possible pool
    for app in spla.possibleApp.copy():
        # remove this applicant from hsa
        spla.possibleApp.remove(app)

        # create boolean statement to keep track if this app is added/removed from schedule
        deletedFromHsa = False
        addedToSpla = False

        # check if hsa can fit this applicant in its schedule
        if spla.canFit(app):
            # add to spla
            spla.addApp(app)
            # update Boolean
            addedToSpla = True

            # check if that applicant in the possible pool of spla
            if app in hsa.possibleApp:
                # remove that applicant from the pool
                hsa.possibleApp.remove(app)
                # update Boolean
                deletedFromHsa = True

        # Run algorithm to maximize hsa score in the following turns with updated schedules
        splaScore, hsaScore = hsaMAX(spla, hsa)

        # choose the best score for spla or break ties by smaller applicant id
        if (splaScore > maxScore or(splaScore == maxScore and app.ID < bestApp.ID)):
            maxScore = splaScore
            bestApp = app

        # revert the changes of schedules to test other applicants before loop close
        # add this applicant from hsa
        spla.possibleApp.add(app)

        # check tracked Boolean to see if the following actions need to be reverted
        if addedToSpla:
            spla.deleteApp(app)
        if deletedFromHsa:
            hsa.possibleApp.add(app)

    return bestApp

# This function attempts to play it out from SPLA player's perspective
def splaMAX(spla, hsa):
    # if both possible applicant pools are empty:
    if len(spla.possibleApp) == 0 and len(hsa.possibleApp) == 0:
        return spla.score, hsa.score
    # if spla pool is empty, play it out from HSA player's perspective
    elif len(spla.possibleApp) == 0:
        return hsaMAX(spla, hsa)

    # initialize best score of spla and corresponding score of hsa
    bestSplaScore = -1
    currentHsaScore = -1

    # loop through all applicants in spla pool
    for app in spla.possibleApp.copy():
        # remove that applicant from pool
        spla.possibleApp.remove(app)

        # create boolean statement to keep track if this app is added/removed from schedule
        deletedFromHsa = False
        addedToSpla = False

        # Check to see if spla schedule can fit this applicant
        if spla.canFit(app):
            spla.addApp(app)
            addedToSpla = True

            # remove this applicant if it is in hsa pool
            if app in hsa.possibleApp:
                hsa.possibleApp.remove(app)
                deletedFromHsa = True

        # recursively play from hsa side with updated schedules
        splaScore, hsaScore = hsaMAX(spla, hsa)

        # update if the achieved score is better
        if splaScore > bestSplaScore:
            bestSplaScore = splaScore
            currentHsaScore = hsaScore

        # revert the changes
        spla.possibleApp.add(app)
        if addedToSpla:
            spla.deleteApp(app)
        if deletedFromHsa:
            hsa.possibleApp.add(app)
    return bestSplaScore, currentHsaScore

# This function attempts to play it out from hsa player's perspective
def hsaMAX(spla, hsa):
    # if both possible applicant pools are empty:
    if len(spla.possibleApp) == 0 and len(hsa.possibleApp) == 0:
        return spla.score, hsa.score
    # if spla pool is empty, play it out from SPLA player's perspective
    elif len(hsa.possibleApp) == 0:
        return splaMAX(spla, hsa)

    # initialize best score of spla and corresponding score of hsa
    bestHsaScore = -1
    currentSplaScore = -1

    # loop through all applicants in hsa pool
    for app in hsa.possibleApp.copy():
        # remove that applicant from pool
        hsa.possibleApp.remove(app)

        # create boolean statement to keep track if this app is added/removed from schedule
        deletedFromSpla = False
        addedToHsa = False

        # Check to see if hsa schedule can fit this applicant
        if hsa.canFit(app):
            hsa.addApp(app)
            addedToHsa = True

            # remove this applicant if it is in spla pool
            if app in spla.possibleApp:
                spla.possibleApp.remove(app)
                deletedFromSpla = True

        # recursively play from spla side with updated schedules
        splaScore, hsaScore = splaMAX(spla, hsa)

        # update if the achieved score is better
        if hsaScore > bestHsaScore:
            bestHsaScore = hsaScore
            currentSplaScore = splaScore

        # revert the changes
        hsa.possibleApp.add(app)
        if addedToHsa:
            hsa.deleteApp(app)
        if deletedFromSpla:
            spla.possibleApp.add(app)
    return currentSplaScore, bestHsaScore

"""MAIN"""
# methods
# function to find the next optimal SPLA applicant to choose from

def main():
    start = time.time()
    # import input.txt file to read
    fileIn = open("input22.txt", "r")
    numBed, numPark, numHsaChosen, hsaChosen, numSplaChosen, splaChosen, numTotalApp, appStrings = readFiles(fileIn)

    # create programs
    spla = SPLA(numPark)
    hsa = HSA(numBed)

    # create applicants with proper categories
    apps = []
    for iter in range(0, numTotalApp):
        apps.append(createApp(splaChosen, spla, hsaChosen, hsa, appStrings[iter]))
        # print appStrings[iter]
    print
    print("All applicants's information are: ")
    for app in apps:
        print(app.ID, app.needDays,app.programs)

    # perform minimax algorithm
    nextApp = getNextAppSpla(spla, hsa)

    # Close the file
    fileIn.close()

    # WRITTING OUTPUT FILE ###
    fileOut = open("output.txt", "w")

    # fileOut.write('hello' + "\n")
    print(nextApp)
    fileOut.write(nextApp.ID + "\n")
    # Close the file
    fileOut.close()
    end = time.time()
    print(end - start)

# methods
# function to find the next optimal SPLA applicant to choose from

main()

