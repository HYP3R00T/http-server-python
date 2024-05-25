# Uncomment this to pass the first stage
import socket
from typing import ByteString
import re


def re_extract(s, pattern):
    search = re.search(pattern, s)
    if search:
        return search.group(1)


class Request:
    def __init__(self, data: ByteString):
        data_str = data.decode()
        lines = data_str.split("\r\n")

        request_line = lines[0]
        self.method, self.path, self.version = request_line.split()

        # To find various header fields
        self.headers = lines[1:]
        self.header = {}
        for line in self.headers:
            if line:
                parts = line.split(":", 1)
                if parts[0] == "User-Agent":
                    self.header[parts[0]] = parts[1].strip()


def main():
    print("Logs from your program will appear here!\n")
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)

    while True:
        try:
            connection, address = server_socket.accept()

            with connection:
                print(f"Accecpted connection from {address}")
                data = connection.recv(1024)
                print(data.decode())
                req = Request(data)

                try:
                    resp = ""
                    if req.path == "/":
                        resp = "HTTP/1.1 200 OK\r\n\r\n"
                    elif req.path.startswith("/echo/"):
                        arg = re_extract(req.path, r"/echo/(.*)")
                        resp = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(arg)}\r\n\r\n{arg}"
                    elif req.path.startswith("/user-agent"):
                        arg = req.header.get("User-Agent", "")
                        resp = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(arg)}\r\n\r\n{arg}"
                    else:
                        raise Exception("Not Found")
                except Exception:
                    resp = "HTTP/1.1 404 Not Found\r\n\r\n"

                connection.sendall(resp.encode())

        except Exception as e:
            print(f"Exception: {e}")


if __name__ == "__main__":
    main()
