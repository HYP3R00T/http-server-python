import socket
import re
import threading
import sys


def re_extract(s, pattern):
    search = re.search(pattern, s)
    if search:
        return search.group(1)


class Request:
    def __init__(self, data):
        data_str = data.decode()
        lines = data_str.split("\r\n")

        request_line = lines[0]
        self.method, self.path, self.version = request_line.split()

        # To find various header fields
        self.headers = lines[1:-1]
        self.header = {}
        for line in self.headers:
            if line:
                print(line)
                parts = line.split(":", 1)
                if parts[0] == "User-Agent":
                    self.header[parts[0]] = parts[1].strip()
                if parts[0] == "Accept-Encoding":
                    self.header[parts[0]] = parts[1].strip()

        # Body
        self.body = lines[-1]


def handle_client(connection, address):
    with connection:
        print(f"Accecpted connection from {address}\n")
        data = connection.recv(1024)
        print(data.decode())
        req = Request(data)

        try:
            resp = ""

            if req.path == "/":
                resp = "HTTP/1.1 200 OK\r\n\r\n"

            elif req.path.startswith("/echo/"):
                arg = re_extract(req.path, r"/echo/(.*)")
                print(arg)
                print(req.header)
                if req.header.get("Accept-Encoding", "") == "gzip":
                    resp = f"HTTP/1.1 200 OK\r\nContent-Encoding: gzip\r\nContent-Type: text/plain\r\nContent-Length: {len(arg)}\r\n\r\n{arg}"
                elif req.header.get("Accept-Encoding", "") == "invalid-encoding":
                    resp = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(arg)}\r\n\r\n{arg}"

            elif req.path.startswith("/user-agent"):
                arg = req.header.get("User-Agent", "")
                resp = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(arg)}\r\n\r\n{arg}"

            elif req.path.startswith("/files"):
                directory = sys.argv[2]
                file_name = re_extract(req.path, r"/files/(.*)")

                if req.method == "GET":
                    try:
                        with open(f"{directory}/{file_name}", "r") as f:
                            body = f.read()
                        resp = f"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: {len(body)}\r\n\r\n{body}"

                    except Exception:
                        raise Exception("Not Found")
                elif req.method == "POST":
                    try:
                        with open(f"{directory}/{file_name}", "w") as f:
                            print(req.body)
                            f.write(req.body)

                        resp = f"HTTP/1.1 201 Created\r\nContent-Type: text/plain\r\nContent-Length: {len(req.body)}\r\n\r\n{req.body}"

                    except Exception:
                        raise Exception("Not Found")

            else:
                raise Exception("Not Found")

        except Exception:
            resp = "HTTP/1.1 404 Not Found\r\n\r\n"

        connection.sendall(resp.encode())


def main():
    print("Logs from your program will appear here!\n")
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)

    while True:
        try:
            connection, address = server_socket.accept()
            client_thread = threading.Thread(
                target=handle_client, args=(connection, address)
            )
            client_thread.start()
        except Exception as e:
            print(f"Exception: {e}")


if __name__ == "__main__":
    main()
