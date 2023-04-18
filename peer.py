from socket import socket, create_server
import threading
import os

TRACKER_PORT = 13000


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def send_command(sock, command, ip=""):
    """Sends a command to the track. Sends a message with the command and the server ip
    of the peer.

    Args:
        sock: The connection to send from.
        command: The command to send
        ip (optional): The server ip of the peer. Defaults to "".
    """
    sock.sendall("\n".join([command, ip]).encode())


def register_peer(ip):
    """Registers the peer in the tracker. Asks the tracker to register it.
    The tracker returns a response code. If this code is 'OK' then the peer sends 
    all their files to the tracker so the tracker can register them.

    Args:
        ip: The server ip of this peer to be registered in the tracker.
    """
    
    sock = socket()
    sock.connect(("localhost", TRACKER_PORT))
    send_command(sock, "REGISTER", ip)
    response = sock.recv(1024).decode()

    if response == "OK":
        files = os.listdir("files/")

        sock.sendall("\n".join(files).encode())
    else:
        print("ERROR")
    sock.close()


def unregister_peer(ip):
    """Tells the tracker to unregister this peer, then exits.

    Args:
        ip: The server ip of this peer to be unregistered in the tracker.
    """

    sock = socket()
    sock.connect(("localhost", TRACKER_PORT))
    send_command(sock, "UNREGISTER", ip)
    sock.close()
    exit()


def get_all_files():
    """Gets all files in the system."""

    sock = socket()
    sock.connect(("localhost", TRACKER_PORT))
    send_command(sock, "GET_FILES")

    files = sock.recv(1024).decode()
    clear_screen()
    print(files)
    sock.close()
    input("Press any key to continue...")


def main():
    port = input("Select port: ")

    server = create_server(("localhost", int(port)))
    ip = server.getsockname()[0] + ":" + str(server.getsockname()[1])

    register_peer(ip)

    while True:
        clear_screen()
        print("Welcome to TextTorrent!")
        print("1) Unregister")
        print("2) Get all files")

        command = input()

        match command:
            case "1":
                unregister_peer(ip)
            case "2":
                get_all_files()


if __name__ == "__main__":
    main()
