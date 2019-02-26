# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()

class State:
    """Data structure for State representation in seach algorithm"""

    def __init__(self, gameState, previousState, action, cost=0):
        self.state = gameState
        self.previous = previousState
        self.action = action
        self.cost = cost

    def getPath(self):
        """Return the list of actions that leads to this State"""
        result = list()
        currentState = self
        while(currentState.previous != None):
            result.insert(0, currentState.action)
            currentState = currentState.previous
        return result

    def __str__(self):
        str = "State ({},{}):\n".format(self.state[0], self.state[1])
        str += "\tcost: {}\n".format(self.cost)
        if(self.previous != None):
            str += "\tprevious:({}/{})\n".format(self.previous[0], self.previous[1])
        if(self.action != None):
            str += "\taction:({})\n".format(self.action)
        return str

    def __eq__(self, other):
        """To compare 2 State object by their state attribute"""
        if isinstance(other, State):
            return self.state == other.state
        else: return False

    def __hash__(self):
        """Needed for __eq__()"""
        return hash(self.state)


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"

    currentState = State(problem.getStartState(), None, None)
    frontier = util.Stack()
    visitedStates = set()
    visitedStates.add(currentState)

    frontier.push(currentState)

    while(not frontier.isEmpty()):
        currentState = frontier.pop()
        visitedStates.add(currentState.state)
        # print(currentState)
        if(problem.isGoalState(currentState.state)):
            return currentState.getPath()
        else:
            for (nextGameState, action, _) in problem.getSuccessors(currentState.state):
                if(nextGameState not in visitedStates):
                    nextState = State(nextGameState, currentState, action)
                    frontier.push(nextState)
    return []


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    currentState = State(problem.getStartState(), None, None)
    frontier = util.Queue()
    visitedStates = set()
    visitedStates.add(currentState)

    frontier.push(currentState)

    while(not frontier.isEmpty()):
        currentState = frontier.pop()
        # print(currentState)
        if(problem.isGoalState(currentState.state)):
            return currentState.getPath()
        else:
            visitedStates.add(currentState.state)
            for (nextGameState, action, _) in problem.getSuccessors(currentState.state):
                if(nextGameState not in visitedStates):
                    nextState = State(nextGameState, currentState, action)
                    if(nextState not in frontier.list):
                        frontier.push(nextState)
    return []

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    currentState = State(problem.getStartState(), None, None, 0)
    frontier = util.PriorityQueue()
    visitedStates = set()
    visitedStates.add(currentState)

    frontier.update(currentState, currentState.cost)

    while(not frontier.isEmpty()):
        currentState = frontier.pop()
        # print(currentState)
        if(problem.isGoalState(currentState.state)):
            return currentState.getPath()
        else:
            visitedStates.add(currentState.state)
            for (nextGameState, action, cost) in problem.getSuccessors(currentState.state):
                if(nextGameState not in visitedStates):
                    nextStateCost = currentState.cost + cost
                    nextState = State(nextGameState, currentState, action, nextStateCost)
                    if(nextState not in frontier.heap):
                        frontier.update(nextState, nextState.cost)
    return []

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    currentState = State(problem.getStartState(), None, None, 0)
    frontier = util.PriorityQueue()
    visitedStates = set()
    visitedStates.add(currentState)

    frontier.update(currentState, currentState.cost + heuristic(currentState.state, problem))

    while(not frontier.isEmpty()):
        currentState = frontier.pop()
        # print(currentState)
        if(problem.isGoalState(currentState.state)):
            return currentState.getPath()
        else:
            visitedStates.add(currentState.state)
            for (nextGameState, action, cost) in problem.getSuccessors(currentState.state):
                if(nextGameState not in visitedStates):
                    nextStateCost = currentState.cost + cost
                    nextState = State(nextGameState, currentState, action, nextStateCost)
                    if(nextState not in frontier.heap):
                        frontier.update(nextState, nextState.cost + heuristic(nextState.state, problem))


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
