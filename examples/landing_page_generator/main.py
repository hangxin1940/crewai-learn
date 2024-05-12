# -*- coding: utf-8 -*-

import json
import os

from crewai import Task, Crew, Agent
from langchain_community.agent_toolkits import FileManagementToolkit

from config import PROXY_SOCKS, OPENAI_KEY, SERPERDEV_API_KEY
from tools.file_tools import FileTools
from tools.template_tools import TemplateTools
from tools.browser_tools import BrowserTools
from tools.search_tools import SearchTools
from tasks import TaskPrompts


class LandingPageCrew:

    def __init__(self, idea):
        self.agents_config = json.loads(open("config/agents.json", "r").read())
        self.idea = idea
        self.__create_agents()

    def run(self):
        expanded_idea = self.__expand_idea()
        components = self.__choose_template(expanded_idea)
        self.__update_components(components, expanded_idea)

    def __expand_idea(self):
        expand_idea_task = Task(
            description=TaskPrompts.expand().format(idea=self.idea),
            agent=self.idea_analyst,
            expected_output="最终答案必须是一份全面的创意报告，详细说明为什么这是一个好创意、价值主张、独特的卖点、为什么人们应该关心它以及独特的功能"
        )

        refine_idea_task = Task(
            description=TaskPrompts.refine_idea(),
            agent=self.communications_strategist,
            expected_output="你的最终答案必须是更新的完整综合想法报告，其中包含'为什么'、'怎么做'、'是什么'这些核心信息以及关键特征和支持论点。"
        )

        crew = Crew(
            agents=[self.idea_analyst, self.communications_strategist],
            tasks=[expand_idea_task, refine_idea_task],
            verbose=True
        )

        expanded_idea = crew.kickoff()
        return expanded_idea

    def __choose_template(self, expanded_idea):
        choose_template_task = Task(
            description=TaskPrompts.choose_template().format(idea=self.idea),
            agent=self.react_developer,
            expected_output="你的最终答案必须只是需要更新的组件完整文件路径的 JSON 数组"
        )

        update_page = Task(
            description=TaskPrompts.update_page().format(idea=self.idea),
            agent=self.react_developer,
            expected_output="最终答案必须只是一个有效的 json 列表，其中包含我们将使用的每个组件的完整路径，与你获取它们的方式相同"
        )

        crew = Crew(
            agents=[self.react_developer],
            tasks=[choose_template_task, update_page],
            verbose=True
        )

        components = crew.kickoff()
        return components

    def __update_components(self, components, expanded_idea):
        components = components.replace("\n", "").replace(" ", "").replace("```", "")
        components = json.loads(components)

        for component in components:
            file_content = open(
                f"./workdir/{component.split('./')[-1]}",
                "r"
            ).read()
            create_content = Task(
                description=TaskPrompts.component_content().format(
                    expanded_idea=expanded_idea,
                    file_content=file_content,
                    component=component
                ),
                agent=self.conetent_editor_agent,
                expected_output="返回一个好的文本选项列表来替换组件上每个单独的现有文本，建议必须基于以下想法，并且长度也必须与原始文本大致相同，我们需要替换所有文本"
            )

            update_component = Task(
                description=TaskPrompts.update_component().format(
                    component=component,
                    file_content=file_content
                ),
                agent=self.react_developer,
                expected_output="你的最终答案必须是更新的组件内容"
            )

            qa_component = Task(
                description=TaskPrompts.qa_component().format(
                    component=component
                ),
                agent=self.react_developer,
                expected_output="你的最终答案应该是确认该组件有效并遵守规则，以及是否必须将更新版本写入文件系统"
            )

            crew = Crew(
                agents=[self.conetent_editor_agent, self.react_developer],
                tasks=[create_content, update_component, qa_component],
                verbose=True
            )

            crew.kickoff()

    def __create_agents(self):
        idea_analyst_config = self.agents_config["senior_idea_analyst"]
        strategist_config = self.agents_config["senior_strategist"]
        developer_config = self.agents_config["senior_react_engineer"]
        editor_config = self.agents_config["senior_content_editor"]

        toolkit = FileManagementToolkit(
            root_dir='workdir',
            selected_tools=["read_file", "list_directory"]
        )

        self.idea_analyst = Agent(
            **idea_analyst_config,
            tools=[SearchTools.search_internet, BrowserTools.scrape_and_summarize_website],
            verbose=True,
        )

        self.communications_strategist = Agent(
            **strategist_config,
            tools=[SearchTools.search_internet, BrowserTools.scrape_and_summarize_website],
            verbose=True
        )

        self.react_developer = Agent(
            **developer_config,
            tools=[
                      SearchTools.search_internet,
                      BrowserTools.scrape_and_summarize_website,
                      TemplateTools.learn_landing_page_options,
                      TemplateTools.copy_landing_page_template_to_project_folder,
                      FileTools.write_file
                  ] + toolkit.get_tools(),
            verbose=True
        )

        self.content_editor_agent = Agent(
            **editor_config,
            tools=[SearchTools.search_internet, BrowserTools.scrape_and_summarize_website],
            verbose=True
        )


if __name__ == "__main__":
    os.environ['http_proxy'] = PROXY_SOCKS
    os.environ['HTTP_PROXY'] = PROXY_SOCKS
    os.environ['https_proxy'] = PROXY_SOCKS
    os.environ['HTTPS_PROXY'] = PROXY_SOCKS

    os.environ["BROWSERLESS_API_KEY"] = ''
    os.environ["SERPER_API_KEY"] = SERPERDEV_API_KEY
    os.environ["OPENAI_API_KEY"] = OPENAI_KEY
    os.environ["OPENAI_MODEL_NAME"] = "gpt-3.5-turbo"

    idea = "3d打印机销售网站"

    crew = LandingPageCrew(idea)
    crew.run()

    print("所有任务已完成！")
