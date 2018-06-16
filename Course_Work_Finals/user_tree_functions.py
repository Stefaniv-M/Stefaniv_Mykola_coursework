import tweepy
import copy
from user_trees import User
import time
from twitter_access_stuff import *


class UserNotFoundError(Exception):
    """
    Return is there is no such Twitter user.
    """
    pass


def authorise(consumer_key, consumer_secret, access_token, access_token_secret):
    """
    Return api object from access tokens and keys.
    :param consumer_key: str
    :param consumer_secret: str
    :param access_token: str
    :param access_token_secret: str
    :return: tweepy.api.API
    """
    # Authorisation:
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    # Creating api object:
    api = tweepy.API(auth)

    # Finally:
    return api


def get_user(api, user_name):
    """
    Return user object if there is user with such name on Twitter. Raise UserNotFoundError if there is no
    such user on Twitter. If user_name is integer number, search by id.
    :param api: tweepy.api.API
    :param user_name: str or int.
    :return: tweepy.models.User
    """
    # Checking input:
    if not isinstance(user_name, str) and not isinstance(user_name, int):
        raise ValueError("You can only get user by his/her id (int) or name (str).")

    # Main part:
    try:
        user = api.get_user(user_name)
        return user
    except tweepy.error.TweepError:
        raise UserNotFoundError("No Twitter user with such name/id exists.")


def get_friends(user):
    """
    Return list of friends of user. If rate limit is exceeded, it will wait 15 minutes.
    :param user: tweepy.models.User
    :return: list of tweepy.models.User
    """
    try:
        friends = user.friends()
        return friends[:]
    except tweepy.error.RateLimitError:
        print("Rate limit reached! Waiting...")
        wait_15_minutes()
        return get_friends(user)
    except tweepy.error.TweepError:
        print("Skipping user whose information is protected.")
        return list()


def get_friends_ids(api, user_id):
    """
    Return list of ids of friends of the user with given id.
    :param api: tweepy.api.API
    :param user_id: int
    :return: list of int
    """
    # Getting user object:
    user = get_user(api, user_id)

    # Getting list of friends of the user:
    friends = get_friends(user)

    # Returning ids of friends of the user:
    return [friend.id for friend in friends]


def build_friend_tree(api, user_id, height):
    """
    Return tree of friends of a user with given depth( 1 - only friends, 2 - plus friends of friends, ...).
    :param api: tweepy.api.API
    :param user_id: int
    :param height: int
    :return: User
    """
    # Checking arguments:
    if not isinstance(user_id, int) or not isinstance(height, int):
        raise ValueError("User id and height of a tree must be int.")

    # Checking if height is correct:
    if not (0 < height < 10):
        raise ValueError("Height must be integer number from 1 to 9.")

    # Checking if such user exists - this will raise error if not:
    get_user(api, user_id)

    # Main part of the function:
    tree_root = User(user_id)

    # "Growing" tree level by level:
    for level in range(height):
        # Getting all users of current level of search:
        users_on_level = tree_root.users_of_level(level)

        # For each of those users getting friends and adding them:
        for user in users_on_level:
            # Getting list of ids of friends of the user:
            friends_ids = get_friends_ids(api, user.get_id_num())

            # Creating a list of User objects:
            friends_users = [User(friend_id) for friend_id in friends_ids]

            # Adding children (method will even mark duplicates):
            user.set_children(friends_users)

    # Returning tree:
    return tree_root


def wait_15_minutes():
    """
    Wait for 15 minutes and print current waiting time.
    :return: NoneType
    """
    # Waiting:
    for i in range(15):
        if i == 14:
            print("1 minute of waiting left.")
        else:
            print("{} minutes of waiting left.".format(15 - i))
        time.sleep(60)

    # Just in case:
    time.sleep(5)

    # After waiting:
    print("Waiting ended!")
    return None


def dict_from_file(file_name):
    """
    Read information about users from a text file and enter it into a dictionary.
    :param file_name: str
    :return: dict
    """
    # Checking input:
    if not isinstance(file_name, str) or not file_name.endswith(".txt"):
        raise ValueError("Name of the file must be str, and have .txt extension.")

    # Reading from file:
    file = open(file_name, "r")
    lines = file.readlines()
    file.close()

    # Removing "\n" from the end of each line and turning each element into an integer:
    for i in range(len(lines)):
        lines[i] = int(lines[i][:-1])

    # Stopping the function if lines is empty:
    if not lines:
        return dict()

    # Recording everything into a dictionary:
    result_dict = dict()
    last_key = lines[0]

    """
    In text file, everything is like that (child elements are children of first parent above them):
    parent
    -child
    -child
    -child
    parent
    parent
    parent
    -child
    -child
    """

    for i in range(len(lines)):
        if lines[i] > 0:
            last_key = lines[i]
            result_dict[last_key] = []
        else:
            result_dict[last_key].append(-1 * lines[i])

    # Finally:
    return result_dict


def tree_from_dict(user_id, user_dict, height):
    """
    Create tree from id of the user and dictionary of friends of users.
    :param user_id: int
    :param user_dict: dict
    :param height: int
    :return: User
    """
    # Checking input:
    if not isinstance(user_id, int) or user_id < 0 or not isinstance(user_dict, dict):
        raise ValueError("Id of the user must be int bigger than zero, and user_dict must be dict.")

    # Checking if height is correct:
    if not (0 < height < 10):
        raise ValueError("Height must be integer number from 1 to 9.")

    # Creating a root:
    tree_root = User(user_id)

    # Building a tree level by level:
    for level in range(height):
        # Getting all users of current level of search:
        users_on_level = tree_root.users_of_level(level)

        # For each of those users getting friends and adding them:
        for user in users_on_level:
            # Getting list of ids of friends of the user:
            friends_ids = user_dict[user.get_id_num()]

            # Creating a list of User objects:
            friends_users = [User(friend_id) for friend_id in friends_ids]

            # Adding children (method will even mark duplicates):
            user.set_children(friends_users)

    # Finally:
    return tree_root


def find_mutual_ids(tree_1, tree_2):
    """
    Return ids of mutual users of tree_1 and tree_2 as list.
    :param tree_1: User
    :param tree_2: User
    :return: list of int
    """
    # Getting lists of all the users:
    all_users_1 = tree_1.all_users() + [tree_1]
    all_users_2 = tree_2.all_users() + [tree_2]

    result_list = []

    # Changing types of values in lists:
    all_users_1 = [user.get_id_num() for user in all_users_1]
    all_users_2 = [user.get_id_num() for user in all_users_2]

    # Checking:
    for user in all_users_1:
        if user in all_users_2:
            result_list.append(user)

    return result_list


def find_link_length(user_id, tree_1, tree_2):
    """
    Find length of link between two users (tree_1 and tree_1 roots) from the user with user_id. It
    is assummed that user_id is in both trees.
    :param user_id: int
    :param tree_1: User
    :param tree_2: User
    :return: int
    """
    # Representations of users in both trees:
    user_1 = tree_1.user_by_id(user_id)
    user_2 = tree_2.user_by_id(user_id)

    return user_1.get_level() + user_2.get_level()


def find_min_link(ids_list, tree_1, tree_2):
    """
    Return id of the user by which tree_1 and tree_2 roots are connected by least amount of mutual friends.
    :param ids_list: list of int
    :param tree_1: User
    :param tree_2: User
    :return: int
    """
    # Checking input:
    if not isinstance(ids_list, list) or not isinstance(tree_1, User) or not isinstance(tree_2, User):
        raise ValueError("Incorrect arguments.")

    result_id = ids_list[0]
    for id1 in ids_list:
        if find_link_length(id1, tree_1, tree_2) < find_link_length(result_id, tree_1, tree_2):
            result_id = id1

    return result_id


def link_to_list(id_num, tree_1, tree_2):
    """
    Return list of ids connecting two users - roots of tree_1 and tree_2 (including ids of those users).
    :param id_num: int
    :param tree_1: User
    :param tree_2: User
    :return: list
    """
    # Checking input:
    if not isinstance(id_num, int) or id_num < 0 or not isinstance(tree_1, User) or not isinstance(tree_2, User):
        raise ValueError("Incorrect function arguments!")

    result_list = [id_num]

    # User representation in tree_1:
    user_1 = tree_1.user_by_id(id_num)
    while user_1.get_parent() is not None:
        user_1 = user_1.get_parent()
        result_list = [user_1.get_id_num()] + result_list

    # ... in tree_2:
    user_2 = tree_2.user_by_id(id_num)
    while user_2.get_parent() is not None:
        user_2 = user_2.get_parent()
        result_list.append(user_2.get_id_num())

    return result_list


def link_to_string(link_list):
    """
    Return string representation of a link list.
    :param link_list: list of int
    :return: str
    """
    api = authorise(consumer_key, consumer_secret, access_token, access_token_secret)

    list_of_names = []

    for id_num in link_list:
        list_of_names.append(get_user(api, id_num).screen_name)

    # Creating string:
    result_str = ""
    for i in range(len(list_of_names) - 1):
        result_str = result_str + list_of_names[i] + " <-> "

    result_str = result_str + list_of_names[-1]

    return result_str
