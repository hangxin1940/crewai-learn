import os
import time

from langchain_community.agent_toolkits import GmailToolkit
from langchain_community.tools import GmailSearch


class Nodes:
    def __init__(self):
        self.gmail = GmailToolkit()

    def check_email(self, state):
        """
        检查新邮件节点
        当前节点并不会改变状态, 但会从状态中匹配邮件是否已被处理
        """
        print("# 检查新邮件")
        search = GmailSearch(api_resource=self.gmail.api_resource)
        emails = search('after:newer_than:100d')
        checked_emails = state['checked_emails_ids'] if state['checked_emails_ids'] else []
        thread = []
        new_emails = []
        for email in emails:
            if (email['id'] not in checked_emails) and (email['threadId'] not in thread) and (
                    os.environ['MY_EMAIL'] not in email['sender']):
                thread.append(email['threadId'])
                new_emails.append({
                    'id': email['id'],
                    'threadId': email['threadId'],
                    'snippet': email['snippet'],
                    'sender': email['sender'],
                })

        checked_emails.extend([email['id'] for email in emails])
        return {
            **state,
            "emails": new_emails,
            "checked_emails_ids": checked_emails
        }

    def wait_next_run(self, state):
        """
        轮询等待节点
        """
        print("## 等待60秒")
        time.sleep(60)
        return state

    def new_emails(self, state):
        """
        此节点检查state的新邮件数量,会更改状态
        """
        if len(state['emails']) == 0:
            print("## 没有新邮件")
            return "end"
        else:
            print("## 有新邮件")
            return "continue"
