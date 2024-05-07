from textwrap import dedent

from crewai import Agent


class GameAgents:

    def senior_engineer_agent(self):
        return Agent(
            role='高级软件工程师',
            goal='根据需要创建软件',
            backstory='你是一家领先科技智囊团的高级软件工程师。你在 Python 编程方面的专业知识。 并尽最大努力编写完美的代码',
            allow_delegation=False,
            verbose=True,
        )

    def qa_engineer_agent(self):
        return Agent(
            role='软件质量控制工程师',
            goal='通过分析给出的错误代码来创建完美的代码',
            backstory=dedent(
                """
                你是一名专门检查代码错误的软件工程师。 你注重细节，并且善于发现隐藏的错误。
                你检查是否缺少导入、变量声明、不匹配的括号和语法错误。
                你还可以检查安全漏洞和逻辑错误.
                """),
            allow_delegation=False,
            verbose=True,
        )

    def chief_qa_engineer_agent(self):
        return Agent(
            role='首席软件质量控制工程师',
            goal='确保代码完成其应做的工作',
            backstory='你觉得程序员总是只做了一半的工作，所以你非常致力于编写高质量的代码。',
            allow_delegation=True,
            verbose=True,
        )
