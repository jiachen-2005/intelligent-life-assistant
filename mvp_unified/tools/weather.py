"""天气查询工具"""
import requests
from typing import Optional


def get_weather(city: str) -> str:
    """
    查询指定城市的天气
    
    参数:
        city: 城市名称（如：北京、上海）
    
    返回:
        天气信息字符串
    """
    # 模拟天气API（实际使用时替换为真实API）
    mock_weather = {
        "北京": {"temperature": "28°C", "condition": "晴", "wind": "东南风2级"},
        "上海": {"temperature": "32°C", "condition": "多云", "wind": "东风3级"},
        "广州": {"temperature": "35°C", "condition": "雷阵雨", "wind": "西南风4级"},
        "深圳": {"temperature": "33°C", "condition": "多云", "wind": "南风2级"},
        "杭州": {"temperature": "30°C", "condition": "阴", "wind": "东北风3级"}
    }
    
    if city in mock_weather:
        info = mock_weather[city]
        return f"{city}天气：{info['condition']}，温度{info['temperature']}，{info['wind']}"
    else:
        return f"暂不支持查询{city}的天气信息"


# LiteLLM 工具定义格式
weather_tool_def = {
    "name": "get_weather",
    "description": "查询指定城市的天气信息",
    "parameters": {
        "type": "object",
        "properties": {
            "city": {
                "type": "string",
                "description": "城市名称，如：北京、上海、广州"
            }
        },
        "required": ["city"]
    }
}