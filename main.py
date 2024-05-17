import os
import socket

# Create a socket object and set options
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Get the port from environment variables or use 8080 as default
port = int(os.getenv('PORT', 8080))
print(f'Server will start on port {port}')

# Bind the socket to a public host and the specified port
s.bind(("0.0.0.0", port))

# Tell the socket to listen for incoming connections
s.listen(5)

http_response = """\
HTTP/1.1 200 OK

Thank you for connecting
"""

# Forever loop to handle incoming connections
while True:
    # Accept an incoming connection
    client, addr = s.accept()

    print(f"Got a connection from {addr}")

    # Send HTTP response
    client.send(http_response.encode('utf-8'))

    # Handle received data
    while True:
        try:
            # Receive data from client
            content = client.recv(1024)

            # If no data is received, break the loop and close the connection
            if not content:
                break
            else:
                # Print received data
                print(f"Received data: {content.decode('utf-8')}")

        except ConnectionResetError:
            # In case of abrupt client disconnection
            print("Connection was reset by client")
            break

    # Close the connection
    print("Closing connection")
    client.close()
