# This is a main module of my coursework.
# You need other modules in order for this one to work. All needed modules you can find in subfolder called "full" in
# folder with a fourth stage of my coursework on a GitHub.
from settings import *
from instruction import Instruction


# Creating settings:
# Helper function:
def is_image(image_str):
    """
    Return True if image_str is *.png image. Return False otherwise.
    :param image_str: str
    :return: bool
    """
    if not image_str.endswith(".png"):
        return False

    # If False was not returned:
    return True


def is_max_link_num(num_str):
    """
    Return True if num_str can represent maximum number of shown links between users (str(int) or 'inf').
    :param num_str: str
    :return: None
    """
    if num_str == "inf":
        return True
    else:
        try:
            # Checking if integer:
            num_int = int(num_str)

            # Must be >= 0:
            return num_int >= 0
        except ValueError:
            return False



image_name = Setting("image_name", is_image, "friends_connections.png", "Name of saved image", "[*.png]")
search_depth = Setting("search_depth", [str(i) for i in range(1, 10)], "2", "How many mutual friends does the"
                                                                            " program have to check by default.",
                       "['1', '2', ..., '9']")
save_image = Setting("save_image", ["True", "False"], "True", "Whether the program must save the image.")
show_image = Setting("show_image", ["True", "False"], "True", "Whether the program must show the image.")
find_one_link = Setting("find_one_link", ["True", "False"], "True", "If True, program will show only one link"
                                                                    " of mutual friends - the shortest one. "
                                                                    "Otherwise it will show all links.")
show_full_trees = Setting("show_full_trees", ["True", "False"], "True", "Whether the image must show full trees "
                                                                        "or only link(s) between users.")
use_cache = Setting("use_cache", ["True", "False"], "False", "Whether the program should use cache.")

max_links_shown = Setting("max_links_shown", is_max_link_num, "inf", "How much links to print on screen after "
                                                                     "finding mutual friends.", "[str(int: int >= 0) or"
                                                                                                " 'inf']")

# Creating panel of those settings:
settings_panel = Settings([search_depth, image_name, save_image, show_image, find_one_link, show_full_trees,
                           use_cache, max_links_shown])

# Save default settings:
settings_panel.write_into_file("default_settings.txt")

# Reading settings from a file:
settings_panel.read_file("default_save_file.txt")


def console_function():
    """
    This function is waiting for the user input and returns list based on it. Program then interprets the list
    as an instruction.
    :return:
    """
    while True:
        print("_" * 120)
        # Read user input:
        input_str = input("> ")

        # Checking if user wants to exit program:
        if input_str == "exit":
            return None
        else:
            try:
                Instruction.instruction(input_str, settings_panel)
            except IndexError:
                print("Incorrect input.")


print("Program starts. Please, enter 'exit' to exit the program. Print 'help' for help.")
console_function()
