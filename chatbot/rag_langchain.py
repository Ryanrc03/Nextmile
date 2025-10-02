#!/usr/bin/env python3
"""
LangChain RAG 集成模块
将新开发的 LangChain RAG 系统集成到现有 API 中
"""

import os
import sys
import logging
from typing import Dict, Any, Optional

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# 添加 RAG_algotirhm 目录到路径
RAG_ALGO_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'RAG_algotirhm', 'rag_core', 'LangChainRag')
if os.path.exists(RAG_ALGO_PATH):
    sys.path.insert(0, RAG_ALGO_PATH)
else:
    # Docker 环境中的路径
    RAG_ALGO_PATH = '/app/RAG_algotirhm/rag_core/LangChainRag'
    if os.path.exists(RAG_ALGO_PATH):
        sys.path.insert(0, RAG_ALGO_PATH)
    else:
        logger.error(f"RAG算法路径不存在: {RAG_ALGO_PATH}")

# 导入 LangChain RAG 组件
try:
    from chatbot import ResumeChatbot
except ImportError as e:
    logger.error(f"无法导入 ResumeChatbot: {e}")
    # 尝试从相对路径导入
    try:
        import sys
        sys.path.append('/app/RAG_algotirhm/rag_core/LangChainRag')
        from chatbot import ResumeChatbot
    except ImportError as e2:
        logger.error(f"导入失败: {e2}")
        raise


class LangChainRAGAdapter:
    """
    LangChain RAG 适配器
    将新的 LangChain RAG 系统适配到现有 API 接口
    """
    
    def __init__(self, persist_directory: Optional[str] = None, config: Optional[Dict] = None):
        """
        初始化 LangChain RAG 适配器
        
        Args:
            persist_directory: ChromaDB 存储目录
            config: 可选配置
        """
        # 设置默认路径
        if persist_directory is None:
            persist_directory = os.path.join(RAG_ALGO_PATH, "docs", "chroma")
        
        logger.info(f"初始化 LangChain RAG 系统，persist_directory: {persist_directory}")
        
        try:
            # 初始化 ResumeChatbot
            self.chatbot = ResumeChatbot(persist_directory=persist_directory, config=config)
            logger.info("LangChain RAG 系统初始化成功")
        except Exception as e:
            logger.error(f"LangChain RAG 系统初始化失败: {e}")
            raise
    
    def query(self, question: str, stream: bool = False, top_k: int = 5) -> Dict[str, Any]:
        """
        查询接口（兼容原有 API）
        
        Args:
            question: 用户问题
            stream: 是否使用流式输出
            top_k: 检索文档数量
            
        Returns:
            包含回答和元数据的字典
        """
        try:
            # 调用 chatbot 的 chat 方法
            result = self.chatbot.chat(question, top_k=top_k, stream=stream)
            
            # 适配返回格式以兼容原有 API
            return {
                "answer": result["answer"],
                "retrieved_docs": result.get("retrieved_docs", []),
                "retrieved_count": result.get("retrieved_count", 0),
                "response_time": 0,  # chatbot 内部已计时
                "success": result.get("success", True)
            }
        except Exception as e:
            logger.error(f"查询处理失败: {str(e)}")
            return {
                "answer": f"抱歉，处理您的问题时出现错误: {str(e)}",
                "retrieved_docs": [],
                "retrieved_count": 0,
                "response_time": 0,
                "success": False,
                "error": str(e)
            }
    
    def get_summary(self) -> Dict[str, Any]:
        """
        获取系统摘要信息
        
        Returns:
            系统摘要字典
        """
        return {
            "system": "LangChain RAG",
            "components": {
                "chunking": "RecursiveCharacterTextSplitter",
                "embedding": "sentence-transformers/all-MiniLM-L6-v2",
                "vectorstore": "ChromaDB",
                "llm": "deepseek-ai/DeepSeek-V3.1",
                "memory": "ConversationBufferMemory"
            },
            "status": "operational"
        }
    
    def clear_history(self):
        """清除对话历史"""
        try:
            self.chatbot.clear_history()
            logger.info("对话历史已清除")
        except Exception as e:
            logger.error(f"清除对话历史失败: {e}")
    
    def get_conversation_history(self):
        """获取对话历史"""
        try:
            return self.chatbot.get_conversation_history()
        except Exception as e:
            logger.error(f"获取对话历史失败: {e}")
            return []


# 测试代码
if __name__ == "__main__":
    # 测试 LangChain RAG 适配器
    try:
        print("初始化 LangChain RAG 适配器...")
        adapter = LangChainRAGAdapter()
        
        print("\n获取系统摘要:")
        print(adapter.get_summary())
        
        print("\n测试查询:")
        test_questions = [
            "What are the candidate's main skills?",
            "Tell me about machine learning projects"
        ]
        
        for question in test_questions:
            print(f"\n问题: {question}")
            result = adapter.query(question, top_k=3)
            print(f"回答: {result['answer']}")
            print(f"检索文档数: {result['retrieved_count']}")
            print(f"成功: {result['success']}")
        
        print("\n测试成功！")
    except Exception as e:
        print(f"测试失败: {e}")
        import traceback
        traceback.print_exc()
