import logging
from utils.slack_functions import get_context_messages, get_permalink_from_message
from llm_functions.respond import get_response_to_messages

from actions.thinking import say_thinking, remove_thinking
from actions.create_issue import create_jira_ticket
from actions.comment_on_issue import comment_on_jira_issue

log = logging.getLogger()


def respond_with_help(app, say, message):
    thread_ts = message.get("thread_ts", message.get("ts"))

    thread_messages = get_context_messages(app, message)

    gpt_model = "gpt-4o"

    thinking_message = say_thinking(say, message)

    try:
        response, tool = get_response_to_messages(gpt_model, thread_messages)

        try:
            if tool:
                if tool["name"] == "create_jira_ticket":
                    project = tool["arguments"]["project"]
                    issue_type = tool["arguments"]["taskType"]
                    summary = tool["arguments"]["summary"]
                    description = tool["arguments"]["description"]
                    description += "\n\nOriginal conversation: {}".format(get_permalink_from_message(app, message))
                    ticket = create_jira_ticket(project, issue_type, summary, description)
                    response = "I made a ticket `{}: {}` for you: {}".format(
                        ticket["key"], summary, ticket["url"]
                    )
                elif tool["name"] == "comment_on_jira_issue":
                    issue_key = tool["arguments"]["issueKey"]
                    comment = tool["arguments"]["comment"]
                    ticket = comment_on_jira_issue(issue_key, comment)
                    response = "I added a comment `{}` to `{}` for you: {}".format(
                        comment, issue_key, ticket["url"]
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
