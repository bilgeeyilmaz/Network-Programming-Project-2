# Multi-User Chat System

This project is a multi-user chat application developed using **Python Socket** and **Threading** modules. The system consists of a central server, a relay server that directs traffic, and clients featuring a **Tkinter**-based Graphical User Interface (GUI).

---

##  Features

- **Graphical User Interface (GUI):** A user-friendly chat window built with the `tkinter` library.
- **TCP Socket Connection:** Reliable message transmission ensuring no data loss.
- **Multi-Threading:** Concurrent message sending and receiving without freezing the user interface.
- **Private Messaging:** Support for private messaging between users (via the `/pm` command).
- **Relay Server:** Allows clients to connect to the main server through an "intermediary layer" (Proxy logic).
- **Logging:** The server saves the entire chat history and connection logs to a `chat_log.txt` file.
- **Auto-Naming:** The server automatically revises the username if a duplicate login occurs (e.g., `Alice` -> `Alice1`).

---

##  Architecture

The system consists of 3 main components:

1.  **Main Server (`server.py`):** The brain of the chat. It manages clients, broadcasts messages, and handles logging.
2.  **Relay Server (`relay.py`):** Acts as a bridge between the Client and the Main Server. It forwards incoming data directly to the main server.
3.  **Client (`client.py`):** The interface used by the user to chat.

```text
[ Client A ] ----> [ Main Server (12345) ] <---- [ Client B ]
                            ^
                            |
                      [ Relay (23456) ]
                            ^
                            |
                      [ Client C ]
```

## Installation & Usage
To run the project, you only need Python 3 installed on your computer. No external library installation is required.

Run the files in the terminal or command prompt (CMD) in the following order:

- Start the Main Server
        
        python server.py
        The server starts listening on 127.0.0.1:12345.

- Start the Relay Server
        
        python relay.py
        The relay listens on 127.0.0.1:23456 and forwards traffic to the main server.

- Start the Clients

You can start multiple clients by opening multiple terminal windows.
        
        python client.py

Connection Settings: You can choose the connection point by changing the SERVER_PORT variable in the client.py file:

12345: Connects directly to the Main Server.

23456: Connects via the Relay Server.

## Commands
You can use the following formats in the chat window:

Action	Command Format	Example
General Message	(Type directly)	Hello everyone!
- Private Message 1	/pm <name> <message>	/pm John How are you?
- Private Message 2	@<name>: <message>	@John: Is the project done?

## File Descriptions
- chat_server.py: Accepts connections (accept), broadcasts messages to all users, filters private messages, and handles logging.

- chat_client.py: Requests a nickname from the user, creates the GUI, and displays messages received from the server. Uses scrolledtext and simpledialog modules.

- chat_relay.py: Handles socket forwarding (port forwarding) logic.

## Screenshots

<img width="682" height="414" alt="Ekran Resmi 2025-11-21 14 48 18" src="https://github.com/user-attachments/assets/e5504bbe-eb67-430e-9e55-aac34a370b9f" />

<img width="603" height="340" alt="Ekran Resmi 2025-11-21 14 49 10" src="https://github.com/user-attachments/assets/c1f08888-cfbd-4167-b1ea-8b862a4a8fbe" />

