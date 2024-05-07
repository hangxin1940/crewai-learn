from textwrap import dedent

from crewai import Task


class GameTasks:
    def code_task(self, agent, game):
        return Task(
            description=dedent(
                """
                你将使用 python 创建一个游戏，以下是说明：
                
                指示
                ------------
                {game}
                
                你的最终答案必须是完整的 python 代码，只有 python 代码，没有其他任何东西。
                """
            ),
            expected_output='最终答案必须是完整的 python 代码，只有 python 代码，没有其他任何东西',
            agent=agent,
        )

    def review_task(self, agent, game):
        return Task(
            description=dedent(
                f"""
                你正在使用 python 帮助创建游戏，以下是说明：

                指示
                ------------
                {game}
                
                使用你获得的代码检查是否有错误。 检查逻辑错误，语法错误、缺少导入、变量声明、括号不匹配、和安全漏洞。
                
                你的最终答案必须是完整的 python 代码，只有 python 代码，没有其他任何东西。
                """
            ),
            expected_output='最终答案必须是完整的 python 代码，只有 python 代码，没有其他任何东西',
            agent=agent,
        )

    def evaluate_task(self, agent, game):
        return Task(
            description=dedent(
                f"""
                你正在使用 python 帮助创建游戏，以下是说明：

                指示
                ------------
                {game}
                
                你将检查代码以确保其完整, 且完成它应该做的工作。
                
                你的最终答案必须是完整的 python 代码，只有 python 代码，没有其他任何东西。
                """
            ),
            expected_output='最终答案必须是完整的 python 代码，只有 python 代码，没有其他任何东西',
            agent=agent
        )
