import os

from config import PROXY_SOCKS, OPENAI_KEY
from graph import WorkFlow

if __name__ == "__main__":
    os.environ['http_proxy'] = PROXY_SOCKS
    os.environ['HTTP_PROXY'] = PROXY_SOCKS
    os.environ['https_proxy'] = PROXY_SOCKS
    os.environ['HTTPS_PROXY'] = PROXY_SOCKS

    os.environ["OPENAI_API_KEY"] = OPENAI_KEY
    os.environ["OPENAI_MODEL_NAME"] = "gpt-3.5-turbo"

    os.environ["TAVILY_API_KEY"] = "xxxx"
    os.environ["MY_EMAIL"] = "aaaa@aaa.com"

    app = WorkFlow().app
    app.invoke({})
