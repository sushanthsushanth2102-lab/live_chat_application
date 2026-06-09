import socket
import threading
import json
import time

# Settings
PORT = 50005
BROADCAST_ADDR = '<broadcast>'

# --- THE BOT'S MEMORY ---
# You can add any questions and answers here.
# Make sure the questions are in lowercase.
KNOWLEDGE_BASE = {
    "what is python?": "Python is a high-level, interpreted programming language.",
    "who created python?": "Guido van Rossum.",
    "what is 2+2?": "The answer is 4.",
    "hello": "Hi! I am the Auto-Bot. Ask me a question!",
    "how are you?": "I am a script, so I am running perfectly!",
}

def auto_respond(question_content):
    """Checks the knowledge base and returns an answer if found."""
    # Convert question to lowercase and remove the '?' for better matching
    clean_q = question_content.lower().replace("?", "").strip()
    return KNOWLEDGE_BASE.get(clean_q)

def listen(my_role, my_username):
    """Listens for broadcasts and auto-responds to known questions."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.bind(('', PORT))
    
    # We need a separate socket just for the auto-reply
    send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    send_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    while True:
        data, addr = sock.recvfrom(4096)
        try:
            packet = json.loads(data.decode('utf-8'))
            msg_type = packet.get("type")
            user = packet.get("user")
            content = packet.get("content")

            # Ignore our own broadcasted messages
            if user == my_username:
                continue

            if msg_type == "QUESTION":
                print(f"\n\n❓ QUESTION FROM {user.upper()}: {content}")
                
                # --- AUTO-ANSWER LOGIC ---
                answer = auto_respond(content)
                if answer:
                    time.sleep(1) # Small delay to make it look like it's thinking
                    print(f"🤖 [Bot] I know this! Sending answer...")
                    
                    reply_packet = {
                        "type": "ANSWER",
                        "user": f"Bot-{my_username}",
                        "content": f"AUTO-REPLY: {answer}"
                    }
                    send_sock.sendto(json.dumps(reply_packet).encode('utf-8'), (BROADCAST_ADDR, PORT))
            
            elif msg_type == "ANSWER":
                print(f"\n[ANSWER] {user}: {content}")

            print(f"\nYour {my_role} Message: ", end="", flush=True)
            
        except Exception:
            pass

def send(role, name):
    """Handles manual sending from the user."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    
    print(f"\n--- {role} MODE ACTIVE ---")
    while True:
        prompt = "Enter Question: " if role == "HOST" else "Enter Answer: "
        msg_content = input(prompt)
        
        if msg_content.strip():
            packet = {
                "type": "QUESTION" if role == "HOST" else "ANSWER",
                "user": name,
                "content": msg_content
            }
            sock.sendto(json.dumps(packet).encode('utf-8'), (BROADCAST_ADDR, PORT))

if __name__ == "__main__":
    print("--- AUTO-ANSWERING LAN CHAT ---")
    
    username = input("Enter your username: ")
    role_choice = input("Are you the (H)ost or (C)lient? ").lower()
    my_role = "HOST" if role_choice.startswith('h') else "CLIENT"

    # Start listening and Auto-Responding in background
    threading.Thread(target=listen, args=(my_role, username), daemon=True).start()

    # Start manual sending
    send(my_role, username)