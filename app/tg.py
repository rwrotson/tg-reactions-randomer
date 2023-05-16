import asyncio
from datetime import datetime as dt
from functools import cache
from random import randint, sample
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import (
    GetAvailableReactionsRequest, SetChatAvailableReactionsRequest
)
from telethon.tl.types import (
    PeerChat, PeerChannel, InputPeerChat, InputPeerChannel,
    ReactionEmoji, ChatReactionsSome
)

from telethon.errors.rpcerrorlist import (
    PeerIdInvalidError, ChatIdInvalidError, ChatAdminRequiredError
)
from telethon.utils import resolve_id

from app.params import Params
from app.modes import ChatOrChannelMode as Mode
from app.logger import get_logger


logger = get_logger('tg')


async def update_all_chats_and_channels(params: Params) -> None:
    logger.info(f'UPDATING STARTED WITH: {params}')

    name = 'random_reactions'
    async with TelegramClient(name, params.api_id, params.api_hash) as client:
        reactions = await get_all_reactions(client)
        funcs_to_gather = []

        for chat_id in params.chat_ids:
            chosen_reacts = sample(reactions, randint(params.min, params.max))
            funcs_to_gather.append(
                set_reactions_to_entity(
                    client, chat_id, Mode.CHAT, chosen_reacts)
            )

        for channel_id in params.channel_ids:
            chosen_reacts = sample(reactions, randint(params.min, params.max))
            funcs_to_gather.append(
                set_reactions_to_entity(
                    client, channel_id, Mode.CHANNEL, chosen_reacts)
            )

        await asyncio.gather(*funcs_to_gather)


@cache
async def get_all_reactions(client: TelegramClient) -> list[ReactionEmoji]:
    all_reactions_obj = await client(GetAvailableReactionsRequest(hash=0))
    return [ReactionEmoji(item['reaction'])
            for item
            in all_reactions_obj.to_dict()['reactions']
            if item['title'] != 'Face with Tears of Joy']


async def set_reactions_to_entity(client: TelegramClient, id_: int, mode: Mode,
                                  reactions: list[ReactionEmoji]) -> None:
    try:
        entity = await get_entity(client, id_, mode)
        await client(SetChatAvailableReactionsRequest(
            peer=entity,
            available_reactions=ChatReactionsSome(reactions)
        ))
    except (PeerIdInvalidError, ChatIdInvalidError, ValueError):
        logger.error(f'{mode.upper()} {id_} WAS NOT FOUND')
    except ChatAdminRequiredError:
        logger.error(f'YOU HAVE NO ADMIN PRIVILEGES FOR {mode.upper()} {id_}')
    else:
        logger.info(
            f'{mode.upper()} {id_} SUCCESSFULLY UPDATED AT {dt.now()}\n'
            f'{len(reactions)} NEW REACTIONS ADDED'
        )


async def get_entity(client: TelegramClient,
                     id_: int, mode: Mode) -> InputPeerChat | InputPeerChannel:
    if mode is mode.CHAT:
        return await get_chat(client, id_)
    elif mode is mode.CHANNEL:
        return await get_channel(client, id_)


async def get_chat(client: TelegramClient, id_: int) -> InputPeerChat:
    real_id, _ = resolve_id(id_)
    return await client.get_input_entity(PeerChat(real_id))


async def get_channel(client: TelegramClient, id_: int) -> InputPeerChannel:
    real_id, _ = resolve_id(id_ if id_ < 0 else -id_)
    return await client.get_input_entity(PeerChannel(real_id))
