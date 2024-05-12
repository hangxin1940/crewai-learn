from crewai_tools import tool


class FileTools:

    @tool("写入文件内容")
    def write_file(data: str):
        """
        用于将具有给定内容的文件写入给定路径。
        该工具的输入应为以`|`分割的两个部分，即文件路径和文件内容。
        例如，`./Keynote/src/components/Hero.jsx|REACT_COMPONENT_CODE_PLACEHOLDER`。
        将 REACT_COMPONENT_CODE_PLACEHOLDER 替换为你要写入文件的实际代码。
        """
        try:
            path, content = data.split("|")
            path = path.replace("\n", "").replace(" ", "").replace("`", "")
            if not path.startswith("./workdir"):
                path = f"./workdir/{path}"

            with open(path, "w") as file:
                file.write(content)
        except Exception as e:
            return "Error with the input format for th tool: " + str(e)
