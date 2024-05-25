# Simple HTTP Server in Python

## Overview

This is a basic HTTP server implemented in Python using sockets. The server can handle various types of requests, including serving files, echoing messages, and returning user-agent information.

## Features

- **Root Path Handling**: Responds with a simple 200 OK message.
- **Echo Path**: Returns the text following `/echo/` in the URL. Supports gzip encoding if requested.
- **User-Agent Path**: Returns the User-Agent string of the client.
- **File Handling**:
  - **GET**: Serves files from a specified directory.
  - **POST**: Allows uploading files to a specified directory.

## Requirements

- Python 3.x

## Usage

1. **Starting the Server**:

   ```bash
   ./server.py [directory]
   ```

   Replace `[directory]` with the path of the directory you want to serve files from. [OPTIONAL]

2. **Connecting to the Server**:
   - The server listens on `localhost` at port `4221`.

## Endpoints

- **Root (`/`)**:
  - **Request**: `GET /`
  - **Response**: `200 OK`
  
- **Echo (`/echo/{message}`)**:
  - **Request**: `GET /echo/hello`
  - **Response**: `hello`
  - Supports gzip encoding if the `Accept-Encoding: gzip` header is present.

- **User-Agent (`/user-agent`)**:
  - **Request**: `GET /user-agent`
  - **Response**: Returns the `User-Agent` string of the client.

- **Files (`/files/{filename}`)**:
  - **GET**:
    - **Request**: `GET /files/example.txt`
    - **Response**: Contents of `example.txt` if it exists in the specified directory.
  - **POST**:
    - **Request**: `POST /files/newfile.txt` with the file content in the request body.
    - **Response**: `201 Created` if the file is successfully uploaded.

## Error Handling

- Returns `404 Not Found` for any unrecognized paths or errors during request processing.

## Notes

- The server logs all requests and responses to the console.
- This implementation is for educational purposes and may lack features needed for production use, such as robust error handling, security, and scalability.

**Thanks to codecrafters.io**: If you're viewing this repo on GitHub, head over to [codecrafters.io](https://codecrafters.io) to try the challenge.
