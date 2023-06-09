from socket import create_server
import os


TRACKER_PORT = 13000

# filename : List[ip]
files = {

}
"""Dict: Filename : [IP]"""


def register_single_file(conn, ip):
    filename = conn.recv(1024).decode()

    if filename in files.keys():
        if ip in files[filename]:
            return

        files[filename].append(ip)
    else:
        files[filename] = [ip]

    print(filename)


def send_peer_for_file(conn, ip):
    """Sends the ip of the first peer which is not the requesting peer
    which have the file requested.

    Args:
        conn: the connection of the asking peer
        ip: the ip of the asking peers server
    """

    filename = conn.recv(1024).decode()

    if filename not in files.keys():
        conn.sendall("ERROR_NO_FILE".encode())
        return

    if ip in files[filename]:
        conn.sendall("ERROR_EXISTING_FILE".encode())
        return

    peers = files[filename]
    for p in peers:
        conn.sendall(p.encode())
        return
    
    conn.sendall("ERROR_NO_PEER".encode())

    

def send_file_list(conn, ip):
    response = "\n".join([k for k, v in files.items() if ip not in v])

    if not response:
        response = "No new files found"

    conn.sendall(response.encode())


def register_peer(conn, ip):
    """Registers a peer after connection. Receives the all the files from the
    peer and adds their files to the files dictionary with their ip.

    Args:
        conn: the peer connection used for receiving the files
        ip: the ip of the server connected to the peer. This is not the ip
        of the connection but rather the ip that should be used when other peers
        fetch the files from them. 
    """

    received_files = conn.recv(1024).decode().split('\n')

    for file in received_files:
        if not file:
            continue

        if file in files.keys():
            files[file].append(ip)
        else:
            files[file] = [ip]


def unregister_peer(ip):
    """Unregisters a peer when requested. Removes the ip provided from the files in the 
    files dictionary.

    Args:
        ip: The ip to be removed from the files dictionary
    """

    empty_files = []

    for filename in files:
        if ip not in files[filename]:
            continue

        files[filename].remove(ip)

        if len(files[filename]) == 0:
            empty_files.append(filename)

    # Remove files without ips
    for file in empty_files:
        del files[file]


def prettyPrint(files: dict[str : list[str]]) -> None:
    """Prints the tracked files, in an orderly fashon

    Args:
        files: Dict of the tracked files
    """
    sep = ", "
    for filename, ip in files.items():
        print(f"File: {filename}, From: {sep.join(ip)}")
    
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    clear_screen()
    print("Tracker")
    sock = create_server(("localhost", TRACKER_PORT))
    sock.listen()
    while True:
        conn = sock.accept()[0]
        response = conn.recv(1024).decode().split("\n")
        command = response[0]
        ip = response[1]

        match command:
            case "REGISTER":
                conn.sendall("OK".encode())
                register_peer(conn, ip)
            case "UNREGISTER":
                unregister_peer(ip)
            case "GET_FILES":
                send_file_list(conn, ip)
            case "REQUEST_FILE":
                conn.sendall("OK".encode())
                send_peer_for_file(conn, ip)
            case "REGISTER_FILE":
                conn.sendall("OK".encode())
                register_single_file(conn, ip)

        clear_screen()
        prettyPrint(files)


if __name__ == "__main__":
    main()
    