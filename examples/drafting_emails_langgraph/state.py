from typing import TypedDict


class EmailsState(TypedDict):
    checked_emails_ids: list[str]  # 已经检查过的邮件, 每次轮询后会更新
    emails: list[dict]  # 新邮件, 当前轮询未处理的邮件
    action_required_emails: dict  # 需要确认是否回复的邮件, 当前轮询未处理的
