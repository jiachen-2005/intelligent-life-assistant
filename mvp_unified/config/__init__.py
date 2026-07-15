"""配置模块 - 集中导出所有配置"""
from .routing_rules import (
    MODELS,
    ROUTING_STRATEGIES,
    get_model_config,
    get_routing_strategy,
    get_models_by_capability,
    get_best_model
)

__all__ = [
    "MODELS",
    "ROUTING_STRATEGIES",
    "get_model_config",
    "get_routing_strategy",
    "get_models_by_capability",
    "get_best_model"
]