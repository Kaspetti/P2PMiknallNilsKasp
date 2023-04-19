from socket import socket, create_server
import _thread
import os

TRACKER_PORT = 13000


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def register_file(ip, filename):
    sock = socket()
    sock.connect(("localhost", TRACKER_PORT))
    send_command(sock, "REGISTER_FILE", ip)
    
    response = sock.recv(1024).decode()

    if response == "OK":
        sock.sendall(filename.encode())
    else:
        print("ERROR REGISTERING FILE IN TRACKER")
    
    sock.close()


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
    print(files)
    sock.close()
    input("Press any key to continue...")


def request_file(ip):
    sock = socket()
    sock.connect(("localhost", TRACKER_PORT))
    send_command(sock, "REQUEST_FILE", ip)

    response = sock.recv(1024).decode()
    
    if response == "OK":
        filename = input("Input file name: ")
        sock.sendall(filename.encode())
        peer = sock.recv(1024).decode()
        sock.close()

        if "ERROR" in peer:
            print("Failed with error: " + peer)
            return
        else:
            peer = peer.split(":")


        sock = socket()
        sock.connect((peer[0], int(peer[1])))
        sock.sendall(filename.encode())
        contents = sock.recv(1024).decode()

        if "ERROR" in contents:
            print("Failed with error: " + contents)
            return
        
        with open("files/" + filename, "w") as f:
            f.write(contents)

        register_file(ip, filename)1
        
        print("Donwload finished. Press any key to continue...")
        input()
    else:
        print("ERROR")


def peer_server(server):
    server.listen()

    while True:
        conn = server.accept()[0]
        filename = conn.recv(1024).decode()
        
        if filename not in os.listdir("files/"):
            conn.sendall("ERROR_NO_FILE".encode())
            continue

        with open("files/" + filename, "r") as f:
            content = f.read()
            conn.sendall(content.encode())


def main():
    port = input("Select port: ")

    server = create_server(("localhost", int(port)))
    ip = server.getsockname()[0] + ":" + str(server.getsockname()[1])
    _thread.start_new_thread(peer_server, (server, ))

    register_peer(ip)
    clear_screen()

    while True:
        print("Welcome to TextTorrent!")
        print("1) Unregister")
        print("2) Get all files")
        print("3) Request file")

        command = input()

        match command:
            case "1":
                unregister_peer(ip)
            case "2":
                get_all_files()
            case "3":
                request_file(ip)


if __name__ == "__main__":
    main()
