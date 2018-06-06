# Twitter Mutual Friends Searcher by Stefaniv Mykola
This is a program I created as my coursework. It is operated
using command line interface in Python console window.

## Getting Started

To get this project running, copy "full.zip" archive from this repository. Then you
just have to unarchive the file and run "main.py" python file. In order for this to
run, Python 3.6 must be installed.

## Running the tests

There are no automated tests for this program because it is working with data that is constantly
changing. But command line interface is understandable
and self-explainatory. You just have to type "help" into the command line to get all the
information about the program.

## About the program

### Purpose and short characteristic of the program
This program is created for finding if two Twitter users have mutual friends in some range
(by "friends" I mean followers of a person). It has a command line interface, and can show
graph of friends of a user, graph of two users and links between them through their mutual
friends. Also, there are settings, in which the user has to choose how deep to rearch friends,
how many links between users the program has to output on screen, and etc.

### Input and output of the program
Input is a command via command line interface. Information gets collected from the Internet.
It is shown in text field. Also, graph with information is shown, and image of the graph is
created.

### Structure
Modules: graphic.py for creating and showing image of a graph, instruction.py - module for
handling instructions from the command line, main.py - main module of the program, settings.py -
module with classes for settings of the program, twitter_access_stuff - module, in which
Twitter developer information must be entered, user_tree_functions.py - different functions
necessary for the program to function, and user_trees.py - module with class of User tree. For
more detailed description of the functions, classes, and their methods see documentation.

### Short instruction for using the program.
The program is operating using command line interface. Each command isn't influencing ones
written after it. You can get all the information about using the program by typing
"help", "help program", "help settings", and "help cache" in the program.
