from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key_123'
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    # Serves the frontend HTML file
    return render_template('index.html')

# Event for when a message is sent from the client
@socketio.on('message')
def handle_message(data):
    print(f"Message received: {data}")
    # Broadcast the message to EVERYONE connected
    emit('announce_message', data, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5000)