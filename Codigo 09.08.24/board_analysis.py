import cv2 as cv
from find_board import *
from chop import slice_and_return
from shape_analysis_v3 import is_empty

#camera position is a number 1 to 3, measured clockwise, where robot is position 0
def check_player_move(board_list, image, camera_position):

    #gets corners of boards bounding box
    top_left, top_right, bottom_right, bottom_left = sort_clockwise(get_bounding_box(image))

    #finds matrix required to complete perspective change
    matrix, square_dimension = perspective_change_matrix(top_left, top_right, bottom_right, bottom_left)

    #completes perspective change
    board = change_perspective(image, matrix, square_dimension)

    if camera_position == 3:
        #rotates 90degrees so as square1 on the board is top left
        board = cv.rotate(board, cv.ROTATE_90_CLOCKWISE)

    if camera_position == 1:
        #rotates 90degrees so as square1 on the board is top left
        board = cv.rotate(board, cv.ROTATE_90_COUNTERCLOCKWISE)

    #slices the board into 9
    square1, square2, square3, square4, square5, square6, square7, square8, square9 = slice_and_return(board)

    #list to iterate through
    square_list = [square1, square2, square3, square4, square5, square6, square7, square8, square9]

    counter = 0
    for i in board_list:

        #if that square has not been played on yet then we must check it's status
        if i == ' ':

            #if empty is not(True) i.e. empty is False i.e. the square contains a cross 
            #then we must write an x into the relevant position on our list
            if not is_empty(square_list[counter]):
                board_list[counter] = 'x'

        counter += 1

    return board_list