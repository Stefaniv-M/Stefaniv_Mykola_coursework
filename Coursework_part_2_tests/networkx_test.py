import networkx as nx
import matplotlib.pyplot as plt

graph_1 = nx.Graph()
graph_1.add_nodes_from(["textnode", 3, 4, 57, 5.66, "lastnode"])
graph_1.add_edge("textnode", 3)
graph_1.add_edge("textnode", "lastnode")

nx.draw_networkx(graph_1)

i = input("Type 'yes' if you want graph to be shown interactively, type anything else to save it into a .png file: ")
if i == "yes":
    plt.show()
else:
    plt.savefig("testfile.png")
