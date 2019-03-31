import socket
import sys
import json
import time
import random


def toolbar(length):
    toolbar_width = length

    # setup toolbar
    sys.stdout.write("[%s]" % (" " * toolbar_width))
    sys.stdout.flush()
    sys.stdout.write("\b" * (toolbar_width + 1))  # return to start of line, after '['

    for i in range(toolbar_width):
        time.sleep(0.1)  # do real work here
        # update the bar
        sys.stdout.write("*")
        sys.stdout.flush()

    sys.stdout.write("]\n")

def read(name):
    with open(name, 'r') as read_file:
        data = json.load(read_file)
        read_file.close()
    return data


def write(name, data):
    with open(name, "w") as write_file:
        json.dump(data, write_file)
        write_file.close()


class acess_Point:
    def __init__(self,ip,port):
        self.ip = ip
        self.port = port

        # Create a datagram socket
        self.UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

        # Bind to address and ip
        self.UDPServerSocket.bind((self.ip, self.port))


    def accept_Packets(self):
        print("Access point is up and listening")
        while(True):
            self.bytesAddressPair = self.UDPServerSocket.recvfrom(1024)
            message = self.bytesAddressPair[0]
            address = self.bytesAddressPair[1]
            server_address_list = []
            for i in range(3):
                server_address_list.append(random.choice(self.data['Node Server Address']))
            msg = json.dumps(server_address_list)
            self.UDPServerSocket.sendto(msg.encode('utf-8'),address)



    def configurefile(self):
        self.data = read('gossip/config.json')
        node_server_address = []
        for i in range(10):
            tup = str(("127.0.0.1",10000+i))
            node_server_address.append(tup)
        self.data["Node Server Address"] = node_server_address
        write('gossip/config.json',self.data)


# Take access point IP and Port input through command line arguments
instance = acess_Point("127.0.0.1", 8080)
print(":::::::::::::ACCESS POINT:::::::::::::")
toolbar(20)
print("Generating configuration for gossip protocol")
instance.configurefile()
toolbar(20)
print("done")
toolbar(20)
instance.accept_Packets()