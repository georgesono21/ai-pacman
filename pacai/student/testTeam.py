from pacai.agents.capture.capture import CaptureAgent
from pacai.agents.capture.reflex import ReflexCaptureAgent
from pacai.agents.capture.defense import DefensiveReflexAgent
from pacai.agents.capture.offense import OffensiveReflexAgent
import time
from pacai.util import util
from pacai.core.directions import Directions
import logging
import random
from pacai.core.directions import Directions
from pacai.core.distance import maze

def createTeam(firstIndex, secondIndex, isRed,
        first = 'MyCaptureTheFlagAgentOne',
        second = 'MyCaptureTheFlagAgentTwo'):
    """
    This function should return a list of two agents that will form the capture team,
    initialized using firstIndex and secondIndex as their agent indexed.
    isRed is True if the red team is being created,
    and will be False if the blue team is being created.
    """

    firstAgent = DefensiveReflexAgent
    secondAgent = OffensiveReflexAgent

    return [
        firstAgent(firstIndex),
        secondAgent(secondIndex),
    ]
    