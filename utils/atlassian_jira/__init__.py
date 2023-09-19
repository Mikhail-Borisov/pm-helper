from typing import Any, Optional
from jira import JIRA, Issue
import os
import re


JIRA_BASE_URL = os.environ['JIRA_BASE_URL'].strip()
JIRA_USER_EMAIL = os.environ['JIRA_USER_EMAIL'].strip()
JIRA_USER_API_TOKEN = os.environ['JIRA_USER_API_TOKEN'].strip()


def parent_issue(issue: Optional[Issue]) -> Optional[Issue]:
    return getattr(getattr(issue, 'fields', None), 'parent', None)


def issuetype(issue: Optional[Issue]) -> Optional[Any]:
    return getattr(getattr(issue, 'fields', None), 'issuetype', None)


def get_issue_field(issue: Optional[Issue], field_name: str) -> Optional[Any]:
    return getattr(getattr(issue, 'fields', None), field_name, None)


def is_story_with_epic(issue: Optional[Issue]) -> bool:
    return issuetype(issue) == 'Story' and parent_issue(issue) is not None and issuetype(parent_issue(issue)) == 'Epic'


bug_keywords = [
    'errors?',
    'fix',
    'miss(ing)?'
    'wrong',
    'invalid',
    'bad',
    'incorrect',
    'fail(ed)?',
    'crash(ed)?'
]
bug_regex = '(' + '|'.join(bug_keywords) + ')'
bug_regex_compiled = re.compile(bug_regex, re.IGNORECASE)

def is_bug(issue: Optional[Issue]) -> bool:
    return issuetype(issue) == 'Bug' \
        or bug_regex_compiled.match(getattr(getattr(issue, 'fields', None), 'summary', '')) is not None


def is_story_without_epic(issue: Optional[Issue]) -> bool:
    return ((issuetype(issue) == 'Story' and parent_issue(issue) is None) or (issuetype(issue) == 'Task')) \
        and not is_bug(issue)


def is_other_issue(issue: Optional[Issue]) -> bool:
    return not is_story_with_epic(issue) and not is_story_without_epic(issue)


def is_unreleased_release(release: Any) -> bool:
    return not getattr(release, 'released', None)


date_regex = r'\d{1,2}-\w{2,3}-\d{1,2}'
date_regex_compiled = re.compile(date_regex)

def starts_with_date(release: Any) -> bool:
    return date_regex_compiled.match(getattr(release, 'name', '')) is not None


def get_krisp_jira() -> JIRA:
    jiraOptions = {'server': JIRA_BASE_URL}
    return JIRA(
        options=jiraOptions,
        basic_auth=(JIRA_USER_EMAIL, JIRA_USER_API_TOKEN)
    )
