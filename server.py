import socket
from threading import Thread

class Server(Thread):
    ''' Server allows the standing up of a server to listen for connections, echoing back any message it recieves '''

    def __init__(self, aq, addr='10.200.3.99', port=5011):
        Thread.__init__(self)
        self.saddr = (addr, port)  # create the server address using the local machine name
        self.actionqueue = aq      # the ActionQueue the server is running alongside

    def run(self):
        print("Starting up server...")
        self.begin()

    def begin(self):
        ''' startServer stands up an echo server '''
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create a TCP/IP socket object
        serversocket.bind(self.saddr)                                    # bind to the port
        serversocket.listen(5)                                           # listen for up to 5 incoming connections

        clientsocket = None
        try:
            while True:
                # wait for a connection
                clientsocket, addr = serversocket.accept()
                print('connection from', addr)

                # recieve a message and send a response
                msg = clientsocket.recv(1024).decode('ascii').replace('\n', '')
                print('\treceived:',msg)
                clientsocket.sendall(msg.encode('ascii')) # just send the original message back as the response
                print('\tresponse sent')

                # see if it matches any predetermined commands
                if msg == 'start' or msg == 'continue':
                    self.actionqueue.execute()
                elif msg == 'speak hello there':
                    # Tango says "hello" and raises his head
                    self.actionqueue.push(self.actionqueue.tango.head,False,4)
                    self.actionqueue.push(self.actionqueue.tango.head,True,4)
                    self.actionqueue.push(self.actionqueue.tango.speak,'hello there')
                    self.actionqueue.execute()
        finally:
            # Clean up the connection no matter what
            clientsocket.close()
