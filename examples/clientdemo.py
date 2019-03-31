import socket
import json

msgFromClient       = "Hello UDP Server"
bytesToSend         = str.encode(msgFromClient)
serverAddressPort   = ("127.0.0.1", 20001)
bufferSize          = 1024

with open("config.json", "r") as read_file:
    data = json.load(read_file)

bytesToSend = json.dumps(data)
bytesToSend = bytesToSend.encode('utf-8')
# Create a UDP socket at client side
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Send to server using created UDP socket
UDPClientSocket.sendto(bytesToSend, serverAddressPort)

msgFromServer = UDPClientSocket.recvfrom(bufferSize)

msg = "Message from Server {}".format(msgFromServer[0])

rmsg = msgFromServer[0].decode('utf-8')
print(msg)
print(rmsg)

rmsg = json.loads(rmsg)
print(rmsg['firstName'])