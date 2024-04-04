from utils import config
from utils.slack_functions import get_context_messages


def handle_offer(app, say, event):
    debug_channel = config["DEBUG_CHANNEL"]
    channel = event["channel"]
    ts = event.get("thread_ts", event.get("ts"))

    thread_messages = get_context_messages(app, event)

    try:
        response = "I think I could help with this: \n >{}".format(
            thread_messages[-1][1]
        )
        app.client.chat_postEphemeral(
            channel=event["channel"],
            user=event["user"],
            text="I think I could help with this",
            blocks=[
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "I think I could help with this",
                    },
                },
                {
                    "type": "actions",
                    "elements": [
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "Yes Please",
                                "emoji": True,
                            },
                            "value": "{}:{}".format(channel, ts),
                            "action_id": "accept_help_button",
                        },
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "emoji": True,
                                "text": "No Thanks",
                            },
                            "action_id": "deny_help_button",
                        },
                    ],
                },
            ],
        )
    except Exception as e:
        say("Something went wrong! {}".format(str(e)), channel=debug_channel)
