from textwrap import dedent


class TaskPrompts:

    @classmethod
    def expand(cls) -> str:
        return dedent(
            """
            这是一个好主意！ 通过进行全面的研究来分析和扩展它。

            最终答案必须是一份全面的创意报告，详细说明为什么这是一个好创意、价值主张、独特的卖点、为什么人们应该关心它以及独特的功能。
            
            主意：
            ----------
            {idea}
            """)

    @classmethod
    def refine_idea(cls) -> str:
        return dedent(
            """
            基于创意报告，使用黄金圈法则，通过“为什么”、“怎么做”和“是什么” 传递策略来扩展创意报告。

            你的最终答案必须是更新的完整综合想法报告，其中包含"为什么"、"怎么做"、"是什么"这些核心信息以及关键特征和支持论点。
            
            你必须返回完整的创意报告和详细信息，如果你做得最好，您将获得 100 美元的小费！
            """
        )

    @classmethod
    def choose_template(cls) -> str:
        return dedent(
            """
            了解模板选项，选择并复制最适合以下想法的模板，
            你必须复制，然后您必须读取刚刚复制的目录中的 `src/component` ，以决定应更新哪些组件文件以使登陆页面符合以下想法。
            
            - 选择文件之前你必须浏览目录。
            - 你不得更新任何定价组件。
            - 你必须仅更新 4 个最重要的组件。
            
            你的最终答案必须只是需要更新的组件完整文件路径的 JSON 数组。
            
            主意
            ----------
            {idea}
            """
        )

    @classmethod
    def update_page(cls) -> str:
        return dedent(
            """
            读取 `./[chosen_template]/src/app/page.jsx` 或 `./[chosen_template]/src/app/(main)/page.jsx` （带有括号的 main）以了解其内容，然后编写更新版本 文件系统从返回中删除不在我们列表中的任何与节相关的组件。 保留imports引用。

            最终答案必须只是一个有效的 json 列表，其中包含我们将使用的每个组件的完整路径，与你获取它们的方式相同。
            
            规则
            -----
            - 切勿在文件内容中添加最后一个点。
            - 切勿在文件上写入 \\n（换行符作为字符串），仅写入代码。
            - 切勿忘记关闭文件中的最后一个括号 (}})。
            - 切勿使用非进口组件。
            - 使用的所有组件均应进口，请勿组装组件。
            - 将文件保存为扩展名为“.jsx”的文件。
            - 返回你获得的组件的相同有效 JSON 列表。
            
            如果你遵守所有规则，您将获得 100 美元小费！
            
            还要更新任何必要的文本以反映此登陆页面是关于以下想法的。
            
            主意
            ----------
            {idea}
            """
        )

    @classmethod
    def component_content(cls) -> str:
        return dedent(
            """
            工程师将更新{component}（代码如下），返回一个好的文本选项列表来替换组件上每个单独的现有文本，建议必须基于以下想法，并且长度也必须与原始文本大致相同，我们需要替换所有文本。

            切勿使用撇号进行缩写！ 如果你表现最好，你将获得 100 美元的小费！
            
            主意
            -----
            {expanded_idea}
            
            REACT组件内容
            -----
            {file_content}
            """
        )

    @classmethod
    def update_component(cls) -> str:
        return dedent(
            """
            你必须使用该工具将 React 组件的更新版本写入以下路径中的文件系统： {component} 用提供的建议替换文本内容。

            你只修改文本内容，不添加或删除任何组件。
            
            你首先编写文件，然后你的最终答案必须是更新的组件内容。
            
            规则
            -----
            - 删除所有链接，这应该是单页着陆页面。
            - 不得虚构图像、视频、GIF、图标、徽标等。
            - 保持相同的风格和顺风等级。
            - 必须在代码开头添加`'use client'`
            - 按钮、链接、导航链接和导航中的 href 应为“#”。
            - 切勿在文件上写入 `\\n`（换行符作为字符串），仅写入代码。
            - 切勿忘记关闭文件中的最后一个括号 (}})。
            - 保留相同的组件导入并且不使用新组件。
            - 切勿使用没有import导入的组件。
            - 使用的所有组件均应进口，请勿组装组件。
            - 将文件保存为扩展名为“.jsx”的文件。
            
            如果你遵守规则我会给你100美元的小费！
            我的生活取决于你的遵循！
            
            待更新内容
            -----
            {file_content}
            """
        )

    @classmethod
    def qa_component(cls) -> str:
        return dedent(
            """
            检查 React 组件代码以确保其有效并遵守以下规则，如果没有，则使用写入文件工具将正确的版本写入文件系统，并将其写入以下路径：{component}。
            
            你的最终答案应该是确认该组件有效并遵守规则，以及是否必须将更新版本写入文件系统。
            
            规则
            -----
            - 切勿使用撇号进行缩写！
            - 使用的所有组件均应正确导入。
            - 必须在代码开头添加`'use client'`。
            - 按钮、链接、导航链接和导航中的 href 应为“#”。
            - 切勿在文件上写入 '\\n'（换行符作为字符串），仅写入代码。
            - 切勿忘记关闭文件中的最后一个括号 (}})。
            - 切勿使用没有import导入的组件。
            - 使用的所有组件均应正确导入，请勿组装组件。
            - 始终对组件类使用`export function`。
            
            如果你遵守所有规则，您将获得 100 美元小费！
            """
        )