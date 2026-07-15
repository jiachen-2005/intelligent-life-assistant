"""股票查询工具"""
from typing import Optional


def get_stock_price(stock_code: str) -> str:
    """
    查询股票价格
    
    参数:
        stock_code: 股票代码（如：600519 贵州茅台，000858 五粮液）
    
    返回:
        股票价格信息字符串
    """
    # 模拟股票数据（实际使用时替换为真实API）
    mock_stocks = {
        "600519": {"name": "贵州茅台", "price": "1680.50", "change": "+2.35%", "volume": "125万手"},
        "000858": {"name": "五粮液", "price": "145.80", "change": "-1.20%", "volume": "234万手"},
        "000001": {"name": "平安银行", "price": "12.35", "change": "+0.82%", "volume": "567万手"},
        "601318": {"name": "中国平安", "price": "48.60", "change": "-0.55%", "volume": "189万手"},
        "300750": {"name": "宁德时代", "price": "218.90", "change": "+3.45%", "volume": "312万手"}
    }
    
    if stock_code in mock_stocks:
        info = mock_stocks[stock_code]
        return f"{info['name']}（{stock_code}）：现价{info['price']}元，涨跌幅{info['change']}，成交量{info['volume']}"
    else:
        return f"暂不支持查询股票代码{stock_code}的信息"


# LiteLLM 工具定义格式
stock_tool_def = {
    "name": "get_stock_price",
    "description": "查询股票价格信息",
    "parameters": {
        "type": "object",
        "properties": {
            "stock_code": {
                "type": "string",
                "description": "股票代码，如：600519（贵州茅台）、000858（五粮液）"
            }
        },
        "required": ["stock_code"]
    }
}