from socket import create_server
import threading

TRACKER_PORT = 13000

# filename : List[ip]
files = {

}


def receive_file():
    pass


def send_file():
    pass


def send_file_list():
    pass


def register_peer(conn):
    received_files = conn.recv(1024).decode().split('\n')

    for file in received_files:
        if file in files.keys():
            files[file].append(conn.getpeername())
        else:
            files[file] = [conn.getpeername()]

    print(files)

def unregister_peer(ip):
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
        command = conn.recv(1024).decode()

        match command:
            case "REGISTER":
                conn.sendall("OK".encode())
                register_peer(conn)

if __name__ == "__main__":
    main()
    