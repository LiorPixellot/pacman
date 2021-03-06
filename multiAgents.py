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
from searchAgents import mazeDistance
import search
from game import Grid
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
        height=currentGameState.data.layout.height
        width=currentGameState.data.layout.width
        mazesize=height*width
        foodscore=[]
        for food in newFood.asList():
            foodscore.append(manhattanDistance(newPos,food))
        ghostscore=[]
        for ghost in newGhostStates:
            ghostscore.append(manhattanDistance(newPos,ghost.configuration.pos))



        if len(foodscore)>0 and min(newScaredTimes)==0:
            minval=-(2*mazesize/(1+min(ghostscore)**2))-min(foodscore)- len(newFood.asList())*mazesize ## first part is for runnig from ghost second part is to reach the food and the third part is to actually eat the food when you get there
        elif len(foodscore)>0 and min(newScaredTimes)>0:
           minval = (2*mazesize / (1 + min(ghostscore) ** 2)) - min(foodscore) - len(newFood.asList()) * mazesize ## to
        else:
            minval = -(2*mazesize / (1 + min(ghostscore) ** 2))  - len(newFood.asList()) *mazesize



        return minval


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

    def minimax(self, gameState,omek, agentnum):
        agentsum = gameState.getNumAgents()
        agentnum=agentnum%agentsum
        evalfun=[None,None]
        if omek == 0 or gameState.isWin() or gameState.isLose() :
            test=self.evaluationFunction(gameState)
            return [self.evaluationFunction(gameState),None]
        if agentnum==0: #agent pacman
            legalActions = gameState.getLegalActions(0)
            maxval = [float('-inf'),None]
            for action in legalActions:
                evalfun=self.minimax(gameState=gameState.generateSuccessor(agentnum, action), omek=omek,agentnum=agentnum+1)
                evalfun[1]=action # see what action took (garbage till the last lv)
                if maxval[0]<evalfun[0]: #take max value
                    maxval=evalfun
            return  maxval
        else: #agent ghost
                legalActions = gameState.getLegalActions(agentnum)
                minval = [float('inf'),None]
                for action in legalActions:
                    if agentnum==agentsum-1:
                        evalfun= self.minimax(gameState=gameState.generateSuccessor(agentnum, action), omek=omek-1,agentnum=agentnum+1) #last ghost and after go down a lv
                    else:
                        evalfun = self.minimax(gameState=gameState.generateSuccessor(agentnum, action), omek=omek , agentnum=agentnum + 1)
                    evalfun[1] = action # see what action took
                    if minval[0] > evalfun[0]: #take max value
                        minval=evalfun
                return  minval



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



        best= self.minimax(gameState=gameState, omek=self.depth, agentnum=0)
        return best[1]
class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """
    def alphabeta(self, gameState,omek, agentnum,alpha=float('-inf'),beta=float('inf')):
        agentsum = gameState.getNumAgents()
        agentnum=agentnum%agentsum
        evalfun=[None,None]
        if omek == 0 or gameState.isWin() or gameState.isLose() :
            test=self.evaluationFunction(gameState)
            return [self.evaluationFunction(gameState),None]
        if agentnum==0: #agent pacman
            legalActions = gameState.getLegalActions(0)
            maxval = [alpha,None]

            for action in legalActions:
                if beta <= alpha:
                    break
                evalfun=self.alphabeta(gameState=gameState.generateSuccessor(agentnum, action), omek=omek,agentnum=agentnum+1,alpha=alpha,beta=beta)
                evalfun[1]=action # see what action took (garbage till the last lv)
                if maxval[0]<evalfun[0]: #take max value
                    maxval=evalfun
                if alpha < maxval[0]:
                    alpha = maxval[0]
            return  maxval

        else: #agent ghost
                legalActions = gameState.getLegalActions(agentnum)
                minval = [beta,None]
                for action in legalActions:
                    if beta <= alpha:
                        break
                    if agentnum==agentsum-1:
                        evalfun= self.alphabeta(gameState=gameState.generateSuccessor(agentnum, action), omek=omek-1,agentnum=agentnum+1,alpha=alpha,beta=beta)
                    else:
                        evalfun = self.alphabeta(gameState=gameState.generateSuccessor(agentnum, action), omek=omek , agentnum=agentnum + 1,alpha=alpha,beta=beta)
                    evalfun[1] = action # see what action took
                    if minval[0] > evalfun[0]: #take max value
                        minval=evalfun
                    if beta > minval[0]:
                        beta = minval[0]
                return  minval
    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        best = self.alphabeta(gameState=gameState, omek=self.depth, agentnum=0)
        return best[1]

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def Expectimax(self, gameState,omek, agentnum):
        agentsum = gameState.getNumAgents()
        agentnum=agentnum%agentsum
        evalfun=[None,None]
        numofmoves=0
        if omek == 0 or gameState.isWin() or gameState.isLose() :
            test=self.evaluationFunction(gameState)
            return [self.evaluationFunction(gameState),None]
        if agentnum==0: #agent pacman
            legalActions = gameState.getLegalActions(0)
            maxval = [float('-inf'),None]
            for action in legalActions:
                evalfun=self.Expectimax(gameState=gameState.generateSuccessor(agentnum, action), omek=omek,agentnum=agentnum+1)
                evalfun[1]=action # see what action took (garbage till the last lv)
                if maxval[0]<evalfun[0]: #take max value
                    maxval=evalfun
            return  maxval
        else: #agent ghost
                legalActions = gameState.getLegalActions(agentnum)
                avgval = [0,None]
                for action in legalActions:
                    if agentnum==agentsum-1:
                        evalfun= self.Expectimax(gameState=gameState.generateSuccessor(agentnum, action), omek=omek-1,agentnum=agentnum+1) #last ghost and after go down a lv
                    else:
                        evalfun = self.Expectimax(gameState=gameState.generateSuccessor(agentnum, action), omek=omek , agentnum=agentnum + 1)
                    evalfun[1] = action # see what action took
                    avgval[0] =avgval[0]+evalfun[0] #take max value

                    numofmoves=numofmoves+1

                if agentnum==agentsum-1:
                    avgval[0]=avgval[0]/numofmoves
                return  avgval


    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        best = self.Expectimax(gameState=gameState, omek=self.depth, agentnum=0)
        return best[1]

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    # Useful information you can extract from a GameState (pacman.py)

    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    height = currentGameState.data.layout.height
    width = currentGameState.data.layout.width
    mazesize = height * width
    foodscore = []
    for food in newFood.asList():
        foodscore.append(manhattanDistance(newPos, food))
    ghostscore = []
    for ghost in newGhostStates:
        ghostscore.append(manhattanDistance(newPos, ghost.configuration.pos))

    if len(foodscore) > 0 and min(newScaredTimes) == 0:
        minval = -(2 * mazesize / (1 + min(ghostscore) ** 2)) - min(foodscore) - len(
            newFood.asList()) * mazesize  ## first part is for runnig from ghost second part is to reach the food and the third part is to actually eat the food when you get there
    elif len(foodscore) > 0 and min(newScaredTimes) > 0:
        minval = (2 * mazesize / (1 + min(ghostscore) ** 2)) - min(foodscore) - len(newFood.asList()) * mazesize  ## to
    else:
        minval = -(2 * mazesize / (1 + min(ghostscore) ** 2)) - len(newFood.asList()) * mazesize

    return minval


# Abbreviation
better = betterEvaluationFunction
