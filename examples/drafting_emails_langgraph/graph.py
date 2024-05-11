from langgraph.graph import StateGraph

from crew.crew import EmailFilterCrew
from state import EmailsState
from nodes import Nodes


class WorkFlow:
    def __init__(self):
        nodes = Nodes()
        workflow = StateGraph(EmailsState)

        # 共三个节点, 分别是检查新邮件, 等待下一次运行, 起草回复
        workflow.add_node("check_new_emails", nodes.check_email)
        workflow.add_node("wait_next_run", nodes.wait_next_run)
        workflow.add_node("draft_responses", EmailFilterCrew().kickoff)

        # 设置入口节点, 首先应当检查新邮件
        workflow.set_entry_point("check_new_emails")

        # 添加条件边, 如果有新邮件则进入起草回复节点, 否则进入等待下一次运行节点
        workflow.add_conditional_edges(
            source="check_new_emails",
            path=nodes.new_emails,  # 条件函数
            path_map={
                "continue": "draft_responses",  # 映射路径: 起草回复
                "end": "wait_next_run"  # 映射路径 : 等待下一次运行
            }
        )

        # 添加普通边: 起草回复 -> 等待下一次运行 -> 检查新邮件
        workflow.add_edge('draft_responses', 'wait_next_run')
        # 添加普通边: 等待下一次运行 -> 检查新邮件
        workflow.add_edge('wait_next_run', 'check_new_emails')

        # 编译工作流
        self.app = workflow.compile()
