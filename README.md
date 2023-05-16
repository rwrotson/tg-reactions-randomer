# Description

This script updates sets of allowable emoji-reactions in Telegram chats. When executed, for every chat provided, it randomly chooses a random number of reactions and sets them as allowable. You can add this script to `crontab`, so that reactions in chats are updated automatically and regularly. 

# Install

```
pip install .
```

Note that the script requires Python>=3.11.

# Usage

```
tg-random-reactions [-h] [-i API_ID] [-s API_HASH] [-f MIN] [-t MAX] [-c CHAT_IDS [CHAT_IDS ...]] [-v CHANNEL_IDS [CHANNEL_IDS ...]] [-e ENV]
```

Note that you can get help by:
```
tg-random-reactions -h
```

## Prerequisites 

In order to run script you need `api_id` and `api_hash` to your Telegram API app.

You can get get it [here](https://my.telegram.org/) at API Development tools section.

Also you need `chat_id` for every chat you want to manage. Sure thing, you need to have admin role in these chats.

One of the ways to get `chat_id` is following. 
1) Create bot with help of `@BotFather` account on Telegram and get a token for it. 
2) Add this bot to your chat.
3) Get the list of updates for your bot here (paste your token): ```https://api.telegram.org/bot<YourBOTToken>/getUpdates```
4) Look for the `chat` object in JSON response, there you can find `id` key. The integer value here is `chat_id`.
5) If needed, more advices on this topic are [here](https://stackoverflow.com/questions/32423837/telegram-bot-how-to-get-a-group-chat-id).

Similarly you need `channel_id` for every channel.

The most simple way to get it is to forward message from your channel to `@JsonDumpBot`. Then in JSON reply look for the key `["message"]["forward_from_chat"]["id"]`. It will look like `"id": -1000000000000`.

## Launch

### Environment variables and .env file

You can set `api_id`, `api_hash`, `chat_ids` and `channel_ids` as environmental variables or in .env files, like that:

```
API_ID=0000000
API_HASH=xx000x00x0x0000x0000xxx000000x00
CHAT_IDS=1000000, 200000, 300000
CHANNEL_IDS=1000000000000
```

Note that `CHAT_IDS` and `CHANNEL_IDS` are strings containing integers seperated by comma. If you have only one `chat_id` or `channel_id` just write it as integer.

### Console params

You can pass `api_id`, `api_hash`, `chat_ids` and `channel_ids` directly to the script by using `--api_id`, `--api_hash`, `--chat_ids` and `--channel_ids` keyword arguments.

Also there are `--min` and `--max` options, which set the interval for the number of reactions that the script will set. If `--min` is 10 and `--max` is 20, the script will randomly choose from 10 to 20 emojies and set them in chat as allowable reactions. Maximum quantity is quantity of all standard Telegram reactions, which is 72.

### Examples

```
tg-reactions-randomer --min 10 --max 20 --api_id 0000000 --api_hash xx000x00x0x0000x0000xxx000000x00 --chat_ids 1000000 200000 300000 --channel_ids 1000000000000
```
Will update reactions in chats with ids 1000000, 2000000 and 3000000 and in channel 1000000000000 and set from 10 to 20 random reactions for each of them.

If you set `api_id`, `api_hash`, `chat_ids` or `channel_ids` as environment variables, you can omit corresponding flags:
```
tg-reactions-randomer --min 10 --max 20 --env /some/path/to/.env
```

You can omit `--env` file path if you have set environents directly:
```
tg-reactions-randomer --min 10 --max 20
```

Also you can omit `--min` and `--max`. Defaults for them are 2 and 42, just run the script to use defaults:
```
tg-reactions-randomer
```

### Recomendations

The script is meant to be used with a crontab. Define an update interval, open a crontab and add a task there.
```
crontab -e
```

```
0 0 * * * tg-reactions-randomer --min 10 --max 20 --env /some/path/to/.env
```
Will run this script every day at 00:00.

***N.B.: First time you run this script on new computer, it creates Session file, which is used to authorize script to manage your Telegram account. However, on the first launch it will ask your phone number and send you confirmation code which is needed to be prompted in terminal. Therefore, run the script at least once before adding it to crontab).***