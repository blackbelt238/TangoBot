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

                # receive a message and send a response
                msg = clientsocket.recv(1024).decode('ascii').replace('\n', '')
                print('  received: \"' + msg + '\"...', end='')
                clientsocket.sendall(msg.encode('ascii')) # just send the original message back as the response
                print('response sent')

                # perform an action based on the given message
                self.doAction(msg, msg.split(' ')[0] == 'add')
        finally:
            # Clean up the connection no matter what
            clientsocket.close()

    def doAction(msg, add):
        ''' doAction performs the action  '''
        accepted = True # indication of if the received phrase is accepted

        # if the action will be immediately executed, ensure Tango bot listens after
        if !add:
            self.actionqueue.push(None)

        # --- ACCEPTED PHRASES ---
        if msg == 'start' or msg == 'continue':
            print('\texecuting actions')
        elif msg == 'speak hello there':
            # Tango says "hello" and raises his head
            self.actionqueue.push(self.actionqueue.tango.head,False,4)
            self.actionqueue.push(self.actionqueue.tango.head,True,4)
            self.actionqueue.push(self.actionqueue.tango.speak,'hello there')
        else:
            accepted = False

        # if the phrase wasn't accepted and a listen command was already pushed, pop it before exiting
        if !accepted and !add:
            print('\tnot an accepted phrase')
            self.actionqueue.pop()
            return
        # if the phrase wasn't accepted and no listen command was pushed, just exit
        elif !accepted:
            print('\tnot an accepted phrase')
            return

        # immediately perform the given command if not instructed to add it
        if !add:
            self.actionqueue.execute()
