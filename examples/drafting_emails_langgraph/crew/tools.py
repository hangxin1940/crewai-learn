from crewai_tools import tool
from langchain_community.agent_toolkits import GmailToolkit
from langchain_community.tools import GmailCreateDraft


class CreateDraftTool:

    @tool("创建邮件草稿")
    def create_draft(data):
        """
        用于创建email草稿。
        此工具的输入应该是一个包含三段信息的文本, 以竖线`|`作为分隔符，其三段文本分别表示为电子邮件的发送对象、电子邮件的主题和内容.。
        例如，`lorem@ipsum.com|很高兴见到你|嘿，很高兴见到你。`
        """
        email, subject, message = data.split("|")
        gmail = GmailToolkit()
        draft = GmailCreateDraft(api_resource=gmail.api_resource)
        result = draft({
            "to": [email],
            "subject": subject,
            "message": message
        })
        return f"\n创建草稿: {result}\n"
