import cv2 as cv
import numpy as np

#Takes a point in a contour and returns it's x co-ordinate
def get_x_coord(point):

    return point[0][0]

#Takes a point in a contour and returns it's y co-ordinate
def get_y_coord(point):

    return point[0][1]

#Takes a set of four points and returns them in clockwise order from top left
def sort_clockwise(contour):

    #sorts by x co-ordinate and gives a list of left hand points
    x_sorted = sorted(contour, key=get_x_coord)
    left_hand = x_sorted[:2]
    
    #sorts those left hand points by y co-ordinate and gives top and bottom 
    left_hand_y_sorted = sorted(left_hand, key=get_y_coord)
    top_left = left_hand_y_sorted[0]
    bottom_left = left_hand_y_sorted[1]

    #list of right hand points
    right_hand = x_sorted[2:4]
    
    #sorts those right hand points by y co-ordinate and gives top and bottom
    right_hand_y_sorted = sorted(right_hand, key=get_y_coord)
    top_right = right_hand_y_sorted[0]
    bottom_right = right_hand_y_sorted[1]

    return top_left, top_right, bottom_right, bottom_left

#finds the bounding box of the board assuming it is the second largest contour
def get_bounding_box(image):

    img = image.copy()

    #copies image passed in black and white and applies a blur
    bandw = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    bandw = cv.medianBlur(bandw, 5)
    
    #applies gaussian thresholding to make binary image
    threshold = cv.adaptiveThreshold(bandw,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,\
                cv.THRESH_BINARY,11,2)

    #finds contours in image
    contours, hierarchy = cv.findContours(threshold, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    #new list in which contours are sorted by area enclosed
    contours_sorted = sorted(contours, key=cv.contourArea)

    #draws on the chosen contour
    drawing = img.copy()
    cv.drawContours(drawing, contours_sorted[-2], -1, (0,255,0), 3)

    #approximates contour down to 4 points
    list = np.linspace(0.001, 1.001, 1000)
    peri = cv.arcLength(contours_sorted[-2], True)
    for simplification in list:
        approx = cv.approxPolyDP(contours_sorted[-2],  simplification * peri, True)
        if len(approx) == 4:
            break

    return approx

#finds perspective change matrix
def perspective_change_matrix(top_left, top_right, bottom_right, bottom_left):
    
    #uses dimension of closest horizontal side to determine size of output image
    square_dimension = abs(bottom_right[0][0] - bottom_left[0][0])

    #points from bounding box and then new corners of image
    pts1 = np.float32([top_left[0], top_right[0], bottom_right[0], bottom_left[0]])
    pts2 = np.float32([[0, 0], [square_dimension, 0], [square_dimension, square_dimension], [0, square_dimension]])

    matrix = cv.getPerspectiveTransform(pts1, pts2)

    return matrix, square_dimension

#uses the given matrix and image to create a warped image of the given dimensions
def change_perspective(image, matrix, square_dimension):

    result = cv.warpPerspective(image, matrix, (square_dimension, square_dimension))

    return result