import socket
import threading
import json
import time

# Settings
PORT = 50005
BROADCAST_ADDR = '<broadcast>'

def listen(my_role):
    """Listens for incoming broadcasts and formats them based on type."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.bind(('', PORT))
    
    while True:
        data, addr = sock.recvfrom(4096)
        try:
            # Decode the JSON data
            packet = json.loads(data.decode('utf-8'))
            msg_type = packet.get("type")
            user = packet.get("user")
            content = packet.get("content")

            # Formatting based on message type
            if msg_type == "QUESTION":
                print(f"\n\n{'='*40}")
                print(f"❓ QUESTION FROM {user.upper()}:")
                print(f"👉 {content}")
                print(f"{'='*40}")
            
            elif msg_type == "ANSWER":
                print(f"\n[ANSWER] {user}: {content}")

            # Re-print the input prompt line
            print(f"Your {my_role} Message: ", end="", flush=True)
            
        except Exception as e:
            pass # Ignore corrupted packets

def send(role):
    """Handles sending based on whether user is Host or Client."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    
    name = input("Enter your username: ")
    print(f"\n--- {role} MODE ACTIVE ---")
    
    while True:
        if role == "HOST":
            prompt = "Enter Question to broadcast: "
            msg_type = "QUESTION"
        else:
            prompt = "Enter your Answer: "
            msg_type = "ANSWER"

        msg_content = input(prompt)
        
        if msg_content.strip():
            # Create a JSON packet
            packet = {
                "type": msg_type,
                "user": name,
                "content": msg_content,
                "timestamp": time.time()
            }
            
            # Broadcast the JSON
            sock.sendto(json.dumps(packet).encode('utf-8'), (BROADCAST_ADDR, PORT))

if __name__ == "__main__":
    print("--- ADVANCED LAN Q&A CHAT ---")
    
    # 1. Choose Role
    role_choice = input("Are you the (H)ost or (C)lient? ").lower()
    if role_choice.startswith('h'):
        my_role = "HOST"
    else:
        my_role = "CLIENT"

    # 2. Start Listening (Background)
    listener_thread = threading.Thread(target=listen, args=(my_role,), daemon=True)
    listener_thread.start()

    # 3. Start Sending (Foreground)
    send(my_role)