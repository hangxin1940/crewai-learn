# %%
"""
创建和使用代理
"""
# %%
"""
关键属性：
role：指定代理在团队中的职角色，例如“分析师”或“客户服务代表”。
goal：定义代理想要实现的目标，与其角色和crew总体目标保持一致。
backstory：为代理的角色增加深度，丰富其在团队中的动机和参与度。
tools：代理用于执行任务的功能或方法，从简单的功能到复杂的集成。
"""
# %%
"""
语言模型选项:
可以使用特定语言模型 (llm) 和函数调用语言模型 (function_calling_llm) 自定义代理，
从而提供对其处理和决策能力的高级控制。
值得注意的是，设置 function_calling_llm 允许覆盖默认的组函数调用语言模型，从而提供更大程度的定制。
"""
# %%
"""
性能与调试选项:
verbose：启用代理操作的详细日志记录，对于调试和优化非常有用。
max_rpm：设置每分钟的最大请求数 。 该属性是可选的，可以设置为 None 无限制，允许在需要时对外部服务进行无限制的查询。
max_iter: 代理可以对单个任务执行的最大迭代次数，从而防止无限循环或过长的执行。 默认值设置为 15，提供彻底性和效率之间的平衡。 一旦代理接近这个数字，它就会尽力给出一个好的答案。
"""
# %%
"""
代理与工具:
通过在初始化期间定义代理的属性和工具来定制代理。工具对于代理的功能至关重要，使他们能够执行专门的任务。
工具属性应该是代理可以使用的工具数组，默认情况下它被初始化为空列表。可以在代理初始化后添加或修改工具以适应新的要求。
"""

# 为代理分配工具
import os
from crewai import Agent
from crewai_tools import SerperDevTool

os.environ["OPENAI_API_KEY"] = "Your Key"
os.environ["SERPER_API_KEY"] = "Your Key"

# 初始化搜索工具
search_tool = SerperDevTool()

# 初始化代理
agent = Agent(
    role='研究分析师',
    goal='提供最新的市场分析',
    backstory='敏锐洞察市场趋势的专家分析师',
    tools=[search_tool],
    memory=True,  # 开启记忆组件
    verbose=True,
    max_rpm=None,  # 每分钟请求不作限制
    max_iter=15,  # 默认的最大迭代次数
    allow_delegation=False
)
# %%
"""
委托与自治:
控制代理委派任务或提出问题的能力对于在 CrewAI 框架内定制其自主性和协作动态至关重要。
默认情况下，allow_delegation 属性设置为 True，使代理能够根据需要寻求帮助或委派任务。
这种默认行为促进了 CrewAI 生态系统内的协作解决问题和效率。
如果需要，可以禁用委派以满足特定的操作要求。
"""
# 禁用委托功能
agent = Agent(
    role='内容作家',
    goal='撰写有关市场趋势的引人入胜的内容',
    backstory='一位经验丰富的作家，擅长市场分析。',
    allow_delegation=False  # 禁用委托
)
