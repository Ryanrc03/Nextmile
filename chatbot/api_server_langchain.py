#!/usr/bin/env python3
"""
新的 API 服务器 - 集成 LangChain RAG 系统
基于原有 API 结构，使用新开发的 LangChain RAG 算法
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import time
import uuid
import logging

# 导入 LangChain RAG 适配器
from rag_langchain import LangChainRAGAdapter
from config import API_CONFIG
from db_config import db_handler

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI 应用初始化
app = FastAPI(
    title="Nextmile Resume RAG Chatbot API (LangChain)",
    description="基于 LangChain 的智能简历问答系统API",
    version="3.0.0"
)

# 添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=API_CONFIG["cors_origins"],
    allow_credentials=API_CONFIG["cors_credentials"],
    allow_methods=API_CONFIG["cors_methods"],
    allow_headers=API_CONFIG["cors_headers"],
)

# Pydantic 模型定义
class Message(BaseModel):
    text: str
    session_id: Optional[str] = None
    user_id: Optional[str] = None

class ChatResponse(BaseModel):
    reply: str
    session_id: str
    conversation_id: Optional[str] = None
    response_time: float
    retrieved_count: int
    success: bool

class HealthResponse(BaseModel):
    status: str
    database: str
    timestamp: float
    rag_system: str
    system_info: dict

class HistoryResponse(BaseModel):
    session_id: str
    history: list
    count: int

# 初始化 LangChain RAG 系统
logger.info("正在初始化 LangChain RAG 系统...")
try:
    rag_system = LangChainRAGAdapter()
    logger.info("LangChain RAG 系统初始化成功")
except Exception as e:
    logger.error(f"LangChain RAG 系统初始化失败: {e}")
    rag_system = None

# 包含管理 API 路由
try:
    from admin_api import router as admin_router
    app.include_router(admin_router)
    logger.info("管理API路由加载成功")
except ImportError as e:
    logger.warning(f"无法加载管理API路由: {e}")

@app.get("/")
async def root():
    """
    根端点 - API 欢迎信息
    """
    return {
        "message": "欢迎使用 Nextmile Resume RAG Chatbot API (LangChain Edition)",
        "version": "3.0.0",
        "description": "基于 LangChain 的智能简历问答系统",
        "rag_system": "LangChain + ChromaDB + sentence-transformers",
        "llm": "DeepSeek-V3.1",
        "endpoints": {
            "chat": "POST /chat - 发送消息给聊天机器人",
            "history": "GET /history/{session_id} - 获取对话历史",
            "health": "GET /health - 检查API健康状态",
            "admin": "GET /admin/* - 管理功能 (需要权限)"
        },
        "features": [
            "基于 LangChain 的 RAG 架构",
            "ChromaDB 向量存储",
            "sentence-transformers 嵌入",
            "对话记忆管理",
            "实时健康监控"
        ]
    }

@app.get("/health", response_model=HealthResponse)
async def health():
    """
    健康检查端点
    """
    # 检查数据库连接
    try:
        db_status = "connected" if db_handler.client.admin.command('ping') else "disconnected"
    except Exception as e:
        logger.error(f"数据库连接检查失败: {e}")
        db_status = "disconnected"
    
    # 检查 RAG 系统状态
    rag_status = "healthy" if rag_system is not None else "unavailable"
    
    # 获取系统信息
    system_info = {}
    if rag_system is not None:
        try:
            system_info = rag_system.get_summary()
        except Exception as e:
            logger.error(f"获取系统信息失败: {e}")
            system_info = {"error": str(e)}
    
    # 整体状态
    overall_status = "healthy" if db_status == "connected" and rag_status == "healthy" else "degraded"
    
    return HealthResponse(
        status=overall_status,
        database=db_status,
        timestamp=time.time(),
        rag_system=rag_status,
        system_info=system_info
    )

@app.get("/history/{session_id}", response_model=HistoryResponse)
async def get_conversation_history(session_id: str, limit: int = 10):
    """
    获取指定会话的对话历史
    
    Args:
        session_id: 会话ID
        limit: 返回的历史记录数量限制
    """
    try:
        history = db_handler.get_conversation_history(session_id, limit)
        
        # 转换 ObjectId 为字符串以便 JSON 序列化
        for conv in history:
            conv["_id"] = str(conv["_id"])
            conv["timestamp"] = conv["timestamp"].isoformat()
        
        return HistoryResponse(
            session_id=session_id,
            history=history,
            count=len(history)
        )
    except Exception as e:
        logger.error(f"获取对话历史失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取对话历史失败: {str(e)}")

@app.post("/chat", response_model=ChatResponse)
async def chat(message: Message):
    """
    聊天端点 - 核心 RAG 问答功能
    
    Args:
        message: 包含用户消息和元数据的请求体
        
    Returns:
        聊天响应，包含 AI 回答和相关元数据
    """
    # 检查 RAG 系统是否可用
    if rag_system is None:
        raise HTTPException(
            status_code=503, 
            detail="RAG系统不可用，请联系管理员"
        )
    
    start_time = time.time()
    session_id = message.session_id or str(uuid.uuid4())
    
    try:
        logger.info(f"处理聊天请求: session_id={session_id}, query='{message.text[:50]}...'")
        
        # 使用 LangChain RAG 系统处理查询
        rag_result = rag_system.query(message.text, stream=False, top_k=5)
        
        if not rag_result['success']:
            logger.error(f"RAG查询失败: {rag_result.get('error', 'Unknown error')}")
            raise HTTPException(
                status_code=500,
                detail=f"查询处理失败: {rag_result.get('error', 'Unknown error')}"
            )
        
        # 计算总响应时间
        total_response_time = time.time() - start_time
        
        # 保存对话到 MongoDB
        conversation_id = None
        try:
            conversation_id = await db_handler.save_conversation_async(
                user_query=message.text,
                bot_response=rag_result['answer'],
                session_id=session_id,
                user_id=message.user_id,
                response_time=total_response_time,
                model_used="langchain"
            )
            logger.info(f"对话已保存: conversation_id={conversation_id}")
        except Exception as e:
            logger.warning(f"保存对话到数据库失败: {e}")
        
        # 返回响应
        return ChatResponse(
            reply=rag_result['answer'],
            session_id=session_id,
            conversation_id=str(conversation_id) if conversation_id else None,
            response_time=total_response_time,
            retrieved_count=rag_result['retrieved_count'],
            success=True
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"处理聊天请求时发生错误: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"处理请求时发生错误: {str(e)}"
        )

@app.post("/clear_history/{session_id}")
async def clear_session_history(session_id: str):
    """
    清除指定会话的对话历史
    
    Args:
        session_id: 会话ID
    """
    try:
        # 清除 RAG 系统的内存
        if rag_system is not None:
            rag_system.clear_history()
        
        # 清除数据库中的历史
        # TODO: 实现数据库历史清除逻辑
        
        return {
            "success": True,
            "message": f"会话 {session_id} 的历史已清除",
            "session_id": session_id
        }
    except Exception as e:
        logger.error(f"清除历史失败: {e}")
        raise HTTPException(status_code=500, detail=f"清除历史失败: {str(e)}")

# 启动命令提示
if __name__ == "__main__":
    import uvicorn
    
    print("\n" + "="*60)
    print("🚀 启动 Nextmile Resume RAG Chatbot API (LangChain)")
    print("="*60)
    print(f"📍 API 地址: http://0.0.0.0:{API_CONFIG['port']}")
    print(f"📚 API 文档: http://0.0.0.0:{API_CONFIG['port']}/docs")
    print(f"🔧 RAG 系统: LangChain + ChromaDB")
    print(f"🤖 LLM: DeepSeek-V3.1")
    print("="*60 + "\n")
    
    uvicorn.run(
        app,
        host=API_CONFIG["host"],
        port=API_CONFIG["port"],
        log_level=API_CONFIG["log_level"]
    )
