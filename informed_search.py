
"""
A* Algorithm and heuristics implementation

Your task for homework 4 is to implement:
1.  astar
2.  single_heuristic
3.  better_heuristic
4.  gen_heuristic
"""
import data_structures


def astar(problem, heuristic):
    """
    A* graph search algorithm
    returns a solution for the given search problem
    :param
    problem (a Problem object) representing the quest
            see Problem class definition in spartanquest.py
    heuristic (a function) the heuristic function to be used
    :return: list of actions representing the solution to the quest
                or None if there is no solution
    """
    # Enter your code here and remove the pass statement below
    closed = set()  # keep track of our explored states
    fringe = data_structures.PriorityQueue()  # astar, using PriorityQueue for the fringe
    state = problem.start_state()
    # print(len(state[1]))
    # print(state)
    # print(single_heuristic(state, problem))
    # print("cost of going east: ", problem.cost[problem.EAST])

    root = data_structures.Node(state, None, None)
    fringe.push(root, heuristic(state, problem))
    while not fringe.is_empty():
        node = fringe.pop()
        if problem.is_goal(node.state):
            return node.solution()  # we found a solution
        if node.state not in closed:  # we are implementing graph search
            closed.add(node.state)
            for child_state, action, action_cost in problem.expand(node.state):
                # cumulative cost of each child would be cumulative cost of parent + cost of action
                child_node = data_structures.Node(child_state, node, action, node.cumulative_cost + action_cost)
                # astar search orders by the sum of backward cost g(n) and forward cost h(n)
                fringe.push(child_node, child_node.cumulative_cost + heuristic(child_state, problem))
    return None  # Failure -  fringe is empty and no solution was found


def null_heuristic(state, problem):
    """
    Trivial heuristic to be used with A*.
    Running A* with this null heuristic, gives us uniform cost search
    :param
    state: A state is represented by a tuple containing:
                the current position of Sammy the Spartan
                a tuple containing the positions of the remaining medals
    problem: (a Problem object) representing the quest
    :return: 0
    """
    return 0


def single_heuristic(state, problem):
    """
    Heuristic based on the Manhattan Distance to the medal.
    Admissible and Consistent because it doesn't take the cost of moving NSEW into account,
    and assumes there are no walls, therefore will always be <= the actual cost
    :param
    state: A state is represented by a tuple containing:
                the current position of Sammy the Spartan
                a tuple containing the positions of the remaining medals
    problem: (a Problem object) representing the quest

    :return: heuristic value- Manhattan distance to the medal
    """
    # Enter your code here and remove the pass statement below
    (sammy, medals) = state
    if len(state[1]) == 1 and not problem.is_goal(state):
        # manhattan_dist = abs(sammy[0] - medals[0][0]) + abs(sammy[1] - medals[0][1])
        return manhattan_distance(sammy, medals[0])
    else:
        return 0

def manhattan_distance(sammy, medals):
    return abs(sammy[0] - medals[0]) + abs(sammy[1] - medals[1])

def better_heuristic(state, problem):
    """
    Heuristic based on the carrot cost of traveling the Manhattan distance to the medal.
    Admissible and Consistent because although it takes the cost of travel into account, it's
    the cost of travelling the Manhattan distance, not taking wall obstacles into account.
    Therefore the heuristic cost will always be <= the actual cost of reaching the medal.
    :param
    state: A state is represented by a tuple containing:
                the current position of Sammy the Spartan
                a tuple containing the positions of the remaining medals
    problem: (a Problem object) representing the quest
    :return: heuristic value- cost of the Manhattan distance to the medal.
    """
    # Enter your code here and remove the pass statement below
    (sammy, medals) = state
    if len(state[1]) == 1 and not problem.is_goal(state):
        return costOfManhattanDist(sammy, medals[0], problem)
        # if(sammy[0] <= medals[0][0]):
        #     xCost = abs(sammy[0] - medals[0][0]) * problem.cost[problem.EAST]
        # else:
        #     xCost = abs(sammy[0] - medals[0][0]) * problem.cost[problem.WEST]
        # if(sammy[1] <= medals[0][1]):
        #     yCost = abs(sammy[1] - medals[0][1]) * problem.cost[problem.SOUTH]
        # else:
        #     yCost = abs(sammy[1] - medals[0][1]) * problem.cost[problem.NORTH]
        # return xCost + yCost
    else:
        return 0

def costOfManhattanDist(sammy, medal, problem):
    if sammy[0] <= medal[0]:
        xCost = abs(sammy[0] - medal[0]) * problem.cost[problem.EAST]
    else:
        xCost = abs(sammy[0] - medal[0]) * problem.cost[problem.WEST]
    if sammy[1] <= medal[1]:
        yCost = abs(sammy[1] - medal[1]) * problem.cost[problem.SOUTH]
    else:
        yCost = abs(sammy[1] - medal[1]) * problem.cost[problem.NORTH]
    return xCost + yCost

def gen_heuristic(state, problem):
    """
    Heuristic for use with problems with multiple medals. Iterates through remaining
    medals and returns the highest cost medal to reach based on the cost of the Manhattan
    distance to it. Admissible and Consistent for the same reason as better_heuristic-
    because heuristic cost is based on Manhattan distance and assumes no wall obstacles exist.
    :param
    state: A state is represented by a tuple containing:
                the current position of Sammy the Spartan
                a tuple containing the positions of the remaining medals
    problem: (a Problem object) representing the quest
    :return: cost of the costliest medal to reach based on Manhattan distance
    """
    # Enter your code here and remove the pass statement below
    (sammy, medals) = state
    if not problem.is_goal(state):
        bestMedal = max(costOfManhattanDist(sammy, medal, problem) for medal in medals)
        return bestMedal
    else:
        return 0
