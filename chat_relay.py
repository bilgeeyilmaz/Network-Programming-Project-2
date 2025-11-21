import socket
import threading


def handle_relay(client_conn, main_server_ip, main_server_port):
    """
    Handles a single relay client's connection.
    Creates a corresponding connection to the main server,
    rewrites nickname by adding '*' prefix if necessary,
    and forwards all traffic between client and server.
    """
    try:
        server_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_conn.connect((main_server_ip, main_server_port))

        # First data is nickname - if it doesn't start with '*', it means it is coming through the relay
        nickname = client_conn.recv(1024).decode()
        if not nickname.startswith("*"):
            nickname = "*" + nickname
        server_conn.send(nickname.encode())

        def forward(src, dest):
            """
            Forwards all data from 'src' socket to 'dest' socket.
            Stops and closes both sockets when connection breaks.
            """
            while True:
                try:
                    data = src.recv(1024)
                    if not data:
                        break
                    dest.sendall(data)
                except:
                    break
            try:
                src.close()
            except:
                pass
            try:
                dest.close()
            except:
                pass

        threading.Thread(target=forward, args=(client_conn, server_conn), daemon=True).start()
        forward(server_conn, client_conn)

    except Exception as e:
        print("[RELAY ERROR]", e)
        try:
            client_conn.close()
        except:
            pass


def start_relay():
    """
    Starts the relay server.
    Listens for incoming client connections and forwards them
    to the main chat server by spawning handler threads.
    """
    host = '127.0.0.1'
    port = 23456
    main_server_ip = '127.0.0.1'
    main_server_port = 12345

    relay_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    relay_socket.bind((host, port))
    relay_socket.listen()

    print(f"[RELAY] {host}:{port} is running, main server: {main_server_ip}:{main_server_port}")

    while True:
        client_conn, addr = relay_socket.accept()
        print(f"[RELAY] New connection: {addr}")
        threading.Thread(target=handle_relay, args=(client_conn, main_server_ip, main_server_port), daemon=True).start()


if __name__ == '__main__':
    start_relay()