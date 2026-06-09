import socket
import threading

# Settings
PORT = 50000
# Broadcast address tells the message to go to every computer on the network
BROADCAST_ADDR = '<broadcast>'

def listen():
    """Listens for incoming messages from anyone on the network."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.bind(('', PORT))
    
    while True:
        data, addr = sock.recvfrom(1024)
        print(f"\r{data.decode('utf-8')}\nYour message: ", end="")

def send():
    """Sends your message to everyone on the network."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    
    name = input("Enter your username: ")
    while True:
        msg = input("Your message: ")
        full_msg = f"{name}: {msg}"
        sock.sendto(full_msg.encode('utf-8'), (BROADCAST_ADDR, PORT))

if __name__ == "__main__":
    print("--- LAN DISCOVERY CHAT ---")
    # Start listening in the background
    threading.Thread(target=listen, daemon=True).start()
    # Start sending in the foreground
    send()