import json
import requests

from utils import config


def call_openai(gpt_model, messages, tools=None):
    chat_url = "https://api.openai.com/v1/chat/completions"
    api_key = config["GPT_KEY"]
    authorization = "Bearer {}".format(api_key)

    headers = {"Authorization": authorization, "Content-Type": "application/json"}
    data = {
        "model": gpt_model,
        "messages": messages,
        "tools": tools,
        "temperature": 0,
        "max_tokens": 1000,
    }
    try:
        response = requests.post(chat_url, headers=headers, data=json.dumps(data))

        if response.status_code != 200:
            raise Exception("OpenAI API error: {}".format(response.text))

        data = response.json()

        response = data["choices"][0]["message"]
    except Exception as e:
        raise Exception("Failed to send messages")

    return response
