import cv2
import numpy
import pprint


def check_square(square):
    # TODO: Possible improvement to check whether the sizes of the squares are good, etc.
    return True


def sort_squares(squares):
    squares.sort(key=lambda s: s[0][0][1], reverse=False)

source_img = cv2.imread('test1.jpg')
img = cv2.cvtColor(source_img, cv2.COLOR_BGR2GRAY)

w, h = img.shape[::-1]
desired_width = 300
multiply = desired_width / w
new_width = int(w * multiply)
new_height = int(h * multiply)

source_img = cv2.resize(source_img, (new_width, new_height))
img = cv2.resize(img, (new_width, new_height))

img = img[0:new_height, 0:new_width//3]
img = cv2.GaussianBlur(img, (5, 5), 0)
ret, img = cv2.threshold(img, 140, 255, cv2.THRESH_BINARY_INV)
im2, contours, hierarchy = cv2.findContours(
    img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

possible_squares = []
for contour in contours:
    perimetr = cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, perimetr * 0.05, True)
    if len(approx) == 4:
        square = numpy.int0(approx)
        possible_squares.append(square)
        # Uncomment for debug
        # cv2.drawContours(source_img, square, -1, (255, 0, 0), 10)

squares = [s for s in possible_squares if check_square(s)]
sort_squares(squares)

for i, s in enumerate(squares):        
    top = 999999
    left = 999999
    bottom = 0
    right = 0
    for point in s:
        if point[0][1] > bottom:
            bottom = point[0][1]
        if point[0][1] < top:
            top = point[0][1]
        if point[0][0] > right:
            right = point[0][0]
        if point[0][0] < left:
            left = point[0][0]
    new_img = img[top:bottom, left:right]
    
    white_pixels = numpy.sum(new_img == 255)
    black_pixels = numpy.sum(new_img == 0) 
    probability = white_pixels / (black_pixels + white_pixels)
    print('Probability on %i square: %.2f' % (i, probability))
    # cv2.imshow('sqr' + str(my_sum), new_img)


# cv2.imshow('img',  img)
# cv2.imshow('source_img', source_img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()



