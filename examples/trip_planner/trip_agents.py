from crewai import Agent
from langchain_openai import ChatOpenAI
from tools.browser_tools import BrowserTools
from tools.calculator_tools import CalculatorTools
from tools.search_tools import SearchTools


class TripAgents:
    """ 旅行规划代理 """

    def city_section_agent(self):
        return Agent(
            role='城市选择专家',
            goal='根据天气、季节和价格选择最佳城市',
            backstory='一位分析旅行数据以选择理想目的地的专家',
            tools=[
                SearchTools.search_internet,
                BrowserTools.scrape_and_summarize_website
            ],
            verbose=True,
        )

    def local_expert(self):
        return Agent(
            role='当地专家',
            goal='提供有关所选城市的最佳见解',
            backstory='一个知识渊博的当地导游, 提供关于这座城市的景点,习俗等丰富信息',
            tools=[
                SearchTools.search_internet,
                BrowserTools.scrape_and_summarize_website
            ],
            verbose=True,
        )

    def travel_concierge(self):
        return Agent(
            role='惊人的旅行礼宾服务',
            goal='为城市提供预算和包装建议，创建最令人惊叹的旅行路线',
            backstory='拥有数十年经验的旅行规划和物流专家',
            tools=[
                SearchTools.search_internet,
                BrowserTools.scrape_and_summarize_website,
                CalculatorTools.calculate,
            ],
            verbose=True,
        )
