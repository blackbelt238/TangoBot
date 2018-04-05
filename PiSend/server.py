import socket

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create a TCP/IP socket object
saddr = (socket.gethostname(), 9999)                             # create the server address using the local machine name
serversocket.bind(saddr)                                         # bind to the port
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
