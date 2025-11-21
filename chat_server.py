import socket
import threading
from datetime import datetime

HOST = '127.0.0.1'
PORT = 12345


clients = {}
lock = threading.Lock()

def broadcast(message):
    """
    Sends a message to all connected clients.
    """
    for client in list(clients.values()):
        try:
            client.send(message.encode())
        except:
            pass


def handle_client(conn, addr):
    """
    Handles all communication for a connected client.
    - Receives nickname
    - Ensures nickname uniqueness
    - Processes public and private messages
    - Handles disconnection
    """
    nickname = None
    try:
        # Receive nickname
        nickname = conn.recv(1024).decode().strip()
        if not nickname:
            conn.close()
            return
        if '*' in nickname:
            nickname = nickname.replace('*', '')  # Remove '*' if coming from relay

        # Ensure unique nickname
        original = nickname
        count = 1
        while nickname in clients:
            nickname = f"{original}{count}"
            count += 1

        clients[nickname] = conn
        print(f"[+] {nickname} connected: {addr}")
        broadcast(f"*** {nickname} joined the chat ***")

        with open("chat_log.txt", "a") as log:
            log.write(f"{datetime.now()} - {nickname} joined\n")

        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    break
                message = data.decode().strip()

                if not message:
                    continue

                if message.lower() == "exit":
                    break


                if message.lower().startswith("/pm"):
                    parts = message.split(" ", 2)
                    if len(parts) < 3:
                        conn.send("Usage: /pm username message".encode())
                        continue
                    target, pm_msg = parts[1], parts[2]
                    timestamp = datetime.now().strftime("[%H:%M:%S]")
                    formatted = f"{timestamp} (PM) {nickname} → {target}: {pm_msg}"
                    if target in clients:
                        try:
                            clients[target].send(formatted.encode())
                        except:
                            pass
                        try:
                            conn.send(formatted.encode())
                        except:
                            pass
                        with open("chat_log.txt", "a") as log:
                            log.write(f"{datetime.now()} - {formatted}\n")
                    else:
                        conn.send(f"User '{target}' is offline.".encode())
                    continue


                if message.startswith("@") and ":" in message:
                    try:
                        target, content = message[1:].split(":", 1)
                        timestamp = datetime.now().strftime("[%H:%M:%S]")
                        formatted = f"{timestamp} (PM) {nickname} → {target.strip()}: {content.strip()}"
                        if target.strip() in clients:
                            clients[target.strip()].send(formatted.encode())
                            conn.send(formatted.encode())
                            with open("chat_log.txt", "a") as log:
                                log.write(f"{datetime.now()} - {formatted}\n")
                        else:
                            conn.send(f"User '{target.strip()}' is offline.".encode())
                        continue
                    except:
                        conn.send("Invalid private message format. Use @username: message".encode())
                        continue

                
                timestamp = datetime.now().strftime("[%H:%M:%S]")
                formatted = f"{timestamp} {nickname}: {message}"
                broadcast(formatted)
                with open("chat_log.txt", "a") as log:
                    log.write(f"{datetime.now()} - {formatted}\n")

            except:
                break

    finally:
        if nickname and nickname in clients:
            del clients[nickname]
            broadcast(f"*** {nickname} left the chat ***")
            print(f"[-] {nickname} disconnected")
        try:
            conn.close()
        except:
            pass


if __name__ == '__main__':
    """
    Starts the chat server and continuously accepts new clients.
    Each client is handled in a separate thread.
    """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[SERVER] Listening on: {HOST}:{PORT}")
    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()