from src.bfs import bfs

parentNode = []
INF = 99999999

def Ford_Fulkerson(graph, source, sink):
    #on an adjacency matrix
    u = 0
    v = 0
    residualGraph = graph #graph we will modify to determine the maxflow
    maxFlow = 0

    while(bfs(residualGraph, source, sink, parentNode)): #if we find a path in the residual graph, execute ford-fulkerson

        pathFlow = INF
        v = sink

        while v != source:
            u = parentNode[v]
            pathFlow = min(pathFlow, residualGraph[u][v])
            v = parentNode[v]

        v = sink



