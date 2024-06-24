# coding=utf-8
from atlassian import Jira
from utils import config


def create_jira_ticket(project, issue_type, summary, description):
    credentials = config.get("CONFIG_GPT3PO_ATLASSIAN_PERMISSIONS")
    if not credentials:
        raise ValueError("No Atlassian credentials found")
    jira = Jira(
        url="https://thematicanalysis.atlassian.net/",
        username=credentials["username"],
        password=credentials["token"],
    )

    issue = jira.issue_create(
        fields={
            "project": {"key": project},
            "issuetype": {"name": issue_type},
            "summary": summary,
            "description": description,
        }
    )

    issue["url"] = "https://thematicanalysis.atlassian.net/browse/{}".format(
        issue["key"]
    )

    return issue
