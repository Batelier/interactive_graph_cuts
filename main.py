from src import ford_fulkerson

print("Interactive Graph Cut for Comuter Vision \nBased on Jolly and and Boykov Paper")

graph = [[0, 16, 13, 0, 0, 0],
        [0, 0, 10, 12, 0, 0],
        [0, 4, 0, 0, 14, 0],
        [0, 0, 9, 0, 0, 20],
        [0, 0, 0, 7, 0, 4],
        [0, 0, 0, 0, 0, 0]]

source = 0 #source node
sink = 5 #sink node
ford_fulkerson.printMincut(graph, source, sink)

