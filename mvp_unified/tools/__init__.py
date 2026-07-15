"""工具模块 - 集中导出所有工具"""
from .weather import get_weather, weather_tool_def
from .stock import get_stock_price, stock_tool_def

# 工具映射表
TOOL_MAP = {
    "get_weather": get_weather,
    "get_stock_price": get_stock_price
}

# 工具定义列表（用于LiteLLM函数调用）
TOOL_DEFS = [
    weather_tool_def,
    stock_tool_def
]

__all__ = ["TOOL_MAP", "TOOL_DEFS", "get_weather", "get_stock_price"]