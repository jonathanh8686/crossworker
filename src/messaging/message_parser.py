import json 
from messages import * 
from loguru import logger

def is_game_event(msg: str) -> bool:
    return len(msg) >= 2 and msg[:2] == "42"

async def game_event_to_message_obj(msg: str) -> dict:
    split = msg.split(',', 1)
    json_str = split[1].rstrip(']')

    dic = json.loads(json_str)
    params = dic['params']

    msg_obj = None

    match dic['type']:
        case "updateCursor":
            msg_obj = UpdateCursorMessage(
                timestamp = dic['timestamp'],
                id = params['id'],
                cell = Cell.parse_obj(params['cell']),
            )
        case "updateCell":
            msg_obj = UpdateCellMessage(
                timestamp = dic['timestamp'],
                id = params['id'],
                cell = Cell.parse_obj(params['cell']),
                value = params['value'],
                pencil = params['pencil']
            )
        case "updateDisplayName":
            msg_obj = UpdateDisplayNameMessage(
                timestamp = dic['timestamp'],

                id = params['id'],
                displayName = params['displayName']
            )
        case "check":
            msg_obj = CheckMessage(
                timestamp = dic['timestamp'],
                id = params['id'],
                cells = params['scope']
            )        
        case "reveal":
            msg_obj = RevealMessage(
                timestamp = dic['timestamp'],
                id = params['id'],
                cells = params['scope']
            )       
        case "reset":
            msg_obj = ResetMessage(
                timestamp = dic['timestamp'],
                id = params['id'],
                cells = params['scope']
            )      
        case "updateClock":
            msg_obj = UpdateClockMessage(
                timestamp = dic['timestamp'],
                id = params['id'],
                action = params['action']
            )       
        case _:
            logger.info("Unidentified message recieved")
            return None
        
    return msg_obj

