from pacai.agents.capture.reflex import ReflexCaptureAgent
import time
from pacai.util import util
import logging
import random


def createTeam(
    firstIndex,
    secondIndex,
    isRed,
    first="MyCaptureTheFlagAgentOne",
    second="MyCaptureTheFlagAgentTwo",
):
    """
    This function should return a list of two agents that will form the capture team,
    initialized using firstIndex and secondIndex as their agent indexed.
    isRed is True if the red team is being created,
    and will be False if the blue team is being created.
    """

    #to get rid of import util error
    util.buildHash()
    firstAgent = MyCaptureTheFlagAgentOne
    secondAgent = MyCaptureTheFlagAgentTwo

    return [
        firstAgent(firstIndex),
        secondAgent(secondIndex),
    ]


class MyCaptureTheFlagAgentOne(ReflexCaptureAgent):
    def chooseAction(self, gameState):
        """
        Picks among the actions with the highest return from `ReflexCaptureAgent.evaluate`.
        """

        
        actions = gameState.getLegalActions(self.index)

        start = time.time()
        values = [self.evaluate(gameState, a) for a in actions]

        # print(values)
        logging.debug(
            "evaluate() time for agent %d: %.4f" % (self.index, time.time() - start)
        )

        maxValue = max(values)
        bestActions = [a for a, v in zip(actions, values) if v == maxValue]
        # print(bestActions)

        return random.choice(bestActions)

    def evaluate(self, gameState, action):
        """
        Computes a linear combination of features and feature weights.
        """

        features = self.getFeatures(gameState, action)
        weights = self.getWeights(gameState, action)
        stateEval = sum(features[feature] * weights[feature] for feature in features)

        return stateEval

    def getFeatures(self, currentGameState, action):
        """
        Returns a dict of features for the state.
        The keys match up with the return from `ReflexCaptureAgent.getWeights`.
        """

        successorGameState = currentGameState.generateSuccessor(self.index, action)

        features = dict()

        newPosition = successorGameState.getAgentPosition(self.index)
        oldFood = self.getFood(currentGameState)
        oldCapsules = self.getCapsules(currentGameState)
        newEnemyStates = self.getOpponents(currentGameState)
        # newScaredTimes = [ghostState.getScaredTimer() for ghostState in newGhostStates]

        for enemy in newEnemyStates:
            ghostVal = 0
            enemyState = successorGameState.getAgentState(enemy)
            distToGhost = self.getMazeDistance(enemyState.getPosition(), newPosition)
            if enemyState.getScaredTimer() != 0:
                ghostVal += 200
                if distToGhost <= 2:
                    ghostVal += 500
            else:
                if distToGhost <= 6:
                    ghostVal -= 500
                else:
                    ghostVal -= 5 / distToGhost
        features["closestGhost"] = ghostVal

        foodVal = 0
        if newPosition in oldFood.asList():
            foodVal += 50
        else:
            for food in oldFood.asList():
                distToFood = self.getMazeDistance(food, newPosition)
                foodVal += 15 / distToFood
        features["closestFood"] = foodVal

        capsuleVal = 0
        if newPosition in oldCapsules:
            capsuleVal += 50
        elif len(oldCapsules) == 0:
            capsuleVal += 100
        else:
            for capsules in oldCapsules:
                distToCapsule = self.getMazeDistance(capsules, newPosition)
                capsuleVal += 15 / distToCapsule
        features["closestCapsule"] = capsuleVal

        return features

    def getWeights(self, gameState, action):
        """
        Returns a dict of weights for the state.
        The keys match up with the return from `ReflexCaptureAgent.getFeatures`.
        """

        weights = dict()
        features = self.getFeatures(gameState, action)
        for feature, val in features.items():
            weights[feature] = 1

            if feature == "closestFood":
                weights[feature] = 1

            elif feature == "closestGhost":
                weights[feature] = 2

            elif feature == "successorScore":
                weights[feature] = 1

            elif feature == "closestCapsule":
                weights[feature] = 2

            elif feature == "numOpponents":
                weights[feature] = 1
        # print(weights)
        return weights


class MyCaptureTheFlagAgentTwo(ReflexCaptureAgent):
    """
    A reflex agent that tries to keep its side Pacman-free.
    This is to give you an idea of what a defensive agent could be like.
    It is not the best or only way to make such an agent.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index)

    def getFeatures(self, gameState, action):
        features = {}

        successor = self.getSuccessor(gameState, action)
        myState = successor.getAgentState(self.index)
        myPos = myState.getPosition()

        # if the next successor position is on the otherside, return 0 (agent is defensive)

        if self.red and myPos[0] >= (gameState.getInitialLayout().width // 2):
            return {}
        elif not self.red and myPos[0] <= (gameState.getInitialLayout().width // 2):
            return {}

        # Computes distance to invaders we can see.
        enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
        invaders = [a for a in enemies if a.isPacman() and a.getPosition() is not None]

        if len(invaders) > 0:
            dists = [self.getMazeDistance(myPos, a.getPosition()) for a in invaders]
            features["invaderDistance"] = 100 / min(dists)

        # distance from center if theres no invaders
        if not invaders:
            distFromCenter = self.getMazeDistance(
                myPos,
                (
                    gameState.getInitialLayout().width // 2,
                    (gameState.getInitialLayout().height // 2),
                ),
            )
            features["distanceFromCenter"] = 1000 / distFromCenter

        return features

    def getWeights(self, gameState, action):
        weights = dict()
        features = self.getFeatures(gameState, action)
        for feature, val in features.items():
            weights[feature] = 1
        # print(weights)
        return weights
