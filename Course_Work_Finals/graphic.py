import networkx as nx
import matplotlib.pyplot as plt
from user_trees import *
from user_tree_functions import *
from twitter_access_stuff import *


def full_trees_draw(tree_1, tree_2, show=False, save=False, image_name=""):
    """
    Create graph with full trees tree_1 and tree_2. If show is True,
    show graph. If save is True, save graph with image_name
    :param tree_1: User
    :param tree_2: User
    :param save: bool
    :param show: bool
    :param image_name: str
    :return: NoneType
    """
    api = authorise(consumer_key, consumer_secret, access_token, access_token_secret)

    graph = nx.Graph()

    # Creating a dictionary with ids and names of the users:
    all_users = tree_1.all_users() + [tree_1, tree_2] + tree_2.all_users()
    all_ids = [user.get_id_num() for user in all_users]

    id_names_dict = dict()

    for id_num in all_ids:
        user = get_user(api, id_num)
        name = user.screen_name
        id_names_dict[id_num] = name

    # Now adding nodes to graph:
    graph.add_nodes_from([id_names_dict[id_1] for id_1 in all_ids])

    # Adding edges:
    for user in all_users:
        user_name = id_names_dict[user.get_id_num()]
        children = user.get_children()
        for child in children:
            child_name = id_names_dict[child.get_id_num()]
            graph.add_edge(user_name, child_name)

    # Putting graph into plot:
    nx.draw_networkx(graph)

    # Showing graph:
    if show:
        plt.show()

    # Saving graph:
    if save:
        plt.savefig(image_name)

    plt.close()

    return None


def only_links(list_of_links, show=False, save=False, image_name=""):
    """
    Same, but show only links on a graph. Each link is list with ids.
    :param list_of_links: list of list
    :param show: bool
    :param save: bool
    :param image_name: str
    :return: NoneType
    """
    api = authorise(consumer_key, consumer_secret, access_token, access_token_secret)

    graph = nx.Graph()

    # Create list of all ids:
    all_ids = []
    for link in list_of_links:
        for id_num in link:
            if id_num not in all_ids:
                all_ids.append(id_num)

    # Dictionary with ids and names:
    id_names_dict = dict()

    for id_num in all_ids:
        user = get_user(api, id_num)
        name = user.screen_name
        id_names_dict[id_num] = name

    # Add nodes to graph:
    graph.add_nodes_from([id_names_dict[id_1] for id_1 in all_ids])

    # Adding edges:
    for link in list_of_links:
        for i in range(len(link) - 1):
            id_1, id_2 = link[i], link[i + 1]
            name_1, name_2 = id_names_dict[id_1], id_names_dict[id_2]
            graph.add_edge(name_1, name_2)

    # Putting graph into plot:
    nx.draw_networkx(graph)

    # Showing graph:
    if show:
        plt.show()

    # Saving graph:
    if save:
        plt.savefig(image_name)

    plt.close()


def draw_all_friends(tree, show=False, save=False, image_name=""):
    """
    Draw full tree.
    :param show: bool
    :param save: bool
    :param image_name: str
    :param tree: User
    :return: NoneType
    """
    api = authorise(consumer_key, consumer_secret, access_token, access_token_secret)

    graph = nx.Graph()

    # Creating a dictionary with ids and names of the users:
    all_users = tree.all_users() + [tree]
    all_ids = [user.get_id_num() for user in all_users]

    id_names_dict = dict()

    for id_num in all_ids:
        user = get_user(api, id_num)
        name = user.screen_name
        id_names_dict[id_num] = name

    # Now adding nodes to graph:
    graph.add_nodes_from([id_names_dict[id_1] for id_1 in all_ids])

    # Adding edges:
    for user in all_users:
        user_name = id_names_dict[user.get_id_num()]
        children = user.get_children()
        for child in children:
            child_name = id_names_dict[child.get_id_num()]
            graph.add_edge(user_name, child_name)

    # Putting graph into plot:
    nx.draw_networkx(graph)

    # Showing graph:
    if show:
        plt.show()

    # Saving graph:
    if save:
        plt.savefig(image_name)

    plt.close()

    return None
