import cv2

def show_image(image, title):
	cv2.imshow(title, image)
	cv2.waitKey(0)
	cv2.destroyAllWindows()


class rect:
	def __init__(self, x, y, width, height):
		self.__x = x
		self.__y = y
		self.__width = width
		self.__height = height

	def x(self):
		return self.__x

	def y(self):
		return self.__y

	def width(self):
		return self.__width

	def height(self):
		return self.__height


def get_holes(image):
	holes = []
	for crop in hole_rect_list:
		holes.append(image[crop.y():crop.y() + crop.height(), crop.x():crop.x() + crop.width()])
	return holes


def get_bars(image):
	bars = []
	for crop in bar_rect_list:
		bars.append(image[crop.y():crop.y() + crop.height(), crop.x():crop.x() + crop.width()])
	return bars


bar_rect_list = []
for i in range(11):
	bar_rect_list.append(rect(550, 850 + 2510*i, 9250, 1570))
for i in range(11):
	bar_rect_list.append(rect(10750, 850 + 2510*i, 9250, 1530))

hole_rect_list = []
hole_rect_list.append(rect(210, 570, 540, 540))
hole_rect_list.append(rect(830, 630, 390, 380))
hole_rect_list.append(rect(3320, 630, 390, 380))
hole_rect_list.append(rect(5520, 630, 390, 380))
hole_rect_list.append(rect(8020, 630, 390, 380))
hole_rect_list.append(rect(8460, 500, 600, 560))

im = cv2.imread("C:\\Users\\Steven\\Desktop\\Projects\\mu2e-smb-fgb-scanner\\Test\\Images\\Frame.jpg", cv2.IMREAD_COLOR)
