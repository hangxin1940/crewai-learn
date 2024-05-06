# %%
"""
代理执行中的用户输入
用户输入在多个代理执行场景中至关重要，允许代理在必要时向用户请求其他信息。
此功能在复杂的决策过程中或当代理需要更多详细信息才能有效完成任务时特别有用。
"""

# %%
"""
要将用户输入集成到代理执行中，在任务定义中设置 human_input 标志。
启用后，代理会在提供最终答案之前提示用户输入。 此输入可以提供额外的上下文、澄清歧义或验证代理的输出。
"""

import os
from crewai import Agent, Task, Crew
from crewai_tools import SerperDevTool

os.environ["SERPER_API_KEY"] = "Your Key"
os.environ["OPENAI_API_KEY"] = "Your Key"

# 加载搜索工具
search_tool = SerperDevTool()

# 定义代理
researcher = Agent(
    role='高级研究分析师',
    goal='发现人工智能和数据科学的前沿发展',
    backstory=(
        '你是一家领先科技智库的高级研究分析师。'
        '你的专长在于识别人工智能和数据科学领域的新兴趋势和技术。'
        '你有剖析复杂数据并提出可行见解的技巧。'
    ),
    verbose=True,
    allow_delegation=False,
    tools=[search_tool],
    max_rpm=100
)
writer = Agent(
    role='技术内容策略师',
    goal='撰写有关技术进步的引人注目的内容',
    backstory=(
        '你是一位著名的技术内容策略师，以有关技术和创新的富有洞察力和引人入胜的文章而闻名。'
        '凭借对科技行业的深入了解，你可以将复杂的概念转化为引人入胜的叙述。'
    ),
    verbose=True,
    allow_delegation=True,
    tools=[search_tool],
    cache=False,  # 关闭缓存
)

# 创建任务
task1 = Task(
    description=(
        '对2024年人工智能的最新进展进行全面分析。'
        '确定关键趋势、突破性技术和潜在的行业影响。'
        '将你的发现整理成一份详细的报告。'
        '在最终确定答案之前，请务必与用户核实草稿是否良好。'
    ),
    expected_output='2024年人工智能最新进展的全面完整报告，无所遗漏',
    agent=researcher,
    human_input=True,
)

task2 = Task(
    description=(
        '利用研究人员报告中的见解，撰写一篇引人入胜的博客文章，重点介绍最重要的人工智能进步。'
        '你的文章应该内容丰富且易于理解，迎合精通技术的受众。'
        '目标是通过叙述来捕捉这些突破的本质及其对未来的影响。'
    ),
    expected_output='一篇引人入胜的 3 段博客文章，采用 Markdown 格式，介绍 2024 年人工智能的最新进展',
    agent=writer
)

# 组建团队并顺序执行任务
crew = Crew(
    agents=[researcher, writer],
    tasks=[task1, task2],
    verbose=2
)

# Get your crew to work!
result = crew.kickoff()

print("######################")
print(result)
