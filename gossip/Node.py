import socket
import sys
import threading
import time
import random
import json

mutex_lock = threading.Lock()
gossip_lock = threading.Lock()

def get_address_tuple(address):
    address = address[1:-1]
    address = address.split(',')
    address[0] = '127.0.0.1'
    address[1] = int(address[1])
    address_tuple = tuple(address)
    return address_tuple


server_address_set = set([])
server_gossip_set = set([])

class Node_Client:
    def __init__(self,node_server_ip,node_server_port):
        self.node_server_ip = node_server_ip
        self.node_server_port = node_server_port
        self.UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    def connect_access_point(self):
        msg = "Send_node_addresses"
        self.UDPClientSocket.sendto(msg.encode('utf-8'),("127.0.0.1",8080))
        apreply = self.UDPClientSocket.recvfrom(1024)
        apreply = apreply[0]
        apreply = apreply.decode('utf-8')
        apreply = json.loads(apreply)
        for i in range(3):
            mutex_lock.acquire()
            server_address_set.add(apreply[i])
            mutex_lock.release()
        print("done")


    def connect_other_node(self):
        msg = str((self.node_server_ip,self.node_server_port))
        mutex_lock.acquire()
        server_address_list = list(server_address_set)
        mutex_lock.release()
        address = random.choice(server_address_list)
        address = get_address_tuple(address)
        print(address)
        self.UDPClientSocket.sendto(msg.encode('utf-8'),address)
        print("sent")


class Node_Server:
    def __init__(self,ip,port):
        self.ip = ip
        self.port = port
        self.UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.UDPServerSocket.bind((self.ip,self.port))
        print("UDP server up and listening")


    def read(self):
        while (True):
            print("listening")
            bytesAddressPair = self.UDPServerSocket.recvfrom(1024)

            message = bytesAddressPair[0]
            address = bytesAddressPair[1]
            new_server_address = message.decode('utf-8')
            # server_address_set.add(new_server_address)
            clientMsg = "Message from Client:{}".format(message)
            clientIP = "Client IP Address:{}".format(address)
            print(clientMsg)
            print(clientIP)


def server_thread():
    # Take IP and Port input through command line arguments
    instance_server = Node_Server(sys.argv[1],int(sys.argv[2]))
    instance_server.read()

if len(sys.argv)==3:
    t2 = threading.Thread(target=server_thread)
    t2.start()
    instance_client = Node_Client(sys.argv[1],int(sys.argv[2]))
    instance_client.connect_access_point()
    while(True):
        print("a: Input to other node")
        print("b: Sync with Access point")
        print("c: print address space")
        a = input()
        if a == 'a':
            instance_client.connect_other_node()
        if a == 'b':
            instance_client.connect_access_point()
        if a == 'c':
            print(server_address_set)


else:
    print("Python3 filename.py ip portnumber")


