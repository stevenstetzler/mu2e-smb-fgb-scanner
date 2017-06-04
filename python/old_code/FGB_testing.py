import cv2
from image_utils import show_image
from class_defs import rect
from image_utils import get_good_crop_rect
import numpy as np


def contrast_stretch(img):
	ret_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	max_val = max(img.flatten())
	min_val = min(img.flatten())
	for x in range(img.shape[0]):
		for y in range(img.shape[1]):
			ret_img[x, y] = int((ret_img[x, y] - min_val) * (255. / (max_val - min_val)))
	return ret_img


hole_rect_list = []
hole_rect_list.append(rect(180, 480, 590, 620))
hole_rect_list.append(rect(780, 500, 440, 540))
hole_rect_list.append(rect(3280, 500, 440, 540))
hole_rect_list.append(rect(5480, 500, 440, 540))
hole_rect_list.append(rect(7980, 500, 440, 540))
hole_rect_list.append(rect(8350, 400, 700, 700))


# full_image = cv2.imread("C:/Users/Steven/Desktop/Projects/mu2e-smb-fgb-scanner/python/Frame.jpg", cv2.IMREAD_COLOR)
# left_bar = full_image[850:850 + 1570, 550:550 + 9250]
# cv2.imwrite("smb_left_bar.jpg", left_bar)

left_bar = cv2.imread("fgb_left_bar.jpg", cv2.IMREAD_COLOR)

# show_image(left_bar, "bar_1")
# exit()

holes = []
for crop in hole_rect_list:
	candidate_hole = left_bar[crop.y():crop.y() + crop.height(), crop.x():crop.x() + crop.width()]
	# show_image(candidate_hole, "Candidate")
	holes.append(candidate_hole)

left_hole = holes[0]
show_image(left_hole, "left hole")
cv2.imwrite("left_hole.jpg", left_hole )

crop = get_good_crop_rect(left_hole)
# left_hole = left_hole[crop.y():crop.y() + crop.height(), crop.x():crop.x() + crop.width()]
# show_image(left_hole, "cropped")

blurred = cv2.GaussianBlur(cv2.cvtColor(left_hole, cv2.COLOR_BGR2GRAY), (5, 5), 2, None, 2)
edged = cv2.Canny(blurred, 25, 50)
kernel = np.ones((3, 3), np.uint8)
dilated = cv2.dilate(edged, kernel, iterations=1)

show_image(edged, "edges")
show_image(dilated, "dialated")

min_rad_search = 207
max_rad_search = 213
min_rad = 207
max_rad = 213

# min_rad_search = 65
# max_rad_search = 75
# min_rad = 69
# max_rad = 73

# min_rad_search = 220
# max_rad_search = 240
# min_rad = 225
# max_rad = 233
canny_thresh = 50

# canny_thresh = 50

gray = cv2.cvtColor(left_hole, cv2.COLOR_BGR2GRAY)
# normalized = contrast_stretch(left_hole)
# show_image(normalized, "normalzied")
circles = cv2.HoughCircles(image=blurred, method=cv2.HOUGH_GRADIENT, dp=1,
                           minDist=3, minRadius=min_rad_search, maxRadius=max_rad_search, param1=canny_thresh, param2=25)
if circles is not None:
	print "Circles:", circles
	good_circles = [circles[0][j] for j in range(len(circles[0])) if (min_rad < circles[0][j][2] < max_rad)]
	print "Good Circles", good_circles
	# print("Found", len(circles[0]), "circles")
	# for (x, y, r) in circles[0]:
	# 	print("Found circle: (" + str(x) + ", " + str(y) + ", " + str(r))
	# cv2.circle(hole, (x, y), r, (0, 255, 0), 2)

	# for circle in good_circles:
	# 	print("radius:", circle[2])
	if len(good_circles) > 0:
		center_x = sum([circle[0] for circle in good_circles]) / len(good_circles)
		center_y = sum([circle[1] for circle in good_circles]) / len(good_circles)
		radius = sum([circle[2] for circle in good_circles]) / len(good_circles)
		return_img = left_hole.copy()
		cv2.circle(return_img, (int(center_x), int(center_y)), int(radius), (0, 255, 0), 2)
		show_image(return_img, "Circle")

