import sys
import cv2
from image_utils import measure_new_image
import file_utils

if len(sys.argv) != 2:
	print("Usage: " + sys.argv[0] + " [new_image_filename]")
	exit()

file_utils.create_path_structure()

filename = sys.argv[1]
print("")
print("INSTRUCTIONS")
print("")
print("Input the numbers of the bars you want to measure.")
print("Ensure the laptop screen and the blue buttons on the scanner are facing you.")
print("Enter a value of -1 for each slot which is not filled")
print("")

bar_nums_left = []
bar_nums_right = []

bar_type = raw_input("What type of bar are you measuring? Answer smb / fgb: ")
while bar_type != 'smb' and bar_type != 'fgb':
	bar_type = raw_input("What type of bar are you measuring? Answer smb / fgb: ")
bar_is_smb = bar_type == 'smb' and bar_type != 'fgb'

use_default = raw_input("Would you like to use default values for the bar numbers (for testing only)? Answer (y)es / (n)o: ")
while use_default != 'yes' and use_default != 'y' and use_default != 'no' and use_default != 'n':
	use_default = raw_input("Would you like to use default values for the bar numbers (for testing only)? Answer (y)es / (n)o: ")

if use_default == 'yes' or use_default == 'y':
	for i in range(1, 12):
		bar_nums_left.append(i)
		bar_nums_right.append(i + 12)
else:
	print("\tLEFT\tRIGHT")
	for i in range(1, 12):
		print("Row " + str(i) + "\t",)
		nums = raw_input("")
		left_and_right = nums.split()
		left = left_and_right[0]
		right = left_and_right[1]
		bar_nums_left.append(int(left))
		bar_nums_right.append(int(right))

bars_nums = []
for b in bar_nums_left:
	bars_nums.append(b)
for b in bar_nums_right:
	bars_nums.append(b)

print("Reading image " + filename)
new_image = cv2.imread(filename, cv2.IMREAD_COLOR)
if new_image is not None:
	measure_new_image(new_image, bars_nums, bar_is_smb=bar_is_smb)
else:
	print("Image input was not valid. Ensure the correct filename was given.")
	exit()



