import socket
import os

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
port = int(os.getenv('PORT', 8080))
s.bind(("0.0.0.0", port))
s.listen(5)

while True:

    client, addr = s.accept()

    print("Got a connection from %s" % str(addr))

    while True:
        content = client.recv(1024)

        if not content:
            break
        else:
            print("Received data: %s" % content.decode('utf-8'))
    
        msg = 'Thank you for connecting' + "\r\n"
        client.send(msg.encode('utf-8'))

    print("Closing connection")
    client.close()
