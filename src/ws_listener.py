import socketio

# standard Python
sio = socketio.Client()

@sio.event
def connect():
    print("I'm connected!")

@sio.event
def message(data):
    print('I received a message!')
    print(data)

sio.connect('wss://api.foracross.com/socket.io/?EIO=3&transport=websocket')
