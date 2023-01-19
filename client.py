import socket

BYTES_TO_READ = 4096

def get(host, port):
    # created our request
    # host will be a string (use utf-8 encoding)
    request_data = b"GET / HTTP/1.1\nHost:" + host.encode('utf-8') + b'\n\n'

    # created our socket
    # internet socket, client socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect to host and port
    s.connect((host,port))

    # sending the bytes in our request data
    s.send(request_data)

    # shutting down the "write" part of socket (done writing things to socket)
    # server can now do whatever they want to do with request
    s.shutdown(socket.SHUT_WR)

    # listen for response from the server
    response = s.recv(BYTES_TO_READ)

    while (len(response) > 0):
        print(response)
        response = s.recv(BYTES_TO_READ)

    s.close()

get("www.google.com", 80)