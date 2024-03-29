
"""
Uninformed Search Algorithm implementation

dfs has been implemented for you.
Your task for homework 3 is to implement bfs and ucs.
"""
import data_structures

def dfs(problem):
    """
    Depth first graph search algorithm - implemented for you
    :param problem (a Problem object) representing the quest
            see Problem class definition in spartanquest.py)
    :return: list of actions representing the solution to the quest
                or None if there is no solution
    """
    closed = set()  # keep track of our explored states
    fringe = data_structures.Stack() # for dfs, the fringe is a stack
    state = problem.start_state()
    root = data_structures.Node(state, None, None)
    fringe.push(root)
    while not fringe.is_empty():
        node = fringe.pop()
        if problem.is_goal(node.state):
            return node.solution()  # we found a solution
        if node.state not in closed:  # we are implementing graph search
            closed.add(node.state)
            for child_state, action, action_cost in problem.expand(node.state):
                child_node = data_structures.Node(child_state, node, action)
                fringe.push(child_node)
    return None  # Failure -  no solution was found

def bfs(problem):
    """
    Breadth first graph search algorithm
    :param problem (a Problem object) representing the quest
            see Problem class definition in spartanquest.py)
    :return: list of actions representing the solution to the quest
            or None if there is no solution
    """
    # Enter your  code here and remove the pass statement below
    closed = set()  # keep track of our explored states
    fringe = data_structures.Queue()  # bfs, using Queue for the fringe
    state = problem.start_state()
    root = data_structures.Node(state, None, None)
    fringe.push(root)
    while not fringe.is_empty():
        node = fringe.pop()
        if problem.is_goal(node.state):
            return node.solution()  # we found a solution
        if node.state not in closed:  # we are implementing graph search
            closed.add(node.state)
            for child_state, action, action_cost in problem.expand(node.state):
                child_node = data_structures.Node(child_state, node, action)
                fringe.push(child_node)
    return None  # Failure -  fringe is empty and no solution was found

"""
Note from grading rubric:
ucs efficiency
    The cumulative cost for each node is stored in the Node object.
    It is NOT recomputed from the start node with every successor state.
The two functions use the Node class to keep track of paths and costs where needed.
    The functions do NOT use the path_cost method in the Problem class.
    The functions use the solution method in the Node class.
"""
def ucs(problem):
    """
    Uniform cost first graph search algorithm
    :param
    problem (a Problem object) representing the quest
            see Problem class definition in spartanquest.py)
    :return: list of actions representing the solution to the quest
    """
    # Enter your code here and remove the pass statement below
    closed = set()  # keep track of our explored states
    fringe = data_structures.PriorityQueue()  # ucs, using PriorityQueue for the fringe
    state = problem.start_state()
    root = data_structures.Node(state, None, None)
    fringe.push(root, 0) # Priority of root is 0
    while not fringe.is_empty():
        node = fringe.pop()
        if problem.is_goal(node.state):
            return node.solution()  # we found a solution
        if node.state not in closed:  # we are implementing graph search
            closed.add(node.state)
            for child_state, action, action_cost in problem.expand(node.state):
                # cumulative cost of each child would be cumulative cost of parent + cost of action
                child_node = data_structures.Node(child_state, node, action, node.cumulative_cost + action_cost)
                fringe.push(child_node, child_node.cumulative_cost)
    return None  # Failure -  fringe is empty and no solution was found

