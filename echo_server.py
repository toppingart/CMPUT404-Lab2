import socket
from threading import Thread

BYTES_TO_READ = 4096
HOST = "127.0.0.1"
PORT = 8080

# takes in a socket and address
def handle_connection(conn, address):
    # since conn is a socket (so will autoclose)
    with conn:
        print(f"Connected by: {address}")
        while True:
            data = conn.recv(BYTES_TO_READ)

            # if the socket connection is shut down by the other party
            if not data:
                break

            print(data)
            conn.send(data)
    


def start_server():
    # with blocks autoclean up resources like socket (auto closed after leaving with block)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST,PORT))

        # applying it to socket level
        # lets us reuse the socket address
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        s.listen()

        # socket between server and address, addr = client's address and port
        conn, addr = s.accept()
        handle_connection(conn, addr)

    

def start_threaded_server():

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # how many requests to queue up
        server_socket.listen(2)

        while True:
            conn, addr = server_socket.accept()
            thread = Thread(target = handle_connection, args = (conn, addr))
            thread.run()

start_server()
# start_threaded_server()