import Queue
import socket
import threading


# Thread class that works with one client
class ServerThread(threading.Thread):
    # overriding of Thread run method
    def run(self):
        # Have our thread serve "forever"
        while True:
            # Get a client out of the queue
            tupleduple = clientPool.get()

            # Check if we actually have an actual client in the client variable:
            if not tupleduple is None:
                client = tupleduple[0]
                groupelist = tupleduple[1]
                print "Received connection:", "ip = ", client[1][0], "port = ", client[1][1]
                # client[0] - client socket;
                # client[1] - client address
                # client[1][0] - client ip
                # client[1][1] - client port
                client[0].sendall("Server has been started to serve you! What is your name?\n")

                i = 0
                name = ""
                while True:
                    buf = client[0].recv(1024)  # read client response
                    buf = buf.strip()
                    print "Server say :" + buf
                    if i == 0:
                        name = buf
                        i = 1
                    if buf == "nicememe":
                        client[0].sendall("nicememe\n")
                        break
                    elif buf:
                        for item in groupelist:
                            item[0].sendall(name + " say: " + buf + "\n")

                client[0].close()
                print 'Closed connection:', client[1][0]
                groupelist.remove(client)
                if len(groupelist) == 0:
                    listOfClients.remove(groupelist)


# Create our Queue:
clientPool = Queue.Queue(0)  # invoke constructor of class Queue
# Create list of clients
listOfClients = []  # couples list
# Start some threads:
for x in xrange(4):
    ServerThread().start()  # invoke constructor of class ServerThread and his run function

# Set up the server:
PORT_NUMBER = 12346
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print "Server On Line"
try:

    server.bind(('', PORT_NUMBER))
    server.listen(2)

    # Have the server serve "forever":
    j = 0

    oneGameList = []  # for two players
    while True:
        newclient = server.accept()
        clientPool.put((newclient, oneGameList))
        oneGameList.append(newclient)
        j += 1
        if j == 2:
            j = 0
            listOfClients.append(oneGameList)
            oneGameList = []
except Exception, e:
    server.close()
    raise e
