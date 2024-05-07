import os

from crewai import Crew

from config import PROXY_SOCKS, SERPERDEV_API_KEY, OPENAI_KEY
from trip_agents import TripAgents
from trip_tasks import TripTasks


class TripCrew:
    def __init__(self, origin, cities, date_range, interests):
        self.origin = origin  # 出发地
        self.cities = cities  # 城市
        self.date_range = date_range  # 起止时间
        self.interests = interests  # 兴趣

    def run(self):
        agents = TripAgents()
        tasks = TripTasks()

        city_selector_agent = agents.city_section_agent()
        local_expert_agent = agents.local_expert()
        travel_concierge_agent = agents.travel_concierge()

        # 确认目的地
        identify_task = tasks.identify_task(
            city_selector_agent,
            self.origin,
            self.cities,
            self.interests,
            self.date_range
        )

        # 手机当地情况
        gather_task = tasks.gather_task(
            local_expert_agent,
            self.origin,
            self.interests,
            self.date_range
        )

        # 规划行程
        plan_task = tasks.plan_task(
            travel_concierge_agent,
            self.origin,
            self.interests,
            self.date_range
        )

        crew = Crew(
            agents=[
                city_selector_agent,
                local_expert_agent,
                travel_concierge_agent,
            ],
            tasks=[
                identify_task,
                gather_task,
                plan_task,
            ],
            verbose=True,
        )

        result = crew.kickoff()
        return result


if __name__ == "__main__":
    os.environ['http_proxy'] = PROXY_SOCKS
    os.environ['HTTP_PROXY'] = PROXY_SOCKS
    os.environ['https_proxy'] = PROXY_SOCKS
    os.environ['HTTPS_PROXY'] = PROXY_SOCKS

    os.environ["BROWSERLESS_API_KEY"] = ""
    os.environ["SERPER_API_KEY"] = SERPERDEV_API_KEY
    os.environ["OPENAI_API_KEY"] = OPENAI_KEY
    os.environ["OPENAI_MODEL_NAME"] = "gpt-3.5-turbo"

    crew = TripCrew(
        origin="北京",
        cities=["重庆", "深圳"],
        date_range="2024-05-01 ~ 2024-05-07",
        interests=["美食", "文化"]
    )
    result = crew.run()
    print(result)
