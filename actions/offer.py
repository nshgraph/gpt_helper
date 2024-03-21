from utils import config
from utils.slack_functions import get_context_messages


def handle_offer(app, say, event):
    debug_channel = config["DEBUG_CHANNEL"]
    thread_ts = event.get("thread_ts", event.get("ts"))

    thread_messages = get_context_messages(app, event)

    try:
        response = "I think I could help with this: \n >{}".format(
            thread_messages[-1][1]
        )
        say(response, channel=debug_channel)
    except Exception as e:
        say("Something went wrong! {}".format(str(e)), channel=debug_channel)
