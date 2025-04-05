class Config:
    DEEPSEEK_API_KEY = "sk-34f4377b70d8412589f6391bae5563e1"
    OPENAI_API_KEY = "sk-prJmnX9deNJ9xX1cXTpgEDc2YOUhcxoFAS8fFSVyxxAvVhZA"
    YUNWU_BASE_URL = "https://yunwu.ai/v1"

    # 支持的模型配置
    MODEL_CONFIGS = {
        "deepseek-chat": {
            "base_url": "https://api.deepseek.com/v1",
            "max_tokens": 8192,
            "default_temperature": 0.7,
            "api_key": DEEPSEEK_API_KEY
        },
        "deepseek-reasoner": {
            "base_url": "https://api.deepseek.com/v1",
            "max_tokens": 8192,
            "default_temperature": 0.7,
            "api_key": DEEPSEEK_API_KEY
        },
        "gpt-4o-mini": {
            "base_url": YUNWU_BASE_URL,
            "max_tokens": 4096,
            "default_temperature": 0.7,
            "api_key": OPENAI_API_KEY
        },
        "o3-mini": {
            "base_url": YUNWU_BASE_URL,
            "max_tokens": 4019,
            "default_temperature": 0.7,
            "api_key": OPENAI_API_KEY
        },
        "o1": {
            "base_url": YUNWU_BASE_URL,
            "max_tokens": 4019,
            "default_temperature": 0.7,
            "api_key": OPENAI_API_KEY
        }
    }

