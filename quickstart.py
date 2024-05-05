import os

from crewai import Agent
from crewai_tools import SerperDevTool
from config import OPENAI_KEY, PROXY_SOCKS, SERPERDEV_API_KEY
from langchain_openai import ChatOpenAI

os.environ['http_proxy'] = PROXY_SOCKS
os.environ['HTTP_PROXY'] = PROXY_SOCKS
os.environ['https_proxy'] = PROXY_SOCKS
os.environ['HTTPS_PROXY'] = PROXY_SOCKS

os.environ["SERPER_API_KEY"] = SERPERDEV_API_KEY
os.environ["OPENAI_API_KEY"] = OPENAI_KEY

search_tool = SerperDevTool()
# %%
"""
第一步,组装代理
定义具有不同角色、背景故事和增强功能（如详细模式和内存使用）的代理。 这些元素增加了深度并指导他们的任务执行和团队内部的互动。
"""

# 创建一个拥有记忆组件的高级研究员代理
researcher = Agent(
    role='高级研究员',  # 角色
    goal='发现{topic}的突破性技术',  # 目标
    backstory='在好奇心的驱使下，你处于创新的前沿，渴望探索和分享可以改变世界的知识。',  # 背景
    tools=[search_tool],  # 工具
    memory=True,
    allow_delegation=True,
    verbose=True
)

# 创建一个拥有委托和自定义工具的作家代理
writer = Agent(
    role='作家',
    goal='讲述有关{topic}的引人入胜的科技故事',
    backstory='你是一位热爱科技的作家，渴望将最新的科技发现转化为引人入胜的故事。',
    tools=[search_tool],
    memory=True,
    allow_delegation=True,
    verbose=True
)

# %%
"""
第二步,定义任务
详细说明代理的具体目标，包括异步执行和输出自定义的新功能。 这些任务确保了他们的角色有针对性的方法。
"""

from crewai import Task

# 研究任务
research_task = Task(
    description=(
        "确定{topic}的下一个大趋势。"
        "专注于识别利弊和整体叙述。"
        "你的最终报告应该清楚地阐明要点、市场机会和潜在风险。"
    ),  # 描述
    expected_output="关于最新人工智能趋势的全面 3 段长报告。",  # 预期输出
    agent=researcher,  # 代理
    tools=[search_tool],  # 工具
)

# 攥写任务, 具备语言模型配置
write_task = Task(
    description=(
        "撰写一篇关于{topic}的富有洞察力的文章。"
        "关注最新趋势及其对行业的影响。"
        "这篇文章应该易于理解、引人入胜且积极。"
    ),
    expected_output="关于 {topic} 进展的 4 段文章，格式为 Markdown",
    agent=writer,
    tools=[search_tool],
    async_execution=False,  # 关闭异步执行
    output_file='new-blog-post.md'
)

# %%
"""
第三步,整合agent组建crew
将代理组合成一个团队，设置他们完成任务所遵循的工作流程。 现在提供配置语言模型以增强交互的选项以及用于优化性能的附加配置。
"""

from crewai import Crew, Process

# 通过一些增强配置来组建以技术为中心的团队
crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, write_task],
    process=Process.sequential,  # 默认以顺序执行
    memory=True,
    cache=True,
    max_rpm=100,  # 执行期间每分钟代理的最大请求限制
)

# %%
"""
第四步, 开始运行crew
运行团队，让他们开始执行任务。 这将触发代理之间的互动，以及他们与工具和任务之间的协作。
"""

# 启动任务
result = crew.kickoff(inputs={"topic": "医疗保健领域的人工智能"})
print(result)
