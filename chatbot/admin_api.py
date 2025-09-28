from db_config import db_handler
from fastapi import APIRouter, HTTPException
from typing import Optional
from datetime import datetime, timedelta
import json

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/conversations")
async def get_all_conversations(limit: int = 50, skip: int = 0):
    """获取所有对话记录"""
    try:
        conversations = list(
            db_handler.collection.find()
            .skip(skip)
            .limit(limit)
            .sort("timestamp", -1)
        )
        # 转换ObjectId为字符串
        for conv in conversations:
            conv["_id"] = str(conv["_id"])
        return {"conversations": conversations, "total": len(conversations)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/conversations/{conversation_id}")
async def get_conversation_by_id(conversation_id: str):
    """根据ID获取特定对话"""
    try:
        from bson import ObjectId
        conversation = db_handler.collection.find_one({"_id": ObjectId(conversation_id)})
        if conversation:
            conversation["_id"] = str(conversation["_id"])
            return conversation
        raise HTTPException(status_code=404, detail="Conversation not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stats")
async def get_database_stats():
    """获取数据库统计信息"""
    try:
        total_conversations = db_handler.collection.count_documents({})
        recent_conversations = db_handler.collection.count_documents({
            "timestamp": {"$gte": datetime.utcnow() - timedelta(days=7)}
        })
        
        # 获取平均响应时间
        pipeline = [
            {"$match": {"metadata.response_time": {"$exists": True}}},
            {"$group": {
                "_id": None,
                "avg_response_time": {"$avg": "$metadata.response_time"},
                "max_response_time": {"$max": "$metadata.response_time"},
                "min_response_time": {"$min": "$metadata.response_time"}
            }}
        ]
        
        response_stats = list(db_handler.collection.aggregate(pipeline))
        
        return {
            "total_conversations": total_conversations,
            "recent_conversations": recent_conversations,
            "response_time_stats": response_stats[0] if response_stats else None
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/conversations/{conversation_id}")
async def delete_conversation(conversation_id: str):
    """删除特定对话"""
    try:
        from bson import ObjectId
        result = db_handler.collection.delete_one({"_id": ObjectId(conversation_id)})
        if result.deleted_count:
            return {"message": "Conversation deleted successfully"}
        raise HTTPException(status_code=404, detail="Conversation not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/export")
async def export_conversations(format: str = "json"):
    """导出所有对话数据"""
    try:
        conversations = list(db_handler.collection.find())
        for conv in conversations:
            conv["_id"] = str(conv["_id"])
            conv["timestamp"] = conv["timestamp"].isoformat()
        
        if format == "json":
            return {"data": conversations}
        elif format == "csv":
            # 可以添加CSV导出逻辑
            pass
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))