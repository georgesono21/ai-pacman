"""
In this file, you will implement generic search algorithms which are called by Pacman agents.
"""

from pacai.util.stack import Stack
from pacai.util.queue import Queue
from pacai.util.priorityQueue import PriorityQueue


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first [p 85].

    Your search algorithm needs to return a list of actions that reaches the goal.
    Make sure to implement a graph search algorithm [Fig. 3.7].

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
    ```
    print("Start: %s" % (str(problem.startingState())))
    print("Is the start a goal?: %s" % (problem.isGoal(problem.startingState())))
    print("Start's successors: %s" % (problem.successorStates(problem.startingState())))
    ```
    """

    # *** Your Code Here ***

    visited = [problem.startingState()]
    stack = Stack()
    stack.push((problem.startingState(), []))

    while stack:
        top = stack.pop()
        possibleActions = problem.successorStates(top[0])

        if problem.isGoal(top[0]):
            # print(len(top[1]))
            return top[1]
            # break

        for action in possibleActions:
            successor = action[0]
            if successor not in visited:
                visited.append(successor)
                newPath = top[1].copy()
                newPath.append(action[1])
                stack.push((successor, newPath))

    return []


def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first. [p 81]
    """

    # *** Your Code Here ***

    visited = [problem.startingState()]
    queue = Queue()
    queue.push((problem.startingState(), []))

    while queue:
        top = queue.pop()
        # print("top[0]: ", top[0])

        if problem.isGoal(top[0]):
            # print(len(top[1]))
            return top[1]

        possibleActions = problem.successorStates(top[0])
        for action in possibleActions:
            successor = action[0]
            # successor = action
            if successor not in visited:
                visited.append(successor)
                newPath = top[1].copy()
                newPath.append(action[1])
                queue.push((successor, newPath))

    return []


def uniformCostSearch(problem):  # food search problem
    """
    Search the node of least total cost first.
    """

    visited = [problem.startingState()]
    pQueue = PriorityQueue()
    pQueue.push((problem.startingState(), [], 0), 0)

    while pQueue:
        top = pQueue.pop()
        possibleActions = problem.successorStates(top[0])

        if problem.isGoal(top[0]):
            # print(len(top[1]))
            return top[1]

        for action in possibleActions:
            successor = action[0]
            if successor not in visited:
                visited.append(successor)
                newPath = top[1].copy()
                newPath.append(action[1])
                pQueue.push(
                    (successor, newPath, top[2] + action[2]), top[2] + action[2]
                )

    return []

    raise NotImplementedError()


def aStarSearch(problem, heuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """

    # print(problem.successorStates(problem.startingState()))
    # print(type(heuristic(sta)))
    visited = [problem.startingState()]
    pQueue = PriorityQueue()
    pQueue.push((problem.startingState(), [], 0), 0)

    while pQueue:
        top = pQueue.pop()
        possibleActions = problem.successorStates(top[0])

        if problem.isGoal(top[0]):
            # print(len(top[1]))
            return top[1]

        for action in possibleActions:
            successor = action[0]
            if successor not in visited:
                visited.append(successor)
                newPath = top[1].copy()
                newPath.append(action[1])
                pQueue.push(
                    (successor, newPath, top[2] + action[2]),
                    top[2] + action[2] + heuristic(successor, problem),
                )

    return []

    # *** Your Code Here ***
    raise NotImplementedError()


#         1
#       /    \
#     2       3
#   /   \
# 4       5

# actions:
# stack: (1,[1])
# stack: (2,[[1,2]], 3, [1,3])


# S: 1
# G: 5

# P:
# [1: None
#  2: 1
#  3: 1
#  4: 2
#  5: 2
#  ]

# stack = [4, 5]

# parent[5] = 2
# parent[2] = 1 == source

# 1, 2,
