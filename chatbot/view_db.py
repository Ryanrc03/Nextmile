#!/usr/bin/env python3
from db_config import db_handler
from datetime import datetime, timedelta
import json

def view_recent_conversations(limit=10):
    """查看最近的对话"""
    print(f"\n=== 最近 {limit} 条对话 ===")
    conversations = list(
        db_handler.collection.find()
        .sort("timestamp", -1)
        .limit(limit)
    )
    
    for i, conv in enumerate(conversations, 1):
        print(f"\n{i}. 时间: {conv['timestamp']}")
        print(f"   查询: {conv['user_query'][:100]}...")
        print(f"   响应: {conv['bot_response'][:100]}...")
        print(f"   响应时间: {conv['metadata'].get('response_time', 'N/A')}秒")

def view_stats():
    """查看统计信息"""
    total = db_handler.collection.count_documents({})
    today = db_handler.collection.count_documents({
        "timestamp": {"$gte": datetime.utcnow().replace(hour=0, minute=0, second=0)}
    })
    
    print(f"\n=== 数据库统计 ===")
    print(f"总对话数: {total}")
    print(f"今日对话数: {today}")

if __name__ == "__main__":
    view_stats()
    view_recent_conversations()
    db_handler.close_connection()