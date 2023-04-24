from socket import socket, create_server
import _thread
import os

TRACKER_PORT = 13000

COMMANDS = {
    "quit" : "Unregisters your files, and exits the program.",
    "get <filenames>" : "Gets specified file",
    "list" : "Lists all files that you do not have.",
    "help" : "Shows this menu"
}

file_store = ""


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def register_file(ip, filename):
    
    global TRACKER_PORT
    
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
    
    global TRACKER_PORT
    
    sock = socket()
    sock.connect(("localhost", TRACKER_PORT))
    send_command(sock, "REGISTER", ip)
    response = sock.recv(1024).decode()

    if response == "OK":
        files = os.listdir(file_store)

        sock.sendall("\n".join(files).encode())
    else:
        print("ERROR")
    sock.close()


def unregister_peer(ip):
    """Tells the tracker to unregister this peer, then exits.

    Args:
        ip: The server ip of this peer to be unregistered in the tracker.
    """
    
    global TRACKER_PORT

    sock = socket()
    sock.connect(("localhost", TRACKER_PORT))
    send_command(sock, "UNREGISTER", ip)
    sock.close()
    exit()


def get_all_files(ip):
    """Gets all files in the system."""

    global TRACKER_PORT

    sock = socket()
    sock.connect(("localhost", TRACKER_PORT))
    send_command(sock, "GET_FILES", ip)

    files = sock.recv(1024).decode()
    print(files)
    sock.close()

def request_file(ip, files: list[str]):
    
    global TRACKER_PORT
    pretty_files = ", ".join(files)
    
    file_count = 0
    
    print(f"Getting {pretty_files}")
    for filename in files:
    
        sock = socket()
        sock.connect(("localhost", TRACKER_PORT))
        send_command(sock, "REQUEST_FILE", ip)

        response = sock.recv(1024).decode()
        
        
        if response == "OK":
        
            sock.sendall(filename.encode())
            peer = sock.recv(1024).decode()
            sock.close()

            if "ERROR" in peer:
                print(f"Failed with error: {peer}, for file: {filename}")
                continue
            else:
                peer = peer.split(":")


            sock = socket()
            sock.connect((peer[0], int(peer[1])))
            sock.sendall(filename.encode())
            contents = sock.recv(1024).decode()

            if "ERROR" in contents:
                print(f"Failed with error: {contents}, for file: {filename}")
                continue
            print(f"Downloading file: {filename}")
            
            with open(f"{file_store}/{filename}", "w") as f:
                f.write(contents)

            register_file(ip, filename)
            file_count += 1
        else:
            print(f"ERROR GETTING FILE: {filename}")
        print(f"Download finished, for file: {filename}.")
        
    print(f"Downloaded ({file_count}/{len(files)} files.)")


def peer_server(server):
    server.listen()

    while True:
        conn = server.accept()[0]
        filename = conn.recv(1024).decode()
        
        if filename not in os.listdir(file_store):
            conn.sendall("ERROR_NO_FILE".encode())
            continue

        with open(f"{file_store}/{filename}", "r") as f:
            content = f.read()
            conn.sendall(content.encode())


def print_help(cmds: dict[str : str]) -> None:
    """Prints all the given commands

    Args:
        cmds (dict): Dictionary containing each command, and their corresponding explanation
    """
    for cmd, ex in cmds.items():
        print(f"{cmd} : {ex}")

def main():
    
    port = input("Select port: ")
    global file_store
    file_store = input("Select filestore: ")

    server = create_server(("localhost", int(port)))
    ip = server.getsockname()[0] + ":" + str(server.getsockname()[1])
    _thread.start_new_thread(peer_server, (server, ))

    register_peer(ip)
    clear_screen()

    print("Welcome to TextTorrent!")
    print("Type 'help' to get a list of all commands")
    while True:
        raw_cmd = input("> ")
        cmd = raw_cmd.split()
        match cmd:
            case ["quit"]:
                unregister_peer(ip)
                
            case ["list"]:
                get_all_files(ip)
            
            case "get", *files:
                request_file(ip, files)
                
            case ["help"]:
                print_help(COMMANDS)
                
            case _:
                print(f"Unknown command: '{raw_cmd}', type 'help', to get a list of all commands.")

if __name__ == "__main__":
    main()
