#!/usr/bin/env python3
"""
重构后的API服务器
仅包含API相关逻辑，RAG算法通过rag_core模块调用
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import time
import uuid
import logging

# 导入RAG核心模块和配置
from rag_core import ResumeRAGCore
from config import API_CONFIG, DEFAULT_EXCEL_PATH
from db_config import db_handler

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI应用初始化
app = FastAPI(
    title="Nextmile Resume RAG Chatbot API",
    description="智能简历问答系统API",
    version="2.0.0"
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=API_CONFIG["cors_origins"],
    allow_credentials=API_CONFIG["cors_credentials"],
    allow_methods=API_CONFIG["cors_methods"],
    allow_headers=API_CONFIG["cors_headers"],
)

# Pydantic模型定义
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

class HistoryResponse(BaseModel):
    session_id: str
    history: list
    count: int

# 初始化RAG系统
logger.info("正在初始化RAG系统...")
try:
    rag_system = ResumeRAGCore(DEFAULT_EXCEL_PATH)
    logger.info("RAG系统初始化成功")
except Exception as e:
    logger.error(f"RAG系统初始化失败: {e}")
    rag_system = None

# 包含管理API路由
try:
    from admin_api import router as admin_router
    app.include_router(admin_router)
    logger.info("管理API路由加载成功")
except ImportError as e:
    logger.warning(f"无法加载管理API路由: {e}")

@app.get("/")
async def root():
    """
    根端点 - API欢迎信息
    """
    return {
        "message": "欢迎使用 Nextmile Resume RAG Chatbot API",
        "version": "2.0.0",
        "description": "基于RAG技术的智能简历问答系统",
        "endpoints": {
            "chat": "POST /chat - 发送消息给聊天机器人",
            "history": "GET /history/{session_id} - 获取对话历史",
            "health": "GET /health - 检查API健康状态",
            "admin": "GET /admin/* - 管理功能 (需要权限)"
        },
        "features": [
            "智能简历内容检索",
            "自然语言问答",
            "对话历史管理",
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
    
    # 检查RAG系统状态
    rag_status = "healthy" if rag_system is not None else "unavailable"
    
    # 整体状态
    overall_status = "healthy" if db_status == "connected" and rag_status == "healthy" else "degraded"
    
    return HealthResponse(
        status=overall_status,
        database=db_status,
        timestamp=time.time(),
        rag_system=rag_status
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
        
        # 转换ObjectId为字符串以便JSON序列化
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
    聊天端点 - 核心RAG问答功能
    
    Args:
        message: 包含用户消息和元数据的请求体
        
    Returns:
        聊天响应，包含AI回答和相关元数据
    """
    # 检查RAG系统是否可用
    if rag_system is None:
        raise HTTPException(
            status_code=503, 
            detail="RAG系统不可用，请联系管理员"
        )
    
    start_time = time.time()
    session_id = message.session_id or str(uuid.uuid4())
    
    try:
        logger.info(f"处理聊天请求: session_id={session_id}, query='{message.text[:50]}...'")
        
        # 使用RAG核心系统处理查询
        rag_result = rag_system.query(message.text, stream=False)
        
        if not rag_result['success']:
            logger.error(f"RAG查询失败: {rag_result.get('error', 'Unknown error')}")
            raise HTTPException(
                status_code=500,
                detail=f"查询处理失败: {rag_result.get('error', 'Unknown error')}"
            )
        
        # 计算总响应时间
        total_response_time = time.time() - start_time
        
        # 保存对话到MongoDB
        conversation_id = None
        try:
            conversation_id = await db_handler.save_conversation_async(
                user_query=message.text,
                bot_response=rag_result['answer'],
                session_id=session_id,
                user_id=message.user_id,
                response_time=total_response_time,
                model_used=rag_system.model_config["model_name"],
                metadata={
                    "retrieved_count": rag_result['retrieved_count'],
                    "rag_response_time": rag_result['response_time']
                }
            )
            logger.info(f"对话已保存到数据库: conversation_id={conversation_id}")
        except Exception as db_error:
            logger.error(f"保存对话到数据库失败: {db_error}")
            # 数据库错误不影响用户体验，继续返回响应
        
        return ChatResponse(
            reply=rag_result['answer'],
            session_id=session_id,
            conversation_id=conversation_id,
            response_time=total_response_time,
            retrieved_count=rag_result['retrieved_count'],
            success=True
        )
        
    except HTTPException:
        # 重新抛出HTTP异常
        raise
    except Exception as e:
        # 处理其他异常
        error_message = f"处理聊天请求时发生未知错误: {str(e)}"
        logger.error(error_message)
        
        # 记录错误到数据库
        error_response_time = time.time() - start_time
        try:
            await db_handler.save_conversation_async(
                user_query=message.text,
                bot_response=f"系统错误: {str(e)}",
                session_id=session_id,
                user_id=message.user_id,
                response_time=error_response_time,
                model_used="error",
                metadata={"error": str(e)}
            )
        except Exception as db_error:
            logger.error(f"保存错误记录到数据库失败: {db_error}")
        
        raise HTTPException(status_code=500, detail=error_message)

@app.get("/system/info")
async def get_system_info():
    """
    获取系统信息
    """
    if rag_system is None:
        raise HTTPException(status_code=503, detail="RAG系统不可用")
    
    try:
        summary = rag_system.get_summary()
        config = rag_system.get_config()
        
        return {
            "rag_summary": summary,
            "rag_config": config,
            "api_config": {
                "cors_enabled": True,
                "cors_origins": API_CONFIG["cors_origins"]
            },
            "system_status": {
                "uptime": time.time(),
                "memory_usage": "N/A",  # 可以添加内存监控
                "active_sessions": "N/A"  # 可以添加会话监控
            }
        }
    except Exception as e:
        logger.error(f"获取系统信息失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取系统信息失败: {str(e)}")

@app.post("/system/reload")
async def reload_rag_system(xlsx_path: Optional[str] = None):
    """
    重新加载RAG系统 (管理功能)
    """
    global rag_system
    
    try:
        logger.info(f"重新加载RAG系统: xlsx_path={xlsx_path}")
        rag_system = ResumeRAGCore(xlsx_path or DEFAULT_EXCEL_PATH)
        
        return {
            "message": "RAG系统重新加载成功",
            "timestamp": time.time(),
            "data_source": xlsx_path or DEFAULT_EXCEL_PATH,
            "summary": rag_system.get_summary()
        }
    except Exception as e:
        logger.error(f"重新加载RAG系统失败: {e}")
        raise HTTPException(status_code=500, detail=f"重新加载RAG系统失败: {str(e)}")

# 错误处理器
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """HTTP异常处理器"""
    logger.error(f"HTTP异常: {exc.status_code} - {exc.detail}")
    return {
        "error": exc.detail,
        "status_code": exc.status_code,
        "timestamp": time.time()
    }

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """通用异常处理器"""
    logger.error(f"未处理的异常: {str(exc)}", exc_info=True)
    return {
        "error": "Internal server error",
        "message": "服务器内部错误，请稍后重试",
        "timestamp": time.time()
    }

def main():
    """主函数 - 启动API服务器"""
    import uvicorn
    
    logger.info("启动Nextmile Resume RAG Chatbot API服务器...")
    logger.info(f"服务器配置: {API_CONFIG['host']}:{API_CONFIG['port']}")
    
    uvicorn.run(
        app, 
        host=API_CONFIG["host"], 
        port=API_CONFIG["port"],
        log_level="info"
    )

if __name__ == "__main__":
    main()