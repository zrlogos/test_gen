from openai import OpenAI
from typing import List, Dict, Optional, Union
from config import Config


class LLMChat:
    """统一的大语言模型聊天客户端"""

    # 支持的模型配置
    MODEL_CONFIGS = {
        "deepseek-chat": {
            "base_url": "https://api.deepseek.com/v1",
            "max_tokens": 8192,
            "default_temperature": 0.7
        },
        "deepseek-reasoner": {
            "base_url": "https://api.deepseek.com/v1",
            "max_tokens": 8192,
            "default_temperature": 0.7
        },
        "gpt-3.5-turbo": {
            "base_url": "https://api.openai.com/v1",
            "max_tokens": 4096,
            "default_temperature": 0.7
        },
        "gpt-4": {
            "base_url": "https://api.openai.com/v1",
            "max_tokens": 8192,
            "default_temperature": 0.7
        }
    }

    def __init__(
            self,
            model: str = "deepseek-chat",
            api_key: Optional[str] = None,
            base_url: Optional[str] = None,
            system_prompt: Optional[str] = None
    ):
        """初始化 LLMChat 实例
        
        Args:
            model: 模型名称
            api_key: API密钥，如果不提供则从Config获取
            base_url: API基础URL，如果不提供则使用模型默认值
            system_prompt: 系统提示词
        """
        self.model = model
        if model not in self.MODEL_CONFIGS:
            raise ValueError(f"不支持的模型: {model}")

        self.model_config = self.MODEL_CONFIGS[model]

        # 确定API密钥
        if api_key is None:
            if "deepseek" in model.lower():
                api_key = Config.DEEPSEEK_API_KEY
            else:
                api_key = Config.OPENAI_API_KEY

        # 确定base_url
        if base_url is None:
            base_url = self.model_config["base_url"]

        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.conversation_history: List[Dict[str, str]] = []

        if system_prompt:
            self.conversation_history.append({
                "role": "system",
                "content": system_prompt
            })

    def chat(
            self,
            message: str,
            temperature: Optional[float] = None,
            max_tokens: Optional[int] = None,
            stream: bool = False,
            response_format: Optional[Dict] = None,
            force_json: bool = False
    ) -> Union[str, dict]:
        """发送消息并获取回复
        
        Args:
            message: 用户输入的消息
            temperature: 温度参数(0-1)
            max_tokens: 最大生成token数
            stream: 是否使用流式输出
            response_format: 返回格式，例如 {'type': 'json_object'}
            force_json: 是否强制返回JSON格式

        Returns:
            助手的回复消息
        """
        if force_json:
            message = f"{message}\n\n请直接返回JSON格式数据，不要包含任何markdown代码块标记。"
            if not response_format:
                response_format = {"type": "json_object"}

        self.conversation_history.append({
            "role": "user",
            "content": message
        })

        kwargs = {
            "model": self.model,
            "messages": self.conversation_history,
            "max_tokens": max_tokens or self.model_config["max_tokens"],
            "temperature": temperature or self.model_config["default_temperature"],
            "stream": stream
        }

        if response_format:
            kwargs["response_format"] = response_format

        try:
            response = self.client.chat.completions.create(**kwargs)

            if stream:
                return response

            assistant_message = response.choices[0].message.content
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })

            return assistant_message

        except Exception as e:
            print(f"调用模型 {self.model} 时出错: {str(e)}")
            raise

    def clear_history(self):
        """清除对话历史"""
        system_message = None
        if self.conversation_history and self.conversation_history[0]["role"] == "system":
            system_message = self.conversation_history[0]

        self.conversation_history.clear()

        if system_message:
            self.conversation_history.append(system_message)

    @property
    def history(self) -> List[Dict[str, str]]:
        """获取对话历史"""
        return self.conversation_history

    @classmethod
    def list_models(cls) -> List[str]:
        """获取支持的模型列表"""
        return list(cls.MODEL_CONFIGS.keys())

    @classmethod
    def get_model_config(cls, model: str) -> Dict:
        """获取指定模型的配置信息"""
        return cls.MODEL_CONFIGS.get(model, {})

    def analyze_code(
            self,
            file_path: str,
            prompt_template: Optional[str] = None,
            **kwargs
    ) -> str:
        """分析代码文件内容
        
        Args:
            file_path: 代码文件路径
            prompt_template: 提示词模板，可包含 {code} 占位符
            **kwargs: 传递给 chat 方法的其他参数
        
        Returns:
            模型的分析响应
        """
        try:
            # 读取代码文件
            with open(file_path, 'r', encoding='utf-8') as f:
                code_content = f.read()
            
            # 如果没有提供提示词模板，使用默认模板
            if prompt_template is None:
                prompt_template = """
请分析以下代码并提供反馈：

```
{code}
```
"""

            # 构建完整的提示词
            prompt = prompt_template.format(code=code_content)

            # 调用 chat 方法进行分析
            response = self.chat(
                prompt,
                temperature=0.7,
                max_tokens=8192,
                stream=False,
                response_format={"type": "json_object"},
                force_json=True
            )

            return response

        except Exception as e:
            print(f"分析代码文件时出错: {str(e)}")
            raise


# 使用示例
if __name__ == "__main__":
    # 使用 Deepseek 模型
    deepseek_chat = LLMChat(
        model="deepseek-chat",
        system_prompt="你是一个有帮助的AI助手。"
    )
    print("Deepseek回复:", deepseek_chat.chat("你好，请介绍一下你自己"))
