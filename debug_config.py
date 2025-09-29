#!/usr/bin/env python3
"""
调试配置文件 - 专门用于Docker调试环境
"""

import os

# 调试模式配置
DEBUG_CONFIG = {
    # 模型配置 - 调试优化
    "model": {
        "base_url": "https://api-inference.modelscope.cn/v1",
        "api_key": "ms-74b8eedd-5f76-419a-a513-f421399093da",
        "model_name": "deepseek-ai/DeepSeek-V3.1",
        "temperature": 0.5,  # 调试时使用较低温度，结果更稳定
        "max_tokens": 1500   # 调试时使用较少token，响应更快
    },
    
    # RAG配置 - 调试优化
    "rag": {
        "similarity_top_k": 3,      # 调试时检索较少文档
        "keyword_weight": 0.7,      # 提高关键词权重，更精确
        "exact_match_weight": 0.2,
        "length_bonus_weight": 0.1,
        "min_score_threshold": 0.05  # 降低阈值，更容易找到结果
    }
}

# API配置 - 调试模式
DEBUG_API_CONFIG = {
    "host": "0.0.0.0",
    "port": 8000,
    "cors_origins": ["*"],
    "cors_credentials": True,
    "cors_methods": ["*"],
    "cors_headers": ["*"],
    "debug": True,
    "reload": True  # 代码修改时自动重载
}

# 日志配置 - 详细调试信息
DEBUG_LOGGING_CONFIG = {
    "level": "DEBUG",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s"
}

# 数据库配置 - Docker环境
DEBUG_DB_CONFIG = {
    "mongodb_uri": os.getenv("MONGODB_URI", "mongodb://admin:password@mongodb:27017/nextmile_chatbot?authSource=admin"),
    "database_name": "nextmile_chatbot_debug",
    "collection_name": "conversations_debug"
}

# 调试工具配置
DEBUG_TOOLS_CONFIG = {
    "enable_detailed_logging": True,
    "save_debug_data": True,
    "show_retrieved_docs": True,
    "show_prompt_details": True,
    "measure_performance": True
}