from user_trees import *


print("Creating a tree...")
root_user = User(1)
root_user.set_children([User(12), User(32), User(41)])

print("Height: " + str(root_user.height()) + "\n")

print("Adding children to children of root...")
for child in root_user.get_children():
    child.set_children([User(234), User(455)])
print("Height: " + str(root_user.height()) + "\n")

print("Printing list of all users in the tree when ignoring repeated:")
print(root_user.all_users())
print("Printing list of all users in the tree when not ignoring repeated:")
print(root_user.all_users(ignore_repeated=False))

print("Checking __str__ method:")
print(User(327))
print(root_user)
