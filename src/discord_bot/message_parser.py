import json

from loguru import logger
from message_types import (
    ChatModel,
    CheckModel,
    CreateEvent,
    GameEvent,
    ResetModel,
    RevealModel,
    SendChatMessageModel,
    UpdateCellModel,
    UpdateClockModel,
    UpdateColorModel,
    UpdateCursorModel,
    UpdateDispayNameModel,
)


def is_sync_message(msg: str) -> bool:
    return len(msg) >= 3 and msg[:3] == "431"


def is_game_event(msg: str) -> bool:
    return len(msg) >= 2 and msg[:2] == "42"


async def parse_sync_event(
    msg: str,
) -> tuple[CreateEvent, list[tuple[str, GameEvent]]]:
    msg = msg.strip("0123456789")
    msg_obj = json.loads(msg)[0]
    create_event = CreateEvent.model_validate(msg_obj[0])
    prior_events: list[tuple[str, GameEvent]] = []
    for event in msg_obj[1:]:
        res = await parse_game_event(f'["game_event", {json.dumps(event)}]')
        prior_events.append(res)

    return (create_event, prior_events)


async def parse_game_event(msg: str) -> tuple[str, GameEvent]:
    msg = msg.strip("0123456789")
    msg_obj = json.loads(msg)
    event_obj = msg_obj[1]

    parsed_obj: GameEvent
    match event_obj["type"]:
        case "updateCursor":
            parsed_obj = UpdateCursorModel.model_validate(event_obj)
        case "updateCell":
            parsed_obj = UpdateCellModel.model_validate(event_obj)
        case "updateDisplayName":
            parsed_obj = UpdateDispayNameModel.model_validate(event_obj)
        case "check":
            parsed_obj = CheckModel.model_validate(event_obj)
        case "reveal":
            parsed_obj = RevealModel.model_validate(event_obj)
        case "updateColor":
            parsed_obj = UpdateColorModel.model_validate(event_obj)
        case "chat":
            parsed_obj = ChatModel.model_validate(event_obj)
        case "sendChatMessage":
            parsed_obj = SendChatMessageModel.model_validate(event_obj)
        case "updateClock":
            parsed_obj = UpdateClockModel.model_validate(event_obj)
        case "reset":
            parsed_obj = ResetModel.model_validate(event_obj)
        case _:
            logger.error(f"Unidentified message recieved: {msg}")
            raise ValueError("Unknown message type recieved")

    return (event_obj["type"], parsed_obj)
