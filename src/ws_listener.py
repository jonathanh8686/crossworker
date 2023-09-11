import socketio
import traceback
import websocket
import time

# standard Python
# sio = socketio.Client()

# @sio.event
# def connect():
#     print("I'm connected!")

# @sio.event
# def message(data):
#     print('I received a message!')
#     print(data)

# sio.connect('wss://api.foracross.com/socket.io/?EIO=3&transport=websocket')

lobby_id = '3850420-phrint'

websocket.enableTrace(True)
ws = websocket.WebSocket()
ws.connect("wss://api.foracross.com/socket.io/?EIO=3&transport=websocket")
print(ws.recv())
print(ws.recv())
ws.send(f'420["join_game", "{lobby_id}"]')
print(ws.recv())
ws.send(f'421["sync_all_game_events","{lobby_id}"]')
print(ws.recv())

while True:
    print(ws.recv())
    ws.send('2')
    time.sleep(1.5)
    
