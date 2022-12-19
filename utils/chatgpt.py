from revChatGPT.revChatGPT import Chatbot
import json
import os
import base64
import pickle
config = None
with open('config.json', encoding='utf-8') as a:
    config = json.load(a)
try:
    bot = Chatbot(config=config, debug=True)

    bot.refresh_session()

    response = bot.get_chat_response("南方科技大学是什么")

    if response['message'] is None:
        print("Error: response['message'] is None")
        assert False
    else:
        print(f"response['message']: {response['message']}")

    print("Success!")
except Exception as exc:
    print(f"Error: {exc}")
    assert False
assert True
