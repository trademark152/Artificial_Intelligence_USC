# Minh Tran
# CSCI 561 Fall 2018
# Assignment 2
# tranmt@usc.edu
# Description: Sleeping accommodation for homeless people

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

"""
Design a game with 2 players: SPLA (alpha) and HSA (beta), SPLA picks first
The initial state is 2 filtered calendars and initial eval_fn
The utility function is sum(beta) - sum(alpha)
The goal is to maximize utility value: meaning minimize sum(alpha) --> highest efficiency for SPLA
Process is to calculate all leaf nodes utility value then backtrack the highest util
"""

class Game:
    """A game has a utility for each state and a terminal test.
    To create a game, subclass this class and implement
    legal_moves, make_move, utility, and terminal_test."""

    def legal_moves(self, state):
        "Return a list of the allowable moves at this point."
        return state.keys()
        # abstract

    def make_move(self, move, state):
        "Return the state that results from making a move from a state."
        abstract

    def utility(self, state, player):
        "Return the value of this final state to player."
        abstract

    def terminal_test(self, state):
        "Return True if this is a final state for the game."
        # in other words, if there are no more legal move from this state
        return not self.legal_moves(state)

    def to_move(self, state):
        "Return the player whose move it is in this state."
        return state.to_move

    def display(self, state):
        "Print or otherwise display the state."
        print state

    def successors(self, state):
        "Return a list of legal (move, state) pairs."
        return [(move, self.make_move(move, state)) for move in self.legal_moves(state)]

    # def __repr__(self):
    #     return '<%s>' % self.__class__.__name__

succs = []
class housingGame(Game):
    # Constructor for the game: including initial state (default 'A'),
    # succs (including all parent: (action - successor) pairs
    # utils (including all corresponding utility score for each state
    # spla and hsa are two players
    def __init__(self, succs, utils, initial):
        self.initial = initial
        self.succs = succs
        self.utils = utils

    # add a pair of action-successor to a parent state
    def add_succs(self, state, action, successor):
        self.succs[state].append([action, successor])

    # assign a score to a state
    def add_utils(self, state, score):
        self.utils[state] = score

    # return all successors of a state
    def successors(self, state):
        return self.succs.get(state)

    # Return the value of this final state to player
    # def utility(self, state, player):
    #     if player == 'MAX':
    #         # return corresponding utility value at that state
    #         return self.utils[state]
    #     else:
    #         return -self.utils[state]

    def terminal_test(self, state):
        # return state not in ('A', 'B', 'C', 'D')
        return state not in ('A')

    # def to_move(self, state):
    #     return if_(state in 'A','MAX','MIN')

# GLOBAL FUNCTIONS
def Dict(**entries):
    """Create a dict out of the argument=value arguments.
    >>> Dict(a=1, b=2, c=3)
    {'a': 1, 'c': 3, 'b': 2}
    """
    return entries

def if_(test, result, alternative):
    """Both result and alternative are always evaluated. However, if
    either evaluates to a function, it is applied to the empty arglist,
    so you can delay execution by putting it in a lambda.
    >>> if_(2 + 2 == 4, 'ok', lambda: expensive_computation())
    'ok'
    """
    if test:
        if callable(result):
            return result()
        return result
    else:
        if callable(alternative):
            return alternative()
        return alternative

def argmin(seq, func):
    """Return an element with lowest func(seq[i]) score;
    tie goes to first one.
    >>> argmin(['one', 'to', 'three', 'be'], len)
    'to'
    """
    # initialize input and output
    best = seq[0]
    best_score = func(best)

    # loop through sequence
    for element in seq:
        element_score = func(element)
        # compare with initialized values
        if element_score < best_score:
            best, best_score = element, element_score
    return best

def argmax(seq, func):
    """Return an element with highest func(seq[i]) score; tie goes to first one"""
    # similar to argmin: when -func(x) is min the func(x) is max
    # using anonymous function lambda to evaluate func(x)
    return argmin(seq, lambda x: -func(x))

def alphabeta_search(state, game, d=4, cutoff_test=None, eval_fn=None):
    """Search game to determine best action; use alpha-beta pruning.
    This version cuts off search and uses an evaluation function."""
    # Denote which player's turn to move
    player = game.to_move(state)

    # Local function with alpha, beta and depth
    def max_value(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            return eval_fn(state)
        v = -infinity
        for (a, s) in game.successors(state):
            v = max(v, min_value(s, alpha, beta, depth + 1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            return eval_fn(state)
        v = infinity
        for (a, s) in game.successors(state):
            v = min(v, max_value(s, alpha, beta, depth + 1))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    # Alphabeta_search:
    # The default test cuts off at depth d or at a terminal state
    cutoff_test = (cutoff_test or
                   (lambda state, depth: depth > d or game.terminal_test(state)))

    # The evaluation function evaluate the game utility at each state for each player
    eval_fn = (eval_fn or
                    (lambda state: game.utility(state, player)))

    # Return the argmax
    action, state = argmax(game.successors(state),
                           lambda ((a, s)): min_value(s, -infinity, infinity, 0))
    return action, state

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

# This function takes in an applicant (as a dict) and check its qualification on Hsa and add them to applicant pool
# LAHSA can only accept women over 17 years old without pets
def isQualHsa(applicant):
    if applicant["age"] > 17 and applicant["gender"] == "F" and applicant["hasPet"] == "N":
        isQual1 = 1
    else:
        isQual1 = 0
    return isQual1

def isQualSpla(applicant):
    if applicant["hasCar"] =="Y" and applicant["hasLicense"] == "Y" and applicant["hasMed"] == "N":
        isQual2 = 1
    else:
        isQual2 = 0
    return isQual2

# Function to create pool of qualified applicant for LAHSA
def createPool(listAppTotal):
    hsaPool = []
    splaPool = []
    sharedPool = []
    for applicant in listAppTotal:
        isQual1 = isQualHsa(applicant)
        isQual2 = isQualSpla(applicant)
        if isQual1 == 1 and isQual2 == 0:
            hsaPool.append(applicant)
        if isQual1 == 0 and isQual2 == 1:
            splaPool.append(applicant)
        if isQual1 == 1 and isQual2 == 1:
            sharedPool.append(applicant)
    return hsaPool, splaPool, sharedPool

# Remove applicant from pool based on id that has been selected
def removeApp(pool, id):
    pool[:] = [d for d in pool if str(d.get('ID')) != id]

# Function to print IDs of applicants in the pool:
def printID(pool):
    for applicant in pool:
        print(applicant["ID"]),

# Function to create a calendar with number of free spaces (bed/park) for each org
def createCalendar(numSpace):
    calendar = {"Mon": numSpace, "Tue": numSpace,"Wed": numSpace,
                "Thu": numSpace, "Fri": numSpace,"Sat": numSpace, "Sun": numSpace}
    return calendar

# Function to reduce number of free spaces after a selection of an applicant
def updateCalendar(calendar, applicant):
    oldCal = calendar.copy()
    # For each day in applicant's request, reduce the corresponding numSpace by 1 in the calendar
    for day in applicant["needDays"]:
        calendar[day] -= 1
    return calendar, oldCal

# Function to calculate utility function when an applicant is selected
# utility is the number of remaining spaces AFTER an applicant is selected
def calUtility(calendar, applicant):
    cal = calendar.copy()
    # For each day in applicant's request, reduce the corresponding numSpace by 1 in the calendar
    for day in applicant["needDays"]:
        cal[day] -= 1
    score = sum(cal.values())
    return score

# Function to find a dict item in a list based on value
def findDictInList(list, key , value):
    for item in list:
        if item[key] == value:
            my_item = item
            break
    else:
        my_item = None
    return my_item

# Function to remove an item from a list of dicts based on value of a key
def removeDictinList(list, key, value):
    itemToRemove = findDictInList(list, key, value)
    newList = list[:]
    newList = [item for item in newList if item['ID']!=itemToRemove['ID']]
    return newList

# Function to calculate utility
def eval_fn(hsaCalendar, splaCalendar):
    score = sum(hsaCalendar.values())-sum(splaCalendar.values())
    return score

"""MAIN"""
# methods
# function to find the next optimal SPLA applicant to choose from

def main():
    # import input.txt file to read
    fileIn = open("input.txt", "r")
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

# methods
# function to find the next optimal SPLA applicant to choose from

main()