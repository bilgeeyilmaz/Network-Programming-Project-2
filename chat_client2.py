import socket
import threading
import tkinter as tk
from tkinter import simpledialog, scrolledtext, messagebox

class ChatClient:
    """
    A GUI-based chat client.
    Connects to the server, sends/receives messages, and supports private messaging.
    """

    SERVER_IP = '127.0.0.1'
    SERVER_PORT = 12345

    def __init__(self, master):
        """
        Creates main GUI components, sets up the user interface,
        and connects the client to the server.
        """
        self.master = master
        self.master.title('Python Chat Client')

        self.chat_area = scrolledtext.ScrolledText(master, wrap=tk.WORD, state='disabled', width=50, height=20)
        self.chat_area.pack(padx=10, pady=5)

        self.entry = tk.Entry(master, width=40)
        self.entry.pack(side=tk.LEFT, padx=(10,0), pady=(0,10))
        self.entry.bind('<Return>', self.send_message)

        self.send_button = tk.Button(master, text='Send', command=self.send_message)
        self.send_button.pack(side=tk.LEFT, padx=5, pady=(0,10))

        self.pm_button = tk.Button(master, text='Private Message', command=self.open_private_message_window)
        self.pm_button.pack(side=tk.LEFT, padx=5, pady=(0,10))

        self.master.protocol('WM_DELETE_WINDOW', self.on_closing)
        self.sock = None
        self.nickname = ''
        self.connect()

    def connect(self):
        """
        Asks the user for a nickname, connects to the server,
        and starts a thread to listen for incoming messages.
        """
        self.nickname = simpledialog.askstring('Nickname', 'Please enter a username:', parent=self.master)
        if not self.nickname:
            self.master.quit()
            return
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.SERVER_IP, self.SERVER_PORT))
            self.sock.send(self.nickname.encode())
        except Exception as e:
            messagebox.showerror('Connection Error', f'Failed to connect to the server:\n{e}')
            self.master.quit()
            return
        threading.Thread(target=self.receive_messages, daemon=True).start()

    def receive_messages(self):
        """
        Continuously listens for incoming messages from the server
        and displays them on the screen.
        Ends the loop if the connection is closed.
        """
        while True:
            try:
                msg = self.sock.recv(1024).decode()
                if not msg:
                    break
                self.append_message(msg)
            except:
                break

    def send_message(self, event=None):
        """
        Sends the message written by the user to the server.
        """
        msg = self.entry.get().strip()
        if not msg:
            return
        try:
            self.sock.send(msg.encode())
        except:
            pass
        self.entry.delete(0, tk.END)

    def append_message(self, msg):
        """
        Adds the received message to the chat area and scrolls automatically.
        """
        self.chat_area.config(state='normal')
        self.chat_area.insert(tk.END, msg + '\n')
        self.chat_area.yview(tk.END)
        self.chat_area.config(state='disabled')

    def open_private_message_window(self):
        """
        Asks the user for a target username and opens a new window
        to send a private message.
        Sends the message to the server in the format /pm <to> <message>.
        """
        target = simpledialog.askstring("Private Message", "Who do you want to send a message to?", parent=self.master)
        if not target:
            return

        pm_win = tk.Toplevel(self.master)
        pm_win.title(f"PM: {target}")

        text_area = scrolledtext.ScrolledText(pm_win, width=50, height=10, state='normal')
        text_area.pack(padx=5, pady=5)

        entry = tk.Entry(pm_win, width=40)
        entry.pack(side=tk.LEFT, padx=(10,0), pady=(0,10))

        def send_pm():
            """
            Creates the command to send a private message to the target user
            and displays it in the private message window.
            """
            msg = entry.get().strip()
            if msg:
                pm_command = f"/pm {target} {msg}"
                try:
                    self.sock.send(pm_command.encode())
                    text_area.insert(tk.END, f"YOU → {target}: {msg}\n")
                except:
                    text_area.insert(tk.END, "(Failed to send)\n")
                entry.delete(0, tk.END)

        send_btn = tk.Button(pm_win, text="Send", command=send_pm)
        send_btn.pack(side=tk.LEFT, padx=5, pady=(0,10))

    def on_closing(self):
        """
        Sends 'exit' to the server and closes the connection
        when the window is closed.
        """
        try:
            self.sock.send('exit'.encode())
            self.sock.close()
        except:
            pass
        self.master.quit()

if __name__ == '__main__':
    root = tk.Tk()
    ChatClient(root)
    root.mainloop()