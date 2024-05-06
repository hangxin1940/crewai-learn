# %%
"""
连接到任何LLM

默认情况下，CrewAI 使用 OpenAI 的 GPT-4 模型进行语言处理.
"""
import os

from crewai import Agent, Task, Crew
from langchain_community.llms.huggingface_endpoint import HuggingFaceEndpoint
from langchain_community.llms.huggingface_hub import HuggingFaceHub
from langchain_openai import ChatOpenAI

# %%
"""
Agent类为CrewAI的基石,以下为重要属性

- role: 定义代理在解决方案中的角色
- goal: 指定代理的目标
- backstory: 代理的供背景故事
- llm: 表示代理使用的大语言模型。 默认情况下，它使用环境变量“OPENAI_MODEL_NAME”中定义的 GPT-4 模型。
- function_calling_llm [可选]: 指定代理用于调用工具的语言模型
- max_iter: 代理执行任务的最大迭代次数，默认为 15
- memory: 是否开启memory
- max_rpm: 代理执行应遵守的每分钟最大请求数
- verbose: 调试日志
- allow_delegation: 允许代理将任务委托给其他代理
- tools: 指定代理执行任务时可用的工具
- step_callback: 提供每一步之后执行的回调函数
- cache: 代理是否应使用缓存来使用工具
"""

# 可以使用环境变量定义模型
os.environ["OPENAI_MODEL_NAME"] = "gpt-3.5-turbo"

# 代理会自动从环境变量加载模型定义
example_agent = Agent(
    role='当地专家',
    goal='提供有关城市的见解',
    backstory='知识渊博的当地导游',
    verbose=True,
    memory=True,
)

# %%
"""
集成 Ollama

Ollama 是本地LLM集成的首选模型,具有高度定制化和隐私的优势.

设置如下环境变量

    ```
    OPENAI_API_BASE='http://localhost:11434/v1'
    OPENAI_MODEL_NAME='openhermes'  # Adjust based on available model
    OPENAI_API_KEY=''
    ```
    
下载Ollama https://ollama.com/download

创建类似如下ModelFile:

    ```
    FROM llama2
    
    # Set parameters
    
    PARAMETER temperature 0.8
    PARAMETER stop Result
    
    # Sets a custom system message to specify the behavior of the chat assistant
    
    # Leaving it blank for now.

    SYSTEM """"""
    ```

创建脚本获取模型

    ```
    #!/bin/zsh
    
    # variables
    model_name="llama2"
    custom_model_name="crewai-llama2"
    
    #get the base model
    ollama pull $model_name
    
    #create the model file
    ollama create $custom_model_name -f ./Llama2ModelFile
    ```
"""

# 使用本地模型
os.environ["OPENAI_API_KEY"] = "NA"

llm = ChatOpenAI(
    model="crewai-llama2",  # 按上面步骤创建的本地模型名称
    base_url="http://localhost:11434/v1"
)

general_agent = Agent(
    role='数学教授',
    goal='为提出数学问题的学生提供解决方案并给出答案',
    backstory='您是一位出色的数学教授，喜欢以每个人都能理解您的解决方案的方式解决数学问题',
    allow_delegation=False,  # 禁止委托任务或问题给其他代理
    verbose=True,
    llm=llm,
)

task = Task(
    description='解决以下数学问题：3+5',
    agent=general_agent,
)

crew = Crew(
    agents=[general_agent],
    tasks=[task],
    verbose=2,
)

result = crew.kickoff()
print(result)

# %%
"""
集成 HuggingFace

使用不同方式使用 HuggingFace 托管LLM
"""

##
# 使用私有端点
llm = HuggingFaceEndpoint(
    endpoint_url="<端点URL>",
    huggingfacehub_api_token="<API_TOKEN>",
    task="text-generation",
    max_new_tokens=512
)

agent = Agent(
    role='HuggingFace代理',
    goal='使用HuggingFace生成文本',
    backstory='GitHub文档的勤奋探索者',
    llm=llm,
)

##
# 使用HuggingFaceHub端点
llm = HuggingFaceHub(
    repo_id="HuggingFaceH4/zephyr-7b-beta",
    huggingfacehub_api_token="<API_TOKEN>",
    task='文本生成',
)

##
# 使用OpenAI兼容端点
# 使用不同的API地址环境变量来切换模型

# FastChat
os.environ["OPENAI_API_BASE"] = "http://localhost:8001/v1"
os.environ["OPENAI_MODEL_NAME"] = "oh-2.5m7b-q51"
os.environ["OPENAI_API_KEY"] = "NA"

# LM Studio
# 启动 LM Studio 并转到“Server”选项卡。 然后从下拉菜单中选择一个模型，然后等待其加载。
# 加载后，单击绿色的“Start Server”按钮并使用显示的 URL、端口和 API 密钥）。
# 以下是自 LM Studio 0.2.19 起的默认设置示例
os.environ["OPENAI_API_BASE"] = "http://localhost:1234/v1"
os.environ["OPENAI_API_KEY"] = "lm-studio"

# Mistral API
os.environ["OPENAI_API_BASE"] = "https://api.mistral.ai/v1"
os.environ["OPENAI_MODEL_NAME"] = "mistral-small"
os.environ["OPENAI_API_KEY"] = "your-mistral-api-key"

# Solar
# https://console.upstage.ai/services/solar
from langchain_community.chat_models.solar import SolarChat

os.environ["SOLAR_API_KEY"] = "your-solar-api-key"
llm = SolarChat(max_tokens=1024)

# text-gen-web-ui
os.environ["OPENAI_API_BASE"] = "http://localhost:5000/v1"
os.environ["OPENAI_MODEL_NAME"] = "NA"
os.environ["OPENAI_API_KEY"] = "NA"

# Cohere
# https://cohere.com/
from langchain_community.chat_models import ChatCohere

os.environ["COHERE_API_KEY"] = "your-cohere-api-key"
llm = ChatCohere()

# Azure Open AI
os.environ["AZURE_OPENAI_VERSION"] = "2022-12-01"
os.environ["AZURE_OPENAI_DEPLOYMENT"] = ""
os.environ["AZURE_OPENAI_ENDPOINT"] = ""
os.environ["AZURE_OPENAI_KEY"] = ""

from dotenv import load_dotenv
from crewai import Agent
from langchain_openai import AzureChatOpenAI

load_dotenv()

azure_llm = AzureChatOpenAI(
    azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"),
    api_key=os.environ.get("AZURE_OPENAI_KEY")
)

azure_agent = Agent(
    role='Azure示例代理',
    goal='演示自定义 LLM 配置',
    backstory='GitHub 文档的勤奋探索者',
    llm=azure_llm
)
