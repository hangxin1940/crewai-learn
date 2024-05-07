from textwrap import dedent

from crewai import Task


class TripTasks:
    """ 旅行规划任务 """

    def identify_task(self, agent, origin, cities, interests, range):
        """ 确认任务 """
        return Task(
            description=dedent(
                f"""
                根据天气模式、季节性事件和旅行成本等特定标准分析和选择最适合旅行的城市。
                这项任务涉及比较多个城市，考虑当前天气状况、即将到来的文化或季节性活动以及总体旅行费用等因素。
    
                你的最终答案必须是关于所选城市的详细报告，以及你发现的有关该城市的所有信息，包括实际航班费用、天气预报和景点。
                {self.__tip_section()}
                
                出发地： {origin}
                城市选项：{cities}
                行程日期： {range}
                旅行者兴趣： {interests}
                """),
            expected_output="关于所选城市的详细报告，以及你发现的有关该城市的所有信息，包括实际航班费用、天气预报和景点",
            agent=agent,
        )

    def gather_task(self, agent, origin, interests, range):
        """ 收集任务 """
        return Task(
            description=dedent(
                f"""
                作为这个城市的当地专家，你必须为前往那里并希望拥有最好旅程的人编制一份深入的指南！
                收集有关主要景点、当地习俗、特别活动和日常活动建议的信息。
                找到最好的去处，只有当地人才会知道的地方。
                本指南应全面概述这座城市所提供的内容，包括一些名不见经传的景点、文化热点、必游地标、天气预报和高额费用项目。
                
                最终的答案必须是一份全面的城市指南，丰富的文化见解和实用技巧，为提升旅行体验而量身定制。
                {self.__tip_section()}
                
                行程日期： {range}
                出发地： {origin}
                旅行者兴趣： {interests}
                """),
            expected_output="一份全面的城市指南，丰富的文化见解和实用技巧，为提升旅行体验而量身定制",
            agent=agent,
        )

    def plan_task(self, agent, origin, interests, range):
        """ 计划任务 """
        return Task(
            description=dedent(
                f"""
                将本指南扩展为完整的 7 天行程，其中包含详细的每日计划，包括天气预报、用餐地点、打包建议和预算明细。
                你必须建议实际的参观地点、实际的住宿酒店和实际的餐厅。                
                这个旅行计划要涵盖行程的方方面面，从到达到出发，将城市导游信息与实际的旅游相结合。
                
                你的最终答案必须是一个完整的扩展旅行计划，格式为 markdown，包括每日时间表、预期的天气状况、推荐的服装和要打包的物品，以及详细的预算，确保有史以来最好的旅行，具体给出你选择每个地方的原因，是什么让它们与众不同！
                {self.__tip_section()}
                
                行程日期： {range}
                出发地： {origin}
                旅行者兴趣： {interests}
                """),
            expected_output="一个完整的扩展旅行计划，格式为 markdown，包括每日时间表、预期的天气状况、推荐的服装和要打包的物品，以及详细的预算，确保有史以来最好的旅行，具体给出你选择每个地方的原因，是什么让它们与众不同",
            agent=agent,
        )

    def __tip_section(self):
        return "如果你做得最好，我会给你 100 美元的小费！"
