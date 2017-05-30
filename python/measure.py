import cv2
import numpy as np
import math
import matplotlib.pyplot as plt


def show_image(image, title):
	cv2.imshow(title, image)
	cv2.waitKey(0)
	cv2.destroyAllWindows()


def find_radius(image, samples, inv=False):
	if inv is True:
		edge_val = 255
	else:
		edge_val = 0
	average_center_x = 0
	average_center_y = 0
	average_radius = 0
	h, w = image.shape
	prev_x_step = 0
	prev_y_step = 0
	counts = 0
	for n in range(0, samples):
		y = int(h / 2)
		x = int(w / 2)
		if samples == 1:
			x_step = 1
			y_step = 0
		else:
			x_step = 1 - n / (samples - 1)
			y_step = n / (samples - 1)
		min_step = min([x_step, y_step])
		if min_step != 0:
			scaling = 1/min_step
		else:
			scaling = 1
		x_step = int(round(x_step * scaling, 1))
		y_step = int(round(y_step * scaling, 1))
		print("Scaled: (", x_step, ",", y_step, ")")

		if x_step == prev_x_step and y_step == prev_y_step:
			continue
		else:
			prev_x_step = x_step
			prev_y_step = y_step
		uncertainty_box = image[y:y + y_step, x:x + x_step]
		while True:
		# while image[y, x] != edge_val:
			x += x_step
			y += y_step
			# Look in the region just passed for white pixels
			if cv2.countNonZero(image[y - y_step:y + 1, x - x_step:x + 1]) != 0:
				break
			if x >= w or y >= h or x < 0 or y < 0:
				print("Out of bounds: (", x, ",", y, ")")
				break
		if x >= w or y >= h or x < 0 or y < 0:
			continue
		right = x - x_step / 2
		bottom = y - y_step / 2
		# print("Top, Right:", bottom, right)

		y = int(h / 2)
		x = int(w / 2)
		while True:
		# while image[y, x] != edge_val:
			x -= x_step
			y -= y_step
			if cv2.countNonZero(image[y:y + y_step + 1, x:x + x_step + 1]) != 0:
				break
			if x >= w or y >= h or x < 0 or h < 0:
				print("Out of bounds: (", x, ",", y, ")")
				break
		if x >= w or y >= h or x < 0 or h < 0:
			continue

		left = x + x_step / 2
		top = y + y_step / 2
		# print("Bottom, Left:", top, left)
		center_x = (right + left) / 2
		center_y = (top + bottom) / 2
		average_center_x += center_x
		average_center_y += center_y

		radius = math.sqrt((right - center_x)**2 + (top - center_y)**2)
		print("Radius:", radius)
		average_radius += radius
		counts += 1
	if counts == 0:
		return 0
	average_center_x = int(average_center_x / counts)
	average_center_y = int(average_center_y / counts)
	average_radius /= counts
	# print("Got Average Radius of", average_radius)
	return average_center_x, average_center_y, average_radius


# while image[y,x] != 255:
		# 	x += x_step
		# 	y += y_step
		# right = x
		# top = y
		# while image[y,x] != 255:
		# 	x -= x_step
		# 	y -= y_step
		# left = x
		# bottom = y
# image = cv2.imread("C:\\Users\\Steven\\Desktop\\Test\\Images\\Frame008 - Copy.jpg", cv2.IMREAD_COLOR)

# bar_0 = image[500:2800, 400:9800]
bar_0 = cv2.imread("bar_0.png", cv2.IMREAD_GRAYSCALE)
# print("Bar Shape:", bar_0.shape)
# show_image(bar_0, "bar_0")
circle = bar_0[925:1425, 367:867]
# cv2.imwrite("bar_0.png", bar_0)
height, width = circle.shape

# _, circle_thresh = cv2.threshold(circle, 120, 255, cv2.THRESH_BINARY)
# percent_white_pixels = 100 * cv2.countNonZero(circle_thresh) / (width * height)
# thresh = 120
#
# fig = plt.figure()
# ax1 = fig.add_subplot(111)
# for ideal_percent in range(630, 650):
# 	while percent_white_pixels > ideal_percent / 10:
# 		thresh += 2
# 		_, circle_thresh = cv2.threshold(circle, thresh, 255, cv2.THRESH_BINARY)
# 		percent_white_pixels = 100 * cv2.countNonZero(circle_thresh) / (width * height)
# 		print("% White:", percent_white_pixels)
# 	while percent_white_pixels < ideal_percent / 10:
# 		thresh -= 2
# 		_, circle_thresh = cv2.threshold(circle, thresh, 255, cv2.THRESH_BINARY)
# 		percent_white_pixels = 100 * cv2.countNonZero(circle_thresh) / (width * height)
# 		print("% White:", percent_white_pixels)
# 	# show_image(circle_thresh, "Threshold " + str(ideal_percent / 10) + "%")
# 	index = []
# 	radii = []
# 	for i in range(1, 30):
# 		index.append(i)
# 		radius = find_radius(circle_thresh, samples=i)
# 		radii.append(radius)
# 	average_over_samples = sum(radii) / len(radii)
#
# 	ax1.scatter(index, radii, label="Avg: " + str(round(average_over_samples, 1)) + " | " + str(ideal_percent) + "%")
# 	# plt.ylim((226, 232))
# plt.xlabel('Number of Samples')
# plt.ylabel('Average Computed Radius')
# plt.legend(loc='upper left');
# plt.show()



# for i in range(0, 40):
# 	ret, thresh = cv2.threshold(circle, 5*i, 255, cv2.THRESH_BINARY)
# 	show_image(thresh, "Thresholded")
# 	cols, rows = thresh.shape
# 	white = 0
# 	for y in range(0, cols):
# 		for x in range(0, rows):
# 			if thresh[y, x] == 255:
# 				white += 1
# 	print("Percent White:", 100*white/(rows*cols))


# for i in range(1, 20):
# 	ret, th1 = cv2.threshold(circle, int(5*i), 255, cv2.THRESH_BINARY)
# 	circle_thresh = cv2.adaptiveThreshold(circle, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, int(2*i + 1), 2)
# 	show_image(circle_thresh, "adaptive threshold")
# 	show_image(th1, "threshold")


_, circle_thresh = cv2.threshold(circle, 120, 255, cv2.THRESH_BINARY)
circle_blurred = cv2.GaussianBlur(circle, (7, 7), 3, None, 3)
circle_edged = cv2.Canny(circle_blurred, 100, 200, 3)
show_image(circle_edged, "edged")

# print("Thresh:", find_radius(circle_thresh, samples=4, inv=False))
# print("Edged:", find_radius(circle_edged, samples=4, inv=True))

index = []
radii = []
for i in range(1, 30):
	index.append(i)
	x, y, radius = find_radius(circle_edged, samples=i, inv=True)
	cv2.circle(circle, (x, y), int(radius), (0, 255, 0))
	radii.append(radius)
show_image(circle, "Circle with circles")
average_over_samples = sum(radii) / len(radii)
plt.figure()
plt.plot(index, radii)
plt.title(str(average_over_samples))
plt.show()

# show_image(circle_edged, "circle")
# circles = cv2.HoughCircles(circle_blurred, cv2.HOUGH_GRADIENT, 1.2, 100)#, None, 200, 40, 228, 254)
# if circles is not None:
# 	circles = np.round(circles[0, :]).astype("int")
# 	for (x, y, r) in circles:
# 		cv2.circle(circle, (x, y), r, (0, 255, 0), 4)
#
# show_image(circle, "with more circles")
