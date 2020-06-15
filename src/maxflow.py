from src.bfs import bfs

parentNode = []
INF = 99999999

def Ford_Fulkerson(graph, source, sink):
    #on an adjacency matrix
    u = 0
    v = 0
    residualGraph = graph #graph we will modify to determine the maxflow
    maxFlow = 0

    #while we find a path in the residual graph, execute ford-fulkerson
    while(bfs(residualGraph, source, sink, parentNode)):

        pathFlow = INF
        v = sink

        #find the smallest pathFlow of the current path
        while v != source: #go to the previous node until we get back to the source
            u = parentNode[v]
            pathFlow = min(pathFlow, residualGraph[u][v]) #get the smallest value of the past in order to make the soustraction
            v = parentNode[v]

        #substract the weight of the smallest pathFlow to the other weight of the path
        v = sink
        while v != source:
            u = parentNode



