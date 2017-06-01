import cv2
from class_defs import rect
import numpy as np
from file_utils import print_measurements_to_file
from file_utils import print_images_to_file

bar_rect_list = []
for i in range(11):
	bar_rect_list.append(rect(550, 850 + 2510*i, 9250, 1570))
for i in range(11):
	bar_rect_list.append(rect(10750, 850 + 2510*i, 9250, 1530))

hole_rect_list = []
hole_rect_list.append(rect(180, 480, 590, 620))
hole_rect_list.append(rect(780, 500, 440, 540))
hole_rect_list.append(rect(3280, 500, 440, 540))
hole_rect_list.append(rect(5480, 500, 440, 540))
hole_rect_list.append(rect(7980, 500, 440, 540))
hole_rect_list.append(rect(8350, 400, 700, 700))


def show_image(image, title):
	cv2.imshow(title, image)
	cv2.waitKey(0)
	cv2.destroyAllWindows()


def measure_new_image(new_image, bar_nums, bar_is_smb=True):
	bar_images = get_bars(new_image)
	problem_bars = []
	for bar, bar_num in zip(bar_images, bar_nums):
		print("Measuring bar " + str(bar_num))
		# show_image(cv2.resize(bar, (int(bar.shape[1]/10), int(bar.shape[0]/10))), "Bar")
		# print_image_to_file(bar, bar_num, -1, bar_is_smb)

		images_to_print = []
		images_to_print.append(bar)

		holes = get_holes(bar)
		measurements = []
		i = 0
		if bar_num == -1:
			continue
		if bar_is_smb:
			for hole, crop in holes:
				if i == 0:
					measurement, drawn_img = measure_circle(hole, crop.x(), crop.y())
					measurements.append(measurement)
				else:
					measurement, drawn_img = measure_square(hole, crop.x(), crop.y())
					measurements.append(measurement)
				# print_image_to_file(drawn_img, bar_num, i, bar_is_smb)
				images_to_print.append(drawn_img)
				i += 1
		else:
			for hole, crop in holes:
				measurement, drawn_img = measure_circle(hole, crop.x(), crop.y())
				measurements.append(measurement)
				# print_image_to_file(drawn_img, bar_num, i, bar_is_smb)
				images_to_print.append(drawn_img)
				i += 1
		for hole_num in range(len(measurements)):
			if -1 in measurements[hole_num]:
				problem_bars.append("[Bar " + str(bar_num) + " Hole " + str(hole_num) + "]")
		print_images_to_file(images_to_print, bar_num, bar_is_smb)
		print_measurements_to_file(measurements, bar_num, is_smb=bar_is_smb)
	if len(problem_bars) > 0:
		print("There was a problem with the bars")
		for b in problem_bars:
			print(str(b))


def is_out_of_bounds(x, y, width, height):
	return x < 0 or y < 0 or x >= width or y >= height


def get_good_crop_rect(image):
	edge = cv2.GaussianBlur(image, (3, 3), 3, None, 3)
	edge = cv2.Canny(image, 100, 200)
	kernel = np.ones((3, 2), np.uint8)
	edge = cv2.dilate(edge, kernel, iterations=1)
	(_, contours, _) = cv2.findContours(edge, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	if contours is not None:
		contours = sorted(contours, key=cv2.contourArea, reverse=True)[:3]
		draw_img = image.copy()
		cv2.drawContours(draw_img, contours, 0, (0, 255, 0), 4)
		# show_image(draw_img, "Hole with best three contour")
		# print(cv2.boundingRect(contours[0]))
		(x, y, w, h) = cv2.boundingRect(contours[0])
		ret_rect = rect(x - 5, y - 5, w + 10, h + 10)
		return ret_rect
	else:
		return None


def get_holes(image):
	holes = []
	for crop in hole_rect_list:
		candidate_hole = image[crop.y():crop.y() + crop.height(), crop.x():crop.x() + crop.width()]
		# show_image(candidate_hole, "Candidate")
		better_rect = get_good_crop_rect(candidate_hole)
		if better_rect is not None:
			candidate_hole = image[crop.y() + better_rect.y():crop.y() + better_rect.y() + better_rect.height(), crop.x() + better_rect.x():crop.x() + better_rect.x() + better_rect.width()]
			# show_image(candidate_hole, "Better")
			crop = rect(crop.x() + better_rect.x(), crop.y() + better_rect.y(), better_rect.width(), better_rect.height())
		holes.append((candidate_hole, crop))
	return holes


def get_bars(image):
	bars = []
	for crop in bar_rect_list:
		bars.append(image[crop.y():crop.y() + crop.height(), crop.x():crop.x() + crop.width()])
	return bars


def measure_circle(img, x_offset, y_offset):
	circles = None
	for thresh in range(25, 15, -1):
		circles = cv2.HoughCircles(image=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), method=cv2.HOUGH_GRADIENT, dp=1,
		                           minDist=3, minRadius=220, maxRadius=240, param1=175, param2=thresh)
		if circles is not None:
			good_circles = [circles[0][j] for j in range(len(circles[0])) if (225 < circles[0][j][2] < 234)]
			if len(good_circles) > 0:
				break
	if circles is not None:
		# print("Found", len(circles[0]), "circles")
		# for (x, y, r) in circles[0]:
		# 	print("Found circle: (" + str(x) + ", " + str(y) + ", " + str(r))
		# cv2.circle(hole, (x, y), r, (0, 255, 0), 2)
		good_circles = [circles[0][j] for j in range(len(circles[0])) if (225 < circles[0][j][2] < 234)]
		# for circle in good_circles:
		# 	print("radius:", circle[2])
		if len(good_circles) > 0:
			center_x = sum([circle[0] for circle in good_circles]) / len(good_circles)
			center_y = sum([circle[1] for circle in good_circles]) / len(good_circles)
			radius = sum([circle[2] for circle in good_circles]) / len(good_circles)
		else:
			return [-1, -1, -1], img.copy()
		# print("Found average circle: (" + str(center_x) + ", " + str(center_y) + ", " + str(radius))
		return_img = img.copy()
		cv2.circle(return_img, (int(center_x), int(center_y)), int(radius), (0, 255, 0), 2)
		# show_image(return_img, "Circle")
		return [center_x + x_offset, center_y + y_offset, radius], return_img
	else:
		return [-1, -1, -1], img.copy()


def measure_square(img, x_offset, y_offset):
	edge = cv2.GaussianBlur(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), (3, 3), 3, None, 3)
	edge = cv2.Canny(edge, 100, 200)

	# show_image(edge, "Square edges")

	height, width = edge.shape

	x = height / 2
	y = width / 2

	left_lim = int(x - 25)
	right_lim = int(x + 25)
	top_lim = int(y - 25)
	bottom_lim = int(y + 25)

	max_left = 0
	max_top = 0
	min_bot = 1000
	min_right = 1000

	for pixel_x in range(left_lim, right_lim):
		pixel_y = int(y)
		while edge[pixel_y, pixel_x] != 255:
			# print(edge[pixel_y, pixel_x])
			pixel_y += 1
			if is_out_of_bounds(pixel_x, pixel_y, width, height):
				break
		# print("Found white or out at y", pixel_y)
		if pixel_y < min_bot and abs(pixel_y - y) > 20:
			min_bot = pixel_y

	for pixel_x in range(left_lim, right_lim):
		pixel_y = int(y)
		while edge[pixel_y, pixel_x] != 255:
			# print(edge[pixel_y, pixel_x])
			pixel_y -= 1
			if is_out_of_bounds(pixel_x, pixel_y, width, height):
				break
		# print("Found white or out at y", pixel_y)
		if pixel_y > max_top and abs(pixel_y - y) > 20:
			max_top = pixel_y

	for pixel_y in range(top_lim, bottom_lim):
		pixel_x = int(x)
		while edge[pixel_y, pixel_x] != 255:
			# print(edge[pixel_y, pixel_x])
			pixel_x += 1
			if is_out_of_bounds(pixel_x, pixel_y, width, height):
				break
		# print("Found white or out at x", pixel_x)
		if pixel_x < min_right and abs(pixel_x - x) > 20:
			min_right = pixel_x

	for pixel_y in range(top_lim, bottom_lim):
		pixel_x = int(x)
		while edge[pixel_y, pixel_x] != 255:
			# print(edge[pixel_y, pixel_x])
			pixel_x -= 1
			if is_out_of_bounds(pixel_x, pixel_y, width, height):
				break
		# print("Found white or out at x", pixel_x)
		if pixel_x > max_left and abs(pixel_x - x) > 20:
			max_left = pixel_x

	return_img = img.copy()
	cv2.rectangle(return_img, (max_left, max_top), (min_right, min_bot), (0, 255, 0))
	# show_image(return_img, "Rectangle")
	center_x = (min_right + max_left)/2.
	center_y = (min_bot + max_top)/2.
	width = min_right - max_left
	height = min_bot - max_top
	# print("Found rectangle:", center_x, center_y, width, height)
	return [center_x + x_offset, center_y + y_offset, width, height], return_img
