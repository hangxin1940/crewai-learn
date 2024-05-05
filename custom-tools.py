# %%
"""
创建和使用工具
"""
from typing import Any

from crewai_tools import BaseTool, tool

# %%
"""
方式1: 继承 BaseTool 创建自定义工具
"""


# 继承 BaseTool 并定义必要的属性和 _run 方法。
class MyCustomTool(BaseTool):
    name: str = "工具名称"
    description: str = "工具描述。好的描述有助于高效利用工具。"

    def _run(self, argument: str) -> str:
        # 实现工具的核心功能
        return "工具输出"


# %%
"""
方式2: 使用 tool 装饰器自定义工具，
"""


@tool("工具名称")
def my_custom_tool(question: str) -> str:
    """
    工具描述。好的描述有助于高效利用工具。
    """
    # 实现工具的核心功能
    return "工具输出"


# 要通过缓存优化工具性能，需要为函数定义 cache_function 属性

def my_cache_strategy(arguments: dict, result: str) -> bool:
    # 自定义缓存逻辑
    some_condition = True
    return True if some_condition else False


my_custom_tool.cache_function = my_cache_strategy
