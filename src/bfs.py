# https://www.youtube.com/watch?v=GoVjOT30xwo&t=1s
#shall return a boolean
def bfs(residualGraph, source, sink, parentNode):
    """Search the shallowest nodes in the search tree first."""
    #Same implementation than DFS but using a Queue
    queue = []
    # To check the nodes we've already explored
    explored = []
    # adding the start_state in the fringe
    queue.push() #add startState                    !!!!!!!! 
    # current_node, action = fringe.pop()
    # print(problem.getSuccessors(current_node))

    while queue.isEmpty() == False:
        # actionsToDo is the list of actions we will return
        current_node, actionsToDo = queue.pop()
        # if we have already visited the node, ignore what's left in the loop
        if current_node in explored:
            continue
        explored.append(current_node)
        if problem.isGoalState(current_node):
            return actionsToDo
        for next_node in (problem.getSuccessors(current_node)):
            updated_actions = actionsToDo + [next_node[1]]
            queue.push((next_node[0], updated_actions))
