# PM Helper

## Summary

This app helps PMs in their routine tasks via Slack bot. It supports the following features:
- Generating release notes for Jira project/team

## Usage

Type `/release-notes WEB` to generate release notes for **WEB** team.

## Configuring environment

The app requires configuration to run. There is `config.json` file where configuration should be added.
First level is the name of Jira project/team that you will use with the Slack bot to generate release notes message for.
Then you have parameters specific to each Jira project/team:

| Parameter | Meaning |
| --------- | ------- |
| **full_name** | `string` Full name of team. Currently not used |
| **release_name** | `string` Name that will be used in release message |
| **mentions** | `list[string]` List of Slack user/group mentions to be included in release message (ex. ["@dev", "@managers"]) |

Also, for the app to work you need to provide some environment variables. Those are listed below:

| Environment variable | Meaning |
| -------------------- | ------- |
| **JIRA_BASE_URL** | Base url of your Jira instance |
| **JIRA_USER_EMAIL** | Email of user the app will use to navigate Jira issues |
| **JIRA_USER_API_TOKEN** | Jira API token for authentication |
| **OPENAI_API_KEY** | OpenAI API token for authentication |
| **SLACK_BOT_TOKEN** | Slack Bot token for authentication |
| **SLACK_APP_TOKEN** | Slack App token for authentication |

## Installing dependencies (for running locally)

```sh
pip install -r requirements.txt
```

**Note**: this will install the libraries into your system-wide Python installation. You should consider creating a virtual environment via `venv` or some other tool

## Running locally

You will need to provide environment variables listed under [Configuring environment](#configuring-environment).
One way to do that is to provide them in Shell like this (same for other variables):

```sh
JIRA_BASE_URL='https://mycompanyname.atlassian.net' python main.py
```

Another way is to create `.env` file in the same folder `main.py` is located with the following structure:

```sh
JIRA_BASE_URL='...'
JIRA_USER_EMAIL='...'
JIRA_USER_API_TOKEN='...'
OPENAI_API_KEY='...'
SLACK_BOT_TOKEN='...'
SLACK_APP_TOKEN='...'
```

and then just run

```sh
python main.py
```

## Building Docker image

```sh
docker build -f Dockerfile --tag pm-helper:<version>
```

## Running Docker

You will need to provide environment variables listed under [Configuring environment](#configuring-environment). You can do it with a command line like this (same for other variables):

```sh
docker run -e JIRA_BASE_URL='...' pm-helper:<version>
```

or use some other method.
