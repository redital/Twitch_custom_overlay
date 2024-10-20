from flask_socketio import SocketIO 

socketio = SocketIO()


users = {}

@socketio.on("connect")
def handle_connect():
    print("Connessione con il client stabilita")

def handle_incoming_request(data):
    print(data)
    socketio.emit("incoming-request", data)