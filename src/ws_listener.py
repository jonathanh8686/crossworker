import websocket
import time
    
class WebsocketClient():
    def __init__(self):
        self.websocket_url = 'wss://api.foracross.com/socket.io/?EIO=3&transport=websocket'
    def join_game(self, game_id):
        self.ws = websocket.WebSocket()

        self.ws.connect(self.websocket_url)
        print(self.ws.recv())
        print(self.ws.recv())
        self.ws.send(f'420["join_game", "{game_id}"]')
        print(self.ws.recv())
        self.ws.send(f'421["sync_all_game_events","{game_id}"]')
        print(self.ws.recv())

        print('Joined game')

    def listen_game(self, game_id):
        last_ping = time.time()
        while True:
            if time.time() - last_ping > 1.5:
                print("I'm sending a msg")
                self.ws.send('2')
                last_ping = time.time()
            try:
                print(self.ws.recv())
            except:
                continue