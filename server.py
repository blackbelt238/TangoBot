import socket

class Server:
    ''' Server allows the standing up of a server to listen for connections, echoing back any message it recieves '''
    saddr = (socket.gethostname(), 9999) # create the server address using the local machine name

    def startServer():
        ''' startServer stands up an echo server '''
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create a TCP/IP socket object
        serversocket.bind(Server.saddr)                                  # bind to the port
        serversocket.listen(5)                                           # listen for up to 5 incoming connections

        while True:
            # wait for a connection
            clientsocket, addr = serversocket.accept()
            try:
                print('connection from', addr)

                # Receive the data in small chunks and retransmit it
                while True:
                    data = clientsocket.recv(16)
                    print('received {}'.format(data.decode('ascii')))
                    if data:
                        print('sending data back to the client')
                        clientsocket.sendall(data)
                    else:
                        print('no data from', addr)
                        break
            finally:
                # Clean up the connection no matter what
                clientsocket.close()
Server.startServer()
