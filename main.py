import os
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

port = int(os.getenv('PORT', 8080))
print(port)

s.bind(("0.0.0.0", port))

s.listen(5)

http_response = """\
HTTP/1.1 200 OK

Thank you for connecting
"""

while True:

    client, addr = s.accept()

    print(f"Got a connection from {addr}")

    while True:
        content = client.recv(1024)

        if not content:
            break
        else:
            print(f"Received data: {content.decode('utf-8')}")

        client.send(http_response.encode('utf-8'))

    print("Closing connection")
    client.close()
