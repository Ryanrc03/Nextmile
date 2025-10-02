"""
Chatbot Module - 人性化对话接口
整合 RAG 组件，提供带记忆的对话功能
职责：调用 retrieval 和 generation 模块，管理对话记忆和交互
"""

from langchain.memory import ConversationBufferMemory
from typing import List, Dict, Any, Optional
import logging

# 导入 retrieval 和 generation 模块
from retreival import load_chroma_db, retrieve_similar_documents
from generation import ResumeRAGGenerator

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class ResumeChatbot:
    """
    带记忆的简历问答聊天机器人
    整合检索和生成功能，提供人性化的对话体验
    """
    
    def __init__(self, persist_directory="docs/chroma/", config: Optional[Dict] = None):
        """
        Initialize the chatbot
        
        Args:
            persist_directory (str): ChromaDB 存储目录
            config (dict): 可选配置
        """
        # 初始化检索模块（直接加载 ChromaDB）
        self.vectordb = load_chroma_db(persist_directory)
        
        # 初始化生成模块
        self.generator = ResumeRAGGenerator(persist_directory, config)
        
        # 初始化对话记忆
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            output_key="answer"
        )
        
        # 对话历史（用于简单展示）
        self.conversation_history = []
        
        # 欢迎消息
        self.welcome_message = "Hello! How can I assist you today? Feel free to ask me anything about my background, experience, or skills!"
        
        logger.info("Chatbot initialized successfully")
    
    def _build_prompt_with_history(self, question: str, retrieved_docs: List[Dict[str, Any]]) -> str:
        """
        构建包含对话历史的 prompt
        
        Args:
            question (str): 用户问题
            retrieved_docs (list): 检索到的文档
            
        Returns:
            完整的 prompt
        """
        # 获取对话历史
        chat_history = self.memory.load_memory_variables({}).get("chat_history", [])
        
        # 构建历史对话文本
        history_text = ""
        if chat_history:
            history_text = "\nPrevious Conversation:\n"
            for msg in chat_history[-4:]:  # 只保留最近4轮对话
                role = "User" if msg.type == "human" else "Assistant"
                history_text += f"{role}: {msg.content}\n"
            history_text += "\n"
        
        # 构建检索到的上下文
        if not retrieved_docs:
            context = "No specific background information found for this query."
        else:
            context_parts = []
            for doc in retrieved_docs[:3]:  # 只使用前3个最相关的文档
                content = doc['content']
                metadata = doc.get('metadata', {})
                context_part = f"""
Source: {metadata.get('source', 'Unknown')} (Page {metadata.get('page', 'N/A')})
Content: {content}
---"""
                context_parts.append(context_part)
            context = "\n".join(context_parts)
        
        # 构建完整 prompt
        prompt = f"""
            You are my digital avatar, speaking as if you were me personally. Answer user questions in a casual, conversational way as if we're having a friendly chat.

{history_text}
My Background (Retrieved Context):
{context}

Current Question: {question}

    Instructions:
    1. Answer as "me" - use first person (I did this, I worked on, I have experience with)
    2. Keep responses conversational and concise (2-4 sentences typically)
    3. If the question relates to previous conversation, acknowledge and build on it naturally
    4. Show technical competence without being overly detailed
    5. Be friendly and approachable, like chatting with a colleague
    6. If you don't have enough info, say so naturally ("I don't think I've worked on that" or "That's not in my experience")
    7. Answer in English
    8. Don't be overly formal - sound human and relatable
    9. If appropriate, end with a friendly follow-up like "Feel free to ask more!" or "Anything else you'd like to know?"

    Answer naturally as me:
    """
        return prompt
    
    def chat(self, user_input: str, top_k: int = 5, stream: bool = False) -> Dict[str, Any]:
        """
        与用户对话（核心方法）
        调用 retrieval 模块检索，调用 generation 模块生成回答
        
        Args:
            user_input (str): 用户输入
            top_k (int): 检索文档数量
            stream (bool): 是否使用流式输出
            
        Returns:
            包含回答和元数据的字典
        """
        try:
            # 1. 使用 retrieval 模块检索相关文档
            retrieved_results = retrieve_similar_documents(user_input, self.vectordb, top_k)
            
            # 将检索结果转换为统一格式
            retrieved_docs = []
            for i, doc in enumerate(retrieved_results):
                retrieved_docs.append({
                    'content': doc.page_content,
                    'metadata': doc.metadata,
                    'rank': i + 1
                })
            
            # 2. 构建带历史的 prompt
            prompt = self._build_prompt_with_history(user_input, retrieved_docs)
            
            # 3. 使用 generation 模块生成回答
            answer = self.generator.generate_response(prompt, stream)
            
            # 4. 保存到记忆中
            self.memory.save_context(
                {"input": user_input},
                {"answer": answer}
            )
            
            # 5. 保存到对话历史
            self.conversation_history.append({
                "role": "user",
                "content": user_input
            })
            self.conversation_history.append({
                "role": "assistant",
                "content": answer
            })
            
            result = {
                "answer": answer,
                "retrieved_docs": retrieved_docs,
                "retrieved_count": len(retrieved_docs),
                "success": True
            }
            
            logger.info(f"Chat completed with {len(retrieved_docs)} retrieved documents")
            return result
            
        except Exception as e:
            error_msg = f"Error during chat: {str(e)}"
            logger.error(error_msg)
            
            return {
                "answer": f"Sorry, I encountered an error: {str(e)}",
                "retrieved_docs": [],
                "retrieved_count": 0,
                "success": False,
                "error": str(e)
            }
    
    def get_welcome_message(self) -> str:
        """获取欢迎消息"""
        return self.welcome_message
    
    def get_conversation_history(self) -> List[Dict[str, str]]:
        """获取对话历史"""
        return self.conversation_history
    
    def clear_history(self):
        """清除对话历史"""
        self.memory.clear()
        self.conversation_history = []
        logger.info("Conversation history cleared")
    
    def get_memory_summary(self) -> str:
        """获取记忆摘要"""
        chat_history = self.memory.load_memory_variables({}).get("chat_history", [])
        if not chat_history:
            return "No conversation history yet."
        
        summary = f"Conversation has {len(chat_history)} messages:\n"
        for i, msg in enumerate(chat_history[-6:], 1):  # 显示最近6条
            role = "User" if msg.type == "human" else "Assistant"
            content_preview = msg.content[:80] + "..." if len(msg.content) > 80 else msg.content
            summary += f"{i}. {role}: {content_preview}\n"
        
        return summary
    
    def run_interactive(self):
        """
        运行交互式聊天循环（命令行界面）
        """
        print("="*60)
        print(self.welcome_message)
        print("="*60)
        print("Type 'exit' or 'quit' to end the conversation")
        print("Type 'history' to see conversation history")
        print("Type 'clear' to clear conversation history")
        print("="*60)
        
        while True:
            try:
                user_input = input("\n You: ").strip()
                
                if not user_input:
                    continue
                
                # 处理特殊命令
                if user_input.lower() in ['exit', 'quit', 'bye']:
                    print("\nAssistant: Thanks for chatting! Have a great day! 👋")
                    break
                
                if user_input.lower() == 'history':
                    print("\n" + self.get_memory_summary())
                    continue
                
                if user_input.lower() == 'clear':
                    self.clear_history()
                    print("\nAssistant: Conversation history cleared! Let's start fresh.")
                    continue
                
                # 正常对话
                print("\nAssistant: ", end="", flush=True)
                result = self.chat(user_input, top_k=3, stream=True)
                
                if not result["success"]:
                    print(f"\n[Error: {result.get('error', 'Unknown error')}]")
                
            except KeyboardInterrupt:
                print("\n\nAssistant: Goodbye! 👋")
                break
            except Exception as e:
                print(f"\n[Unexpected error: {str(e)}]")
                logger.error(f"Interactive chat error: {str(e)}")


# Example usage and testing
if __name__ == "__main__":
    # 初始化 chatbot
    chatbot = ResumeChatbot(persist_directory="docs/chroma/")
    
    # 方式 1: 交互式命令行聊天
    print("\n=== Starting Interactive Chat ===\n")
    chatbot.run_interactive()
    
    # 方式 2: 程序化测试（注释掉交互式后可运行）
    """
    print("\n=== Testing Chatbot Programmatically ===\n")
    
    # 测试对话
    test_conversations = [
        "What are your main skills?",
        "Tell me more about your machine learning experience",
        "Have you worked with deep learning?"
    ]
    
    print(f"Chatbot: {chatbot.get_welcome_message()}\n")
    
    for question in test_conversations:
        print(f"User: {question}")
        result = chatbot.chat(question, top_k=3, stream=False)
        print(f"Chatbot: {result['answer']}")
        print(f"[Retrieved {result['retrieved_count']} documents]\n")
    
    # 显示对话历史
    print("\n=== Conversation History ===")
    print(chatbot.get_memory_summary())
    """
