from socket import socket, create_server
import threading
import random

TRACKER_PORT = 13000

files = ["test.txt", "tissemann.txt"]


def register_peer(ip):
    """Registers the peer in the tracker. Asks the tracker to register it.
    The tracker returns a response code. If this code is 'OK' then the peer sends 
    all their files to the tracker so the tracker can register them.

    Args:
        ip: The server ip of this peer to be registered in the tracker.
    """
    
    sock = socket()
    sock.connect(("localhost", TRACKER_PORT))
    sock.sendall("\n".join(["REGISTER", ip]).encode())
    response = sock.recv(1024).decode()

    if response == "OK":
        sock.sendall("\n".join(files).encode())
    else:
        print("ERROR")
    sock.close()


def unregister_peer(ip):
    """Tells the tracker to unregister this peer, then exits.

    Args:
        ip: The server ip of this peer to be unregistered in the tracker.
    """

    sock  = socket()
    sock.connect(("localhost", TRACKER_PORT))
    sock.sendall("\n".join(["UNREGISTER", ip]).encode())
    sock.close()
    exit()


def main():
    server = create_server(("localhost", random.randint(14000, 14010)))
    ip = server.getsockname()[0] + ":" + str(server.getsockname()[1])

    register_peer(ip)

    while True:
        print("Welcome to TextTorrent!")
        print("1) Unregister")
        command = input()

        match command:
            case "1":
                unregister_peer(ip)


if __name__ == "__main__":
    main()
