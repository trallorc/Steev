# coding=utf-8
import socket
import threading


class ConnectAndSendThread(threading.Thread):
    def run(self):
        # Connect to the server:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('localhost', 12345))
        # Start reading from server in separate thread
        ReadThread(client).start()

        while True:
            # Send some messages:
            buf = raw_input(">>")
            buf = buf.strip()
            client.sendall(buf + "\n")
            if buf == "Bye":
                break


class ReadThread(threading.Thread):
    def __init__(self, client):
        self.client = client
        threading.Thread.__init__(self)

    def run(self):
        while True:
            buf = self.client.recv(1024)
            buf = buf.strip()
            print buf
            if buf == "Bye":
                break
        self.client.close()

    # Main code


ConnectAndSendThread().start()
