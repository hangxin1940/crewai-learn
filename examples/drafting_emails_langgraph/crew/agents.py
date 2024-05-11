from textwrap import dedent

from crewai import Agent
from langchain_community.agent_toolkits import GmailToolkit
from langchain_community.tools import GmailGetThread
from langchain_community.tools.tavily_search import TavilySearchResults

from crew.tools import CreateDraftTool


class EmailFilterAgents:
    def __init__(self):
        self.gmail = GmailToolkit()

    def email_filter_agent(self):
        return Agent(
            role='高级电子邮件分析师',
            goal='过滤掉不必要的电子邮件，例如新闻通讯和促销内容',
            backstory=dedent(
                """
                作为高级电子邮件分析师，你在电子邮件内容分析方面拥有丰富的经验。
                你善于区分重要电子邮件与垃圾邮件、时事通讯和其他不相关内容。 
                你的专业知识在于识别电子邮件重要性的关键模式和标记.
                """
            ),
            tools=[
                GmailGetThread(api_resource=self.gmail.api_resource),  # 用于拉取邮件
                TavilySearchResults()  # 用于搜索邮件内容的相关事实
            ],
            verbose=True,
            allow_delegation=False,
        )

    def email_action_agent(self):
        return Agent(
            role='电子邮件行动专家',
            goal='识别需要采取行动的电子邮件并编制其 id 列表',
            backstory=dedent(
                """
                凭借对细节的敏锐洞察力和理解上下文的技巧，你擅长识别需要立即采取行动的电子邮件。
                你的技能包括根据电子邮件的内容和上下文来解释电子邮件的紧迫性和重要性。
                """
            ),
            tools=[
                GmailGetThread(api_resource=self.gmail.api_resource),  # 用于拉取邮件
                TavilySearchResults()  # 用于搜索邮件内容的相关事实
            ],
            verbose=True,
            allow_delegation=False,
        )

    def email_response_writer(self):
        return Agent(
            role='电子邮件回复撰写员',
            goal='为需要回复的电子邮件起草回复',
            backstory=dedent(
                """
                你是一位熟练的作家，擅长撰写清晰、简洁且有效的电子邮件回复。
                你的优势在于有效沟通的能力，确保每个回复都是针对电子邮件的特定需求和上下文而量身定制的
                """
            ),
            tools=[
                TavilySearchResults(),  # 用于搜索邮件内容的相关事实
                GmailGetThread(api_resource=self.gmail.api_resource),
                CreateDraftTool.create_draft  # 创建草稿
            ],
            verbose=True,
            allow_delegation=False,
        )
