import cv2 as cv
import numpy as np

def get_contours_colour_masking(image):

    #hue(colour wheel), saturation(white to full colour), and value (how dark)
    H = 35 #0
    S = 60 #0
    V = 110 #0
    H2 = 100 #180
    S2 = 255 #255
    V2 = 255 #255

    hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)

    lower_boundary = np.array([H, S, V])
    upper_boundary = np.array([H2,S2,V2])

    mask = cv.inRange(hsv, lower_boundary, upper_boundary)

    #finds contours in image
    contours, hierarchy = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    #new list in which contours are sorted by area enclosed
    contours_sorted_colour_masking = sorted(contours, key=cv.contourArea, reverse = True)

    return contours_sorted_colour_masking

#only need to search for crosses as robot places circles itself
def is_empty(image):

    #assumes square is empty and looks for cross
    empty = True

    image_area = image.shape[0] * image.shape[1]

    contours = get_contours_colour_masking(image)

    #if no contours found then definitely empty
    if len(contours) == 0:
        return empty

    if len(contours) < 7:

        #checks all contours for cross
        for i in contours[0:len(contours)]:

            #from experience:
            #circles usually take up an area of ~ 30-35%
            #crosses usually take up an area of ~ 20-25%
            #when empty... noise usually takes up an area of less than 1%
            if cv.contourArea(i) / image_area > 0.15:
                empty = False
    
    else:

        #checks only first 6 contours for cross
        for i in contours[0:6]:

            #from experience:
            #circles usually take up an area of ~ 30-35%
            #crosses usually take up an area of ~ 20-25%
            #when empty... noise usually takes up an area of less than 1%
            if cv.contourArea(i) / image_area > 0.15:
                empty = False
    
    return empty

