import json
import shutil
from pathlib import Path

from crewai_tools import tool


class TemplateTools:

    @tool("了解着陆页选项")
    def learn_landing_page_options(input: str):
        """了解可以使用的模板"""
        templates = json.load(open("config/templates.json"))
        return json.dumps(templates, indent=2)

    @tool("将登陆页面模板复制到项目文件夹")
    def copy_landing_page_template_to_project_folder(landing_page_template: str):
        """
        将着陆页模板复制到你的项目文件夹，以便你可以开始修改它，它需要着陆页模板文件夹作为输入
        """
        source_path = Path(f"templates/{landing_page_template}")
        destination_path = Path(f"workdir/{landing_page_template}")
        destination_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(source_path, destination_path)
        return f"模板已复制到 {landing_page_template} 并准备修改，主要文件应位于 ./{landing_page_template}/src/components 下，你应该重点关注这些文件。"
