""" Adversarial search credit to AIMA repository code"""
# Define global constants
infinity = 1.0e10

# Dictionary
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

    player = game.to_move(state)

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

    # Body of alphabeta_search starts here:
    # The default test cuts off at depth d or at a terminal state
    cutoff_test = (cutoff_test or
                   (lambda state, depth: depth > d or game.terminal_test(state)))
    eval_fn = eval_fn or (lambda state: game.utility(state, player))
    action, state = argmax(game.successors(state),
                           lambda ((a, s)): min_value(s, -infinity, infinity, 0))
    return action, state

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

    # def to_move(self, state):
    #     "Return the player whose move it is in this state."
    #     return state.to_move

    def display(self, state):
        "Print or otherwise display the state."
        print state

    def successors(self, state):
        "Return a list of legal (move, state) pairs."
        return [(move, self.make_move(move, state)) for move in self.legal_moves(state)]

    # def __repr__(self):
    #     return '<%s>' % self.__class__.__name__

class Fig62Game(Game):
    """The game represented in [Fig. 6.2]. Serves as a simple test case"""
    # succs = {'A': [('a1', 'B'), ('a2', 'C'), ('a3', 'D')],
    #          'B': [('b1', 'B1'), ('b2', 'B2'), ('b3', 'B3')],
    #          'C': [('c1', 'C1'), ('c2', 'C2'), ('c3', 'C3')],
    #          'D': [('d1', 'D1'), ('d2', 'D2'), ('d3', 'D3')]}
    # utils = Dict(B1=3, B2=12, B3=8, C1=2, C2=4, C3=6, D1=14, D2=5, D3=2)

    succs = {'A': [('a1', 'A1'), ('a2', 'A2')],
              'A1': [('b1', 'B1'), ('b2', 'B2')],
              'A2': [('b3', 'B3'), ('b4', 'B4')],
              'B1': [('c1', 'C1'), ('c2', 'C2')],
              'B2': [('c3', 'C3'), ('c4', 'C4')],
              'B3': [('c5', 'C5'), ('c6', 'C6')],
              'B4': [('c7', 'C7'), ('c8', 'C8')],
              'C1': [('d1', 'D1'), ('d2', 'D2')],
              'C2': [('d3', 'D3'), ('d4', 'D4')],
              'C3': [('d5', 'D5'), ('d6', 'D6')],
              'C4': [('d7', 'D7'), ('d8', 'D8')],
              'C5': [('d9', 'D9'), ('d10', 'D10')],
              'C6': [('d11', 'D11'), ('d12', 'D12')],
              'C7': [('d13', 'D13'), ('d14', 'D14')],
              'C8': [('d15', 'D15'), ('d16', 'D16')]}

    utils = Dict(D1=10, D2=5, D3=7, D4=11, D5=12, D6=8, D7=9, D8=8,
                 D9=5, D10=12, D11=11, D12=12, D13=9, D14=8, D15=7, D16=10)

    # Define initial state
    initial = 'A'

    # Return a list of legal (move, state) pairs.
    def successors(self, state):
        return self.succs.get(state, [])

    # Return the value of this final state to player
    def utility(self, state, player):
        if player == 'MAX':
            # return corresponding utility value at that state
            return self.utils[state]
        else:
            return -self.utils[state]

    def terminal_test(self, state):
        # return state not in ('A', 'B', 'C', 'D')
        return state not in ('A','A1','A2','B1','B2','B3','B4',
                              'C1','C2','C3','C4','C5','C6','C7','C8')

    def to_move(self, state):
        return if_(state in 'A','MAX','MIN')

class housingGame(Game):

    succs1 = Dict(A1 = 4, A2 = 3, A3 = 6)
    print(succs1)

    utils = Dict(D1=10, D2=5, D3=7, D4=11, D5=12, D6=8, D7=9, D8=8,
                 D9=5, D10=12, D11=11, D12=12, D13=9, D14=8, D15=7, D16=10)

    # Define initial state
    initial = 'A'

    # Return a list of legal (move, state) pairs.
    def successors(self, state):
        return self.succs.get(state, [])

    # Return the value of this final state to player
    def utility(self, state, player):
        if player == 'MAX':
            # return corresponding utility value at that state
            return self.utils[state]
        else:
            return -self.utils[state]

    def terminal_test(self, state):
        # return state not in ('A', 'B', 'C', 'D')
        return state not in ('A','A1','A2','B1','B2','B3','B4',
                              'C1','C2','C3','C4','C5','C6','C7','C8')

    def to_move(self, state):
        return if_(state in 'A','MAX','MIN')

def main():
    g = Fig62Game()
    state = 'A'

    # Test the functions
    # print g.display(state)
    print ("Player to move is", g.to_move(state))
    # print g.utility(state,'MIN')
    print ("Is current state terminal", g.terminal_test(state))

    print(g.successors(state))

    depth = 0
    while depth < 4:
        action, state = alphabeta_search(state, g)
        print(action, state)
        depth += 1

main()