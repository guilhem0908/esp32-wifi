import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("0.0.0.0", 80)
s.listen(5)

while True:

    client, addr = s.accept()

    while True:
        content = client.recv(32)

        if len(content) == 0:
            break

        else:
            print(content)

    print("Closing connection")
    client.close()
