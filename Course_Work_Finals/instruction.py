from settings import *
from user_trees import *
from user_tree_functions import *
from twitter_access_stuff import *
from graphic import *


class Instruction:
    """
    Class representing instructions.
    """
    def __init__(self):
        """
        Initialise an instance of Instruction class. Arguments are not needed.
        """
        pass

    @staticmethod
    def instruction(args_str, settings):
        """
        Run instruction for a string.
        :param args_str: str
        :param settings: Settings
        :return: NoneType
        """
        # Checking argument:
        if not isinstance(args_str, str):
            raise ValueError("Argument of Instruction.instruction() must be str.")

        # Splitting argument:
        args = args_str.split()

        # Checking which instruction to run:
        # For settings:
        if len(args) < 1:
            # Stop the method.
            return None

        elif args[0] == "settings":
            if len(args) == 2:
                if args[1] == "info":
                    Instruction._print_settings_info()
                elif args[1] == "show":
                    print(str(settings))
                elif args[1] == "save":
                    settings.write_into_file("default_save_file.txt")
                elif args[1] == "save_files":
                    Instruction._print_custom_save_files()
                elif args[1] == "load":
                    Instruction._load_settings_from_file(settings, "default_save_file.txt")
                elif args[1] == "restore":
                    Instruction._load_settings_from_file(settings, "default_settings.txt")
                else:
                    print("Incorrect input.")
            elif len(args) == 3:
                if args[1] == "save":
                    Instruction._write_settings_into_file(settings, args[2])
                elif args[1] == "load":
                    Instruction._load_settings_from_file(settings, args[2])
                else:
                    print("Incorrect input.")
            elif len(args) == 4:
                if args[1] == "change":
                    Instruction._change_setting(settings, args[2], args[3])
                else:
                    print("Incorrect input.")
            else:
                print("Incorrect input.")

        # For help:
        elif args[0] == "help":
            if len(args) == 1:
                Instruction._print_basic_help()
            elif len(args) == 2:
                if args[1] == "settings":
                    Instruction._print_settings_info()
                elif args[1] == "program":
                    Instruction._print_program_help()
                elif args[1] == "cache":
                    Instruction._print_cache_help()
                else:
                    print("Incorrect input.")
            else:
                print("Incorrect input.")

        # For finding friends:
        elif args[0] == "cache":
            if len(args) == 2:
                if args[1] == "show":
                    Instruction._print_cache_file()
                elif args[1] == "clear":
                    file = open("cache.txt", "w")
                    file.write("")
                    file.close()
                elif args[1] == "help":
                    Instruction._print_cache_help()
                else:
                    print("Incorrect instruction.")
            else:
                if args[1] == "add":
                    users = args[2:]
                    Instruction._cache_users(settings, users)
                else:
                    print("Incorrect instructions")

        elif args[0] == "friends":
            if len(args) == 3 and args[1] == "all":
                name = args[2]
                Instruction._friends_all(settings, name)
            elif len(args) == 4 and args[1] == "mutual":
                name_1, name_2 = args[2], args[3]
                Instruction._mutual_friends(settings, name_1, name_2)
            else:
                print("Incorrect input.")

        elif len(args) == 1 and args[0] == "info":
            print("Program for finding mutual friends created by Mykola Stefaniv as coursework.")

        else:
            print("Incorrect input.")

    @staticmethod
    def _change_setting(settings, setting_name, new_value):
        """
        Change setting with setting_name of group settings to new_value. Raise a special error if it is a
        bad input.
        :param settings: Settings
        :param setting_name: str
        :param new_value: str
        :return: NoneType
        """
        # Checking arguments:
        if not isinstance(settings, Settings) or not isinstance(setting_name, str) or \
           not isinstance(new_value, str):
            raise ValueError("Incorrect arguments for Instruction.change_setting().")

        # Changing setting and working on errors:
        try:
            setting = settings.setting_by_name(setting_name)
        except ValueError:
            print("There is no such setting!")
            return None

        try:
            setting.set_value(new_value)
        except ValueError:
            print("Bad value for a setting!")
            return None

        # If all done correctly:
        print("Setting successfully changed!")

        # Save information:
        settings.write_into_file("default_save_file.txt")

    @staticmethod
    def _print_settings_info():
        """
        Print information about program settings.
        :return: NoneType
        """
        print("The way this program works is mostly controlled by settings.")
        print("Type 'settings show' to see all settings, their current and possible values.")
        print("Type 'settings change <setting_name> <new_value>' to change current setting.")
        print("Type 'settings save' to save settings into default save file.")
        print("Type 'setting save <file_name>' to save settings into a new, custom save file.")
        print("Type 'settings save_files' to see names of all custom save files.")
        print("Type 'settings load' to load settings from a default save file.")
        print("Type 'settings load <file_name>' to load settings from a custom save file.")
        print("Type 'settings restore' to restore all settings to their default values (doesn't change save files).")

    @staticmethod
    def _write_settings_into_file(settings, file_name):
        """
        Save settings into a file which is not default.
        :param settings: Settings
        :param file_name: str
        :return: NoneType
        """
        # Checking arguments (not their types because method is private):
        if not file_name.endswith(".txt"):
            print("You can only save settings as *.txt file.")
            return None

        # Checking file_name:
        if file_name in ("default_save_file.txt", "default_settings.txt", "custom_save_files.txt", "cache.txt"):
            print("You can't use 'default_save_file.txt', 'default_settings.txt', 'cache.txt' or 'custom_save_"
                  "files.txt' "
                  "as save file for your settings.")
            return None

        # Save:
        settings.write_into_file(file_name)

        # Checking if file_name in text file with names of all save files:
        file = open("custom_save_files.txt", "r")
        save_files = file.readlines()
        file.close()

        # Changing list of all custom save files if needed:
        if file_name not in save_files:
            file = open("custom_save_files.txt", "w")
            save_files.append(file_name)
            for elem in save_files:
                file.write(elem + "\n")

        print("Settings successfully saved.")
        return None

    @staticmethod
    def _print_custom_save_files():
        """
        How the name suggests.
        :return: NoneType
        """
        file = open("custom_save_files.txt", "r")
        lines = file.readlines()
        file.close()
        print("All custom save files:")
        for line in lines:
            print(line)
        return None

    @staticmethod
    def _load_settings_from_file(settings, file_name):
        """
        As the name suggests.
        :param settings: Settings
        :param file_name: str
        :return: NoneType
        """
        if not file_name.endswith(".txt"):
            print("You can only load settings from *.txt files.")
            return None

        if file_name == "custom_save_files.txt":
            print("This and only this file cannot contain settings.")
            return None

        file = open("custom_save_files.txt", "r")
        lines = file.readlines()
        file.close()

        lines.append("default_settings.txt")
        lines.append("default_save_file.txt")

        if file_name not in lines:
            print("No such save file.")
            return None

        settings.read_file(file_name)
        print("Successfully changed settings!")
        return None

    @staticmethod
    def _print_basic_help():
        """
        Output basic help on screen.
        :return: NoneType
        """
        print("Type 'help settings' to see settings commands.")
        print("Type 'help program' to know how to use program.")
        print("Type 'help cache' to see information about the cache.")

    @staticmethod
    def _print_program_help():
        """
        Print information about how to use the program.
        :return: NoneType
        """
        print("Type 'help' if you don't know something.")
        print("Type 'info' to get information about the program.")
        print("Type 'friends all <person_name>' to show all Twitter friends of a person.")
        print("Type 'friends mutual <person_1> <person_2>' to show if two people have mutual friends on Twitter.")

    @staticmethod
    def _print_cache_help():
        """
        Print information about caching.
        :return: NoneType
        """
        print("Cache is a text file in which information about users and their friends may be stored.")
        print("This is useful because search information takes some time sometimes.")
        print("Whether the program uses cache or not is specified in the settings.")
        print("Type 'cache show' to show cache.")
        print("Type 'cache help' to show this information.")
        print("Type 'cache clear' to clear the cache (if you add something to cache, old information remains there).")
        print("Type 'cache add <user_1> to add information about the user and friends of his friends to the cache."
              "Depth of search is specified in settings.")
        print("Type 'cache add <user_1> <user_2> ... <user_n> to add multiple users and friends of their friends to "
              "cache.")

    @staticmethod
    def _print_cache_file():
        """
        Print information about cache file.
        :return: NoneType
        """
        cache_dict = dict_from_file("cache.txt")
        for key in cache_dict:
            print("{}: {}".format(key, cache_dict[key]))

    @staticmethod
    def _cache_users(settings, names_list):
        """
        Cache users.
        :param names_list: list
        :return: NoneType
        """
        # Extracting setting:
        depth_setting = settings.setting_by_name("search_depth")
        depth = int(depth_setting.get_current_value())

        result_str = ""

        for name in names_list:
            api = authorise(consumer_key, consumer_secret, access_token, access_token_secret)
            user = get_user(api, name)
            id_num = user.id
            tree = build_friend_tree(api, id_num, depth)
            tree_str = tree.in_file_tree()
            result_str = result_str + tree_str

        # Into file:
        file = open("cache.txt", "a")
        file.write(result_str)
        file.close()

    @staticmethod
    def _friends_all(settings, person_name):
        """
        Return list of names of all friends of a person with depth specified in settings.
        :param settings: str
        :param person_name: str
        :return: list
        """
        api = authorise(consumer_key, consumer_secret, access_token, access_token_secret)

        user_1 = get_user(api, person_name)
        id_1 = user_1.id

        # Getting useful settings:
        def setting_value(setting_name):
            """
            Helper function.
            :param setting_name: str
            :return: str
            """
            return settings.setting_by_name(setting_name).get_current_value()

        save = setting_value("save_image")
        image_name = setting_value("image_name")
        show = setting_value("show_image")
        use_cache = setting_value("use_cache")
        depth = int(setting_value("search_depth"))

        if show == "True":
            show = True
        else:
            show = False

        if save == "True":
            save = True
        else:
            save = False

        # First of all, creating tree:
        if use_cache == "True":
            dict_of_friends = dict_from_file("cache.txt")

            # Checking for error:
            if id_1 not in dict_of_friends.keys():
                print("Sorry, but the program couldn't find one of the users in cache.")
                return None

            # Tree:
            tree_1 = tree_from_dict(id_1, dict_of_friends, depth)

        # If we don't have to use cache:
        else:
            tree_1 = build_friend_tree(api, id_1, depth)

        print("Successfully found friends.")

        # Now drawing tree:
        if show or save:
            draw_all_friends(tree_1, show, save, image_name)

    @staticmethod
    def _mutual_friends(settings, person_1, person_2):
        """
        Search for mutual friends depending on settings.
        :param settings: Settings
        :param person_1, person_2: str
        :return: list of str
        """
        api = authorise(consumer_key, consumer_secret, access_token, access_token_secret)

        user_1 = get_user(api, person_1)
        user_2 = get_user(api, person_2)
        id_1 = user_1.id
        id_2 = user_2.id

        # Getting useful settings:
        def setting_value(setting_name):
            """
            Helper function.
            :param setting_name: str
            :return: str
            """
            return settings.setting_by_name(setting_name).get_current_value()

        save = setting_value("save_image")
        image_name = setting_value("image_name")
        show = setting_value("show_image")
        one_link = setting_value("find_one_link")
        full_trees = setting_value("show_full_trees")
        use_cache = setting_value("use_cache")
        depth = int(setting_value("search_depth"))
        max_links_num = setting_value("max_links_shown")

        if show == "True":
            show = True
        else:
            show = False

        if save == "True":
            save = True
        else:
            save = False

        # First of all, creating trees:
        if use_cache == "True":
            dict_of_friends = dict_from_file("cache.txt")

            # Checking for error:
            if id_1 not in dict_of_friends.keys() or id_2 not in dict_of_friends.keys():
                print("Sorry, but the program couldn't find one of the users in cache.")
                return None

            # Trees:
            tree_1 = tree_from_dict(id_1, dict_of_friends, depth)
            tree_2 = tree_from_dict(id_2, dict_of_friends, depth)

        # If we don't have to use cache:
        else:
            tree_1 = build_friend_tree(api, id_1, depth)
            tree_2 = build_friend_tree(api, id_2, depth)

        # Now finding mutual friends between people:
        # Finding mutual users in trees:
        mutual_ids = find_mutual_ids(tree_1, tree_2)

        # Getting all links:
        list_of_links = []
        for id_num in mutual_ids:
            link = link_to_list(id_num, tree_1, tree_2)
            list_of_links.append(link)

        # Printing results on the screen:
        if list_of_links:
            print("There are mutual friends between two users. Link(s):")
            # Settings that limit number of links shown:
            if max_links_num == "inf":
                links_num = len(list_of_links)
            else:
                links_num = int(max_links_num)

            if one_link == "True":
                min_id = find_min_link(mutual_ids, tree_1, tree_2)
                link = link_to_list(min_id, tree_1, tree_2)
                print(link_to_string(link))
            else:
                for link in list_of_links[:links_num]:
                    print(link_to_string(link))
        else:
            print("There are no mutual friends between two users.")

        # Showing image:
        if not show and not save:
            # To save resources:
            return None

        elif full_trees == "True":
            full_trees_draw(tree_1, tree_2, show, save, image_name)

        else:
            if one_link == "True":
                # Showing only one link - the shortest one:
                best_id = find_min_link(mutual_ids, tree_1, tree_2)
                link = link_to_list(best_id, tree_1, tree_2)
                only_links([link], show, save, image_name)
            else:
                # Showing all links:
                only_links(list_of_links, show, save, image_name)
