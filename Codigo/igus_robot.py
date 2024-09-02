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

def alive():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Enter the IP address of the robot (192.168.3.11) here if you're not using a CPRog/iRC simulation
    server_address = ('192.168.3.11', 3920)
    sock.connect(server_address)

    # The ALIVEJOG message needs to be sent regularly (at least once a second) to keep the connection alive
    messageAliveJog = "CRISTART 1234 ALIVEJOG 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 CRIEND"


    # Encode the messages
    encodedAliveJog=messageAliveJog.encode('utf-8')
    arrayAliveJog=bytearray(encodedAliveJog)
        

    # Send ALIVEJOG
    sock.sendall(arrayAliveJog)
    time.sleep(0.1)		

