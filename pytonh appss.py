import socket
import threading

# Connection Data
host = '127.0.0.1'
port = 55555

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Allows immediate restart
server.bind((host, port))
server.listen()

clients = []

def broadcast(message):
    """Sends a message to all connected clients."""
    for client in clients[:]: 
        try:
            client.send(message)
        except:
            if client in clients:
                clients.remove(client)

def handle(client):
    """Handles the communication with a single client."""
    while True:
        try:
            # Changed to utf-8 to allow emojis and special characters
            message = client.recv(1024)
            if not message:
                break
            
            print(f"Broadcasting: {message.decode('utf-8')}")
            broadcast(message)
        except:
            break
            
    if client in clients:
        clients.remove(client)
    client.close()

def receive():
    """Main loop to accept new connections."""
    print(f"--- SERVER ACTIVE ---")
    print(f"Listening on {host}:{port}...")
    print("Waiting for clients to connect...")
    
    try:
        while True:
            client, address = server.accept()
            print(f"New Connection from: {str(address)}")

            clients.append(client)

            # daemon=True ensures the thread closes when the server stops
            thread = threading.Thread(target=handle, args=(client,), daemon=True)
            thread.start()
    except KeyboardInterrupt:
        print("\nServer is shutting down...")
    finally:
        server.close()

if __name__ == "__main__":
    receive()