import json
import os

import requests
from bs4 import BeautifulSoup
from crewai import Agent, Task
from crewai_tools import tool
from unstructured.partition.html import partition_html


class BrowserTools:

    @tool("抓取网页内容")
    def scrape_and_summarize_website(website: str):
        """
        用于抓取网页内容并生成摘要。
        """
        response = requests.request("GET", website)
        soup = BeautifulSoup(response.text.strip(), 'html.parser')
        content = soup.text
        content = [content[i:i + 8000] for i in range(0, len(content), 8000)]
        summaries = []
        for chunk in content:
            agent = Agent(
                role="首席研究员",
                goal="根据你正在处理的内容进行惊人的研究和总结",
                backstory="你是一家大公司的首席研究员，你需要对给定主题进行研究。",
                allow_delegation=False,
            )

            task = Task(
                agent=agent,
                description=f"分析和总结以下内容，确保在摘要中包含最相关的信息，仅返回摘要而不返回其他内容。\n\nCONTENT\n----------\n{chunk}"
            )

            summary = task.execute()
            summaries.append(summary)
        return "\n\n".join(summaries)

    @tool("抓取网页内容")
    def scrape_and_summarize_website_browserless(website: str):
        """
        用于抓取网页内容并生成摘要。
        """
        url = f"https://chrome.browserless.io/content?token={os.environ['BROWSERLESS_API_KEY']}"
        payload = json.dumps({"url": website})
        headers = {
            'cache-control': 'no-cache',
            'content-type': 'application/json',
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        elements = partition_html(text=response.text)
        content = "\n\n".join(str(el) for el in elements)
        content = [content[i:i + 8000] for i in range(0, len(content), 8000)]
        summaries = []
        for chunk in content:
            agent = Agent(
                role="首席研究员",
                goal="根据你正在处理的内容进行惊人的研究和总结",
                backstory="你是一家大公司的首席研究员，你需要对给定主题进行研究。",
                allow_delegation=False,
            )

            task = Task(
                agent=agent,
                description=f"分析和总结以下内容，确保在摘要中包含最相关的信息，仅返回摘要而不返回其他内容。\n\nCONTENT\n----------\n{chunk}"
            )

            summary = task.execute()
            summaries.append(summary)
        return "\n\n".join(summaries)
