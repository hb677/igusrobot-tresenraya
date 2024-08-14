import cv2 as cv
import random
from igus_robot import *
import RPi.GPIO as GPIO
from board_analysis import check_player_move

def pickup_and_place(pieces_left, to):
    file_number = to + 1
    sendMessageToRobot('LoadProgram pickup_' + str(pieces_left) + 'leftcorrect.xml')
    time.sleep(0.3)
    sendMessageToRobot('StartProgram')
    time.sleep(3.8)
    sendMessageToRobot('LoadProgram place_to' + str(file_number) + 'correct.xml')
    time.sleep(0.3)
    sendMessageToRobot('StartProgram')

def who_first():
    who = input('player(p) or computer(c) first?')

    if who == 'P' or who =='p':
        return 'player'
    if who == 'C' or who =='c':
        return 'computer'

#given a board and a letter, this function returns True if that letter(x for player, o for computer) has won.
def is_winner(board_list, letter):

    return ((board_list[6] == letter and board_list[7] == letter and board_list[8] == letter) or # across the bottom
    (board_list[3] == letter and board_list[4] == letter and board_list[5] == letter) or # across the middle
    (board_list[0] == letter and board_list[1] == letter and board_list[2] == letter) or # across the top
    (board_list[6] == letter and board_list[3] == letter and board_list[0] == letter) or # down the left side
    (board_list[7] == letter and board_list[4] == letter and board_list[1] == letter) or # down the middle
    (board_list[8] == letter and board_list[5] == letter and board_list[2] == letter) or # down the right side
    (board_list[6] == letter and board_list[4] == letter and board_list[2] == letter) or # diagonal
    (board_list[8] == letter and board_list[4] == letter and board_list[0] == letter)) # diagonal

#make a duplicate of the board list and return
def get_board_copy(board_list):

    dupe_board = []

    for i in board_list:
        dupe_board.append(i)

    return dupe_board

def make_move(board_list, letter, index_0to8):
    board_list[index_0to8] = letter

#returns the index of the computers move from 0 to 8
def get_computer_move(board_list):
    
    #first check if there's any moves we can make to win the game
    for i in range(0, 9):
        #space must be empty to be able to check a move there
        if board_list[i] == ' ':
            copy = get_board_copy(board_list)
            make_move(copy, 'o', i)
            if is_winner(copy, 'o'):
                return i
            
    #next check if player can win on next turn
    for i in range(0, 9):
        #space must be empty to be able to check a move there
        if board_list[i] == ' ':
            copy = get_board_copy(board_list)
            make_move(copy, 'x', i)
            if is_winner(copy, 'x'):
                return i
    
    #next check corners
    possible_moves = []
    for i in [0, 2, 6, 8]:
        #space must be empty to be able to make a move there
        if board_list[i] == ' ':
            possible_moves.append(i)
    #choose a random move from possible corners
    if len(possible_moves) != 0:
        return random.choice(possible_moves)
    
    #next check centre
    if board_list[4] == ' ':
        return 4
    
    #finally check sides
    possible_moves = []
    for i in [1, 3, 5, 7]:
        #space must be empty to be able to make a move there
        if board_list[i] == ' ':
            possible_moves.append(i)
    #choose a random move from possible corners
    if len(possible_moves) != 0:
        return random.choice(possible_moves)
    
    #if checked all moves and none possible then board is full
    return 'no move'

#initialise camera
cam_port = int(input('which camera port are we using?'))
camera_position = input('what position is the camera in (1-3)?')
print('initialising camera...')
cam = cv.VideoCapture(cam_port)

#initialise robot
sendMessageToRobot("Connect")
sendMessageToRobot("Reset")
sendMessageToRobot("Enable")

#intialise button>>

# Desactivar advertencias (warnings)
GPIO.setwarnings(False)
# Configurar la librería para usar el número de pin.
# Llame GPIO.setmode(GPIO.BCM) para usar el canal SOC definido por Broadcom
GPIO.setmode(GPIO.BOARD)
# Configurar el pin 3 como entrada
boton=3
GPIO.setup(boton, GPIO.IN)

while True:

    #reset the board
    the_board = [' '] * 9
    pieces_left = 5
    turn = who_first()

    game_is_playing = True

    while game_is_playing:

        if turn == 'player':
            print('press button once finished')

            #button code from Marcos
            while True:
                boton_push = GPIO.input(boton)
                if boton_push==0:
                    break
            turn = 'computer'

        elif turn == 'computer':
            
            #live capture
            result, capture = cam.read() 

            the_board = check_player_move(the_board, capture, int(camera_position))
            print('player made move:')
            print(the_board)
            
            if is_winner(the_board, 'x'):
                print('player won')
                game_is_playing = False

            else:
                move = get_computer_move(the_board)

                if move == 'no move':
                    print('draw')
                    game_is_playing = False

                else:
                    make_move(the_board, 'o', move)
                    pickup_and_place(pieces_left, move)
                    print('computer made move:')
                    print(the_board)

                    if is_winner(the_board, 'o'):
                        print('computer won')
                        game_is_playing = False
                    
                    else:
                        pieces_left -= 1
                        turn = 'player'

    play_again = input('do you want to play again (yes[y] or no[n])?')
    if not play_again.lower().startswith('y'):
        break
                
