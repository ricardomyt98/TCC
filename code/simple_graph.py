import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms import centrality
from networkx.algorithms.shortest_paths.weighted import single_source_dijkstra
from networkx.classes import graph


class PathInfo:
    def __init__(self, centrality: int, numNodes: int) -> None:
        self.centrality = centrality
        self.numNodes = numNodes


def get_dijkstra_trees_from_a_graph(g: dict) -> dict:
    graphDict = {}

    for node in g:
        if node not in graphDict:
            graphDict[node] = single_source_dijkstra(g, node)[1]

    return graphDict


def get_shortest_paths_from_dijkstra_trees(graphDict: dict) -> dict:
    pathDict = {}

    for i in graphDict.values():
        for j in i.values():
            path = str(j).replace("[", "").replace("]", "")
            if path not in pathDict and len(path) > 1:
                newPathInfo = PathInfo(0, len(j))
                pathDict[path] = newPathInfo

    return pathDict


def all_shortest_paths_centrality(pathDict: dict) -> dict:
    # For each shortest path (i), check if it is contained in another (j). If it is, plus one
    for i in pathDict:
        for j in pathDict:
            if i in j:
                pathDict[i].centrality += 1

    # Get the number of Dijkstra trees
    numDijkstraTrees = len(pathDict)

    # Normalizing centrality values
    for path in pathDict:
        pathDict[path].centrality /= numDijkstraTrees * pathDict[path].numNodes


def print_all_paths_and_centrality(pathDict: dict) -> None:
    for key, value in pathDict.items():
        msg = "path: {}".format(key)
        spaces = 20 - len(msg)
        for i in range(spaces):
            msg += " "
        msg += "centrality: {}".format(value.centrality)
        print(msg)

def main() -> None:
    G = nx.Graph()
    G.add_edge(1, 2)
    G.add_edge(1, 3)
    G.add_edge(1, 5)
    G.add_edge(2, 3)
    G.add_edge(3, 4)
    G.add_edge(4, 5)

    # Explicitly set positions
    pos = {1: (0, 0), 2: (-1, 0.3), 3: (2, 0.17), 4: (4, 0.255), 5: (5, 0.03)}

    options = {
        "font_size": 36,
        "node_size": 3000,
        "node_color": "white",
        "edgecolors": "black",
        "linewidths": 5,
        "width": 5,
    }
    nx.draw_networkx(G, pos, **options)

    # Set margins for the axes so that nodes aren't clipped
    ax = plt.gca()
    ax.margins(0.20)
    plt.axis("off")
    plt.show()

    dijkstraTrees = get_dijkstra_trees_from_a_graph(G)
    shortestPaths = get_shortest_paths_from_dijkstra_trees(dijkstraTrees)
    all_shortest_paths_centrality(shortestPaths)
    print_all_paths_and_centrality(shortestPaths)

main()
