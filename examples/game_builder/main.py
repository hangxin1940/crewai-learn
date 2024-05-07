import os

from crewai import Crew

from config import PROXY_SOCKS, OPENAI_KEY
from tasks import GameTasks

from agents import GameAgents

if __name__ == "__main__":
    os.environ['http_proxy'] = PROXY_SOCKS
    os.environ['HTTP_PROXY'] = PROXY_SOCKS
    os.environ['https_proxy'] = PROXY_SOCKS
    os.environ['HTTPS_PROXY'] = PROXY_SOCKS

    os.environ["OPENAI_API_KEY"] = OPENAI_KEY
    os.environ["OPENAI_MODEL_NAME"] = "gpt-3.5-turbo"

    tasks = GameTasks()
    agents = GameAgents()

    game = "贪吃蛇"

    # 创建代理
    senior_engineer_agent = agents.senior_engineer_agent()
    qa_engineer_agent = agents.qa_engineer_agent()
    chief_qa_engineer_agent = agents.chief_qa_engineer_agent()

    # 创建任务
    code_game = tasks.code_task(senior_engineer_agent, game)
    review_game = tasks.review_task(qa_engineer_agent, game)
    approve_game = tasks.evaluate_task(chief_qa_engineer_agent, game)

    crew = Crew(
        agents=[
            senior_engineer_agent,
            qa_engineer_agent,
            chief_qa_engineer_agent,
        ],
        tasks=[
            code_game,
            review_game,
            approve_game,
        ],
        verbose=True,
    )

    game_code = crew.kickoff()
    print(game_code)
