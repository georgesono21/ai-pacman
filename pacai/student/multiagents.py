import random

from pacai.agents.base import BaseAgent
from pacai.agents.search.multiagent import MultiAgentSearchAgent

# from pacai.student.searchAgents import foodHeuristic
from pacai.core.distance import manhattan
from pacai.core.directions import Directions
from pacai.core.actions import Actions


class ReflexAgent(BaseAgent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.
    You are welcome to change it in any way you see fit,
    so long as you don't touch the method headers.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        `ReflexAgent.getAction` chooses among the best options according to the evaluation function.

        Just like in the previous project, this method takes a
        `pacai.core.gamestate.AbstractGameState` and returns some value from
        `pacai.core.directions.Directions`.
        """

        # Collect legal moves.
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions.
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [
            index for index in range(len(scores)) if scores[index] == bestScore
        ]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best.

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current `pacai.bin.pacman.PacmanGameState`
        and an action, and returns a number, where higher numbers are better.
        Make sure to understand the range of different values before you combine them
        in your evaluation function.
        """

        successorGameState = currentGameState.generatePacmanSuccessor(action)

        # Useful information you can extract.
        # newPosition = successorGameState.getPacmanPosition()
        # oldFood = currentGameState.getFood()
        # newGhostStates = successorGameState.getGhostStates()
        # newScaredTimes = [ghostState.getScaredTimer() for ghostState in newGhostStates]

        # *** Your Code Here ***

        newPosition = successorGameState.getPacmanPosition()
        oldFood = currentGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.getScaredTimer() for ghostState in newGhostStates]

        # for foodPosition in oldFood.asList():
        #     if food

        # print(newGhostStates)
        # if newPosition in newGhostStates:
        # return 0
        for i in range(len(newGhostStates)):
            for neighbor in Actions.getLegalNeighbors(
                newPosition, successorGameState._layout.walls
            ):
                # print(neighbor, ghost._position)
                if neighbor == newGhostStates[i]._position and newScaredTimes[i] == 0:
                    return 0

        distances = list()
        for pos in oldFood.asList():
            distances.append(manhattan(newPosition, pos))

        if not distances:
            return 500

        print(500 - min(distances), newPosition)
        return 500 - min(distances)

        return successorGameState.getScore()


class MinimaxAgent(MultiAgentSearchAgent):
    """
    A minimax agent.

    Here are some method calls that might be useful when implementing minimax.

    `pacai.core.gamestate.AbstractGameState.getNumAgents()`:
    Get the total number of agents in the game

    `pacai.core.gamestate.AbstractGameState.getLegalActions`:
    Returns a list of legal actions for an agent.
    Pacman is always at index 0, and ghosts are >= 1.

    `pacai.core.gamestate.AbstractGameState.generateSuccessor`:
    Get the successor game state after an agent takes an action.

    `pacai.core.directions.Directions.STOP`:
    The stop direction, which is always legal, but you may not want to include in your search.

    Method to Implement:

    `pacai.agents.base.BaseAgent.getAction`:
    Returns the minimax action from the current gameState using
    `pacai.agents.search.multiagent.MultiAgentSearchAgent.getTreeDepth`
    and `pacai.agents.search.multiagent.MultiAgentSearchAgent.getEvaluationFunction`.
    """

    def getAction(self, state):
        # for i in state.getLegalActions()
        # return max()

        maxUtility = -1111111
        maxUtilityMove = Directions.STOP
        for action in state.getLegalActions(0):
            successorState = state.generateSuccessor(0, action)
            utility = self.max_value(successorState, 0, 0)

            # print(utility)
            if utility > maxUtility:
                maxUtilityMove = action
                maxUtility = utility

        return maxUtilityMove

    def max_value(self, state, turn, depth):
        # in this turn should be 0
        # print("max: ", turn, depth, turn % state.getNumAgents())
        if state.isLose() or state.isWin() or self.getTreeDepth() <= depth:
            return self.getEvaluationFunction()(state)
        else:
            turn += 1
            depth += 1
            maxUtility = -111111  # worst case
            for action in state.getLegalActions(turn % state.getNumAgents()):
                if action == Directions.STOP:
                    continue

                successorState = state.generateSuccessor(
                    turn % state.getNumAgents(), action
                )
                maxUtility = max(
                    maxUtility, self.min_value(successorState, turn, depth)
                )

            return maxUtility

    def min_value(self, state, turn, depth):
        # print("min: ", turn, depth, turn % state.getNumAgents())
        if state.isOver() or self.getTreeDepth() <= depth:
            return self.getEvaluationFunction()(state)
        else:
            minUtility = 111111  # worst case
            turn += 1

            if turn % state.getNumAgents() == 0:  # if next turn is
                # for action in state.getLegalActions():
                #     if action == Directions.STOP:
                #         continue

                #     successorState = state.generateSuccessor(0, action)
                #     minUtility = min(minUtility, self.max_value(state, turn, depth))

                # return minUtility
                return self.max_value(state, turn, depth)
            else:
                for action in state.getLegalActions(turn % state.getNumAgents()):
                    if action == Directions.STOP:
                        continue
                    # print("min: ", action)
                    successorState = state.generateSuccessor(
                        turn % state.getNumAgents(), action
                    )
                    minUtility = min(
                        self.min_value(successorState, turn, depth), minUtility
                    )

            return minUtility

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    A minimax agent with alpha-beta pruning.

    Method to Implement:

    `pacai.agents.base.BaseAgent.getAction`:
    Returns the minimax action from the current gameState using
    `pacai.agents.search.multiagent.MultiAgentSearchAgent.getTreeDepth`
    and `pacai.agents.search.multiagent.MultiAgentSearchAgent.getEvaluationFunction`.
    """

    def getAction(self, state):
        # for i in state.getLegalActions()
        # return max()

        maxUtility = -1111111
        maxUtilityMove = Directions.STOP
        for action in state.getLegalActions(0):
            successorState = state.generateSuccessor(0, action)
            utility = self.max_value(successorState, 0, 0, -111111, 1111111)

            # print(utility)
            if utility > maxUtility:
                maxUtilityMove = action
                maxUtility = utility

        return maxUtilityMove

    def max_value(self, state, turn, depth, alpha, beta):
        # in this turn should be 0
        # print("max: ", turn, depth, turn % state.getNumAgents())
        if state.isLose() or state.isWin() or self.getTreeDepth() <= depth:
            return self.getEvaluationFunction()(state)
        else:
            turn += 1
            depth += 1
            maxUtility = -111111  # worst case
            for action in state.getLegalActions(turn % state.getNumAgents()):
                if action == Directions.STOP:
                    continue

                successorState = state.generateSuccessor(
                    turn % state.getNumAgents(), action
                )

                utility = self.min_value(successorState, turn, depth, alpha, beta)
                if maxUtility < utility:
                    maxUtility = utility
                    alpha = max(alpha, maxUtility)

                if maxUtility >= beta:
                    return maxUtility

            return maxUtility

    def min_value(self, state, turn, depth, alpha, beta):
        # print("min: ", turn, depth, turn % state.getNumAgents())
        if state.isOver() or self.getTreeDepth() <= depth:
            return self.getEvaluationFunction()(state)
        else:
            minUtility = 111111  # worst case
            turn += 1

            if turn % state.getNumAgents() == 0:  # if next turn is
                for action in state.getLegalActions():
                    if action == Directions.STOP:
                        continue

                    successorState = state.generateSuccessor(0, action)
                    utility = self.max_value(state, turn, depth, alpha, beta)

                    if minUtility > utility:
                        minUtility = utility
                        beta = min(beta, minUtility)

                    if minUtility <= alpha:
                        return minUtility

                return minUtility
            else:
                for action in state.getLegalActions(turn % state.getNumAgents()):
                    if action == Directions.STOP:
                        continue
                    # print("min: ", action)
                    successorState = state.generateSuccessor(
                        turn % state.getNumAgents(), action
                    )
                    minUtility = min(
                        self.min_value(successorState, turn, depth, alpha, beta),
                        minUtility,
                    )

            return minUtility

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
    An expectimax agent.

    All ghosts should be modeled as choosing uniformly at random from their legal moves.

    Method to Implement:

    `pacai.agents.base.BaseAgent.getAction`:
    Returns the expectimax action from the current gameState using
    `pacai.agents.search.multiagent.MultiAgentSearchAgent.getTreeDepth`
    and `pacai.agents.search.multiagent.MultiAgentSearchAgent.getEvaluationFunction`.
    """

    def getAction(self, state):
        # for i in state.getLegalActions()
        # return max()

        maxUtility = -1111111
        maxUtilityMove = Directions.STOP
        for action in state.getLegalActions(0):
            successorState = state.generateSuccessor(0, action)
            utility = self.max_value(successorState, 0, 0)

            print(utility)
            if utility > maxUtility:
                maxUtilityMove = action
                maxUtility = utility

        return maxUtilityMove

    def max_value(self, state, turn, depth):
        # in this turn should be 0
        # print("max: ", turn, depth, turn % state.getNumAgents())
        if state.isLose() or state.isWin() or self.getTreeDepth() <= depth:
            return self.getEvaluationFunction()(state)
        else:
            turn += 1
            depth += 1
            maxUtility = -111111  # worst case
            for action in state.getLegalActions(turn % state.getNumAgents()):
                if action == Directions.STOP:
                    continue

                successorState = state.generateSuccessor(
                    turn % state.getNumAgents(), action
                )
                maxUtility = max(
                    maxUtility, self.chance_value(successorState, turn, depth)
                )

            return maxUtility

    def chance_value(self, state, turn, depth):
        # print("min: ", turn, depth, turn % state.getNumAgents())
        if state.isOver() or self.getTreeDepth() <= depth:
            return self.getEvaluationFunction()(state)
        else:
            expectedUtility = 0  # worst case
            numLegalMoves = len(state.getLegalActions())
            runningSum = 0
            turn += 1

            if turn % state.getNumAgents() == 0:  # if next turn is
                for action in state.getLegalActions(0):
                    if action == Directions.STOP:
                        continue

                    successorState = state.generateSuccessor(0, action)
                    runningSum += self.max_value(state, turn, depth)

                expectedUtility = runningSum / numLegalMoves
                return expectedUtility

            else:
                for action in state.getLegalActions(turn % state.getNumAgents()):
                    if action == Directions.STOP:
                        continue
                    # print("min: ", action)
                    successorState = state.generateSuccessor(
                        turn % state.getNumAgents(), action
                    )

                    runningSum += self.chance_value(successorState, turn, depth)

                expectedUtility = runningSum / numLegalMoves
                return expectedUtility

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable evaluation function.

    DESCRIPTION: <write something here so we know what you did>
    """

    # Useful information you can extract.
    # newPosition = successorGameState.getPacmanPosition()
    # oldFood = currentGameState.getFood()
    # newGhostStates = successorGameState.getGhostStates()
    # newScaredTimes = [ghostState.getScaredTimer() for ghostState in newGhostStates]

    # *** Your Code Here ***
    state = currentGameState
    position = state.getPacmanPosition()
    oldFood = currentGameState.getFood()
    capsules = currentGameState.getCapsules()
    ghostStates = state.getGhostStates()
    scaredTimes = [ghostState.getScaredTimer() for ghostState in ghostStates]

    ghostDistances = list()
    for ghost in ghostStates:
        ghostDistances.append(manhattan(position, ghost.getPosition()))

    foodDistances = list()
    for pos in oldFood.asList():
        foodDistances.append(manhattan(position, pos))

    capsuleDistances = list()
    for pos in capsules:
        capsuleDistances.append(manhattan(position, pos))

    score = currentGameState.getScore()

    # if position in oldFood.asList():
    #     score += 40

    # if position in capsules:
    #     score += 80

    for i, dist in enumerate(ghostDistances):
        if dist < 4:
            if scaredTimes[i]:
                score += 1400
            else:
                score -= 650
        else:
            score -= 65 / dist

    for dist in foodDistances:
        score += 30 / dist

    for dist in capsuleDistances:
        score += 33 / dist

    return score

    # score = currentGameState.getScore()
    # print("\nscore: ", score)
    # score += closestCapsuleDistance * -0.5
    # score += closestFoodDistance * -0.3
    # print("score: ", score)

    # if scaredTimes[lowestGhostDistanceIndex] == 0:
    #     if ghostDistanceFromPacman < 3:
    #         score -= (ghostDistanceFromPacman) ** 3
    #     else:
    #         score -= ghostDistanceFromPacman * 0.5
    # else:
    #     score += 20

    # print("score: ", score)

    # score = currentGameState.getScore()
    # score += 20 / closestFoodDistance
    # score += 50 / closestCapsuleDistance

    # if scaredTimes[lowestGhostDistanceIndex]:
    #     score += 50
    # else:
    #     if closestGhostDistance < 5:
    #         score -= 200 / closestGhostDistance

    #     else:
    #         score -= 50 / (closestGhostDistance + 1)

    # return currentGameState.getScore() + score

    # capsuleWeight = 2

    # print(
    #     "closest: ", closestGhostDistance, closestFoodDistance, closestCapsuleDistance
    # )
    # score = (
    #     (closestFoodDistance * foodWeight)
    #     + (ghostWeight * closestGhostDistance)
    #     + (capsuleWeight * closestCapsuleDistance)
    #     + currentGameState.getScore()
    # )
    # print(score)
    # return score
    # return currentGameState.getScore()


class ContestAgent(MultiAgentSearchAgent):
    """
    Your agent for the mini-contest.

    You can use any method you want and search to any depth you want.
    Just remember that the mini-contest is timed, so you have to trade off speed and computation.

    Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
    just make a beeline straight towards Pacman (or away if they're scared!)

    Method to Implement:

    `pacai.agents.base.BaseAgent.getAction`
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)
