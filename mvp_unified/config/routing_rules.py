"""模型路由规则配置 - 集中管理所有模型和路由策略"""
from typing import Dict, Any

# 模型配置 - 使用 LiteLLM 兼容格式
MODELS = {
    "glm-4.5-flash": {
        "model": "zhipu/glm-4.5-flash",
        "api_key": "your_zhipu_api_key",
        "description": "智谱AI GLM-4.5-Flash（推荐，响应快）",
        "capabilities": ["general", "tool_use"],
        "priority": 1
    },
    "glm-4-flash": {
        "model": "zhipu/glm-4-flash",
        "api_key": "your_zhipu_api_key",
        "description": "智谱AI GLM-4-Flash（轻量版）",
        "capabilities": ["general"],
        "priority": 2
    },
    "deepseek-chat": {
        "model": "deepseek/deepseek-chat",
        "api_key": "your_deepseek_api_key",
        "description": "深度求索 DeepSeek",
        "capabilities": ["general"],
        "priority": 3
    },
    "qwen-max": {
        "model": "qwen/qwen-max",
        "api_key": "your_aliyun_api_key",
        "description": "阿里云通义千问",
        "capabilities": ["general", "tool_use"],
        "priority": 4
    },
    "gpt-4o-mini": {
        "model": "gpt-4o-mini",
        "api_key": "your_openai_api_key",
        "description": "OpenAI GPT-4o-mini",
        "capabilities": ["general", "tool_use"],
        "priority": 5
    }
}

# 路由策略配置
ROUTING_STRATEGIES = {
    "default": "glm-4.5-flash",  # 默认模型
    
    # 按用户意图路由
    "intent_based": {
        "weather": "glm-4.5-flash",      # 天气查询
        "stock": "glm-4.5-flash",        # 股票查询
        "code": "deepseek-chat",         # 代码生成
        "math": "gpt-4o-mini",           # 数学推理
        "general": "glm-4.5-flash"       # 通用对话
    },
    
    # 按工具类型路由
    "tool_based": {
        "weather_tool": "glm-4.5-flash",
        "stock_tool": "glm-4.5-flash"
    },
    
    # 按模型能力路由
    "capability_based": {
        "tool_use": ["glm-4.5-flash", "qwen-max", "gpt-4o-mini"],
        "general": ["glm-4.5-flash", "glm-4-flash", "deepseek-chat"]
    }
}


def get_model_config(model_name: str) -> Dict[str, Any]:
    """获取模型配置"""
    return MODELS.get(model_name, {})


def get_routing_strategy(strategy: str = "default") -> Any:
    """获取路由策略"""
    return ROUTING_STRATEGIES.get(strategy, ROUTING_STRATEGIES["default"])


def get_models_by_capability(capability: str) -> list:
    """按能力获取可用模型列表"""
    return [name for name, config in MODELS.items() 
            if capability in config.get("capabilities", [])]


def get_best_model(intent: str = None, tool_name: str = None) -> str:
    """根据意图或工具选择最佳模型"""
    # 优先按工具路由
    if tool_name and tool_name in ROUTING_STRATEGIES.get("tool_based", {}):
        return ROUTING_STRATEGIES["tool_based"][tool_name]
    
    # 按意图路由
    if intent and intent in ROUTING_STRATEGIES.get("intent_based", {}):
        return ROUTING_STRATEGIES["intent_based"][intent]
    
    # 默认模型
    return ROUTING_STRATEGIES["default"]