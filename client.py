import socket

class Client:
    ''' Client allows the sending of messages to a server address '''
    saddr = (socket.gethostname(), 9999) # server address using the local machine name

    def sendMessage(message):
        ''' sendMessage takes in a message, sends it to the server at saddr, and returns the response '''

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create a TCP/IP socket object
        s.connect(Client.saddr)                               # connection to hostname on the port.

        try:
            # Send the message across the socket
            print('sending {!r}'.format(message))
            message += '\n'
            s.sendall(message.encode('ascii'))

            # return the response
            return s.recv(1024).decode('ascii')

        # close the connection no matter what
        finally:
            s.close()
