from datetime import datetime
from typing import Optional

# 数据模型结构
conversation_schema = {
    "_id": "ObjectId",  # MongoDB自动生成
    "timestamp": "datetime",  # 对话时间
    "user_query": "string",   # 用户查询
    "bot_response": "string", # 模型响应
    "session_id": "string",   # 会话ID（可选，用于关联多轮对话）
    "user_id": "string",      # 用户ID（可选）
    "metadata": {
        "response_time": "float",  # 响应时间（秒）
        "model_used": "string",    # 使用的模型名称
        "confidence": "float"      # 响应置信度（可选）
    }
}