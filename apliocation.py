import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

class ChatClient:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(('127.0.0.1', 55555))

        self.win = tk.Tk()
        self.win.title("Python Desktop Chat")

        self.chat_label = tk.Label(self.win, text="Chat:")
        self.chat_label.pack(padx=20, pady=5)

        self.text_area = scrolledtext.ScrolledText(self.win)
        self.text_area.pack(padx=20, pady=5)

        self.msg_label = tk.Label(self.win, text="Message:")
        self.msg_label.pack(padx=20, pady=5)

        self.input_area = tk.Entry(self.win)
        self.input_area.pack(padx=20, pady=5)

        self.send_button = tk.Button(self.win, text="Send", command=self.write)
        self.send_button.pack(padx=20, pady=5)

        thread = threading.Thread(target=self.receive)
        thread.start()
        self.win.mainloop()

    def write(self):
        message = f"User: {self.input_area.get()}"
        self.client.send(message.encode('ascii'))
        self.input_area.delete(0, 'end')

    def receive(self):
        while True:
            try:
                message = self.client.recv(1024).decode('ascii')
                self.text_area.insert('end', message + "\n")
            except:
                self.client.close()
                break

client = ChatClient()