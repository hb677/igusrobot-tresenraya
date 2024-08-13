import socket
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_address = ('192.168.3.11', 3920)
print("Connecting...")
sock.connect(server_address)
print("Connected")

# The ALIVEJOG message needs to be sent regularly (at least once a second) to keep the connection alive
messageAliveJog = "CRISTART 1234 ALIVEJOG 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 CRIEND"

# Encode the messages
encodedAliveJog=messageAliveJog.encode('utf-8')
arrayAliveJog=bytearray(encodedAliveJog)

while True:
    print("Sending ALIVEJOG")
    sock.sendall(arrayAliveJog)
    time.sleep(0.1)	