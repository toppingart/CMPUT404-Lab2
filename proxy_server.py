import socket
from threading import Thread

BYTES_TO_READ = 4096
PROXY_SERVER_HOST = "127.0.0.1"
PROXY_SERVER_PORT = 8080

# dealing with only one socket in a function
def send_request(host, port, request_data):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:

        # sending data to google
        client_socket.connect((host, port))
        client_socket.send(request_data)
        client_socket.shutdown(socket.SHUT_WR)

        data = client_socket.recv(BYTES_TO_READ)
        result = b'' + data
        while (len(data) > 0):
            data = client_socket.recv(BYTES_TO_READ)
            result += data

        return result

def handle_connection(conn, addr):

    # makes sure socket is closed up
    with conn:
        print(f"Connected by: {addr}")

        request = b''
        while True:

            # reading request from client
            data = conn.recv(BYTES_TO_READ)
            if not data:
                break
            print(data)
            request += data
        
        # response from google
        response = send_request("www.google.com", 80, request)

        # send it back to the client
        conn.sendall(response)

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((PROXY_SERVER_HOST, PROXY_SERVER_PORT))
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # how many requests to queue up
        server_socket.listen(2)

        conn, addr = server_socket.accept()
        handle_connection(conn, addr)

def start_threaded_server():

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((PROXY_SERVER_HOST, PROXY_SERVER_PORT))
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # how many requests to queue up
        server_socket.listen(2)

        while True:
            conn, addr = server_socket.accept()
            thread = Thread(target = handle_connection, args = (conn, addr))
            thread.run()





# start_server()
start_threaded_server()