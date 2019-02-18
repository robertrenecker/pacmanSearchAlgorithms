# multiAgents.py
# --------------
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
        from util import manhattanDistance as mh
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
        evalScore = successorGameState.getScore()
        #Return new food left score (less food left => better score)
        # foodLeft = newFood.count(True)
        # evalScore += (1/foodLeft) if foodLeft>0 else 100

        #min distance to next food
        foodDistances = []
        minFoodDistance = 0

        #Use food locations from pacnan.py file
        foodGrid = newFood.asList()
        for i,food in enumerate(foodGrid):
            foodDistances.append(mh(food, newPos)+i)
        if foodDistances:
            minFoodDistance = min(foodDistances)

        evalScore-= minFoodDistance



        # minDistanceToNextFood = min([mh(newPos, foodPos) for foodPos in ])
        #Is there a ghost on next step?
        ghostDistances = [mh(ghostPos.getPosition(), newPos) for ghostPos in newGhostStates]
        minDistance = min(ghostDistances)
        #Willing distance to be from ghost.
        if minDistance < 3 and minDistance >0:
            #Lower the score more for higher ghost distances
            #Why does this work?? (This should give lower score to a move that moves away from ghost lol?)
            evalScore /= 2*minDistance

            #otherwise a realistic approach is to just aggregate the score
            #evalScore += 2*minDistance





        return evalScore

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



        #Get num layers / agents to move through
        numAgents = gameState.getNumAgents()


        def recursiveMinMax(currState, currDepth, currAgent):
            #Get legal moves of currState
            legalActions = currState.getLegalActions(currAgent)
            #Base case is if depth == 0 or if game is over (no other moves to take)
            if currDepth == 0 or len(legalActions) == 0:

                return (None, self.evaluationFunction(currState))

            #move up agent list
            successorAgent =  (currAgent+1) % numAgents
            successorDepth = currDepth
            if successorAgent == 0:
                successorDepth -= 1

            #Now with new agents:
            actionToTake = None
            value = None
            if currAgent == 0:
                value = -1e500
                for action in legalActions:
                #get successorGameState
                    successorState = currState.generateSuccessor(currAgent, action)
                    returnValue, successorValue = recursiveMinMax(successorState, successorDepth, successorAgent)
                    if successorValue > value:
                        actionToTake = action
                        value = successorValue
            #otherwise if it is a ghost layer
            else:
                value = 1e500
                for action in legalActions:
                    successorState = currState.generateSuccessor(currAgent, action)
                    returnValue, successorValue = recursiveMinMax(successorState, successorDepth, successorAgent)
                    if successorValue < value:
                        actionToTake = action
                        value = successorValue


            return (actionToTake, value)

        finalChoice, finalValue = recursiveMinMax(gameState, self.depth, 0)

        return finalChoice






class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        numAgents = gameState.getNumAgents()

        #alpha is the best that a white node / pacman has seen (*agent 0)
        #beta is the best that a black node / ghost has seen (agent 1+)
        def recursiveMinMax(currState, currDepth, currAgent, alpha, beta):
            #Get legal moves of currState
            legalActions = currState.getLegalActions(currAgent)
            #Base case is if depth == 0 or if game is over (no other moves to take)
            if currDepth == 0 or len(legalActions) == 0:

                return (None, self.evaluationFunction(currState))

            #move up agent list
            successorAgent =  (currAgent+1) % numAgents
            successorDepth = currDepth
            if successorAgent == 0:
                successorDepth -= 1

            #Now with new agents:
            actionToTake = None
            value = None
            if currAgent == 0:
                value = -1e500
                for action in legalActions:
                #get successorGameState
                    successorState = currState.generateSuccessor(currAgent, action)
                    returnValue, successorValue = recursiveMinMax(successorState, successorDepth, successorAgent, alpha, beta)
                    if successorValue > value:
                        actionToTake = action
                        value = successorValue
                    if value > beta:
                        break
                    alpha = max(alpha, successorValue)



            #otherwise if it is a ghost layer
            else:
                value = 1e500
                for action in legalActions:
                    successorState = currState.generateSuccessor(currAgent, action)
                    returnValue, successorValue = recursiveMinMax(successorState, successorDepth, successorAgent, alpha, beta)
                    if successorValue < value:
                        actionToTake = action
                        value = successorValue
                    if successorValue < alpha:
                        break
                    beta = min(value, beta)




            return (actionToTake, value)

        finalChoice, finalValue = recursiveMinMax(gameState, self.depth, 0, -1e500, 1e500)

        return finalChoice
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
        numAgents = gameState.getNumAgents()


        def recursiveMinMax(currState, currDepth, currAgent):
            #Get legal moves of currState
            legalActions = currState.getLegalActions(currAgent)
            #Base case is if depth == 0
            if currDepth == 0 or len(legalActions) == 0:

                return (None, self.evaluationFunction(currState))

            #move up agent list
            successorAgent =  (currAgent+1) % numAgents
            successorDepth = currDepth
            if successorAgent == 0:
                successorDepth -= 1

            #Now with new agents:
            actionToTake = None
            value = None
            if currAgent == 0:
                value = -1e500
                for action in legalActions:
                #get successorGameState
                    successorState = currState.generateSuccessor(currAgent, action)
                    returnValue, successorValue = recursiveMinMax(successorState, successorDepth, successorAgent)
                    if successorValue > value:
                        actionToTake = action
                        value = successorValue
            #otherwise if it is a ghost layer
            else:
                value = 0
                for action in legalActions:
                    successorState = currState.generateSuccessor(currAgent, action)
                    returnValue, successorValue = recursiveMinMax(successorState, successorDepth, successorAgent)


                    value += successorValue
                value /= float(len(legalActions))

            return (actionToTake, value)

        finalChoice, finalValue = recursiveMinMax(gameState, self.depth, 0)

        return finalChoice

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
