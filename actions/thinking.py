def say_thinking(say, event, gpt_model):
    thread_ts = event.get("thread_ts", event.get("ts"))

    thinking_message = "Thinking..."
    if gpt_model == "gpt-4":
        thinking_message = "Thinking in 4D..."

    thinking_message = say(thinking_message, thread_ts=thread_ts)

    return thinking_message


def remove_thinking(app, thinking_message):
    # clean up thinking message
    app.client.chat_delete(
        channel=thinking_message["channel"], ts=thinking_message["ts"]
    )
