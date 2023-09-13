import json

def is_game_event(msg: str) -> bool:
    return len(msg) >= 2 and msg[:2] == "42"

async def game_event_to_json(msg: str) -> dict:
    split = msg.split(',', 1)
    json_str = split[1].rstrip(']')

    dic = json.loads(json_str)

    formatted_json = dic['params']

    formatted_json['type'] = dic['type']
    formatted_json['timestamp'] = dic['timestamp']

    return formatted_json

