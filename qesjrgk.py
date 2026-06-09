import socket
import threading

# RECTIFIED: Use '0.0.0.0' or '' to listen on all available interfaces
host = '0.0.0.0' 
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

try:
    server.bind((host, port))
except socket.gaierror:
    # Fallback if 0.0.0.0 also fails on certain restricted systems
    server.bind(('', port)) 

server.listen()

clients = []

def broadcast(message):
    for client in clients[:]: 
        try:
            client.send(message)
        except:
            if client in clients:
                clients.remove(client)

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            if not message:
                break
            print(f"Broadcasting: {message.decode('ascii')}")
            broadcast(message)
        except:
            break
            
    if client in clients:
        clients.remove(client)
    client.close()

def receive():
    # Use 127.0.0.1 for the print statement so you know where to connect
    print(f"Server is running... Connect your client to 127.0.0.1 port {port}")
    while True:
        try:
            client, address = server.accept()
            print(f"Connected with {str(address)}")
            clients.append(client)
            thread = threading.Thread(target=handle, args=(client,))
            thread.start()
        except:
            break

if __name__ == "__main__":
    receive()