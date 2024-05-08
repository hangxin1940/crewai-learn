from textwrap import dedent

from crewai import Task


class EmailFilterTasks:
    def filter_emails_task(self, agent, emails):
        return Task(
            description=dedent(
                """
                分析一批电子邮件并过滤掉不必要的电子邮件，例如垃圾邮件和促销活动。
                利用你在电子邮件内容分析方面的专业知识来区分重要电子邮件和其他电子邮件，注意发件人并避免无效电子邮件。
                
                确保过滤实际针对用户的消息并避免通知。
                
                电子邮件
                --------
                {emails}
                
                你的最终答案必须是相关的 thread_ids 和 sender, 使用项目符号列出。
                """
            ),
            expected_output='最终答案必须是相关的 thread_ids 和 sender, 使用项目符号列出。',
            agent=agent
        )

    def action_required_emails_task(self, agent):
        return Task(
            description=dedent(
                """
                对于每个电子邮件thread，仅使用实际 Thread ID 拉取和分析整个thread。
                了解对话的上下文、关键点和整体情绪。
                
                确定每个问题在响应中需要解决的主要问题或关注点
                
                你的最终答案必须是包含以下内容的所有电子邮件的列表：
                - thread_id
                - 电子邮件thread的摘要
                - 突出显示要点
                - 识别用户以及他将回答谁
                - 线程中的沟通方式
                - 发件人的电子邮件地址
                """
            ),
            expected_output=dedent("""
                你的最终答案必须是包含以下内容的所有电子邮件的列表：
                    - thread_id
                    - 电子邮件thread的摘要
                    - 突出显示要点
                    - 识别用户以及他将回答谁
                    - 线程中的沟通方式
                    - 发件人的电子邮件地址
                """
                                   ),
            agent=agent,
        )

    def draft_responses_task(self, agent):
        return Task(
            description=dedent(
                """
                根据确实需要回复的电子邮件，为每封电子邮件起草回复。
                确保每个回复都是针对电子邮件中概述的特定需求和背景进行定制的。
                
                - 假设用户的角色并模仿threads中的通信风格。
                - 如有必要，请随意对该主题进行研究，以提供更详细的答复。
                - 如果有必要进行研究，请在起草回复之前进行。
                - 如果您需要再次拉动线程，请仅使用实际的thread_id来执行此操作。
                
                使用提供的工具起草每个回复。
                使用该工具时传递以下输入：
                - to（待回复的发件人）
                - subject
                - message
                
                在回复最终答案之前，你必须创建所有草稿。
                你的最终答复必须确认所有答复均已起草。
                """
            ),
            expected_output='你的最终答复必须确认所有答复均已起草',
            agent=agent
        )
