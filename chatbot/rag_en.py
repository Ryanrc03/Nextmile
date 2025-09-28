#!/usr/bin/env python3
"""
Resume RAG QA System
Intelligent Q&A system based on XLSX files using DeepSeek-V3.1 model
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional
import os
import re
import time
import uuid
from openai import OpenAI
from db_config import db_handler

class ResumeRAGSystem:
    def __init__(self, xlsx_path: str = None):
        """
        Initialize Resume RAG System
        
        Args:
            xlsx_path: Path to XLSX file, use sample data if None
        """
        # Initialize OpenAI client
        self.client = OpenAI(
            base_url='https://api-inference.modelscope.cn/v1',
            api_key='ms-74b8eedd-5f76-419a-a513-f421399093da'
        )
        
        # Load data
        self.data = self._load_data(xlsx_path)
        print(f"✅ Data loaded successfully, {len(self.data)} records found")
        
    def _load_data(self, xlsx_path: str = None) -> pd.DataFrame:
        """Load XLSX data or use sample data"""
        if xlsx_path and os.path.exists(xlsx_path):
            try:
                df = pd.read_excel(xlsx_path)
                print(f"📁 Loading data from file: {xlsx_path}")
                return df
            except Exception as e:
                print(f"❌ Failed to load file: {e}")
                print("🔄 Using sample data instead")
        else:
            print("📝 Using built-in sample data")
            
        # Use sample data
        return pd.DataFrame([
            {
                "type": "Work",
                "company_organization": "Baidu Inc.",
                "position_title": "AI/ML Engineer",
                "context": "Enhanced the Outline Generation module's performance through a multi-stage data pipeline that included model Supervised fine-tuning (LoRA), log data cleansing and annotation, resulting in an 80% win rate in GSB evaluations. Technologies: LoRA, Data Pipeline, Model Fine-tuning"
            },
            {
                "type": "Work",
                "company_organization": "Baidu Inc.",
                "position_title": "AI/ML Engineer",
                "context": "Automated 40% of data annotation tasks by leveraging role-playing prompt engineering on the Deepseek-v3, also optimized 3 evaluation rules salvaging 20+% of data for valuable use. Technologies: Deepseek-v3, Prompt Engineering"
            },
            {
                "type": "Work",
                "company_organization": "Baidu Inc.",
                "position_title": "AI/ML Engineer",
                "context": "Accelerated the template update speed of Baidu Wenku's AI PPT Generator by leveraging LLM Fine-Tuning and post processing strategies, achieving 90% stability and enabling the deployment of 300+ templates. Technologies: LLM Fine-Tuning, Post Processing"
            },
            {
                "type": "Work",
                "company_organization": "Baidu Inc.",
                "position_title": "AI/ML Engineer",
                "context": "Evaluated the latest LLM models(Deepseek) and applied it to text to tabular data task, achieving 95% accuracy. Technologies: Deepseek, LLM Evaluation"
            },
            {
                "type": "Work",
                "company_organization": "Apple Inc.",
                "position_title": "Data Scientist",
                "context": "Leveraged Word Embedding and MiniBatch K-Means to analyze real-time chat data from a newly launched Apple TikTok live-stream, identifying top 10 categories that informed script optimizations and resulted in a 7% reduction in return rate. Technologies: Word Embedding, MiniBatch K-Means, Real-time Data Analysis"
            },
            {
                "type": "Work",
                "company_organization": "Apple Inc.",
                "position_title": "Data Scientist",
                "context": "Boosted GenZ viewership by 21.29% and retention by 13.9% on TikTok outdoor live-streams by leveraging A/B testing to optimize content. Technologies: A/B Testing, Content Optimization"
            },
            {
                "type": "Work",
                "company_organization": "Apple Inc.",
                "position_title": "Data Scientist",
                "context": "Informed live content strategy by applying Difference in Difference(DID) analysis to Apple's continuous interconnection scenarios, which resulted in a 3% boost in click-through rates and an 8.9% increase in interaction rates. Technologies: Difference in Difference Analysis, Statistical Analysis"
            },
            {
                "type": "Work",
                "company_organization": "Michelin(China) Investment Co. Ltd.",
                "position_title": "Information Technology Intern",
                "context": "Automated a reseller sentiment analysis system with 75% accuracy using pre-trained Chinese Word Embedding and BiLSTM on e-commerce comments, leading to a 3.2% increase in sales. Technologies: Chinese Word Embedding, BiLSTM, Sentiment Analysis"
            },
            {
                "type": "Work",
                "company_organization": "Michelin(China) Investment Co. Ltd.",
                "position_title": "Information Technology Intern",
                "context": "Extracted 3000+ tire specifications from websites like Tesla and BYD by leveraging a Python Scrapy web crawler, providing crucial market data to inform product strategy for a new electric vehicle tire series. Technologies: Python, Scrapy, Web Crawling"
            },
            {
                "type": "Work",
                "company_organization": "Michelin(China) Investment Co. Ltd.",
                "position_title": "Information Technology Intern",
                "context": "Developed a data pipeline and visualization module for SharePoint internal software by integrating and processing unstructured data sources, which drove strategic SKU selection for a new tire launch in the Asia-Pacific region. Technologies: Data Pipeline, SharePoint, Data Visualization"
            },
            {
                "type": "Project",
                "company_organization": "Machine Learning Course",
                "position_title": "A Deep Reinforcement Learning Based Stock Automated Trading System",
                "context": "Developed a Deep Deterministic Policy Gradient-based automated trading agent, leveraging advanced data preprocessing to improve annual returns by 10% in backtesting scenarios. Technologies: Deep Reinforcement Learning, DDPG, Data Preprocessing"
            },
            {
                "type": "Project",
                "company_organization": "Undergraduate Research",
                "position_title": "Facial Emotion Recognition System",
                "context": "Developed a CNN-based facial emotion classifier with 80% accuracy on the FER-2013 dataset. Integrated the classifier into an interactive PyQt5 system to analyze emotional data and visualize insights. Award: Excellent Award. Technologies: CNN, PyQt5, FER-2013 Dataset, Data Visualization, Emotion Analysis"
            }
        ])
    
    def _simple_similarity_search(self, query: str, k: int = 5) -> List[Dict]:
        """Simple text similarity search"""
        query_lower = query.lower()
        query_words = set(re.findall(r'\w+', query_lower))
        
        results = []
        for idx, row in self.data.iterrows():
            # Combine all text content
            content = f"{row.get('type', '')} {row.get('company_organization', '')} {row.get('position_title', '')} {row.get('context', '')}"
            content_lower = content.lower()
            content_words = set(re.findall(r'\w+', content_lower))
            
            # Calculate similarity score
            # 1. Keyword matching
            common_words = query_words.intersection(content_words)
            keyword_score = len(common_words) / max(len(query_words), 1)
            
            # 2. Exact word matching with weight
            exact_matches = sum(1 for word in query_words if word in content_lower)
            exact_score = exact_matches / max(len(query_words), 1)
            
            # 3. Length matching bonus
            length_bonus = min(len(content_words) / 50, 1) * 0.1
            
            # Combined score
            total_score = keyword_score * 0.6 + exact_score * 0.3 + length_bonus
            
            if total_score > 0:
                results.append({
                    'score': total_score,
                    'data': row,
                    'index': idx
                })
        
        # Sort by score and return top k
        results.sort(key=lambda x: x['score'], reverse=True)
        return results[:k]
    
    def _create_prompt(self, query: str, relevant_data: List[Dict]) -> str:
        """Create prompt for AI model"""
        if not relevant_data:
            return f"""
            You are my digital avatar, answering as if you were me personally.
            
            User Question: {query}
            
            Hey! I don't think I have relevant experience in that area based on what's in my background. Feel free to ask me about other things I've worked on!
            
            Keep it conversational and answer in English.
            """
        
        context_parts = []
        for item in relevant_data:
            row = item['data']
            context_part = f"""
                Type: {row.get('type', 'Unknown')}
                Company/Organization: {row.get('company_organization', 'Unknown')}
                Position/Project: {row.get('position_title', 'Unknown')}
                Details: {row.get('context', 'No details available')}
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
    
    def query(self, question: str, stream: bool = True) -> str:
        """
        Query resume information
        
        Args:
            question: User question
            stream: Whether to use streaming output
            
        Returns:
            Answer string
        """
        print(f"\n🔍 Searching for relevant information...")
        
        # 1. Retrieve relevant documents
        relevant_data = self._simple_similarity_search(question, k=5)
        
        if relevant_data:
            print(f"📊 Found {len(relevant_data)} relevant entries")
            for i, item in enumerate(relevant_data[:3], 1):
                score = item['score']
                company = item['data'].get('company_organization', 'Unknown')
                position = item['data'].get('position_title', 'Unknown')
                print(f"   {i}. {company} - {position} (relevance: {score:.2f})")
        else:
            print("⚠️ No relevant information found")
        
        # 2. Create prompt
        prompt = self._create_prompt(question, relevant_data)
        
        # 3. Call the model
        try:
            print(f"\n🤖 Generating answer...")
            response = self.client.chat.completions.create(
                model='deepseek-ai/DeepSeek-V3.1',
                messages=[
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ],
                stream=stream,
                temperature=0.7,
                max_tokens=2000
            )
            
            if stream:
                return self._handle_stream_response(response)
            else:
                return response.choices[0].message.content
                
        except Exception as e:
            error_msg = f"❌ Error occurred during query: {str(e)}"
            print(error_msg)
            return error_msg
    
    def _handle_stream_response(self, response) -> str:
        """Handle streaming response"""
        full_answer = ""
        done_reasoning = False
        
        try:
            print("\n" + "="*60)
            for chunk in response:
                delta = chunk.choices[0].delta
                
                # Handle reasoning content
                reasoning_chunk = getattr(delta, 'reasoning_content', None) or ""
                if reasoning_chunk:
                    print(reasoning_chunk, end='', flush=True)
                
                # Handle answer content
                answer_chunk = getattr(delta, 'content', None) or ""
                if answer_chunk:
                    if not done_reasoning and reasoning_chunk == "":
                        print('\n\n💡 Answer:\n')
                        done_reasoning = True
                    print(answer_chunk, end='', flush=True)
                    full_answer += answer_chunk
            
            print("\n" + "="*60)
            return full_answer
            
        except Exception as e:
            error_msg = f"\n❌ Error processing response: {str(e)}"
            print(error_msg)
            return error_msg
    
    def get_summary(self) -> Dict[str, Any]:
        """Get resume summary statistics"""
        work_data = self.data[self.data['type'] == 'Work']
        project_data = self.data[self.data['type'] == 'Project']
        
        summary = {
            "total_records": len(self.data),
            "work_experience": len(work_data),
            "project_experience": len(project_data),
            "companies_involved": list(self.data['company_organization'].unique()),
            "key_skills": self._extract_skills()
        }
        return summary
    
    def _extract_skills(self) -> List[str]:
        """Extract skill keywords"""
        skills = set()
        
        # Extract content after "Technologies:"
        for _, row in self.data.iterrows():
            context = row.get('context', '')
            
            # Find content after "Technologies:"
            tech_match = re.search(r'Technologies:\s*([^.]+)', context)
            if tech_match:
                tech_text = tech_match.group(1)
                # Split by comma and clean
                tech_items = [item.strip() for item in tech_text.split(',')]
                skills.update(tech_items)
        
        return sorted(list(skills))[:10]  # Return top 10 skills
    
    def search_by_company(self, company: str) -> pd.DataFrame:
        """Search by company"""
        mask = self.data['company_organization'].str.contains(company, case=False, na=False)
        return self.data[mask]
    
    def search_by_skill(self, skill: str) -> pd.DataFrame:
        """Search by skill"""
        mask = self.data['context'].str.contains(skill, case=False, na=False)
        return self.data[mask]

def main():
    """Main function - Interactive Q&A"""
    print("🚀 Starting Resume RAG QA System...")
    print("=" * 60)
    
    # Get XLSX file path
    xlsx_path = input("📁 Please enter XLSX file path (press Enter for sample data): ").strip()
    if not xlsx_path:
        xlsx_path = None
    
    try:
        # Initialize system
        rag_system = ResumeRAGSystem(xlsx_path)
        
        # Show summary
        summary = rag_system.get_summary()
        print(f"\n📊 Resume Summary:")
        print(f"   Total Records: {summary['total_records']}")
        print(f"   Work Experience: {summary['work_experience']}")
        print(f"   Project Experience: {summary['project_experience']}")
        print(f"   Companies: {', '.join(summary['companies_involved'][:5])}")
        print(f"   Key Skills: {', '.join(summary['key_skills'][:8])}")
        
        print(f"\n💡 System ready! Please enter your questions")
        print("   Type 'quit' or 'q' to exit")
        print("   Type 'help' for assistance")
        print("=" * 60)
        
        # Interactive loop
        while True:
            try:
                question = input("\n🔍 Enter your question: ").strip()
                
                if question.lower() in ['quit', 'exit', 'q']:
                    print("👋 Thank you for using the system, goodbye!")
                    break
                
                if question.lower() in ['help', 'h']:
                    show_help()
                    continue
                
                if not question:
                    print("❗ Please enter a valid question")
                    continue
                
                # Process query
                answer = rag_system.query(question)
                
            except KeyboardInterrupt:
                print("\n\n👋 User interrupted, exiting program")
                break
            except Exception as e:
                print(f"\n❌ An error occurred: {str(e)}")
                
    except Exception as e:
        print(f"❌ System initialization failed: {str(e)}")

def show_help():
    """Show help information"""
    print(f"\n📖 Help Information:")
    print(f"   • Ask about work experience: 'What work was done at Baidu?'")
    print(f"   • Ask about projects: 'What machine learning projects exist?'")
    print(f"   • Ask about skills: 'What deep learning technologies were used?'")
    print(f"   • Ask about achievements: 'What were the main results at Apple?'")
    print(f"   • Data analysis: 'What data analysis experience is there?'")
    print(f"   • Company comparison: 'What are the differences between companies?'")

def batch_test():
    """Batch testing functionality"""
    print("🧪 Batch Test Mode")
    
    rag_system = ResumeRAGSystem()
    
    test_questions = [
        "What work was done during the Baidu internship?",
        "What machine learning project experience is there?",
        "What deep learning technologies were used?",
        "What were the achievements at Apple?",
        "What data analysis experience exists?",
        "What programming skills are mastered?"
    ]
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n{'='*60}")
        print(f"Test Question {i}: {question}")
        print(f"{'='*60}")
        
        try:
            answer = rag_system.query(question, stream=False)
            print(f"\nAnswer: {answer}")
        except Exception as e:
            print(f"Error: {str(e)}")
        
        input("\nPress Enter to continue to next question...")

# FastAPI app initialization
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源，生产环境中应该指定具体的前端URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic model for request body
class Message(BaseModel):
    text: str
    session_id: Optional[str] = None
    user_id: Optional[str] = None

# Initialize ResumeRAGSystem
rag_system = ResumeRAGSystem()

# Include admin API routes
try:
    from admin_api import router as admin_router
    app.include_router(admin_router)
    print("✅ Admin API routes loaded successfully")
except ImportError as e:
    print(f"⚠️ Warning: Could not load admin API routes: {e}")

@app.get("/")
async def root():
    """
    Root endpoint - API welcome message
    """
    return {
        "message": "Welcome to Nextmile Resume RAG Chatbot API",
        "version": "1.0.0",
        "endpoints": {
            "chat": "POST /chat - Send a message to the chatbot",
            "history": "GET /history/{session_id} - Get conversation history",
            "health": "GET /health - Check API health"
        }
    }

@app.get("/health")
async def health():
    """
    Health check endpoint
    """
    try:
        # Test database connection
        db_status = "connected" if db_handler.client.admin.command('ping') else "disconnected"
    except:
        db_status = "disconnected"
    
    return {
        "status": "healthy",
        "database": db_status,
        "timestamp": time.time()
    }

@app.get("/history/{session_id}")
async def get_conversation_history(session_id: str, limit: int = 10):
    """
    Get conversation history for a session
    """
    try:
        history = db_handler.get_conversation_history(session_id, limit)
        # Convert ObjectId to string for JSON serialization
        for conv in history:
            conv["_id"] = str(conv["_id"])
            conv["timestamp"] = conv["timestamp"].isoformat()
        
        return {
            "session_id": session_id,
            "history": history,
            "count": len(history)
        }
    except Exception as e:
        return {"error": str(e)}

@app.post("/chat")
async def chat(message: Message):
    """
    Chat endpoint for querying the Resume RAG system.
    """
    start_time = time.time()
    session_id = message.session_id or str(uuid.uuid4())
    
    try:
        # Use the query method from ResumeRAGSystem
        response = rag_system.query(message.text, stream=False)
        
        # 计算响应时间
        response_time = time.time() - start_time
        
        # 保存对话到MongoDB
        conversation_id = await db_handler.save_conversation_async(
            user_query=message.text,
            bot_response=response,
            session_id=session_id,
            user_id=message.user_id,
            response_time=response_time,
            model_used="DeepSeek-V3.1"
        )
        
        print(f"💾 Conversation saved to MongoDB with ID: {conversation_id}")
        
        return {
            "reply": response,
            "session_id": session_id,
            "conversation_id": conversation_id,
            "response_time": response_time
        }
        
    except Exception as e:
        # 错误情况也记录到数据库
        error_response = f"Error: {str(e)}"
        response_time = time.time() - start_time
        
        try:
            await db_handler.save_conversation_async(
                user_query=message.text,
                bot_response=error_response,
                session_id=session_id,
                user_id=message.user_id,
                response_time=response_time,
                model_used="error"
            )
        except Exception as db_error:
            print(f"Failed to save error to database: {db_error}")
        
        return {"error": str(e)}

if __name__ == "__main__":
    import sys
    import uvicorn
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "test":
            batch_test()
        elif sys.argv[1] == "help":
            show_help()
        elif sys.argv[1] == "interactive":
            main()
        else:
            print("Usage:")
            print("  python script.py                # Start FastAPI server")
            print("  python script.py interactive    # Interactive mode")
            print("  python script.py test          # Batch testing")
            print("  python script.py help          # Show help")
    else:
        # Start FastAPI server by default
        print("🚀 Starting FastAPI server...")
        uvicorn.run(app, host="0.0.0.0", port=8000)
