# coding=utf-8
from atlassian import Jira
from utils import config


def comment_on_jira_issue(issue_key, comment):
    credentials = config.get("CONFIG_GPT3PO_ATLASSIAN_PERMISSIONS")
    if not credentials:
        raise ValueError("No Atlassian credentials found")
    jira = Jira(
        url="https://thematicanalysis.atlassian.net/",
        username=credentials["username"],
        password=credentials["token"],
    )

    issue = jira.issue_add_comment(issue_key, comment)


    issue["url"] = "https://thematicanalysis.atlassian.net/browse/{}".format(
        issue_key
    )

    return issue
