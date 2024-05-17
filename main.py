import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("0.0.0.0", 80))
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
