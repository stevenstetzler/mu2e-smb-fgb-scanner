import cv2
import numpy as np


def show_image(image, title):
	cv2.imshow(title, image)
	cv2.waitKey(0)
	cv2.destroyAllWindows()


MIN_MATCH_COUNT = 10

print("Reading images...")
template_orig = cv2.imread("C:\\Users\\Steven\\Desktop\\Test\\Measurements\\Bars\\SMB_0.jpg", 0)
image_orig = cv2.imread("C:\\Users\\Steven\\Desktop\\Test\\Measurements\\Bars\\SMB_10.jpg", 0)

template = cv2.resize(template_orig, (int(template_orig.shape[1]/10), int(template_orig.shape[0]/10)))
image = cv2.resize(image_orig, (int(image_orig.shape[1]/10), int(image_orig.shape[0]/10)))

# Initiate SIFT detector
sift = cv2.xfeatures2d.SIFT_create()

print("Finding keypoints and dsecriptors...")
# find the keypoints and descriptors with SIFT
kp1, des1 = sift.detectAndCompute(image, None)
kp2, des2 = sift.detectAndCompute(template, None)

FLANN_INDEX_KDTREE = 0
index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
search_params = dict(checks=50)

flann = cv2.FlannBasedMatcher(index_params, search_params)

print("Matching features...")
matches = flann.knnMatch(des1, des2, k=2)

print("Performing comparison test...")
# store all the good matches as per Lowe's ratio test.
good = []
for m, n in matches:
	if m.distance < 0.55 * n.distance:
		good.append(m)

print("# Matches: ", len(good))

print("Matching images...")
if len(good) > MIN_MATCH_COUNT:
	src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
	dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)

	M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
	matchesMask = mask.ravel().tolist()
	print(M)
	h, w = image.shape
	pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
	dst = cv2.perspectiveTransform(pts, M)
	img2 = cv2.polylines(template, [np.int32(dst)], True, 255, 3, cv2.LINE_AA)

	h_2, w_2 = img2.shape
	adjusted_image = cv2.warpPerspective(image, M, (w_2, h_2))
	# cv2.imshow("Warped", adjusted_image)
	# cv2.waitKey(0)
	# cv2.destroyAllWindows()

	show_image(template, "Template")
	show_image(adjusted_image, "Adjusted")
	adjusted_image_orig = cv2.warpPerspective(image_orig, M, (image_orig.shape[1], image_orig.shape[0]))
	show_image(adjusted_image_orig, "Adjusted original")
