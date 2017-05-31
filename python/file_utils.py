import os
import cv2

def modify_measurements(measurements):
	# All measurements in the form: [center_x, center_y, width / radius, height / ~]
	# Each set of measurements will contain 6 measurements for the 6 measured holes

	# x = 0, y = 0 is defined to be the center of the left most hole
	zero_x = measurements[0][0];
	zero_y = measurements[0][1];
	# y = 0 is defned to lie along the line connected the center of the left most and right most hole
	# transform all of the measurements to these coordinates
	slope = (measurements[5][1] - zero_y) / (measurements[5][0] - zero_x)
	for measurement in measurements:
		measurement[0] -= zero_x
		measurement[1] -= zero_y + slope*measurement[0]
	for measurement in measurements:
		for i in range(len(measurement)):
			measurement[i] *= 25.4 / 2400.


def print_measurements_to_file(measurements, bar_num, is_smb):
	if is_smb:
		filename = "measurements\\measurement_smb.txt"
	else:
		filename = "measurements\\measurement_fgb.txt"
	if os.path.isfile(filename):
		out_file = open(filename, 'a+')
	else:
		out_file = open(filename, 'w+')
		out_file.write("\tLeft Hole\t\t\t\t\tSquare 1\t\t\t\t\tSquare 2\t\t\t\t\tSquare 3\t\t\t\t\tSquare 4\t\t\t\t\tRight Hole\n");
		out_file.write("Bar Num\t");
		out_file.write("x (mm)\ty (mm)\tradius (mm)\t~\tflagged\t");
		out_file.write("x (mm)\ty (mm)\twidth (mm)\theight (mm)\tflagged\t");
		out_file.write("x (mm)\ty (mm)\twidth (mm)\theight (mm)\tflagged\t");
		out_file.write("x (mm)\ty (mm)\twidth (mm)\theight (mm)\tflagged\t");
		out_file.write("x (mm)\ty (mm)\twidth (mm)\theight (mm)\tflagged\t");
		out_file.write("x (mm)\ty (mm)\twidth (mm)\theight (mm)\tflagged\n");

	modify_measurements(measurements)
	line = ''
	# Bar num should be here
	line += str(bar_num) + '\t'

	for measurement in measurements:
		for data in measurement:
			line += str(data) + '\t'
		# Flagging should be here
		line += '\t'
	line += '\n'
	out_file.write(line)


def print_image_to_file(img, bar_num, hole_num, is_smb=True):
	dir_path = "measurements\\"
	if is_smb:
		dir_path += "smb_images\\smb_"
	else:
		dir_path += "fgb_images\\fgb_"
	dir_path_bar = dir_path + str(bar_num)
	if not os.path.exists(dir_path_bar):
		os.makedirs(dir_path_bar)
	# 	print("WARNING: A bar with number " + str(bar_num) + " has already been measured.")
	# j = 1
	# while os.path.exists(dir_path):
	# 	dir_path_bar = dir_path + str(bar_num) + "_" + str(j)

	filename = dir_path_bar + "\\hole_" + str(hole_num) + ".jpg"
	cv2.imwrite(filename, img)
