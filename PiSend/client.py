import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create a TCP/IP socket object
serv_addr = (socket.gethostname(), 9999)              # create the server address using the local machine name
s.connect(serv_addr)                                  # connection to hostname on the port.

try:

    # Send data
    message = b'This is the message.  It will be repeated.'
    print('sending {!r}'.format(message))
    s.sendall(message)

    # Look for the response
    amount_received = 0
    amount_expected = len(message)

    while amount_received < amount_expected:
        data = s.recv(16)
        amount_received += len(data)
        print('received {!r}'.format(data))

finally:
    print('closing socket')
    s.close()
# # Receive no more than 1024 bytes
# msg = s.recv(1024)
#
# s.close()
# print (msg.decode('ascii'))
