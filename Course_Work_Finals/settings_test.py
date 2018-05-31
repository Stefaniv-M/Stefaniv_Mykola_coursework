from settings import *
from user_trees import *


# Testing:

print("Testing writing settings on the screen and into a file:")
# Creating settings:
size = Setting("Size", [str(i) for i in range(10)], "5", "sizething")
color = Setting("Color", ["Red", "Yellow", "Green", "Black"], "Yellow", "colorthing")

# Creating settings panel:
image_settings = Settings([size, color])

# Writing settings into a file:
image_settings.write_into_file("image_settings_test.txt")

# Print results on the screen:
print(image_settings)

print("\nTesting getting settings from the file:")
color.set_value("Green")
print(image_settings)
print("After reading from file:")
image_settings.read_file("image_settings_test.txt")
print(image_settings)

def testfunc(elem):
    return elem in ["Hello", "world"]

new_setting = Setting("new_setting", testfunc, "world", "Setting with function as possible_values",
                      "('Hello' or 'world')")
print(new_setting)
