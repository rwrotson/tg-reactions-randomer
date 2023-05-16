import os
from dotenv import load_dotenv


def parse_params_from_env(path: str | None) -> dict:
    load_dotenv(path)
    return {
        'api_id': parse_int_from_env_file_by_key('API_ID'),
        'api_hash': parse_str_from_env_file_by_key('API_HASH'),
        'chat_ids': parse_list_of_ints_from_env_file_by_key('CHAT_IDS'),
        'channel_ids': parse_list_of_ints_from_env_file_by_key('CHANNEL_IDS')
    }


def parse_int_from_env_file_by_key(key: str) -> int | None:
    return int(os.getenv(key)) if os.getenv(key) else None


def parse_str_from_env_file_by_key(key: str) -> str | None:
    return os.getenv(key)


def parse_list_of_ints_from_env_file_by_key(key: str) -> list[int]:
    if os.getenv(key):
        list_of_ints = [
            int(channel_id.strip()) if channel_id.strip().isdigit() else None
            for channel_id
            in os.getenv(key).split(',')
        ]
        if None in list_of_ints:
            return []
        return list_of_ints
    return []
