import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox

class ChatClient:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            # Attempt to connect to the server
            self.client.connect(('127.0.0.1', 55555))
        except ConnectionRefusedError:
            # Rectify the error by showing a message and closing
            print("Error: Could not connect to the server. Make sure server.py is running!")
            # We use a dummy root for the messagebox if the main window isn't up
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("Connection Error", "The Server is not running. Start server.py first!")
            exit()

        self.win = tk.Tk()
        self.win.title("Python Desktop Chat")

        self.chat_label = tk.Label(self.win, text="Chat:")
        self.chat_label.pack(padx=20, pady=5)

        self.text_area = scrolledtext.ScrolledText(self.win)
        self.text_area.pack(padx=20, pady=5)
        self.text_area.config(state='disabled') # Make it read-only initially

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
                # Update text area (must enable then disable to edit)
                self.text_area.config(state='normal')
                self.text_area.insert('end', message + "\n")
                self.text_area.config(state='disabled')
                self.text_area.yview('end')
            except:
                self.client.close()
                break

if __name__ == "__main__":
    client = ChatClient()