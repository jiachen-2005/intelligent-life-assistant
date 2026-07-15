"""模型路由规则配置 - 集中管理所有模型和路由策略"""
from typing import Dict, Any

# 模型配置 - 使用 LiteLLM 兼容格式
MODELS = {
    "glm-4.7-flash": {
        "model": "openai/glm-4.7-flash",
        "api_key": "73d2ca9aa9574274ac522bb32caf0e91.pz18OIAB7ecFrkST",
        "api_base": "https://api.z.ai/api/paas/v4",
        "description": "智谱AI GLM-4.7-Flash（推荐，免费）",
        "capabilities": ["general", "tool_use"],
        "priority": 1
    },
    "glm-4-flash": {
        "model": "openai/glm-4-flash",
        "api_key": "your_zhipu_api_key",
        "api_base": "https://open.bigmodel.cn/api/paas/v4",
        "description": "智谱AI GLM-4-Flash（轻量版）",
        "capabilities": ["general"],
        "priority": 2
    },
    "deepseek-chat": {
        "model": "deepseek/deepseek-chat",
        "api_key": "your_deepseek_api_key",
        "api_base": "https://api.deepseek.com/v1",
        "description": "深度求索 DeepSeek",
        "capabilities": ["general"],
        "priority": 3
    },
    "qwen-max": {
        "model": "openai/qwen-max",
        "api_key": "your_aliyun_api_key",
        "api_base": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "description": "阿里云通义千问",
        "capabilities": ["general", "tool_use"],
        "priority": 4
    },
    "gpt-4o-mini": {
        "model": "gpt-4o-mini",
        "api_key": "your_openai_api_key",
        "api_base": None,
        "description": "OpenAI GPT-4o-mini",
        "capabilities": ["general", "tool_use"],
        "priority": 5
    }
}

# 路由策略配置
ROUTING_STRATEGIES = {
    "default": "glm-4.7-flash",

    "intent_based": {
        "weather": "glm-4.7-flash",
        "stock": "glm-4.7-flash",
        "code": "deepseek-chat",
        "math": "gpt-4o-mini",
        "general": "glm-4.7-flash"
    },

    "tool_based": {
        "weather_tool": "glm-4.7-flash",
        "stock_tool": "glm-4.7-flash"
    },

    "capability_based": {
        "tool_use": ["glm-4.7-flash", "qwen-max", "gpt-4o-mini"],
        "general": ["glm-4.7-flash", "glm-4-flash", "deepseek-chat"]
    }
}


def get_model_config(model_name: str) -> Dict[str, Any]:
    return MODELS.get(model_name, {})


def get_routing_strategy(strategy: str = "default") -> Any:
    return ROUTING_STRATEGIES.get(strategy, ROUTING_STRATEGIES["default"])


def get_models_by_capability(capability: str) -> list:
    return [name for name, config in MODELS.items()
            if capability in config.get("capabilities", [])]


def get_best_model(intent: str = None, tool_name: str = None) -> str:
    if tool_name and tool_name in ROUTING_STRATEGIES.get("tool_based", {}):
        return ROUTING_STRATEGIES["tool_based"][tool_name]

    if intent and intent in ROUTING_STRATEGIES.get("intent_based", {}):
        return ROUTING_STRATEGIES["intent_based"][intent]

    return ROUTING_STRATEGIES["default"]