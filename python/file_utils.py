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
		if measurement[0] != '-':
			measurement[0] -= zero_x
		if measurement[1] != '-':
			measurement[1] -= zero_y + slope*measurement[0]
	for measurement in measurements:
		for i in range(len(measurement)):
			if measurement[i] != '-':
				measurement[i] *= 25.4 / 2400.


def print_measurements_to_file(measurements, bar_num, is_smb):
	if is_smb:
		filename = "measurements\\smb_measurements.txt"
		if os.path.isfile(filename):
			out_file = open(filename, 'a+')
		else:
			out_file = open(filename, 'w+')
			out_file.write(
				"\tLeft Hole\t\t\t\tSquare 1\t\t\t\t\tSquare 2\t\t\t\t\tSquare 3\t\t\t\t\tSquare 4\t\t\t\t\tRight Hole\n")
			out_file.write("Bar Num\t")
			out_file.write("x (mm)\ty (mm)\tradius (mm)\tflagged\t")
			out_file.write("x (mm)\ty (mm)\twidth (mm)\theight (mm)\tflagged\t")
			out_file.write("x (mm)\ty (mm)\twidth (mm)\theight (mm)\tflagged\t")
			out_file.write("x (mm)\ty (mm)\twidth (mm)\theight (mm)\tflagged\t")
			out_file.write("x (mm)\ty (mm)\twidth (mm)\theight (mm)\tflagged\t")
			out_file.write("x (mm)\ty (mm)\twidth (mm)\theight (mm)\tflagged\n")
	else:
		filename = "measurements\\fgb_measurements.txt"
		if os.path.isfile(filename):
			out_file = open(filename, 'a+')
		else:
			out_file = open(filename, 'w+')
			out_file.write(
				"\tLeft Hole\t\t\t\tFiber 1\t\t\t\tFiber 2\t\t\t\tFiber 3\t\t\t\tFiber 4\t\t\t\tRight Hole\n")
			out_file.write("Bar Num\t")
			out_file.write("x (mm)\ty (mm)\tradius (mm)\tflagged\t")
			out_file.write("x (mm)\ty (mm)\tradius (mm)\tflagged\t")
			out_file.write("x (mm)\ty (mm)\tradius (mm)\tflagged\t")
			out_file.write("x (mm)\ty (mm)\tradius (mm)\tflagged\t")
			out_file.write("x (mm)\ty (mm)\tradius (mm)\tflagged\t")
			out_file.write("x (mm)\ty (mm)\tradius (mm)\tflagged\n")

	for measurement in measurements:
		for i in range(len(measurement)):
			if measurement[i] < 0:
				measurement[i] = '-'

	modify_measurements(measurements)
	line = ''
	line += str(bar_num) + '\t'
	for measurement in measurements:
		for data in measurement:
			line += str(data) + '\t'
		line += '\t'
	line += '\n'
	out_file.write(line)


def print_images_to_file(list_of_images, bar_num, is_smb):
	dir_path = "measurements\\"
	if is_smb:
		dir_path += "smb_images\\smb_"
	else:
		dir_path += "fgb_images\\fgb_"
	dir_path_bar = dir_path + str(bar_num)
	# If the path to the bar folder doesn't exist, make it
	if not os.path.exists(dir_path_bar):
		os.makedirs(dir_path_bar)
	else:
		bar_type = 'smb' if is_smb else 'fgb'
		print("WARNING: A " + bar_type + ' with bar number ' + str(bar_num) + ' was already measured.')
		# Find a folder name which hasn't been made yet
		j = 0
		while os.path.exists(dir_path_bar):
			dir_path_bar = dir_path + str(bar_num) + "_" + str(j)
			j += 1
		# If we're printing out a whole bar image, then make a new folder as this must be a new duplicate bar
		os.makedirs(dir_path_bar)
		# Otherwise, we're printing a hole image, meaning it belongs in the most recently made duplicate folder
	filename = dir_path_bar + "\\bar_" + str(bar_num) + ".jpg"
	cv2.imwrite(filename, list_of_images[0])
	for i in range(1, len(list_of_images)):
		filename = dir_path_bar + "\\hole_" + str(i) + ".jpg"
		cv2.imwrite(filename, list_of_images[i])


def print_image_to_file(img, bar_num, hole_num, is_smb):
	dir_path = "measurements\\"
	if is_smb:
		dir_path += "smb_images\\smb_"
	else:
		dir_path += "fgb_images\\fgb_"
	dir_path_bar = dir_path + str(bar_num)
	# If the path to the bar folder doesn't exist, make it
	if not os.path.exists(dir_path_bar):
		os.makedirs(dir_path_bar)
	else:
		# If is does and we're saving the image of a whole bar, throw a warning as it must be a duplicate
		if hole_num == -1:
			bar_type = 'smb' if is_smb else 'fgb'
			print("WARNING: A " + bar_type + ' with bar number ' + str(bar_num) + ' was already measured.')
		# Find a folder name which hasn't been made yet
		j = 0
		while os.path.exists(dir_path_bar):
			dir_path_bar = dir_path + str(bar_num) + "_" + str(j)
			j += 1
		# If we're printing out a whole bar image, then make a new folder as this must be a new duplicate bar
		if hole_num == -1:
			os.makedirs(dir_path_bar)
		# Otherwise, we're printing a hole image, meaning it belongs in the most recently made duplicate folder

	if hole_num == -1:
		filename = dir_path_bar + "\\bar_" + str(bar_num) + ".jpg"
	else:
		filename = dir_path_bar + "\\hole_" + str(hole_num) + ".jpg"
	cv2.imwrite(filename, img)


def create_path_structure():
	measure_smb_dir = 'measurements\\smb_images'
	measure_fgb_dir = 'measurements\\smb_images'
	new_images_dir = 'images'
	dirs = [measure_smb_dir, measure_fgb_dir, new_images_dir]
	for directory in dirs:
		if not os.path.isdir(directory):
			os.makedirs(directory)
