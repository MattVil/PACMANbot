# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"

        SCARED_DISTANCE = 2
        ghostDistance = [manhattanDistance(ghost.getPosition(), newPos) for ghost in newGhostStates]

        for ghostCloseFlag in (True for dist in ghostDistance if dist < SCARED_DISTANCE):
            return float('-inf')

        return -1*min([manhattanDistance(food, newPos) for food in currentGameState.getFood().asList()])

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        return self.min_max(gameState, self.depth)[1]

    def min_max(self, gameState, depth, agentIndex=0):

        if((depth == 0) or gameState.isWin() or gameState.isLose()):
            return (self.evaluationFunction(gameState), None)

        nbAgents = gameState.getNumAgents()
        if(agentIndex == (nbAgents-1)):
            nextDepth = depth-1
        else:
            nextDepth = depth

        nextAgentIndex = (agentIndex+1)%nbAgents
        actions = []
        for action in gameState.getLegalActions(agentIndex):
            nextGameState = gameState.generateSuccessor(agentIndex, action)
            actions.append((self.min_max(nextGameState, nextDepth, nextAgentIndex)[0], action))

        if(agentIndex == 0):
            return max(actions)
        return min(actions)

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        alpha, beta = float("-inf"), float("inf")
        actions = gameState.getLegalActions(0)
        bestScore = float("-inf")
        bestAction = None

        for action in actions:
            nextState = gameState.generateSuccessor(0, action)
            score = self.min_value(nextState, 0, 1, alpha, beta)
            alpha = max(alpha, score)
            if score > bestScore:
                bestAction = action
                bestScore = score
        return bestAction

    def max_value(self, gameState, depth, agentIndex, alpha, beta):
        nodeDepth = depth + 1
        if(nodeDepth==self.depth or gameState.isWin() or gameState.isLose()):
            return self.evaluationFunction(gameState)

        value = float("-inf")
        actions = gameState.getLegalActions(0)
        localAlpha = alpha
        for action in actions:
            successor = gameState.generateSuccessor(0, action)
            value = max(value, self.min_value(successor, nodeDepth, 1, localAlpha, beta))
            if(value > beta):
                return value
            localAlpha = max(localAlpha, value)
        return value

    def min_value(self, gameState, depth, agentIndex, alpha, beta):
        nodeDepth = depth + 1
        if(gameState.isWin() or gameState.isLose()):
            return self.evaluationFunction(gameState)

        value = float("inf")
        actions = gameState.getLegalActions(agentIndex)
        localBeta = beta
        for action in actions:
            successor = gameState.generateSuccessor(agentIndex, action)
            if(agentIndex == (gameState.getNumAgents()-1)):
                value = min(value, self.max_value(successor, depth, 0, alpha, localBeta))
                if(value < alpha):
                    return value
                localBeta = min(localBeta, value)
            else:
                value = min(value, self.min_value(successor, depth, agentIndex+1, alpha, localBeta))
                if(value < alpha):
                    return value
                localBeta = min(localBeta, value)
        return value


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"

        bestValue = float("-inf")
        bestAction = 'Stop'
        actions = gameState.getLegalActions(0)
        for action in actions:
            successor = gameState.generateSuccessor(0, action)
            value = self.expectimax(successor, 0, 1)
            # maybe not the best way to deal with equal values
            if((value == bestValue) and (random.uniform(0, 1) > 0.5)):
                bestValue = value
                bestAction = action
            elif(value > bestValue):
                bestValue = value
                bestAction = action
        return bestAction

    def expectimax(self, gameState, depth, agentIndex):
        if(agentIndex >= gameState.getNumAgents()):
            agentIndex = 0
            depth += 1

        if(depth==self.depth or gameState.isWin() or gameState.isLose()):
            return self.evaluationFunction(gameState)

        actions = gameState.getLegalActions(agentIndex)
        if(agentIndex != 0):
            sumValues = 0
            for action in actions:
                successor = gameState.generateSuccessor(agentIndex, action)
                sumValues += self.expectimax(successor, depth, agentIndex+1)
            return sumValues/len(actions)
        else:
            value = float("-inf")
            for action in actions:
                successor = gameState.generateSuccessor(agentIndex, action)
                value = max(self.expectimax(successor, depth, agentIndex+1), value)
            return value



def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: eval = currentScore - sum(foodCoef*foodDistance)
                                     - sum(capsuleCoef*capsuleDistance)
                                     + sum(ghostCoef*ghostSign*ghostDistance)

                                     Where ghostSign =  1  if normal ghost
                                           ghostSign = -1  if scared ghost

                 Give different values ​​to the coefficients will leads to
                 different behavior. The best behavior founded is with :
                    foodCoef = 0.5
                    capsuleCoef = 18.15
                    ghostCoef = 1
                 The average score is 1279.9
    """
    "*** YOUR CODE HERE ***"
    foodPos = currentGameState.getFood().asList()
    foodDist = []
    ghostStates = currentGameState.getGhostStates()
    capsules = currentGameState.getCapsules()
    currentPos = list(currentGameState.getPacmanPosition())

    #1/2/1 - 862.5
    #0.1/2/1 - 1063.0
    #0.1/10/1 - 1245.3
    #0.1/10/0.5 - 1239.8 NEVER BELOW 1000
    #0.5/15/1 - 1265.7 NEVER BELOW 1100
    #0.5/18.15/1 - 1279.9 NEVER BELOW 1100
    foodCoef = 0.5
    capsuleCoef = 18.15
    ghostCoef = 1

    score = currentGameState.getScore()

    for food in foodPos:
        foodDist = manhattanDistance(food, currentPos)
        score -= foodCoef*foodDist

    for ghost in ghostStates:
        ghostDist = manhattanDistance(ghost.getPosition(), currentPos)
        if(ghost.scaredTimer > 0):
            ghostSign = -1
        else:
            ghostSign = 1
        score += ghostCoef*ghostSign*ghostDist

    for capsule in capsules:
        capsuleDist = manhattanDistance(capsule, currentPos)
        score -= capsuleCoef*capsuleDist

    return score

# Abbreviation
better = betterEvaluationFunction
