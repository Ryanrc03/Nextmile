#!/usr/bin/env python3
"""
Core RAG (Retrieval-Augmented Generation) System for Resume QA
纯算法实现，与API服务解耦，便于本地调试和优化
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional, Tuple
import os
import re
import time
import logging
from openai import OpenAI
from config import MODEL_CONFIG, RAG_CONFIG, DEFAULT_EXCEL_PATH, LOGGING_CONFIG

# 设置日志
logging.basicConfig(
    level=getattr(logging, LOGGING_CONFIG["level"]),
    format=LOGGING_CONFIG["format"]
)
logger = logging.getLogger(__name__)

class ResumeRAGCore:
    """
    Resume RAG 核心算法类
    专注于RAG算法逻辑，不包含API相关代码
    """
    
    def __init__(self, xlsx_path: Optional[str] = None, config: Optional[Dict] = None):
        """
        初始化RAG核心系统
        
        Args:
            xlsx_path: Excel文件路径，如果为None则使用样例数据
            config: 自定义配置，覆盖默认配置
        """
        self.model_config = {**MODEL_CONFIG, **(config.get("model", {}) if config else {})}
        self.rag_config = {**RAG_CONFIG, **(config.get("rag", {}) if config else {})}
        
        # 初始化OpenAI客户端
        self.client = OpenAI(
            base_url=self.model_config["base_url"],
            api_key=self.model_config["api_key"]
        )
        
        # 加载数据
        self.data = self._load_data(xlsx_path)
        logger.info(f"数据加载成功，共{len(self.data)}条记录")
        
        # 预处理数据以提高检索效率
        self._preprocess_data()
        
    def _load_data(self, xlsx_path: Optional[str] = None) -> pd.DataFrame:
        """加载Excel数据或使用样例数据"""
        if xlsx_path and os.path.exists(xlsx_path):
            try:
                df = pd.read_excel(xlsx_path)
                logger.info(f"从文件加载数据: {xlsx_path}")
                return df
            except Exception as e:
                logger.error(f"加载文件失败: {e}")
                logger.info("使用内置样例数据")
        else:
            if xlsx_path:
                logger.warning(f"文件不存在: {xlsx_path}，使用内置样例数据")
            else:
                logger.info("使用内置样例数据")
        
        # 使用样例数据
        return self._get_sample_data()
    
    def _get_sample_data(self) -> pd.DataFrame:
        """获取样例数据"""
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
    
    def _preprocess_data(self):
        """预处理数据以提高检索效率"""
        logger.info("预处理数据...")
        
        # 为每行数据预计算词汇集合，提高检索速度
        self.processed_data = []
        for idx, row in self.data.iterrows():
            content = f"{row.get('type', '')} {row.get('company_organization', '')} {row.get('position_title', '')} {row.get('context', '')}"
            content_lower = content.lower()
            content_words = set(re.findall(r'\w+', content_lower))
            
            self.processed_data.append({
                'index': idx,
                'row': row,
                'content': content,
                'content_lower': content_lower,
                'content_words': content_words,
                'content_length': len(content_words)
            })
    
    def retrieve(self, query: str, top_k: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        检索相关文档
        
        Args:
            query: 查询字符串
            top_k: 返回top k个结果，默认使用配置中的值
            
        Returns:
            相关文档列表，每个文档包含score, data, index字段
        """
        if top_k is None:
            top_k = self.rag_config["similarity_top_k"]
            
        start_time = time.time()
        logger.debug(f"开始检索，查询: {query}")
        
        # 预处理查询
        query_lower = query.lower()
        query_words = set(re.findall(r'\w+', query_lower))
        
        results = []
        for item in self.processed_data:
            score = self._calculate_similarity_score(
                query_words, 
                query_lower,
                item['content_words'],
                item['content_lower'],
                item['content_length']
            )
            
            if score > self.rag_config["min_score_threshold"]:
                results.append({
                    'score': score,
                    'data': item['row'],
                    'index': item['index']
                })
        
        # 按分数排序并返回top k
        results.sort(key=lambda x: x['score'], reverse=True)
        top_results = results[:top_k]
        
        retrieval_time = time.time() - start_time
        logger.debug(f"检索完成，耗时{retrieval_time:.3f}s，找到{len(top_results)}个相关文档")
        
        return top_results
    
    def _calculate_similarity_score(self, query_words: set, query_lower: str, 
                                  content_words: set, content_lower: str, 
                                  content_length: int) -> float:
        """
        计算相似度分数
        
        Args:
            query_words: 查询词汇集合
            query_lower: 小写查询字符串
            content_words: 内容词汇集合
            content_lower: 小写内容字符串
            content_length: 内容长度
            
        Returns:
            相似度分数
        """
        if not query_words:
            return 0.0
        
        # 1. 关键词匹配分数
        common_words = query_words.intersection(content_words)
        keyword_score = len(common_words) / len(query_words)
        
        # 2. 精确匹配分数
        exact_matches = sum(1 for word in query_words if word in content_lower)
        exact_score = exact_matches / len(query_words)
        
        # 3. 长度奖励分数（避免过短的文档得分过高）
        length_bonus = min(content_length / 50, 1) * self.rag_config["length_bonus_weight"]
        
        # 综合分数
        total_score = (
            keyword_score * self.rag_config["keyword_weight"] +
            exact_score * self.rag_config["exact_match_weight"] +
            length_bonus
        )
        
        return total_score
    
    def generate_prompt(self, query: str, retrieved_docs: List[Dict[str, Any]]) -> str:
        """
        生成AI模型的prompt
        
        Args:
            query: 用户查询
            retrieved_docs: 检索到的相关文档
            
        Returns:
            构造的prompt字符串
        """
        if not retrieved_docs:
            return f"""
You are my digital avatar, answering as if you were me personally.

User Question: {query}

Hey! I don't think I have relevant experience in that area based on what's in my background. Feel free to ask me about other things I've worked on!

Keep it conversational and answer in English.
"""
        
        # 构建上下文
        context_parts = []
        for item in retrieved_docs:
            row = item['data']
            context_part = f"""
Type: {row.get('type', 'Unknown')}
Company/Organization: {row.get('company_organization', 'Unknown')}
Position/Project: {row.get('position_title', 'Unknown')}
Details: {row.get('context', 'No details available')}
Relevance Score: {item['score']:.3f}
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
        调用AI模型生成回答
        
        Args:
            prompt: 输入prompt
            stream: 是否使用流式输出
            
        Returns:
            AI生成的回答
        """
        try:
            logger.debug("调用AI模型生成回答...")
            start_time = time.time()
            
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
                generation_time = time.time() - start_time
                logger.debug(f"回答生成完成，耗时{generation_time:.3f}s")
                return result
                
        except Exception as e:
            error_msg = f"生成回答时发生错误: {str(e)}"
            logger.error(error_msg)
            return error_msg
    
    def _handle_stream_response(self, response) -> str:
        """处理流式响应"""
        full_answer = ""
        
        try:
            for chunk in response:
                delta = chunk.choices[0].delta
                
                # 处理回答内容
                answer_chunk = getattr(delta, 'content', None) or ""
                if answer_chunk:
                    full_answer += answer_chunk
            
            return full_answer
            
        except Exception as e:
            error_msg = f"处理流式响应时发生错误: {str(e)}"
            logger.error(error_msg)
            return error_msg
    
    def query(self, question: str, stream: bool = False) -> Dict[str, Any]:
        """
        完整的查询流程
        
        Args:
            question: 用户问题
            stream: 是否使用流式输出
            
        Returns:
            包含回答和相关信息的字典
        """
        start_time = time.time()
        
        try:
            # 1. 检索相关文档
            retrieved_docs = self.retrieve(question)
            
            # 2. 生成prompt
            prompt = self.generate_prompt(question, retrieved_docs)
            
            # 3. 生成回答
            answer = self.generate_response(prompt, stream)
            
            total_time = time.time() - start_time
            
            result = {
                "answer": answer,
                "retrieved_docs": retrieved_docs,
                "retrieved_count": len(retrieved_docs),
                "response_time": total_time,
                "success": True,
                "prompt": prompt  # 用于调试
            }
            
            logger.info(f"查询完成，耗时{total_time:.3f}s，检索到{len(retrieved_docs)}个相关文档")
            return result
            
        except Exception as e:
            error_msg = f"查询过程中发生错误: {str(e)}"
            logger.error(error_msg)
            
            return {
                "answer": error_msg,
                "retrieved_docs": [],
                "retrieved_count": 0,
                "response_time": time.time() - start_time,
                "success": False,
                "error": str(e)
            }
    
    def get_summary(self) -> Dict[str, Any]:
        """获取简历摘要统计信息"""
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
        """提取技能关键词"""
        skills = set()
        
        # 提取"Technologies:"后的内容
        for _, row in self.data.iterrows():
            context = row.get('context', '')
            
            # 查找"Technologies:"后的内容
            tech_match = re.search(r'Technologies:\s*([^.]+)', context)
            if tech_match:
                tech_text = tech_match.group(1)
                # 按逗号分割并清理
                tech_items = [item.strip() for item in tech_text.split(',')]
                skills.update(tech_items)
        
        return sorted(list(skills))[:15]  # 返回前15个技能
    
    def search_by_company(self, company: str) -> pd.DataFrame:
        """按公司搜索"""
        mask = self.data['company_organization'].str.contains(company, case=False, na=False)
        return self.data[mask]
    
    def search_by_skill(self, skill: str) -> pd.DataFrame:
        """按技能搜索"""
        mask = self.data['context'].str.contains(skill, case=False, na=False)
        return self.data[mask]
    
    def update_config(self, new_config: Dict[str, Any]):
        """更新配置"""
        if "model" in new_config:
            self.model_config.update(new_config["model"])
        if "rag" in new_config:
            self.rag_config.update(new_config["rag"])
        logger.info("配置已更新")
    
    def get_config(self) -> Dict[str, Any]:
        """获取当前配置"""
        return {
            "model": self.model_config,
            "rag": self.rag_config
        }