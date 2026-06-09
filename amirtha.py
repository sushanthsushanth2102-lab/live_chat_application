import socket
import threading

def receive_messages(sock):
    while True:
        try:
            data = sock.recv(1024).decode()
            if data: print(f"\nPartner: {data}")
        except: break

choice = input("Do you want to (H)ost or (C)onnect? ").lower()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

if choice == 'h':
    s.bind(('0.0.0.0', 9999))
    s.listen(1)
    print("Waiting for partner...")
    conn, addr = s.accept()
    print(f"Connected to {addr}")
else:
    ip = input("Enter partner's IP: ")
    s.connect((ip, 9999))
    conn = s

# Start thread to listen
threading.Thread(target=receive_messages, args=(conn,), daemon=True).start()

while True:
    msg = input("You: ")
    conn.send(msg.encode())


    