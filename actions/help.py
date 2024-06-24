import logging
from utils.slack_functions import get_context_messages
from llm_functions.respond import get_response_to_messages

from actions.thinking import say_thinking, remove_thinking
from actions.create_issue import create_jira_ticket

log = logging.getLogger()


def respond_with_help(app, say, message):
    thread_ts = message.get("thread_ts", message.get("ts"))

    thread_messages = get_context_messages(app, message)

    gpt_model = "gpt-4o"

    thinking_message = say_thinking(say, message)

    try:
        response, tool = get_response_to_messages(gpt_model, thread_messages)

        try:
            if tool and tool["name"] == "create_jira_ticket":
                project = tool["arguments"]["project"]
                issue_type = tool["arguments"]["taskType"]
                summary = tool["arguments"]["summary"]
                description = tool["arguments"]["description"]
                ticket = create_jira_ticket(project, issue_type, summary, description)
                response = "I made a ticket `{}` for you: {}".format(
                    summary, ticket["url"]
                )
        except Exception as e:
            log.error(str(e))
            response = "I couldn't create a ticket for you. Please try again: {}\nArguments were: {}".format(
                e, tool["arguments"]
            )

        say(response, thread_ts=thread_ts)
    except Exception as e:
        say("Something went wrong! {}".format(str(e)), thread_ts=thread_ts)

    remove_thinking(app, thinking_message)
