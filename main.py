import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

s.bind(("0.0.0.0", 80))

s.listen(5)

http_response = """\
HTTP/1.1 200 OK

Thank you for connecting
"""

while True:

    client, addr = s.accept()

    print(f"Got a connection from {addr}")

    while True:
        content = client.recv(32)

        if not content:
            break
        else:
            print(f"Received data: {content.decode('ascii')}")

        client.send(http_response.encode('ascii'))

    print("Closing connection")
    client.close()
