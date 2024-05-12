import json
import os

import requests
from crewai_tools import tool
import serpapi


class SearchTools:

    @tool("搜索互联网")
    def search_internet(query: str):
        """用于在互联网上搜索给定主题并返回相关结果"""
        client = serpapi.Client(api_key=os.environ['SERPER_API_KEY'])
        results = client.search({
            'engine': 'baidu',
            'q': query,
        })
        string = []
        for result in results.data['organic_results']:
            string.append(
                '\n'.join(
                    [
                        f"Title: {result['title']}",
                        f"Link: {result['link']}",
                        f"Snippet: {result['snippet']}",
                        "\n-------------"
                    ]
                )
            )
        return "\n".join(string)
