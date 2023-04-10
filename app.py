import os
import json
import requests
import logging
import base64
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_bolt.adapter.aws_lambda import SlackRequestHandler

from utils import config

log = logging.getLogger()

chatUrl = "https://api.openai.com/v1/chat/completions"

# Install the Slack app and get xoxb- token in advance
app = App(process_before_response=True, token=config["SLACK_BOT_TOKEN"], signing_secret=config["SLACK_SIGNING_SECRET"])


def respond_to_slack_within_3_seconds(body, ack):
    ack(f"Accepted!")


def get_image_for_message(message):
    return None
    if len(message.get("files", [])) > 0:
        file_url = message["files"][0]["url_private"]
        # Get the contents of the image file
        try:
            headers = {"Authorization": "Bearer " + config["SLACK_BOT_TOKEN"]}
            image_response = requests.get(file_url, headers=headers)
            print(image_response)
            image_contents = image_response.content
            image_contents = base64.b64encode(image_contents).decode('utf-8')
            return {"image": image_contents}
        except Exception as e:
            print("Error getting image contents: {}".format(e))
    return None


def handle_message(say, event):
    channel = event["channel"]
    thread_ts = event.get("thread_ts", event.get("ts"))

    if thread_ts:
        thread = app.client.conversations_replies(
            channel=channel,
            ts=thread_ts
        )

        # Extract messages text
        thread_messages = []
        for thread_message in thread["messages"]:
            actor = "user" if thread_message.get("is_bot", False) else "assistant"
            message = thread_message["text"]
            image = get_image_for_message(thread_message)
            if image:
                message = [message, image]
            thread_messages.append(("user", message))
    else:
        message = event["text"]
        image = get_image_for_message(thread_message)
        if image:
            message = [message, image]
        thread_messages = [("user", message)]

    print("thread_messages", json.dumps(thread_messages))
    thinking_message = "Thinking..."
    gpt_model = "gpt-3.5-turbo"

    if "(be special)" in event["text"]:
        thinking_message = "Thinking in 4D..."
        gpt_model = "gpt-4"

    api_key = config["GPT_KEY"]

    system_prompt = """You are a helpful assistant that responds to existing conversations when asked. You are provided with the entire thread of conversation."""

    thinking_message = say(thinking_message, thread_ts=thread_ts)

    messages = [
        {"role": "system", "content": system_prompt},
    ] + [{"role": message[0], "content": message[1]} for message in thread_messages]

    authorization = "Bearer {}".format(api_key)

    headers = {"Authorization": authorization, "Content-Type": "application/json"}
    data = {
        "model": gpt_model,
        "messages": messages,
        "temperature": 0,
        "max_tokens": 1000,
    }

    try:
        response = requests.post(chatUrl, headers=headers, data=json.dumps(data))

        if response.status_code != 200:
            raise Exception("OpenAI API error: {}".format(response.text))

    
        data = response.json()
        response = data["choices"][0]["message"]["content"]

        app.client.chat_delete(channel=channel, ts=thinking_message["ts"])

        say(response, thread_ts=thread_ts)
    except Exception as e:
        say("Something went wrong! {}".format(str(e)), thread_ts=thread_ts)


app.event("app_mention")(ack=respond_to_slack_within_3_seconds, lazy=[handle_message])
app.event("message")(ack=respond_to_slack_within_3_seconds, lazy=[handle_message])
    

if __name__ == "__main__":
    SocketModeHandler(app, config["SLACK_APP_TOKEN"]).start()

SlackRequestHandler.clear_all_log_handlers()
logging.basicConfig(format="%(asctime)s %(message)s", level=logging.DEBUG)


def lambda_handler(event, context):
    print(event)
    slack_handler = SlackRequestHandler(app=app)
    res = slack_handler.handle(event, context)
    return res
