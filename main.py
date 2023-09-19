import json
import logging
import os
from typing import Any

from dotenv import load_dotenv
load_dotenv()

from utils.notion import ask_notion_to_shorten, ask_notion_to_summarize
from utils.atlassian_jira import get_krisp_jira, is_story_with_epic, is_story_without_epic, is_other_issue, is_unreleased_release, starts_with_date, get_issue_field
from slack_bolt import App, Ack
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk import WebClient


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

SLACK_BOT_TOKEN = os.environ['SLACK_BOT_TOKEN'].strip()
SLACK_APP_TOKEN = os.environ['SLACK_APP_TOKEN'].strip()

app = App(token=SLACK_BOT_TOKEN)


def get_project_settings(project_name: str) -> dict[str, Any]:
    with open('./config.json', 'r') as settings_file:
        settings = json.load(settings_file)
    return settings[project_name]


def format_issue_row(issue):
    return f'<{issue.permalink()}|{issue.key}> {ask_notion_to_shorten(str(get_issue_field(issue, "summary")))}\n'


def format_issue_row_with_desciption(issue):
    summary_line = format_issue_row(issue)
    if hasattr(issue.fields, 'description'):
        description = ask_notion_to_summarize(issue.fields.description)
        return summary_line + '- ' + description + '\n'
    else:
        return summary_line


def construct_release_message(project, release, release_issues, team_release_name, mentions):
    # Create header for message (announcement)
    header = f'Latest {team_release_name} release :potted_plant: :rocket:\n'

    # Create body for message (issues with descriptions)
    stories_with_epic = list(filter(is_story_with_epic, release_issues))
    stories_without_epic = list(filter(is_story_without_epic, release_issues))
    other_issues = list(filter(is_other_issue, release_issues))

    body = ''
    if stories_with_epic:
        body += ':chart_with_upwards_trend: NEW FEATURES\n'
        for story in stories_with_epic:
            body += format_issue_row_with_desciption(story)
    if stories_without_epic:
        body += ':chart_with_upwards_trend: IMPROVEMENTS\n'
        for story in stories_without_epic:
            body += format_issue_row_with_desciption(story)
    if other_issues:
        body += ':bug: Additional Features and Bug Fixes:\n'
        for issue in other_issues:
            body += format_issue_row(issue)

    # Create footer here (mentions)
    footer = "___\n" + ", ".join(map(lambda m: '<' + m + '>', mentions))

    return header + '\n' + body + '\n' + footer


@app.command('/release-notes')
def release_notes(ack: Ack, command: dict, client: WebClient):
    ack()

    project_name = command['text'].strip()
    channel_id = command['channel_id']
    logging.info(f'Processing request to generate release notes for {project_name} team')

    settings = get_project_settings(project_name)

    jira = get_krisp_jira()
    project = jira.project(project_name)
    releases = jira.project_versions(project_name)
    unreleased_releases = filter(starts_with_date, filter(is_unreleased_release, releases))

    team_release_name = settings['release_name']
    mentions = settings['mentions']

    for release in unreleased_releases:
        release_issues = jira.search_issues(f'project = {project_name} AND fixVersion = "{release.name}"')  # We can use JQL here
        release_message = construct_release_message(project, release, release_issues, team_release_name, mentions)
        client.chat_postMessage(
            channel=channel_id,
            text=release_message,
            blocks=[
                {
                    'type': 'section',
                    'text': {
                        'type': 'mrkdwn',
                        'text': release_message
                    }
                }
            ],
            unfurl_links=False,
            unfurl_media=False
        )
    logging.info(f'Finished generation of release notes for {project_name} team')


if __name__ == '__main__':
    SocketModeHandler(app, SLACK_APP_TOKEN).start()
