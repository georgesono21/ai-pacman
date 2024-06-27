from pacai.agents.learning.value import ValueEstimationAgent


class ValueIterationAgent(ValueEstimationAgent):
    """
    A value iteration agent.

    Make sure to read `pacai.agents.learning` before working on this class.

    A `ValueIterationAgent` takes a `pacai.core.mdp.MarkovDecisionProcess` on initialization,
    and runs value iteration for a given number of iterations using the supplied discount factor.

    Some useful mdp methods you will use:
    `pacai.core.mdp.MarkovDecisionProcess.getStates`,
    `pacai.core.mdp.MarkovDecisionProcess.getPossibleActions`,
    `pacai.core.mdp.MarkovDecisionProcess.getTransitionStatesAndProbs`,
    `pacai.core.mdp.MarkovDecisionProcess.getReward`.

    Additional methods to implement:

    `pacai.agents.learning.value.ValueEstimationAgent.getQValue`:
    The q-value of the state action pair (after the indicated number of value iteration passes).
    Note that value iteration does not necessarily create this quantity,
    and you may have to derive it on the fly.

    `pacai.agents.learning.value.ValueEstimationAgent.getPolicy`:
    The policy is the best action in the given state
    according to the values computed by value iteration.
    You may break ties any way you see fit.
    Note that if there are no legal actions, which is the case at the terminal state,
    you should return None.
    """

    def __init__(self, index, mdp, discountRate=0.9, iters=100, **kwargs):
        super().__init__(index, **kwargs)

        self.mdp = mdp
        self.discountRate = discountRate
        self.iters = iters
        self.values = {}  # A dictionary which holds the q-values for each state.

        # Compute the values here.

        states = self.mdp.getStates()
        # for state in states:
        #     self.values[state] = 0

        for iter in range(iters):
            newValues = {}
            for state in states:
                if self.mdp.isTerminal(state):
                    newValues[state] = 0
                    continue

                # qValues = list()
                maxQ = float('-inf')
                for action in self.mdp.getPossibleActions(state):
                    qValue = self.getQValue(state, action)

                    maxQ = max(maxQ, qValue)
                    # qValues.append(qValue)

                # if not qValues:
                #     newValues[state] = 0
                # else:
                #     newValues[state] = max(qValues)
                newValues[state] = maxQ
            self.values = newValues

            print(self.values)

        # raise NotImplementedError

    def getQValue(self, state, action):
        if self.mdp.isTerminal(state):
            return 0

        transitionStatesAndProb = self.mdp.getTransitionStatesAndProbs(state, action)
        qValue = 0
        for transState, prob in transitionStatesAndProb:
            qValue += prob * (
                self.mdp.getReward(state, action, transState)
                + (self.discountRate * self.getValue(transState))
            )

        return qValue

    def getPolicy(self, state):
        # return super().getPolicy(state)

        if self.mdp.isTerminal(state):
            return None

        maxQValue = float('-inf')
        maxQValueAction = None
        for action in self.mdp.getPossibleActions(state):
            # if action == "exit":
            #    return "exit"

            qValue = self.getQValue(state, action)

            if qValue > maxQValue:
                maxQValue = qValue
                maxQValueAction = action

        return maxQValueAction

    def getValue(self, state):
        """
        Return the value of the state (computed in __init__).
        """

        return self.values.get(state, 0.0)

    def getAction(self, state):
        """
        Returns the policy at the state (no exploration).
        """

        return self.getPolicy(state)
