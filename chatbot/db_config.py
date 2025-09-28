import os
from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
import uuid

class MongoDBHandler:
    def __init__(self):
        # MongoDB连接字符串，建议使用环境变量
        self.connection_string = os.getenv(
            'MONGODB_URI', 
            'mongodb://localhost:27017/'
        )
        self.database_name = os.getenv('DB_NAME', 'nextmile_chatbot')
        self.collection_name = 'conversations'
        
        # 同步客户端
        self.client = MongoClient(self.connection_string)
        self.db = self.client[self.database_name]
        self.collection = self.db[self.collection_name]
        
        # 异步客户端
        self.async_client = AsyncIOMotorClient(self.connection_string)
        self.async_db = self.async_client[self.database_name]
        self.async_collection = self.async_db[self.collection_name]
    
    def save_conversation(self, user_query: str, bot_response: str, 
                         session_id: str = None, user_id: str = None,
                         response_time: float = None, model_used: str = None):
        """保存对话记录到MongoDB"""
        conversation_data = {
            "timestamp": datetime.utcnow(),
            "user_query": user_query,
            "bot_response": bot_response,
            "session_id": session_id or str(uuid.uuid4()),
            "user_id": user_id,
            "metadata": {
                "response_time": response_time,
                "model_used": model_used or "default",
                "confidence": None  # 可以后续添加
            }
        }
        
        try:
            result = self.collection.insert_one(conversation_data)
            return str(result.inserted_id)
        except Exception as e:
            print(f"Error saving conversation: {e}")
            return None
    
    async def save_conversation_async(self, user_query: str, bot_response: str,
                                    session_id: str = None, user_id: str = None,
                                    response_time: float = None, model_used: str = None):
        """异步保存对话记录"""
        conversation_data = {
            "timestamp": datetime.utcnow(),
            "user_query": user_query,
            "bot_response": bot_response,
            "session_id": session_id or str(uuid.uuid4()),
            "user_id": user_id,
            "metadata": {
                "response_time": response_time,
                "model_used": model_used or "default",
                "confidence": None
            }
        }
        
        try:
            result = await self.async_collection.insert_one(conversation_data)
            return str(result.inserted_id)
        except Exception as e:
            print(f"Error saving conversation: {e}")
            return None
    
    def get_conversation_history(self, session_id: str, limit: int = 10):
        """获取对话历史"""
        try:
            conversations = self.collection.find(
                {"session_id": session_id}
            ).sort("timestamp", -1).limit(limit)
            return list(conversations)
        except Exception as e:
            print(f"Error fetching conversation history: {e}")
            return []
    
    def close_connection(self):
        """关闭数据库连接"""
        self.client.close()
        self.async_client.close()

# 全局数据库处理器实例
db_handler = MongoDBHandler()