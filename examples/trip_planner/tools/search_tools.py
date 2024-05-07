import json
import os
from typing import Any
import serpapi

from crewai_tools import tool


class SearchTools:

    @tool("搜索工具")
    def search_internet(question: str, **kwargs: Any) -> str:
        """
        网上搜索很有用, 给定主题并返回相关结果
        """

        client = serpapi.Client(api_key=os.environ['SERPER_API_KEY'])
        results = client.search({
            'engine': 'baidu',
            'q': question,
        })
        top_result_to_return = 4  # 只需要前4个结果即可

        string = []
        for result in results.data['organic_results'][:top_result_to_return]:
            try:
                string.append('\n'.join([
                    f"标题: {result['title']}", f"链接: {result['link']}",
                    f"摘要: {result['snippet']}", "\n-----------------"
                ]))
            except KeyError:
                next

        return '\n'.join(string)
