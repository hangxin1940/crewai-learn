import json
import os
from typing import Any

from bs4 import BeautifulSoup
from crewai import Agent, Task
from unstructured.partition.html import partition_html
import requests
from crewai_tools import tool


class BrowserTools:

    @tool("抓取网页内容")
    def scrape_and_summarize_website(url: str, **kwargs: Any) -> str:
        """ 用于抓取和总结网站内容 """
        response = requests.request("GET", url)
        soup = BeautifulSoup(response.text.strip(), 'html.parser')
        content = soup.text
        content = [content[i:i + 8000] for i in range(0, len(content), 8000)]
        summaries = []
        for chunk in content:
            agent = Agent(
                role='首席研究员',
                goal='根据你正在处理的内容进行惊人的研究和总结',
                backstory="你是一家大公司的首席研究员，需要对给定主题进行研究。",
                allow_delegation=False
            )
            task = Task(
                agent=agent,
                description=
                f'分析和总结以下内容，确保在摘要中包含最相关的信息，仅返回摘要而不返回其他内容.\n\n内容\n----------\n{chunk}',
                expected_output='分析和总结内容, 摘要中包含最相关的信息，仅返回摘要而不返回其他内容'
            )
            summary = task.execute()
            summaries.append(summary)
        return "\n\n".join(summaries)

    @tool("抓取网页内容")
    def scrape_and_summarize_website_browserless(url):
        """ 用于抓取和总结网站内容 """
        website = f"https://chrome.browserless.io/content?token={os.environ['BROWSERLESS_API_KEY']}"
        payload = json.dumps({"url": url})
        headers = {'cache-control': 'no-cache', 'content-type': 'application/json'}
        response = requests.request("POST", website, headers=headers, data=payload)
        elements = partition_html(text=response.text)
        content = "\n\n".join([str(el) for el in elements])
        content = [content[i:i + 8000] for i in range(0, len(content), 8000)]
        summaries = []
        for chunk in content:
            agent = Agent(
                role='首席研究员',
                goal='根据你正在处理的内容进行惊人的研究和总结',
                backstory="你是一家大公司的首席研究员，需要对给定主题进行研究。",
                allow_delegation=False
            )
            task = Task(
                agent=agent,
                description=
                f'分析和总结以下内容，确保在摘要中包含最相关的信息，仅返回摘要而不返回其他内容.\n\n内容\n----------\n{chunk}'
            )
            summary = task.execute()
            summaries.append(summary)
        return "\n\n".join(summaries)
