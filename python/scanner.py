import sys
import cv2
from image_utils import measure_new_image

if len(sys.argv) != 2:
	print("Usage: " + sys.argv[0] + " [new_image_filename]")
	exit()

filename = sys.argv[1]

print("Input the numbers of the bars you want to measure.")
print("Ensure the laptop screen and the blue buttons on the scanner are facing you.")
print("Input numbers moving down the left column then down the right column. Enter -1 for slots which don't have bars in them")

print("\tLEFT\tRIGHT")
bar_nums_left = []
bar_nums_right = []
for i in range(1, 12):
	print(str(i) + "\t", end='')
	nums = input("")
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

new_image = cv2.imread(filename, cv2.IMREAD_COLOR)
measure_new_image(new_image, bars_nums, bar_is_smb=True)



