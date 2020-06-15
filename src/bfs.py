
#import/define a queue

#shall return a boolean
def bfs(problem):
    """Search the shallowest nodes in the search tree first."""
    #Same implementation than DFS but using a Queue
    from util import Queue
    fringe = Queue()
    # To check the nodes we've already explored
    explored = []
    # adding the start_state in the fringe
    fringe.push((problem.getStartState(), []))
    # current_node, action = fringe.pop()
    # print(problem.getSuccessors(current_node))

    while fringe.isEmpty() == False:
        # actionsToDo is the list of actions we will return
        current_node, actionsToDo = fringe.pop()
        # if we have already visited the node, ignore what's left in the loop
        if current_node in explored:
            continue
        explored.append(current_node)
        # if we reached the goal state return actions we've done
        if problem.isGoalState(current_node):
            return actionsToDo
        for next_node in (problem.getSuccessors(current_node)):
            # next_node[0] are the coordinates
            # next_node[1] is the path from current_node to next_node
            updated_actions = actionsToDo + [next_node[1]]
            fringe.push((next_node[0], updated_actions))
