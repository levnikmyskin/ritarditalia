import json


def get_bot_token(path="./bot_token.json") -> str:
    with open(path, 'r') as f:
        return json.load(f)['token']
