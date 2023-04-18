from socket import create_server

TRACKER_PORT = 13000

# filename : List[ip]
files = {

}


def send_peer_for_file(conn, ip):
    """Sends the ip of the first peer which is not the requesting peer
    which have the file requested.

    Args:
        conn (_type_): _description_
        ip (_type_): _description_
    """

    filename = conn.recv(1024).decode()
    peers = files[filename]
    for p in peers:
        if p != ip:
            conn.sendall(p.encode())
            break


def send_file_list(conn):
    conn.sendall("\n".join(files.keys()).encode())


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
        files[filename].remove(ip)

        if len(files[filename]) == 0:
            empty_files.append(filename)

    # Remove files without ips
    for file in empty_files:
        del files[file]


def main():
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
                send_file_list(conn)
            case "REQUEST_FILE":
                conn.sendall("OK".encode())
                send_peer_for_file(conn, ip)

        print(files)


if __name__ == "__main__":
    main()
    