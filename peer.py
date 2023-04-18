from socket import socket
import threading

TRACKER_PORT = 13000

files = ["test.txt", "tissemann.txt"]


def register_peer():
    sock = socket()
    sock.connect(("localhost", TRACKER_PORT))
    sock.sendall("REGISTER".encode())
    response = sock.recv(1024).decode()

    if response == "OK":
        sock.sendall("\n".join(files).encode())
    else:
        print("ERROR")
    sock.close()


def unregister_peer():
    sock  = socket()
    sock.connet(("localhost", TRACKER_PORT))



if __name__ == "__main__":
    register_peer()
