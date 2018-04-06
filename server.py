import socket

class Server:
    ''' Server allows the standing up of a server to listen for connections, echoing back any message it recieves '''
    saddr = (socket.gethostname(), 9999) # create the server address using the local machine name
    actionqueue = None                   # the ActionQueue the server is running alongside

    def start():
        ''' startServer stands up an echo server '''
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create a TCP/IP socket object
        serversocket.bind(Server.saddr)                                  # bind to the port
        serversocket.listen(5)                                           # listen for up to 5 incoming connections

        try:
            while True:
                # wait for a connection
                clientsocket, addr = serversocket.accept()
                print('connection from', addr)

                # recieve a message
                msg = clientsocket.recv(1024).decode('ascii')
                # see if it matches any predetermined commands
                if msg == 'start':
                    Server.actionqueue.execute()
        finally:
            # Clean up the connection no matter what
            clientsocket.close()
Server.start()
