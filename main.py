import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("0.0.0.0", 80)
s.listen(5)

while True:

    client, addr = s.accept()

    while True:
        content = client.recv(32)

        print("Got a connection from %s" % str(addr))
    
        msg = 'Thank you for connecting' + "\r\n"
        s.send(msg.encode('ascii'))

    print("Closing connection")
    client.close()
