from src.bfs import bfs

parentNode = []
INF = 99999999

def printMincut(residualGraph, source, sink):
    # we will use the residual graph to determine the min cut
    realGraph = [i[:] for i in residualGraph]
    rows = len(residualGraph)
    columns = len(residualGraph[0])
    #on an adjacency matrix
    u = 0
    v = 0

    maxFlow = 0
    parentNode = [-5] * rows #inconsistent values for now since we don't know the parent nodes
    #while we find a path in the residual graph, execute ford-fulkerson
    while(bfs(residualGraph, source, sink, parentNode)):

        pathFlow = INF
        v = sink

        #find the smallest pathFlow of the current path
        while v != source: #go to the previous node until we get back to the source
            u = parentNode[v]
            pathFlow = min(pathFlow, residualGraph[u][v]) #get the smallest value of the past in order to substract
            v = parentNode[v]

        #substract the weight of the smallest pathFlow to the other weight of the path
        v = sink
        while v != source:
            u = parentNode[v]
            residualGraph[u][v] -= pathFlow #substract the smallest pathFlow weight
            residualGraph[v][u] += pathFlow #add the weight in the opposte direction [reste légèrement flou]
            v = parentNode[v]

        maxFlow += pathFlow

    for i in range(rows):
        for j in range(columns):
            if residualGraph[i][j] == 0 and realGraph[i][j] > 0: #
                print(str(i) + " - " + str(j))

    #print(residualGraph)

#what's next :
#get the cut graph