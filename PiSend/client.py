import socket

def sendTextToAndroid(message):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create a TCP/IP socket object
    serv_addr = (socket.gethostname(), 9999)              # create the server address using the local machine name
    s.connect(serv_addr)                                  # connection to hostname on the port.

    try:
        # Send data
        print('sending {!r}'.format(message))
        s.sendall(message.encode('ascii'))

        # Look for the response
        amount_received = 0
        amount_expected = len(message)
        echo = ''

        # incrementally reconstruct the message
        while amount_received < amount_expected:
            data = s.recv(16)
            echo += data.decode('ascii')
            amount_received += len(data)
        print("\nServer echoed:", echo)

    finally:
        # close the connection no matter what
        s.close()
