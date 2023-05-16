import asyncio

from app.params import get_params
from app.tg import update_all_chats_and_channels
from app.exceptions import CustomValueException, NotAllParamsException
from app.logger import get_logger


logger = get_logger('main')


def main():
    try:
        params = get_params()
    except (CustomValueException, NotAllParamsException) as e:
        logger.error(e)
    else:
        asyncio.run(update_all_chats_and_channels(params))


if __name__ == '__main__':
    main()
