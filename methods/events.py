from flask_socketio import SocketIO 

socketio = SocketIO()


users = {}

@socketio.on("connect")
def handle_connect():
    print("Connessione con il client stabilita")

def handle_incoming_request(data):
    print(data)
    socketio.emit("incoming-request", data)

def handle_new_goal(data):
    print(data)
    socketio.emit("update-goal", data)
    
def handle_points_update(data):
    print(data)
    socketio.emit("increment-total-cost", data)