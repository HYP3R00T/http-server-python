# Uncomment this to pass the first stage
import socket


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    connection, address = server_socket.accept()
    print(f"Accecpted connection from {address}")

    data = connection.recv(1024)
    print(data.decode())
    data_components = data.decode("utf-8").split(r"\r\n")
    # [print(i) for i in data_components]

    request_line = data_components[0]
    path = request_line.split(" ")[1]
    if path == "/":
        connection.sendall(b"HTTP/1.1 200 OK\r\n\r\n")
    else:
        connection.sendall(b"HTTP/1.1 404 Not Found\r\n\r\n")


if __name__ == "__main__":
    main()
