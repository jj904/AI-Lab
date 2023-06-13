
"""
Sudoku puzzle solver implementation

q1:  Basic Backtracking Search
q2:  Backtracking Search with AC-3
q3:  Backtracking Search with MRV Ordering and AC-3
"""
import csp


# Enter your helper functions here
def createDomain(puzzle):
    """
    creates a dictionary representing variables and their domains.
    The dictionary keys are variable names and the values are sets
    representing their domains.
    :param puzzle:The dictionary keys are tuples
    (row, column) representing the filled puzzle squares and the values
    are the corresponding numbers assigned to these squares.
    :return: dictionary of domains at every index
    """
    domain = {}  # create empty dictionary
    for row in range(9):
        for column in range(9):  # for every index
            if (row, column) not in puzzle.keys():  # blank spot in sudoku puzzle
                domain[(row, column)] = {1, 2, 3, 4, 5, 6, 7, 8, 9}
            else:
                domain[(row, column)] = {puzzle[(row, column)]}  # value corresponding to index
    return domain


def createNeighborSet(row, column):
    """
    Given an index, returns a set of its neighbors
    :param row: index of row
    :param column: index of column
    :return: set of neighbors of (row, column)
    """
    setOfNeighbors = set()
    for i in range(9):
        if i != row:
            setOfNeighbors.add((i, column))  # adds column neighbors
        if i != column:
            setOfNeighbors.add((row, i))  # adds row neighbors

    # add neighbors in the corresponding 3 by 3 region
    tbtRow = row // 3
    tbtColumn = column // 3
    for j in range(tbtRow * 3, tbtRow * 3 + 3):
        for k in range(tbtColumn * 3, tbtColumn * 3 + 3):
            if j != row and k != column:
                setOfNeighbors.add((j, k))
    return setOfNeighbors


def createNeighbors(puzzle):
    """
    Creates a dictionary representing binary constraints.
    The dictionary keys are variable names and the values are sets
    containing all the variables that are connected to the key.
    (Variables are connected if they both appear in a constraint)
    :param puzzle:
    :return: dictionary of key(tuple) representing index, and value being
    the set of that index's neighbors
    """
    neighbors = {}  # create empty dictionary
    for i in range(9):
        for j in range(9):
            neighbors[(i, j)] = createNeighborSet(i, j)
    return neighbors


def createConstraints(var1, val1, var2, val2):
    """
    a function that takes as arguments two variables
        and two values: f(var1, val1, var2, val2).
        The function must return True if var1 and var2 satisfy the
        constraint when their respective values are val1 and val2.
    :param var1: row column tuple
    :param val1: value of row column tuple index
    :param var2: neighbor row column tuple
    :param val2: value of neighbor
    :return:
    """
    return val1 != val2  # constraint is that neighbors must be alldiff


def build_csp(puzzle):
    """
    Create a CSP object representing the puzzle.
    :param puzzle (dictionary): The dictionary keys are tuples
    (row, column) representing the filled puzzle squares and the values
    are the corresponding numbers assigned to these squares.
    :return: CSP object
    """
    # Enter your code here and remove the pass statement below
    return csp.CSP(createDomain(puzzle), createNeighbors(puzzle), createConstraints)


def q1(puzzle):
    """
    Solve the given puzzle with basic backtracking search
    :param puzzle (dictionary): The dictionary keys are tuples
    (row, column) representing the filled puzzle squares and the values
    are the corresponding numbers assigned to these squares.
    :return: a tuple consisting of a solution (dictionary) and the
    CSP object.
    """
    # Enter your code here and remove the pass statement below
    q1_csp = build_csp(puzzle)
    return q1_csp.backtracking_search(), q1_csp


def q2(puzzle):
    """
    Solve the given puzzle with backtracking search and AC-3 as
    a preprocessing step.
    :param puzzle (dictionary): The dictionary keys are tuples
    (row, column) representing the filled puzzle squares and the values
    are the corresponding numbers assigned to these squares.
    :return: a tuple consisting of a solution (dictionary) and the
    CSP object.
    """
    # Enter your code here and remove the pass statement below
    q2_csp = build_csp(puzzle)
    q2_csp.ac3_algorithm()  # AC-3 as a preprocessing step
    return q2_csp.backtracking_search(), q2_csp


def q3(puzzle):
    """
    Solve the given puzzle with backtracking search and MRV ordering and
    AC-3 as a preprocessing step.
    :param puzzle (dictionary): The dictionary keys are tuples
    (row, column) representing the filled puzzle squares and the values
    are the corresponding numbers assigned to these squares.
    :return: a tuple consisting of a solution (dictionary) and the
    CSP object.
    """
    # Enter your code here and remove the pass statement below
    q3_csp = build_csp(puzzle)
    q3_csp.ac3_algorithm()
    return q3_csp.backtracking_search("MRV"), q3_csp
