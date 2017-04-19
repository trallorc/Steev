import Queue
import socket
import threading
import thread
import time
import sys


# Extends Thread class that works with one client
class ServerThread(threading.Thread):
    # overriding of constructor
    def __init__(self):
        threading.Thread.__init__(self)
        self.waitToStart = True
        self.id = 0;
        self.groupeList = None
        self.socket = None
        self.counter = 0
        self.newgamecounter = 0
        self.gameon = False

    def loop(self):  # animation loop
        ##self.gameon = True
        i = 0
        while self.gameon:
            time.sleep(2)
            for item in self.groupeList:
                item.socket.sendall("tick" + str(i) + "\n")
            i += 1

    # overriding of Thread run method
    def run(self):
        # Have our thread serve "forever"
        while True:
            # Get a client out of the queue
            tuple = clientPool.get()

            # Check if we actually have an actual client in the client variable:
            if tuple != None:
                client = tuple[0]  # client[0] - socket; client[1][0] - ip;
                # client[1][1] -port
                self.socket = client[0]
                self.groupeList = tuple[1]
                self.groupeList.append(self)

                self.id = int(tuple[2])

                print "Received connection from ip=:", client[1][0], "port=", client[1][1]

                self.socket.sendall("Wait for start##" + str(self.id) + "\n")

                if self.id == 3:

                    for item in self.groupeList:
                        item.socket.sendall("start\n")
                        item.waitToStart = False
                    time.sleep(2)
                while self.waitToStart:
                    time.sleep(2)

                print str(self.id) + " end sleep"
                if self.id == 1:
                    thread.start_new_thread(self.loop, ())  # run function self.loop in new thread

                while True:
                    buf = str(client[1][0]) + ": " + client[0].recv(1024)
                    buf = buf.strip()
                    # print "Server got :" + buf

                    if buf == "Bye":
                        self.socket.sendall("Bye\n")
                        break
                    else:

                        for item in self.groupeList:
                            item.socket.sendall(buf + "\n")

                self.socket.close()
                print 'Closed connection from ip=', client[1][0], "port=", client[1][1]
                self.groupeList.remove(self)
                time.sleep(2)
                if len(self.groupeList) == 0:
                    listOfCouples.remove(self.groupeList)


# Create our Queue. The Queue is used to share items between the threads.
clientPool = Queue.Queue(0)
listOfCouples = []
# Start some threads:
for x in xrange(4):
    ServerThread().start()  # ServerThread() - run constructor, start() - run run() method

# Set up the server:
PORT_NUMBER = 12346
# create an INET, STREAMing socket
# INET socket - IP protocol based sockets which use IP addresses and ports
# A socket is just an abstraction of a communication end point
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Address Family : AF_INET (this is IP version 4 or IPv4 - 32 bit address - 4 byte address)
# Type : SOCK_STREAM (this means connection oriented TCP protocol)
# Connection means a reliable "stream" of data. The TCP packets have an "order" or "sequence"
# Apart from SOCK_STREAM type of sockets there is another type called SOCK_DGRAM which indicates the UDP protocol.
# Other sockets like UDP , ICMP , ARP dont have a concept of "connection". These are non-connection based
# communication. Which means you keep sending or receiving packets from anybody and everybody.


# Helps to system forget server after 1 second
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

try:

    # bind socket to localhost and  PORT_NUMBER
    server.bind(('', PORT_NUMBER))

    # become a server socket
    server.listen(4)
    print "Server is listening"
    # the argument to listen  - (5) tells the socket library that we want it to queue up
    # as many as 5 connect requests when the program is already busy.
    # the 6th connection request shall be rejected.

    j = 0  # mone of players in couple
    #  Create list of one couple
    oneGameList = []
    # Have the server serve "forever":
    while True:
        newclient = server.accept()  # Connected point. Server wait for client
        # newClient - tuple : (clientsocket, address), address : tuple(ip,port)
        clientPool.put((newclient, oneGameList, j))  # add tuple to  clientPool

        j += 1
        if j == 4:
            listOfCouples.append(oneGameList)
            j = 0
            oneGameList = []

except Exception, e:
    server.close()
    sys.exit(1)
    raise e
