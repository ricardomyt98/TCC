import urllib.request
import io
import zipfile
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import pyplot as plt
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


def print_pair_paths(i, j) -> None:
    msg = "i: {}".format(i)
    spaces = 20 - len(msg)
    for n in range(spaces):
        msg += " "
    msg += "j: {}".format(j)
    print(msg)


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
        msg = "path: [{}]".format(key)
        spaces = 50 - len(msg)
        for i in range(spaces):
            msg += " "
        msg += "centrality: [{}]".format(value.centrality)
        print(msg)


def plot_weights(pathDict: dict) -> None:

    path = list(pathDict.keys())
    centrality = []

    for x in pathDict.values():
        centrality.append(x.centrality)

    # Figure Size
    fig, ax = plt.subplots(figsize=(16, 9))

    # Horizontal Bar Plot
    ax.barh(path, centrality)

    # Remove axes splines
    for s in ['top', 'bottom', 'left', 'right']:
        ax.spines[s].set_visible(False)

    # Remove x, y Ticks
    ax.xaxis.set_ticks_position('none')
    ax.yaxis.set_ticks_position('none')

    # Add padding between axes and labels
    ax.xaxis.set_tick_params(pad=5)
    ax.yaxis.set_tick_params(pad=10)

    # Add x, y gridlines
    ax.grid(b=True, color='grey', linestyle='-.', linewidth=0.5, alpha=0.2)

    # Show top values
    ax.invert_yaxis()

    # Add annotation to bars
    for i in ax.patches:
        plt.text(i.get_width()+0.2, i.get_y()+0.5, str(round((i.get_width()), 2)),
                 fontsize=10, fontweight='bold', color='grey')

    # Add Plot Title
    ax.set_title('Path Centrality Distribution', loc='left', )

    # Show Plot
    plt.show()


def plot_graph(G) -> None:
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


def simple_graph_generator():
    G = nx.Graph()
    G.add_edge(1, 2)
    G.add_edge(1, 3)
    G.add_edge(1, 5)
    G.add_edge(2, 3)
    G.add_edge(3, 4)
    G.add_edge(4, 5)
    return(G)


def karate_club_graph_generator():
    G = nx.karate_club_graph()
    # for v in G:
    #     print(f"{v:4} {G.degree(v):6}")
    return(G)


def football_graph_generator():
    url = "http://www-personal.umich.edu/~mejn/netdata/football.zip"

    sock = urllib.request.urlopen(url)  # open URL
    s = io.BytesIO(sock.read())  # read into BytesIO "file"
    sock.close()

    zf = zipfile.ZipFile(s)  # zipfile object
    txt = zf.read("football.txt").decode()  # read info file
    gml = zf.read("football.gml").decode()  # read gml data
    # throw away bogus first line with # from mejn files
    gml = gml.split("\n")[1:]
    G = nx.parse_gml(gml)  # parse gml data
    return G

def plot_centrality_values(pathDict: dict) -> None:
    l = []

    for val in pathDict.values():
        if val.centrality not in l:
            l.append(val.centrality)

    l.sort()

    plt.plot(l)
    plt.ylabel('Shortest paths centrality distribution')
    plt.ylabel('Shortest path enumeration')
    plt.show()


def main() -> None:
    # G = simple_graph_generator()
    # G = karate_club_graph_generator()
    G = football_graph_generator()

    # print(G.number_of_nodes())
    # print(G.number_of_edges())

    # plot_graph(G)

    dijkstraTrees = get_dijkstra_trees_from_a_graph(G)
    shortestPaths = get_shortest_paths_from_dijkstra_trees(dijkstraTrees)
    all_shortest_paths_centrality(shortestPaths)
    # plot_weights(shortestPaths)
    print_all_paths_and_centrality(shortestPaths)

    # plot_centrality_values(shortestPaths)


main()
