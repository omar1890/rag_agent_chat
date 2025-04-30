import math
from langchain.tools import Tool

def safe_eval(expr):
    try:
        # Limit available functions
        allowed = {"sqrt": math.sqrt, "pow": math.pow, "abs": abs}
        return str(eval(expr, {"__builtins__": None}, allowed))
    except Exception as e:
        return f"Error: {str(e)}"

def get_calculator_tool():
    return Tool(
        name="Calculator",
        description="Useful for solving simple math problems. Input should be a valid math expression.",
        func=safe_eval
    )
