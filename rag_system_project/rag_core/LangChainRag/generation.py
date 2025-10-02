from openai import OpenAI as OpenAIClient
import logging
from typing import List, Dict, Any, Optional
# Import retrieval functions from retrieval module
from retreival import load_chroma_db, retrieve_similar_documents

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Model Configuration
MODEL_CONFIG = {
    "base_url": "https://api-inference.modelscope.cn/v1",
    "api_key": "ms-74b8eedd-5f76-419a-a513-f421399093da",
    "model_name": "deepseek-ai/DeepSeek-V3.1",
    "temperature": 0.7,
    "max_tokens": 2000
}

class ResumeRAGGenerator:
    """
    Resume RAG Generation class using LangChain
    负责从检索结果生成自然语言回答
    """
    
    def __init__(self, persist_directory="docs/chroma/", config: Optional[Dict] = None):
        """
        Initialize the RAG Generator
        
        Args:
            persist_directory (str): Directory where the ChromaDB is stored.
            config (dict): Optional configuration overrides.
        """
        self.model_config = {**MODEL_CONFIG, **(config.get("model", {}) if config else {})}
        self.persist_directory = persist_directory
        
        # Load ChromaDB using retrieval module
        self.vectordb = load_chroma_db(persist_directory)
        
        # Initialize OpenAI client
        self.client = OpenAIClient(
            base_url=self.model_config["base_url"],
            api_key=self.model_config["api_key"]
        )
        
        logger.info("RAG Generator initialized successfully")
    
    def retrieve_documents(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Retrieve relevant documents from ChromaDB using retrieval module
        
        Args:
            query (str): User query
            top_k (int): Number of documents to retrieve
            
        Returns:
            List of retrieved documents with metadata
        """
        try:
            # Use retrieval module's function
            results = retrieve_similar_documents(query, self.vectordb, top_k)
            
            retrieved_docs = []
            for i, doc in enumerate(results):
                retrieved_docs.append({
                    'content': doc.page_content,
                    'metadata': doc.metadata,
                    'rank': i + 1
                })
            
            logger.info(f"Retrieved {len(retrieved_docs)} documents for query: {query}")
            return retrieved_docs
            
        except Exception as e:
            logger.error(f"Error retrieving documents: {str(e)}")
            return []
    
    def build_simple_prompt(self, query: str, retrieved_docs: List[Dict[str, Any]]) -> str:
        """
        构建简单的 prompt（不含对话历史）
        注意：chatbot 模块会使用自己的 prompt 构建方法来添加对话历史
        这个方法主要用于单独测试 generation 模块
        
        Args:
            query (str): User query
            retrieved_docs (list): Retrieved documents
            
        Returns:
            Constructed prompt string
        """
        if not retrieved_docs:
            return f"""
You are my digital avatar, answering as if you were me personally.

User Question: {query}

Hey! I don't think I have relevant experience in that area based on what's in my background. Feel free to ask me about other things I've worked on!

Keep it conversational and answer in English.
"""
        
        # Build context from retrieved documents
        context_parts = []
        for doc in retrieved_docs:
            content = doc['content']
            metadata = doc.get('metadata', {})
            
            context_part = f"""
Document {doc['rank']}:
Content: {content}
Source: {metadata.get('source', 'Unknown')}
Page: {metadata.get('page', 'Unknown')}
---"""
            context_parts.append(context_part)
        
        context = "\n".join(context_parts)
        
        prompt = f"""
You are my digital avatar, speaking as if you were me personally. Answer user questions in a casual, conversational way as if we're having a friendly chat.

My Background:
{context}

User Question: {query}

Instructions:
1. Answer as "me" - use first person (I did this, I worked on, I have experience with)
2. Keep responses short and conversational (2-4 sentences max)
3. Show technical competence without going into excessive detail
4. Be friendly and approachable, like chatting with a colleague
5. If you don't have enough info, say so naturally ("I don't think I've worked on that" or "That's not something I have experience with")
6. Answer in English
7. Don't be overly formal - sound human and relatable

Answer naturally as me:
"""
        return prompt
    
    def generate_response(self, prompt: str, stream: bool = False) -> str:
        """
        Call AI model to generate response
        
        Args:
            prompt (str): Input prompt
            stream (bool): Whether to use streaming
            
        Returns:
            AI generated response
        """
        try:
            logger.debug("Calling AI model to generate response...")
            
            response = self.client.chat.completions.create(
                model=self.model_config["model_name"],
                messages=[
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ],
                stream=stream,
                temperature=self.model_config["temperature"],
                max_tokens=self.model_config["max_tokens"]
            )
            
            if stream:
                return self._handle_stream_response(response)
            else:
                result = response.choices[0].message.content
                logger.debug("Response generation completed")
                return result
                
        except Exception as e:
            error_msg = f"Error generating response: {str(e)}"
            logger.error(error_msg)
            return error_msg
    
    def _handle_stream_response(self, response) -> str:
        """Handle streaming response"""
        full_answer = ""
        
        try:
            for chunk in response:
                delta = chunk.choices[0].delta
                answer_chunk = getattr(delta, 'content', None) or ""
                if answer_chunk:
                    full_answer += answer_chunk
                    print(answer_chunk, end='', flush=True)
            
            print()  # New line after streaming
            return full_answer
            
        except Exception as e:
            error_msg = f"Error handling stream response: {str(e)}"
            logger.error(error_msg)
            return error_msg
    
    def query(self, question: str, top_k: int = 6, stream: bool = False) -> Dict[str, Any]:
        """
        Complete RAG query pipeline (用于独立测试 generation 模块)
        注意：chatbot 模块会使用自己的流程来添加对话历史
        
        Args:
            question (str): User question
            top_k (int): Number of documents to retrieve
            stream (bool): Whether to use streaming
            
        Returns:
            Dictionary containing answer and metadata
        """
        import time
        start_time = time.time()
        
        try:
            # 1. Retrieve relevant documents
            retrieved_docs = self.retrieve_documents(question, top_k)
            
            # 2. Generate prompt (simple version without chat history)
            prompt = self.build_simple_prompt(question, retrieved_docs)
            
            # 3. Generate response
            answer = self.generate_response(prompt, stream)
            
            total_time = time.time() - start_time
            
            result = {
                "answer": answer,
                "retrieved_docs": retrieved_docs,
                "retrieved_count": len(retrieved_docs),
                "response_time": total_time,
                "success": True,
                "prompt": prompt  # For debugging
            }
            
            logger.info(f"Query completed in {total_time:.3f}s with {len(retrieved_docs)} documents")
            return result
            
        except Exception as e:
            error_msg = f"Error during query: {str(e)}"
            logger.error(error_msg)
            
            return {
                "answer": error_msg,
                "retrieved_docs": [],
                "retrieved_count": 0,
                "response_time": time.time() - start_time,
                "success": False,
                "error": str(e)
            }

# Example usage
if __name__ == "__main__":
    # Initialize the generator
    generator = ResumeRAGGenerator(persist_directory="docs/chroma/")
    
    # Test queries
    test_questions = [
        "What are the candidate's main skills?",
        "Tell me about machine learning projects",
        "What experience does the candidate have with deep learning?"
    ]
    
    for question in test_questions:
        print(f"\n{'='*60}")
        print(f"Question: {question}")
        print(f"{'='*60}")
        
        result = generator.query(question, top_k=6, stream=False)
        
        print(f"\nAnswer: {result['answer']}")
        print(f"\nRetrieved {result['retrieved_count']} documents")
        print(f"Response time: {result['response_time']:.3f}s")
        
        # Print retrieved documents
        print("\nRetrieved Documents:")
        for doc in result['retrieved_docs']:
            print(f"  - Rank {doc['rank']}: {doc['content'][:100]}...")
