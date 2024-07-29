# Code for robot movements
# 
#
   
import socket
import time
def sendMessageToRobot(message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Enter the IP address of the robot (192.168.3.11) here if you're not using a CPRog/iRC simulation
    server_address = ('192.168.3.11', 3920)
    print("Connecting...")
    sock.connect(server_address)
    print("Connected")

    try:
    # The ALIVEJOG message needs to be sent regularly (at least once a second) to keep the connection alive
        messageAliveJog = "CRISTART 1234 ALIVEJOG 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 CRIEND"
    # This is my intended message (I use CMD DOUT since this creates a log entry on success)
        message = "CRISTART 1234 CMD " + message + " CRIEND"


    # Encode the messages
        encodedAliveJog=messageAliveJog.encode('utf-8')
        encoded=message.encode('utf-8')
        arrayAliveJog=bytearray(encodedAliveJog)
        array=bytearray(encoded)
        

    # Send first ALIVEJOG to establish the connection
        print("Sending ALIVEJOG")
        sock.sendall(arrayAliveJog)
        time.sleep(0.1)
        
    # Send the main message
        print("Sending message")
        sock.sendall(array)
        
        
    # I'm sending 10 more ALIVEJOG messages to keep the connection alive.
    # If I drop the connection too early our message may not get through.
    # A production program should send this once or twice a second from a parallel thread.
        print("Keeping connection alive")
        for i in range (1, 10):
            print("Sending ALIVEJOG")
            sock.sendall(arrayAliveJog)
            time.sleep(0.1)			

    finally:
        print("Finally")
        sock.close()



# Tic Tac Toe 
#
#

import random

def inputPlayerLetter():
    # Lets the player type which letter they want to be.
    # Returns a list with the player's letter as the first item, and the computer's letter as the second.
    letter = 'X'

    # the first element in the tuple is the player's letter, the second is the computer's letter.
    if letter == 'X':
        return ['X', 'O']
    else:
        return ['O', 'X']

def whoGoesFirst():
    who = input('Player(P) or computer(C) first?')

    if who == 'P' or who =='p':
        return 'player'
    if who == 'C' or who =='c':
        return 'computer'

def playAgain():
    # This function returns True if the player wants to play again, otherwise it returns False.
    print('Do you want to play again? (yes or no)')
    return input().lower().startswith('y')

def makeMove(board, letter, move):
    board[move] = letter
    

def isWinner(bo, le):
    # Given a board and a player's letter, this function returns True if that player has won.
    # We use bo instead of board and le instead of letter so we don't have to type as much.
    return ((bo[7] == le and bo[8] == le and bo[9] == le) or # across the top
    (bo[4] == le and bo[5] == le and bo[6] == le) or # across the middle
    (bo[1] == le and bo[2] == le and bo[3] == le) or # across the bottom
    (bo[7] == le and bo[4] == le and bo[1] == le) or # down the left side
    (bo[8] == le and bo[5] == le and bo[2] == le) or # down the middle
    (bo[9] == le and bo[6] == le and bo[3] == le) or # down the right side
    (bo[7] == le and bo[5] == le and bo[3] == le) or # diagonal
    (bo[9] == le and bo[5] == le and bo[1] == le)) # diagonal

def getBoardCopy(board):
    # Make a duplicate of the board list and return it the duplicate.
    dupeBoard = []

    for i in board:
        dupeBoard.append(i)

    return dupeBoard

def isSpaceFree(board, move):
    # Return true if the passed move is free on the passed board.
    return board[move] == ' '

def getPlayerMove(board):
    # Let the player type in his move.
    move = ' '
    while move not in '1 2 3 4 5 6 7 8 9'.split() or not isSpaceFree(board, int(move)):
        print('What is your next move? (1-9)')
        move = input()
    return int(move)

def chooseRandomMoveFromList(board, movesList):
    # Returns a valid move from the passed list on the passed board.
    # Returns None if there is no valid move.
    possibleMoves = []
    for i in movesList:
        if isSpaceFree(board, i):
            possibleMoves.append(i)

    if len(possibleMoves) != 0:
        return random.choice(possibleMoves)
    else:
        return None

def getComputerMove(board, computerLetter):
    # Given a board and the computer's letter, determine where to move and return that move.
    if computerLetter == 'X':
        playerLetter = 'O'
    else:
        playerLetter = 'X'

    # Here is our algorithm for our Tic Tac Toe AI:
    # First, check if we can win in the next move
    for i in range(1, 10):
        copy = getBoardCopy(board)
        if isSpaceFree(copy, i):
            makeMove(copy, computerLetter, i)
            if isWinner(copy, computerLetter):
                return i

    # Check if the player could win on his next move, and block them.
    for i in range(1, 10):
        copy = getBoardCopy(board)
        if isSpaceFree(copy, i):
            makeMove(copy, playerLetter, i)
            if isWinner(copy, playerLetter):
                return i

    # Try to take one of the corners, if they are free.
    move = chooseRandomMoveFromList(board, [1, 3, 7, 9])
    if move != None:
        return move

    # Try to take the center, if it is free.
    if isSpaceFree(board, 5):
        return 5

    # Move on one of the sides.
    return chooseRandomMoveFromList(board, [2, 4, 6, 8])

def isBoardFull(board):
    # Return True if every space on the board has been taken. Otherwise return False.
    for i in range(1, 10):
        if isSpaceFree(board, i):
            return False
    return True

while True:
    # Initialise robot
    sendMessageToRobot("Connect")
    sendMessageToRobot("Reset")
    sendMessageToRobot("Enable")
    # Reset the board
    theBoard = [' '] * 10
    piecesleft = 5
    playerLetter, computerLetter = inputPlayerLetter()
    turn = whoGoesFirst()
    print('The ' + turn + ' will go first.')
    gameIsPlaying = True

    while gameIsPlaying:
        if turn == 'player':
            # Player's turn.
            print(theBoard)
            move = getPlayerMove(theBoard)
            makeMove(theBoard, playerLetter, move)

            if isWinner(theBoard, playerLetter):
                print(theBoard)
                print('player win')
                sendMessageToRobot("LoadProgram LOST.xml")
                time.sleep(0.5)
                sendMessageToRobot("StartProgram")
                gameIsPlaying = False
            else:
                if isBoardFull(theBoard):
                    print(theBoard)
                    print('tie')
                    break
                else:
                    turn = 'computer'

        else:
            # Computer's turn.
            move = getComputerMove(theBoard, computerLetter)
            makeMove(theBoard, computerLetter, move)

            if int(piecesleft) == 5:
                sendMessageToRobot("LoadProgram pickup_5leftcorrect.xml")
                time.sleep(0.5)
                sendMessageToRobot("StartProgram")
            if int(piecesleft) == 4:
                sendMessageToRobot("LoadProgram pickup_4leftcorrect.xml")
                time.sleep(0.5)
                sendMessageToRobot("StartProgram")
            if int(piecesleft) == 3:
                sendMessageToRobot("LoadProgram pickup_3leftcorrect.xml")
                time.sleep(0.5)
                sendMessageToRobot("StartProgram")
            if int(piecesleft) == 2:
                sendMessageToRobot("LoadProgram pickup_2leftcorrect.xml")
                time.sleep(0.5)
                sendMessageToRobot("StartProgram")
            if int(piecesleft) == 1:
                sendMessageToRobot("LoadProgram pickup_1leftcorrect.xml")
                time.sleep(0.5)
                sendMessageToRobot("StartProgram")

            finishedpickup = input('Click enter if robot finished pick-up')

            sendMessageToRobot('LoadProgram place_to' + str(move) +'correct.xml')
            time.sleep(0.5)
            sendMessageToRobot("StartProgram")
            piecesleft -= 1

            if isWinner(theBoard, computerLetter):
                print(theBoard)
                print('computer win')
                sendMessageToRobot("LoadProgram WIN.xml")
                time.sleep(0.5)
                sendMessageToRobot("StartProgram")
                gameIsPlaying = False
            else:
                if isBoardFull(theBoard):
                    print(theBoard)
                    print('tie')
                    break
                else:
                    turn = 'player'

    if not playAgain():
        break