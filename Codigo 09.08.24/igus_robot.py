def sendMessageToRobot(sock, message):

# This is my intended message (I use CMD DOUT since this creates a log entry on success)
    message = "CRISTART 1234 CMD " + message + " CRIEND"

# Encode the message
    encoded=message.encode('utf-8')
    array=bytearray(encoded)
    
# Send the main message
    print("Sending message")
    sock.sendall(array)
        