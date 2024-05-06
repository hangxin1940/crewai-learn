# %%
"""
分层流程

CrewAI中的分层流程引入了一种结构化的任务管理方法，模拟传统的组织层次结构，以实现高效的任务委派和执行。
这种系统化的工作流程可确保以最佳效率和准确性处理任务，从而提高项目成果。

分层流程旨在利用 GPT-4 等先进模型，优化token使用，同时更高效地处理复杂任务。

默认情况下，CrewAI中的任务通过顺序流程进行管理。
然而，采用分层方法可以在任务管理中实现清晰的层次结构，其中“manager”代理(由crewAI自动创建)协调工作流程、委派任务并验证结果，以实现简化和有效的执行。

任务委派："manager"代理根据机组成员的角色和能力在机组成员之间分配任务。
结果验证："manager"代理评估结果以确保它们符合所需的标准。
高效的工作流程：模拟公司结构，提供有组织的任务管理方法。
"""
from crewai import Agent, Crew, Process
from langchain_openai import ChatOpenAI

# %%
"""
实现分层代理
"""

# 定义代理
researcher = Agent(
    role='研究员',
    goal='深入分析',
    backstory='经验丰富的数据分析师，善于发现隐藏的趋势。',
    llm=ChatOpenAI(
        model="gpt-3.5-turbo",
    ),
    cache=True,
    verbose=True,
)

writer = Agent(
    role='作家',
    goal='创建引人入胜的内容',
    backstory='热衷于技术领域讲故事的创意作家。',
    llm=ChatOpenAI(
        model="gpt-3.5-turbo",
    ),
    cache=True,
    verbose=True,
)

# 通过分层流程和附加配置建立crew
project_crew = Crew(
    tasks=[...],  # 委派和执行的任务
    agents=[researcher, writer],
    manager_llm=ChatOpenAI(
        model="gpt-3.5-turbo",
    ),  # 设定 'manager' 代理的语言模型
    process=Process.hierarchical,  # 设置分层流程
    memory=True,
)

"""
实际工作流程

任务分配：'manager'考虑每个代理的能力和可用工具，战略性地分配任务。
执行和审查：代理可以使用异步执行和回调函数选项来完成任务，以简化工作流程。
顺序任务进展：尽管是一个分层过程，但任务遵循逻辑顺序以顺利进展，并在'manager'代理的监督下进行。
"""
