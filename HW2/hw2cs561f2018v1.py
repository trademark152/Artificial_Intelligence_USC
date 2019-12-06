# Minh Tran
# CSCI 561 Fall 2018
# Assignment 2
# tranmt@usc.edu
# Description: Sleeping accommodation for homeless people

# Define global constants
infinity = 1.0e10
import numpy as np

# CLASSES
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

# PROBLEM-SPECIFIC FUNCTIONS
"""Function to read input file
   Output numBed, numPark, numApp..."""
def readFiles(fileIn):
    ### READING INPUT FILE ###
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
    numAppHsa = int(lines[2])
    print("The number of applicants already chosen by LAHSA is " + str(numAppHsa))

    # Extract the next L lines: L number of applicant ID (5 digits)
    listAppIDHsa = []
    remLines1 = lines[3:3+numAppHsa]
    # print("All ID of applicants chosen by LAHSA are: "),
    for line in remLines1:
        line = line.strip()
        listAppIDHsa.append(line)
        # print(line),

    # Next line: positive integer S: number of applicants chosen by SPLA so far:
    numAppSpla = int(lines[3+numAppHsa])
    print("The number of applicants already chosen by SPLA is " + str(numAppSpla))

    # Extract the next S lines: S number of applicant ID for SPLA (5 digits)
    listAppIDSpla = []
    remLines2 = lines[3+numAppHsa+1: 3+numAppHsa+1+numAppSpla]
    # print("All ID of applicants chosen by SPLA are: "),
    for line in remLines2:
        line = line.strip()
        listAppIDSpla.append(line)
        # print(line),
    print

    # Next line: positive integer A: total number of applicants:
    numAppTotal = str(lines[3 + numAppHsa + 1 + numAppSpla])
    print("The total number of applicants is " + (numAppTotal))

    # Extract the next A lines: list of A applicant information (full digits)
    listAppTotal = []
    remLines3 = lines[3 + numAppHsa + 1 + numAppSpla+1:]
    print("All applicants's information are: ")
    for line in remLines3:
        line = line.strip()
        # create an empty dictionary for each applicant
        info = {}
        # within each series, first 5 digits is ID:
        id = line[0:5]
        info["ID"] = id

        gender = line[5]
        info["gender"] = gender

        age = int(line[6:9])
        info["age"] = age

        hasPet = line[9]
        info["hasPet"] = hasPet

        hasMed = line[10]
        info["hasMed"] = hasMed

        hasCar = line[11]
        info["hasCar"] = hasCar

        hasLicense = line[12]
        info["hasLicense"] = hasLicense

        # needDay
        needDay = []
        if int(line[13])==1:
            needDay.append("Mon")
        if int(line[14])==1:
            needDay.append("Tue")
        if int(line[15])==1:
            needDay.append("Wed")
        if int(line[16])==1:
            needDay.append("Thu")
        if int(line[17])==1:
            needDay.append("Fri")
        if int(line[18])==1:
            needDay.append("Sat")
        if int(line[19])==1:
            needDay.append("Sun")
        info["needDays"] = needDay

        # add each applicant to a list
        listAppTotal.append(info)

        print(info)

    # Extract the next A lines: list of A applicant information (full digits) and save as list of dicts

    return numBed, numPark, numAppHsa, listAppIDHsa, numAppSpla, listAppIDSpla, numAppTotal, listAppTotal

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

# This func intends to generate a layer with corresponding score value and successors
# Input is game, state (where u want to create a new layer) and current pool of applicants
def create_layer(g, state, pool, depth, splaCalendar, hsaCalendar):
    # initialize list of possible successor states
    # g.succs[state] = []
    for i in range(len(pool)):
        # specify applicants
        app = pool[i]

        # Add all successors ('ID', node name) to the current state
        g.add_succs(state, app.get('ID'), str(state).upper() + str(i))

        # add score to each successor state
        if depth % 2 == 1:
            # calculate utility function for each successor state
            score = calUtility(splaCalendar, app)
            g.add_utils(str(state).upper() + str(i), sum(hsaCalendar.values()) - score)
        else:
            # calculate utility function for each successor state
            score = calUtility(hsaCalendar, app)
            g.add_utils(str(state).upper() + str(i), score - sum(splaCalendar.values()))
    return g

# Function to create the full search tree start at state
def recursiveSolver(g, state, pool, depth, splaCalendar, hsaCalendar):
    while depth < 3:
        depth += 1
        for state in g.successors(state):
            # Specify which calendar to place applicant
            if depth % 2 == 1:
                splaCalendar = updateCalendar(splaCalendar, findDictInList(init_pool, 'ID', state[0]))
                hsaCalendar = hsaCalendar
            else:
                hsaCalendar = updateCalendar(hsaCalendar, findDictInList(init_pool, 'ID', state[0]))
                splaCalendar = splaCalendar

            # remove placed applicant out of the pool
            newPool = removeDictinList(init_pool, 'ID', state[0])

            g = create_layer(g, state[1], newPool, depth, splaCalendar, hsaCalendar)
    return g

"""MAIN"""
def main():
    # import input.txt file to read
    fileIn = open("input1.txt", "r")
    numBed, numPark, numAppHsa, listAppIDHsa, numAppSpla, listAppIDSpla, numAppTotal, listAppTotal = readFiles(fileIn)

    # Create a free calendar of each org initially
    print("Initial calendars:")
    hsaCalendar = createCalendar(numBed)
    splaCalendar = createCalendar(numPark)
    print("HSA: ", hsaCalendar)
    print("SPLA: ", splaCalendar)

    # Create pool of all qualified applicants
    hsaPool, splaPool, sharedPool = createPool(listAppTotal)

    print
    print("IDs of applicants qualified for both LAHSA and SPLA are: "),
    printID(sharedPool)

    print
    print("IDs of applicants qualified for only LAHSA are: "),
    printID(hsaPool)

    print
    print("IDs of applicants qualified for only SPLA are: "),
    printID(splaPool)

    print
    # REMOVE CHOSEN APPLICANTS OUT OF SELECTION POOL
    if listAppIDSpla:
        for id in listAppIDSpla:
            removeApp(sharedPool, id)
            removeApp(splaPool, id)
            app = findDictInList(listAppTotal, 'ID', id)

            # Update calendar of available remaining spaces:
            splaCalendar, oldsplaCal = updateCalendar(splaCalendar, app)

    if listAppIDHsa:
        for id in listAppIDHsa:
            removeApp(sharedPool, id)
            removeApp(hsaPool, id)
            # find applicant with that id
            app = findDictInList(listAppTotal, 'ID', id)

            # Update calendar of available remaining spaces:
            hsaCalendar, oldhsaCal = updateCalendar(hsaCalendar, app)

    # Print updated calendars after initial selections
    print
    print("Starting state of 2 calendars: ")
    print("HSA: ", sum(hsaCalendar.values()))
    print("SPLA: ", sum(splaCalendar.values()))


    # PRiNT all available applicant for selection
    print
    print("IDs of AVAILABLE applicants qualified for both LAHSA and SPLA are: "),
    printID(sharedPool)

    print
    print("IDs of AVAILABLE applicants qualified for only LAHSA are: "),
    printID(hsaPool)

    print
    print("IDs of AVAILABLE applicants qualified for only SPLA are: "),
    printID(splaPool)

    """Create a housing game"""
    init_state = 'A'
    g = housingGame({init_state: []}, {init_state: eval_fn(hsaCalendar, splaCalendar)}, init_state)
    print
    print(g.succs)
    print(g.utils)

    # g.add_succs('A', '00002', 'A0')
    # g.add_utils('A', 1)
    # print
    # print(g.succs)
    # print(g.utils)
    #
    # g.add_succs('A', '00003', 'A1')
    # g.add_utils('A0', 2)
    # g.add_utils('A1', 5)
    # print
    # print(g.succs)
    # print(g.utils)

    # Create initial layer
    depth = 1
    g = create_layer(g, init_state, sharedPool, depth, splaCalendar, hsaCalendar)
    print
    print(g.succs)
    print(g.utils)


    # g = recursiveSolver(g, init_state, sharedPool, depth, splaCalendar, hsaCalendar)

    # Create 2nd layer
    for state in g.successors(init_state):
        print
        print state
        #Specify which calendar to place applicant
        if depth % 2 == 1:
            splaCalendar, oldsplaCal = updateCalendar(splaCalendar, findDictInList(sharedPool, 'ID', state[0]))
        else:
            hsaCalendar, oldhsaCal = updateCalendar(hsaCalendar, findDictInList(sharedPool, 'ID', state[0]))
        print("1st step state of 2 calendars: ")
        print("HSA: ", sum(hsaCalendar.values()))
        print("SPLA: ", sum(splaCalendar.values()))

        # remove placed applicant out of the pool
        newPool = removeDictinList(sharedPool, 'ID', state[0])
        printID(newPool)
        depth += 1
        print(g.succs)
        g = create_layer(g, state[1], newPool, depth, splaCalendar, hsaCalendar)
        print
        print(g.succs)
        print(g.utils)

        if depth % 2 == 0:
            splaCalendar = oldsplaCal
        else:
            hsaCalendar = oldhsaCal

    # print
    # while depth < 3:
    #     depth += 1
    #     for state in g.successors(init_state):
    #         # Specify which calendar to place applicant
    #         if depth % 2 == 1:
    #             splaCalendar = updateCalendar(splaCalendar, findDictInList(sharedPool, 'ID', state[0]))
    #             hsaCalendar = hsaCalendar
    #         else:
    #             hsaCalendar = updateCalendar(hsaCalendar, findDictInList(sharedPool, 'ID', state[0]))
    #             splaCalendar = splaCalendar
    #
    #         # remove placed applicant out of the pool
    #         newPool = removeDictinList(sharedPool, 'ID', state[0])
    #
    #         # print
    #         # printID(newPool)
    #
    #         g = create_layer(g, state[1], newPool, depth, splaCalendar, hsaCalendar)

    # g = recursiveSolver(g, state, sharedPool, depth, splaCalendar, hsaCalendar)

    # print
    # print(depth)
    # print(g.succs)
    # print(g.utils)


    # action, state = alphabeta_search('A', g)
    # print(action, state)


    # print g.succs
    # print g.utils

    # Test the functions
    # print g.display(state)
    # print ("Player to move is", g.to_move(state))
    # print g.utility(state,'MIN')
    # print ("Is current state terminal", g.terminal_test(state))

    # depth = 0
    # while depth < 4:
    #     action, state = alphabeta_search(state, g)
    #     print(action, state)
    #     depth += 1



    # Close the file
    fileIn.close()

    # WRITTING OUTPUT FILE ###
    fileOut = open("output.txt", "w")
    # fileOut.write(selectApp["ID"])
    fileOut.write('hello')
    # Close the file
    fileOut.close()

main()