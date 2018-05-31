class User:
    """
    Node of tree of users and their friends.
    Each node is more independent for my
    convenience.
    """
    def __init__(self, id_num):
        """
        Initialise User by his id number.
        :param id_num: int
        """
        # Checking argument:
        if not isinstance(id_num, int):
            raise ValueError("User Id number must be int.")

        # Setting everything:
        self._id_num = id_num
        self._parent = None
        self._children = None

        # This argument is True if User is already somewhere
        # higher in a tree:
        self.already_was_in_tree = False

    def get_parent(self):
        """
        Return parent user of this one.
        :return: User or NoneType
        """
        return self._parent

    def get_id_num(self):
        """
        Return Id number of the user.
        :return: int
        """
        return self._id_num

    def get_children(self, ignore_repeated=True):
        """
        Return list of all children of a current User.
        If ignore_repeated is True, users who are repeated are
        not returned in resulting list.
        :param ignore_repeated: bool
        :return: list
        """
        # If current user has no children (friends):
        if self._children is None:
            return []

        result_list = []
        for child in self._children:
            if not(child.already_was_in_tree and ignore_repeated):
                result_list.append(child)
        return result_list

    def get_root(self):
        """
        Return root user of a tree given user is in (if given user
        is not in a tree, the method will return given user).
        :return: User
        """
        # Setting cursor for a current user:
        current_user = self

        # Moving cursor upward through the tree until there is
        # nowhere to go:
        while current_user.get_parent() is not None:
            current_user = current_user.get_parent()

        # Finally:
        return current_user

    def is_root(self):
        """
        Return True if current User is root of a tree.
        :return: bool
        """
        return self._parent is None

    def all_users(self, ignore_repeated=True):
        """
        Return all the users that are children of a current node.
        Current node is not included in result list. If
        ignore_repeated is True, the program won't return copies of
        users (setting it to False may be useful when building a
        graph).
        :param ignore_repeated: bool
        :return: list
        """
        result_list = []

        # This is a recursive method:

        # If current user does not have children (friends):
        if self._children is None:
            # Return an empty list:
            return []
        # Otherwise:
        else:
            for child in self._children:
                # Condition to ignore repeated users:
                if not (ignore_repeated and
                        child.already_was_in_tree):
                    result_list.append(child)
                    # Recursive call:
                    result_list = result_list + \
                        child.all_users(ignore_repeated)

            return result_list

    def height(self):
        """
        Return height of a tree with current user as a root.
        :return: int
        """
        h = 0
        current_node = self

        # Going down until there is nowhere to go (it is
        # assumed that tree is perfectly balanced every time):
        while current_node._children is not None:
            h += 1
            current_node = current_node._children[0]

        # Finally:
        return h

    def get_level(self):
        """
        Get level of a current user in a tree (level of a root
        is 0, level of children of the root is 1, and so fourth).
        :return: int
        """
        return self.get_root().height() - self.height()

    def users_of_level(self, level_num, ignore_repeated=True):
        """
        Return all users of a level level_num of a tree with
        root as a current user.
        :param level_num: int
        :param ignore_repeated: bool
        :return: list
        """
        # Checking input:
        if not isinstance(level_num, int):
            raise ValueError("Number of level in tree "
                             "of users must be int.")

        # Main part:
        result_list = []

        # Adding users:
        # adding self to all_users:
        all_users = self.all_users(ignore_repeated) + [self]
        for user in all_users:
            if user.get_level() == level_num:
                result_list.append(user)

        # Finally:
        return result_list

    def first_occur(self):
        """
        Return first occurrence of a user in a tree with root as
        a main root.
        :return: User
        """
        # Searching in tree of main root for first occurrence
        # of user with id of given one:
        return self.get_root().user_by_id(self.get_id_num())

    def user_by_id(self, id_num):
        """
        Search tree for a user with an id. Return first occurrence of
        him. Return None if there is no such user in a tree. We
        are talking about a tree with current user as a root.
        :param id_num: int
        :return: User or NoneType
        """
        # Checking levels of tree from top to bottom (to get non-repeated user version first):
        for level in range(self.height() + 1):
            # If there is a user with given id on that level:
            if id_num in [user.get_id_num() for user in self.users_of_level(level)]:
                # Return a User object:
                return self.users_of_level(level)[[user.get_id_num() for user in
                                                   self.users_of_level(level)].index(id_num)]

        # If User object wasn't found:
        return None

    def set_parent(self, parent):
        """
        Set a parent of a current User.
        :param parent: User or None
        :return: None
        """
        # Checking arguments:
        if not isinstance(parent, User) and parent is not None:
            raise ValueError("Parent of a User must be User "
                             "or None.")

        # Setting:
        self._parent = parent

    def set_children(self, list_of_children):
        """
        Set children (friends) of a current User. It includes
        checking each child if it is its first occurrence in a
        main tree and change a variable for that.
        :param list_of_children: list of User
        :return: NoneType
        """
        # Checking arguments:
        if not isinstance(list_of_children, list) or \
                False in [isinstance(child, User)
                          for child in list_of_children]:
            raise ValueError("List of children must be a list "
                             "containing User objects only.")

        # Clearing current list of children:
        self._children = []

        # Adding children to a list, also checking each one for
        # previous occurrences in a main tree:
        root = self.get_root()

        # For each child in list of children:
        for child in list_of_children:
            # If user with the same id is in the main tree:
            if child.get_id_num() in [user.get_id_num()
                                      for user in
                                      root.all_users()]:
                child.already_was_in_tree = True
            # Add child:
            self._children.append(child)
            # Set parent of a child:
            child.set_parent(self)

    def __str__(self):
        """
        Return string representation of a User.
        :return: str
        """
        return "User:\n" \
               "--id_num={}\n" \
               "--children={}".format(self.get_id_num(), self.get_children())

    def __repr__(self):
        """
        Return short string representation of a User.
        :return: str
        """
        return "User({})".format(self.get_id_num())

    def in_file_user(self):
        """
        Return in-file representation of a user for saving it later. Example:
        232323
        -2323
        -2323
        (user at the top, friends with minuses before them).
        :return: str
        """
        result_str = str(self.get_id_num()) + "\n"

        children = self.get_children()

        for child in children:
            child_str = "-" + str(child.get_id_num()) + "\n"
            result_str = result_str + child_str

        return result_str

    def in_file_tree(self):
        """
        Return in file representation of all users of a tree with current user as a root.
        :return: str
        """
        # Adding current user:
        result_str = self.in_file_user()

        # Adding all other users:
        all_users = self.all_users()
        for user in all_users:
            if user.get_level() != user.get_root().height():
                result_str = result_str + user.in_file_user()

        # Returning:
        return result_str
