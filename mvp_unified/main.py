"""MVP统一入口 - 路由策略 + LiteLLM调用 + 工具执行"""
import json
from typing import List, Dict, Any
from litellm import completion

# 导入配置和工具
from config import (
    MODELS, 
    get_model_config, 
    get_best_model, 
    get_models_by_capability
)
from tools import TOOL_MAP, TOOL_DEFS


class MVPAgent:
    def __init__(self, model_name: str = None):
        """
        初始化Agent
        
        参数:
            model_name: 模型名称，若为None则使用默认模型
        """
        self.current_model_name = model_name or "glm-4.5-flash"
        self.messages: List[Dict[str, Any]] = []
        self._init_system_message()
    
    def _init_system_message(self):
        """初始化系统消息"""
        system_prompt = """你是一个智能生活助理，具备工具调用能力。请根据用户需求：
1. 如果需要查询天气或股票，调用相应工具
2. 如果不需要工具，直接回答用户
3. 工具调用必须使用JSON格式输出

可用工具：
- get_weather: 查询天气
- get_stock_price: 查询股票价格

输出格式：
{"action": "tool_call", "tool_name": "工具名", "params": {"参数": "值"}}
或
{"action": "final_answer", "content": "自然语言回答"}
"""
        self.messages.append({"role": "system", "content": system_prompt})
    
    def _call_llm(self, model_name: str) -> str:
        """
        调用LiteLLM
        
        参数:
            model_name: 模型名称
        
        返回:
            LLM响应内容
        """
        model_config = get_model_config(model_name)
        if not model_config:
            raise ValueError(f"未知模型: {model_name}")
        
        response = completion(
            model=model_config["model"],
            api_key=model_config["api_key"],
            messages=self.messages,
            tools=TOOL_DEFS,
            max_tokens=512,
            temperature=0.7
        )
        
        return response.choices[0].message.content
    
    def _execute_tool(self, tool_name: str, params: Dict[str, Any]) -> str:
        """
        执行工具
        
        参数:
            tool_name: 工具名称
            params: 工具参数
        
        返回:
            工具执行结果
        """
        if tool_name in TOOL_MAP:
            try:
                return TOOL_MAP[tool_name](**params)
            except Exception as e:
                return f"工具执行失败: {str(e)}"
        else:
            return f"未知工具: {tool_name}"
    
    def _route_model(self, user_query: str) -> str:
        """
        路由策略：根据用户查询选择最佳模型
        
        参数:
            user_query: 用户查询
        
        返回:
            模型名称
        """
        # 简单的意图识别（可扩展为更复杂的NLP模型）
        query_lower = user_query.lower()
        
        if "天气" in query_lower:
            return get_best_model(intent="weather")
        elif "股票" in query_lower or "股价" in query_lower:
            return get_best_model(intent="stock")
        elif "代码" in query_lower or "编程" in query_lower:
            return get_best_model(intent="code")
        elif "数学" in query_lower or "计算" in query_lower:
            return get_best_model(intent="math")
        else:
            return get_best_model(intent="general")
    
    def run(self, user_query: str) -> str:
        """
        运行Agent主循环
        
        参数:
            user_query: 用户查询
        
        返回:
            Agent响应
        """
        # 路由选择模型
        model_name = self._route_model(user_query)
        self.current_model_name = model_name
        
        # 添加用户消息
        self.messages.append({"role": "user", "content": user_query})
        
        try:
            # 调用LLM
            content = self._call_llm(model_name)
            content = content.replace("```json", "").replace("```", "").strip()
            
            # 解析响应
            action_data = json.loads(content)
            
            if action_data["action"] == "tool_call":
                # 执行工具
                result = self._execute_tool(
                    action_data["tool_name"], 
                    action_data["params"]
                )
                self.messages.append({"role": "assistant", "content": content})
                self.messages.append({"role": "user", "content": f"工具执行结果: {result}"})
                return result
            
            elif action_data["action"] == "final_answer":
                final_content = action_data.get("content", "未知响应")
                self.messages.append({"role": "assistant", "content": content})
                return final_content
            
            else:
                return f"未知动作: {action_data.get('action')}"
        
        except json.JSONDecodeError:
            # LLM直接返回自然语言
            self.messages.append({"role": "assistant", "content": content})
            return content
        
        except Exception as e:
            return f"【错误】{str(e)}"
    
    def switch_model(self, model_name: str) -> str:
        """
        切换模型
        
        参数:
            model_name: 模型名称
        
        返回:
            切换结果
        """
        if model_name in MODELS:
            self.current_model_name = model_name
            self.messages = self.messages[:1]  # 清空对话历史
            return f"已切换到模型: {model_name} - {MODELS[model_name]['description']}"
        else:
            return f"未知模型: {model_name}。可用模型: {', '.join(MODELS.keys())}"
    
    def get_current_model_info(self) -> str:
        """获取当前模型信息"""
        model_config = MODELS.get(self.current_model_name)
        if model_config:
            return f"当前模型: {self.current_model_name} - {model_config['description']}"
        return f"当前模型: {self.current_model_name}"
    
    def clear_history(self):
        """清空对话历史"""
        self.messages = self.messages[:1]


def main():
    """主交互循环"""
    agent = MVPAgent()
    print("=== MVP Unified Agent（多模型支持）===")
    print(agent.get_current_model_info())
    print("命令列表:")
    print("  /model          - 查看可用模型")
    print("  /model <名称>   - 切换模型")
    print("  /clear          - 清空对话历史")
    print("  /exit /quit     - 退出")
    print("-" * 60)
    
    while True:
        try:
            user_input = input("\n你: ").strip()
            
            if user_input.lower() in ["exit", "quit", "/exit", "/quit"]:
                print("再见！")
                break
            
            if user_input.lower() == "/clear":
                agent.clear_history()
                print("对话历史已清空")
                continue
            
            if user_input.lower() == "/model":
                print("\n可用模型列表:")
                for name, config in MODELS.items():
                    status = "✓" if name == agent.current_model_name else " "
                    print(f"  [{status}] {name}: {config['description']}")
                print(f"\n当前模型: {agent.current_model_name}")
                continue
            
            if user_input.lower().startswith("/model "):
                model_name = user_input[7:].strip()
                response = agent.switch_model(model_name)
                print(f"助手: {response}")
                continue
            
            if not user_input:
                continue
            
            response = agent.run(user_input)
            print(f"助手: {response}")
            
        except KeyboardInterrupt:
            print("\n再见！")
            break


if __name__ == "__main__":
    main()