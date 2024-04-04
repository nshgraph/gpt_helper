from utils.slack_functions import remove_message


def say_thinking(say, message, gpt_model):
    thread_ts = message.get("thread_ts", message.get("ts"))

    thinking_message = "Thinking..."
    if gpt_model == "gpt-4":
        thinking_message = "Thinking in 4D..."

    thinking_message = say(thinking_message, thread_ts=thread_ts)

    return thinking_message


def remove_thinking(app, thinking_message):
    # clean up thinking message
    remove_message(app, thinking_message["channel"], thinking_message["ts"])
