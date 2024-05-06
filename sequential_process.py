# %%
"""
顺序流程

顺序过程确保任务按照线性顺序一个接一个地执行。 这种方法非常适合需要按特定顺序完成任务的项目。
"""
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI

# 最适合任务明确、分步进行的项目

# 定义代理
researcher = Agent(
    role='研究员',
    goal='进行基础研究',
    backstory='一位经验丰富的研究人员，热衷于发现见解',
    llm=ChatOpenAI(
        model="gpt-3.5-turbo",
    ),
)

analyst = Agent(
    role='分析师',
    goal='分析研究结果',
    backstory='一位细心的分析师，有发现模式的诀窍',
    llm=ChatOpenAI(
        model="gpt-3.5-turbo",
    ),
)

writer = Agent(
    role='作家',
    goal='撰写报告',
    backstory='一位熟练的作家，具有撰写引人入胜的叙事的天赋',
    llm=ChatOpenAI(
        model="gpt-3.5-turbo",
    ),
)

# 按顺序定义任务
research_task = Task(description='收集相关数据等等...', agent=researcher)
analysis_task = Task(description='分析数据等等...', agent=analyst)
writing_task = Task(description='撰写报告等等...', agent=writer)

# 以顺序流程组建crew
report_crew = Crew(
    agents=[researcher, analyst, writer],
    tasks=[research_task, analysis_task, writing_task],
    process=Process.sequential,
)
