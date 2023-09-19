import os
from notionai import NotionAI


NOTIONAI_API_TOKEN = os.environ['NOTIONAI_API_TOKEN'].strip()


def get_krisp_notionai() -> NotionAI:
    spaces = NotionAI.get_spaces(token=NOTIONAI_API_TOKEN)
    krisp_space_id = next(filter(lambda space: space['name'] == 'Krisp', spaces))['id']
    return NotionAI(token=NOTIONAI_API_TOKEN, space_id=krisp_space_id)


def ask_notion_to_shorten(issue: str) -> str:
    ai = get_krisp_notionai()
    return ai.make_shorter(issue)


def ask_notion_to_summarize(description: str) -> str:
    ai = get_krisp_notionai()
    return ai.summarize(description)
