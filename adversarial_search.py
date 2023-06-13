
"""
Adversarial search algorithms implementation

Your task for homework 6 is to implement:
1.  minimax
2.  alphabeta
3.  abdl (alpha beta depth limited)
"""
import random
import math  # You can use math.inf to initialize to infinity


def rand(game_state):
    """
    Generate a random move.
    :param game_state: GameState object
    :return:  a tuple representing the row column of the random move
    """
    done = False
    while not done:
        row = random.randint(0, game_state.size - 1)
        col = random.randint(0, game_state.size - 1)
        if game_state.available(row, col):
            done = True
    return row, col

# Note: The agents take turns playing.  So when an agent is in control of a state, it is the other agent who is in
# control of the successor state.  The same agent cannot make a move and be in control of the successor state.
def minimax(game_state):
    """
    Find the best move for our AI agent using the minimax algorithm.
    (searching the entire tree from the current game state)
    :param game_state: GameState object
    :return:  a tuple representing the row column of the best move
    """
    # Enter your code here and remove the raise statement below
    moveList = game_state.possible_moves()
    return max(moveList, key=lambda move: value(game_state.successor(move, 'AI'), 'user'))
    # raise NotImplementedError


def value(game_state, agent):
    """
    Calculate the minimax value for any state under the given agent's
    control.
    :param game_state: GameState object - state may be terminal or
    non-terminal
    :param agent: (string) 'user' or 'AI' - AI is max
    :return: (integer) value of that state -1, 0 or 1
    """
    # Enter your code here and remove the pass statement below
    # if the state is a terminal state: return the state’s utility
    if game_state.is_win('user'):
        return -1
    if game_state.is_tie():
        return 0
    if game_state.is_win('AI'):
        return 1
    # if the agent is MAX: return max-value(state)
    if agent == 'AI':
        return max_value(game_state)
    # if the agent is MIN: return min - value(state)
    else:
        return min_value(game_state)
    # pass


def max_value(game_state):
    """
    Calculate the minimax value for a non-terminal state under Max's
    control (AI agent)
    :param game_state: non-terminal GameState object
    :return: (integer) value of that state -1, 0 or 1
    """
    # Enter your code here and remove the pass statement below
    moveList = game_state.possible_moves()
    v = max(value(game_state.successor(move, 'AI'), 'user') for move in moveList)
    return v
    # pass


def min_value(game_state):
    """
    Calculate the minimax value for a non-terminal state under Min's
    control (user)
    :param game_state: non-terminal GameState object
    :return: (integer) value of that state -1, 0 or 1
    """
    # Enter your code here and remove the pass statement below
    moveList = game_state.possible_moves()
    v = min(value(game_state.successor(move, 'user'), 'AI') for move in moveList)
    return v
    # pass


def alphabeta(game_state):
    """
    Find the best move for our AI agent using the minimax algorithm
    with alpha beta pruning.
    :param game_state: GameState object
    :return:  a tuple representing the row column of the best move
    """
    # Enter your code here and remove the raise statement below
    alpha = -math.inf
    beta = math.inf
    moveList = game_state.possible_moves()
    return max(moveList, key=lambda move: ab_value(game_state.successor(move, 'AI'), 'user', alpha, beta))
    # raise NotImplementedError


def ab_value(game_state, agent, alpha, beta):
    """
    Calculate the minimax value for any state under the given agent's
    control using alpha beta pruning
    :param game_state: GameState object - state may be terminal or
    non-terminal.
    :param agent: (string) 'user' or 'AI' - AI is max
    :return: (integer) value of that state -1, 0 or 1
    """
    # Enter your code here and remove the pass statement below
    # if the state is a terminal state: return the state’s utility
    if game_state.is_win('user'):
        return -1
    if game_state.is_tie():
        return 0
    if game_state.is_win('AI'):
        return 1
    # if the agent is MAX: return abmax_value(state, α, β)
    if agent == 'AI':
        return abmax_value(game_state, alpha, beta)
    # if the agent is MIN: return abmin_value(state, α, β)
    else:
        return abmin_value(game_state, alpha, beta)
    # pass


def abmax_value(game_state, alpha, beta):
    """
    Calculate the minimax value for a non-terminal state under Max's
    control (AI agent) using alpha beta pruning
    :param game_state: non-terminal GameState object
    :return: (integer) value of that state -1, 0 or 1
    """
    # Enter your code here and remove the pass statement below
    v = -math.inf
    moveList = game_state.possible_moves()
    for move in moveList:
        v = max(v, ab_value(game_state.successor(move, 'AI'), 'user', alpha, beta))
        if v >= beta:
            return v
        alpha = max(alpha, v)
    return v
    # pass


def abmin_value(game_state, alpha, beta):
    """
    Calculate the minimax value for a non-terminal state under Min's
    control (user) using alpha beta pruning
    :param game_state: non-terminal GameState object
    :return: (integer) value of that state -1, 0 or 1
    """
    # Enter your code here and remove the pass statement below
    v = math.inf
    moveList = game_state.possible_moves()
    for move in moveList:
        v = min(v, ab_value(game_state.successor(move, 'user'), 'AI', alpha, beta))
        if v <= alpha:
            return v
        beta = min(beta, v)
    return v
    # pass


def abdl(game_state, depth):
    """
    Find the best move for our AI agent by limiting the alpha beta
    search the given depth and using the evaluation function
    game_state.eval()
    :param game_state: GameState object
    :return:  a tuple representing the row column of the best move
    """
    # Enter your code here and remove the raise statement below
    alpha = -math.inf
    beta = math.inf
    moveList = game_state.possible_moves()
    return max(moveList, key=lambda move: abdl_value(game_state.successor(move, 'AI'), 'user', alpha, beta, depth))
    # raise NotImplementedError


def abdl_value(game_state, agent, alpha, beta, depth):
    """
    Calculate the utility for any state under the given agent's control
    using depth limited alpha beta pruning and the evaluation
    function game_state.eval()
    :param game_state: GameState object - state may be terminal or
    non-terminal
    :param agent: (string) 'user' or 'AI' - AI is max
    :return: (integer) utility of that state
    """
    # Enter your code here and remove the pass statement below
    x = game_state.size * 2 + 2  # winnable rows + columns + both diagonals
    # Losing terminal states MUST have a value < any non-terminal state (but still finite)
    if game_state.is_win('user'):
        return -x
    if game_state.is_tie():
        return 0
    # Winning terminal states MUST have a value > any non-terminal state (but still finite)
    if game_state.is_win('AI'):
        return x
    # if maximum depth reached use the evaluation function
    if depth == 0:
        return game_state.eval()
    # if the agent is MAX: return abdlmax_value(state, α, β, depth)
    if agent == 'AI':
        return abdlmax_value(game_state, alpha, beta, depth)
    # if the agent is MIN: return abdlmin_value(state, α, β, depth)
    else:
        return abdlmin_value(game_state, alpha, beta, depth)
    # pass


def abdlmax_value(game_state, alpha, beta, depth):
    """
    Calculate the utility for a non-terminal state under Max's control
    using depth limited alpha beta pruning and the evaluation
    function game_state.eval()
    :param game_state: non-terminal GameState object
    :return: (integer) utility (evaluation function) of that state
    """
    # Enter your code here and remove the pass statement below
    v = -math.inf
    moveList = game_state.possible_moves()
    for move in moveList:
        v = max(v, abdl_value(game_state.successor(move, 'AI'), 'user', alpha, beta, depth - 1))
        if v >= beta:
            return v
        alpha = max(alpha, v)
    return v
    # pass


def abdlmin_value(game_state, alpha, beta, depth):
    """
    Calculate the utility for a non-terminal state under Min's control
    using depth limited alpha beta pruning and the evaluation
    function game_state.eval()
    :param game_state: non-terminal GameState object
    :return: (integer) utility (evaluation function) of that state
    """
    # Enter your code here and remove the pass statement below
    v = math.inf
    moveList = game_state.possible_moves()
    for move in moveList:
        v = min(v, abdl_value(game_state.successor(move, 'user'), 'AI', alpha, beta, depth - 1))
        if v <= alpha:
            return v
        beta = min(beta, v)
    return v
    # pass
