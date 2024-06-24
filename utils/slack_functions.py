from utils import config


def get_context_messages(app, message):
    channel = message["channel"]
    thread_ts = message.get("thread_ts")

    if thread_ts:
        thread = app.client.conversations_replies(channel=channel, ts=thread_ts)

        # Extract messages text
        thread_messages = []
        for thread_message in thread["messages"]:
            actor = "user" if thread_message.get("is_bot", False) else "assistant"
            message = thread_message["text"]
            thread_messages.append((actor, message))
    else:
        message = message["text"]
        thread_messages = [("user", message)]

    return thread_messages


def message_is_in_thread(app, event):
    thread_ts = event.get("thread_ts")
    return thread_ts is not None


def is_bot_part_of_thread(app, event):
    bot_user = config["BOT_USER_ID"]
    channel = event["channel"]

    thread_ts = event.get("thread_ts")
    if not thread_ts:
        return False

    thread = app.client.conversations_replies(channel=channel, ts=thread_ts)
    for message in thread["messages"]:
        if message.get("user") == bot_user:
            return True

    return False


def get_message_from_reference(app, channel, message_ts):
    message = app.client.conversations_history(
        channel=channel, latest=message_ts, limit=1, inclusive=True
    )
    return message["messages"][0]


def remove_message(app, channel, ts):
    # clean up thinking message
    app.client.chat_delete(channel=channel, ts=ts)


def get_permalink_from_message(app, channel, message_ts):
    response = app.client.chat_getPermalink(channel=channel, message_ts=message_ts)
    return response["permalink"]
