#!/usr/bin/env python3
"""
调试版API服务器 - 增强调试功能
"""

import os
import sys
import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import time
import uuid

# 检查是否在调试模式
DEBUG_MODE = os.getenv("DEBUG_MODE", "false").lower() == "true"

if DEBUG_MODE:
    try:
        from debug_config import DEBUG_CONFIG, DEBUG_API_CONFIG, DEBUG_LOGGING_CONFIG
        MODEL_CONFIG = DEBUG_CONFIG["model"]
        RAG_CONFIG = DEBUG_CONFIG["rag"]
        API_CONFIG = DEBUG_API_CONFIG
        LOGGING_CONFIG = DEBUG_LOGGING_CONFIG
        print("🔧 使用调试配置")
    except ImportError:
        print("⚠️ 调试配置不可用，使用默认配置")
        from config import MODEL_CONFIG, RAG_CONFIG, API_CONFIG, LOGGING_CONFIG
else:
    from config import MODEL_CONFIG, RAG_CONFIG, API_CONFIG, LOGGING_CONFIG

# 设置详细日志
logging.basicConfig(
    level=getattr(logging, LOGGING_CONFIG["level"]),
    format=LOGGING_CONFIG["format"]
)
logger = logging.getLogger(__name__)

# 导入RAG核心模块
from rag_core import ResumeRAGCore
from db_config import db_handler

# FastAPI应用初始化
app = FastAPI(
    title="Nextmile Resume RAG Chatbot API (Debug)",
    description="智能简历问答系统API - 调试版本",
    version="2.0.0-debug"
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
    debug: Optional[bool] = False  # 调试模式标志

class DebugChatResponse(BaseModel):
    reply: str
    session_id: str
    conversation_id: Optional[str] = None
    response_time: float
    retrieved_count: int
    success: bool
    debug_info: Optional[dict] = None  # 调试信息

# 初始化RAG系统
logger.info("正在初始化RAG系统...")
try:
    # 在调试模式下使用调试配置
    if DEBUG_MODE:
        custom_config = {
            "model": MODEL_CONFIG,
            "rag": RAG_CONFIG
        }
        rag_system = ResumeRAGCore(config=custom_config)
    else:
        rag_system = ResumeRAGCore()
    
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
    """根端点 - 显示调试信息"""
    debug_status = "🔧 调试模式" if DEBUG_MODE else "🚀 生产模式"
    
    return {
        "message": f"欢迎使用 Nextmile Resume RAG Chatbot API - {debug_status}",
        "version": "2.0.0-debug",
        "debug_mode": DEBUG_MODE,
        "environment": "Docker Debug Container",
        "endpoints": {
            "chat": "POST /chat - 发送消息给聊天机器人",
            "debug_chat": "POST /debug/chat - 调试模式聊天",
            "health": "GET /health - 检查API健康状态",
            "debug": "GET /debug/* - 调试功能",
            "admin": "GET /admin/* - 管理功能"
        }
    }

@app.get("/health")
async def health():
    """健康检查端点"""
    try:
        db_status = "connected" if db_handler.client.admin.command('ping') else "disconnected"
    except Exception as e:
        logger.error(f"数据库连接检查失败: {e}")
        db_status = "disconnected"
    
    rag_status = "healthy" if rag_system is not None else "unavailable"
    overall_status = "healthy" if db_status == "connected" and rag_status == "healthy" else "degraded"
    
    return {
        "status": overall_status,
        "database": db_status,
        "timestamp": time.time(),
        "rag_system": rag_status,
        "debug_mode": DEBUG_MODE,
        "container": "Docker Debug Environment"
    }

@app.post("/chat", response_model=DebugChatResponse)
async def chat(message: Message):
    """标准聊天端点"""
    return await debug_chat(message)

@app.post("/debug/chat", response_model=DebugChatResponse)
async def debug_chat(message: Message):
    """调试模式聊天端点 - 返回详细调试信息"""
    if rag_system is None:
        raise HTTPException(status_code=503, detail="RAG系统不可用")
    
    start_time = time.time()
    session_id = message.session_id or str(uuid.uuid4())
    
    try:
        logger.debug(f"处理调试聊天请求: session_id={session_id}, query='{message.text}'")
        
        # 使用RAG核心系统处理查询，获取详细结果
        rag_result = rag_system.query(message.text, stream=False)
        
        if not rag_result['success']:
            logger.error(f"RAG查询失败: {rag_result.get('error', 'Unknown error')}")
            raise HTTPException(status_code=500, detail=f"查询处理失败: {rag_result.get('error', 'Unknown error')}")
        
        total_response_time = time.time() - start_time
        
        # 构建调试信息
        debug_info = None
        if DEBUG_MODE or message.debug:
            debug_info = {
                "retrieved_documents": [
                    {
                        "score": doc["score"],
                        "company": doc["data"].get("company_organization", "Unknown"),
                        "position": doc["data"].get("position_title", "Unknown"),
                        "content_preview": doc["data"].get("context", "")[:100] + "..."
                    }
                    for doc in rag_result.get("retrieved_docs", [])
                ],
                "rag_config": rag_system.get_config()["rag"],
                "model_config": {
                    "model_name": rag_system.get_config()["model"]["model_name"],
                    "temperature": rag_system.get_config()["model"]["temperature"],
                    "max_tokens": rag_system.get_config()["model"]["max_tokens"]
                },
                "timing": {
                    "rag_processing_time": rag_result['response_time'],
                    "total_response_time": total_response_time,
                    "overhead_time": total_response_time - rag_result['response_time']
                }
            }
            
            logger.debug(f"调试信息: {debug_info}")
        
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
                    "rag_response_time": rag_result['response_time'],
                    "debug_mode": DEBUG_MODE
                }
            )
            logger.debug(f"对话已保存: conversation_id={conversation_id}")
        except Exception as db_error:
            logger.error(f"保存对话失败: {db_error}")
        
        return DebugChatResponse(
            reply=rag_result['answer'],
            session_id=session_id,
            conversation_id=conversation_id,
            response_time=total_response_time,
            retrieved_count=rag_result['retrieved_count'],
            success=True,
            debug_info=debug_info
        )
        
    except HTTPException:
        raise
    except Exception as e:
        error_message = f"处理聊天请求时发生错误: {str(e)}"
        logger.error(error_message, exc_info=True)
        
        raise HTTPException(status_code=500, detail=error_message)

@app.get("/debug/config")
async def get_debug_config():
    """获取当前调试配置"""
    if rag_system is None:
        raise HTTPException(status_code=503, detail="RAG系统不可用")
    
    return {
        "debug_mode": DEBUG_MODE,
        "rag_config": rag_system.get_config(),
        "api_config": API_CONFIG,
        "logging_level": LOGGING_CONFIG["level"]
    }

@app.post("/debug/config")
async def update_debug_config(new_config: dict):
    """更新调试配置"""
    if rag_system is None:
        raise HTTPException(status_code=503, detail="RAG系统不可用")
    
    try:
        rag_system.update_config(new_config)
        logger.info(f"配置已更新: {new_config}")
        
        return {
            "message": "配置更新成功",
            "new_config": rag_system.get_config(),
            "timestamp": time.time()
        }
    except Exception as e:
        logger.error(f"配置更新失败: {e}")
        raise HTTPException(status_code=500, detail=f"配置更新失败: {str(e)}")

@app.get("/debug/test")
async def debug_test():
    """调试测试端点"""
    test_queries = [
        "What work experience do you have?",
        "Tell me about your projects",
        "What technologies do you know?"
    ]
    
    results = []
    for query in test_queries:
        try:
            result = rag_system.query(query, stream=False)
            results.append({
                "query": query,
                "success": result['success'],
                "retrieved_count": result['retrieved_count'],
                "response_time": result['response_time']
            })
        except Exception as e:
            results.append({
                "query": query,
                "success": False,
                "error": str(e)
            })
    
    return {
        "test_results": results,
        "timestamp": time.time()
    }

def main():
    """主函数 - 启动调试API服务器"""
    import uvicorn
    
    logger.info("启动Nextmile Resume RAG Chatbot API调试服务器...")
    logger.info(f"调试模式: {DEBUG_MODE}")
    logger.info(f"服务器配置: {API_CONFIG['host']}:{API_CONFIG['port']}")
    
    # 在调试模式下启用热重载
    reload = DEBUG_MODE and API_CONFIG.get("reload", False)
    
    uvicorn.run(
        "api_server_debug:app",  # 使用模块名
        host=API_CONFIG["host"], 
        port=API_CONFIG["port"],
        log_level="debug" if DEBUG_MODE else "info",
        reload=reload
    )

if __name__ == "__main__":
    main()