from crewai_tools import tool


class CalculatorTools:

    @tool("数学计算器")
    def calculate(operation: str) -> str:
        """
        对于执行任何数学计算很有用，如加、减、乘、除等
        该工具的输入应该是数学表达式，如“200*7”或“5000/2*10”
        """
        try:
            # TODO 此处会有安全隐患,不建议使用 `eval`
            return eval(operation)
        except SyntaxError:
            return "Error: Invalid syntax in mathematical expression"
