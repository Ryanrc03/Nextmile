#!/usr/bin/env python3
"""
简历RAG QA系统
基于XLSX文件的智能问答系统，使用DeepSeek-V3.1模型
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional
import os
import re
from openai import OpenAI

class ResumeRAGSystem:
    def __init__(self, xlsx_path: str = None):
        """
        初始化简历RAG系统
        
        Args:
            xlsx_path: XLSX文件路径，如果为None则使用示例数据
        """
        # 初始化OpenAI客户端
        self.client = OpenAI(
            base_url='https://api-inference.modelscope.cn/v1',
            api_key='ms-74b8eedd-5f76-419a-a513-f421399093da'
        )
        
        # 加载数据
        self.data = self._load_data(xlsx_path)
        print(f"✅ 数据加载完成，共 {len(self.data)} 条记录")
        
    def _load_data(self, xlsx_path: str = None) -> pd.DataFrame:
        """加载XLSX数据或使用示例数据"""
        if xlsx_path and os.path.exists(xlsx_path):
            try:
                df = pd.read_excel(xlsx_path)
                print(f"📁 从文件加载数据: {xlsx_path}")
                return df
            except Exception as e:
                print(f"❌ 文件加载失败: {e}")
                print("🔄 使用示例数据")
        else:
            print("📝 使用内置示例数据")
            
        # 使用示例数据
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
        """简单的文本相似度搜索"""
        query_lower = query.lower()
        query_words = set(re.findall(r'\w+', query_lower))
        
        results = []
        for idx, row in self.data.iterrows():
            # 组合所有文本内容
            content = f"{row.get('type', '')} {row.get('company_organization', '')} {row.get('position_title', '')} {row.get('context', '')}"
            content_lower = content.lower()
            content_words = set(re.findall(r'\w+', content_lower))
            
            # 计算相似度分数
            # 1. 关键词匹配
            common_words = query_words.intersection(content_words)
            keyword_score = len(common_words) / max(len(query_words), 1)
            
            # 2. 完整词匹配加权
            exact_matches = sum(1 for word in query_words if word in content_lower)
            exact_score = exact_matches / max(len(query_words), 1)
            
            # 3. 长度匹配奖励
            length_bonus = min(len(content_words) / 50, 1) * 0.1
            
            # 综合分数
            total_score = keyword_score * 0.6 + exact_score * 0.3 + length_bonus
            
            if total_score > 0:
                results.append({
                    'score': total_score,
                    'data': row,
                    'index': idx
                })
        
        # 按分数排序并返回前k个
        results.sort(key=lambda x: x['score'], reverse=True)
        return results[:k]
    
    def _create_prompt(self, query: str, relevant_data: List[Dict]) -> str:
        """创建提示词"""
        if not relevant_data:
            return f"""
你是一个专业的简历分析助手。

用户问题: {query}

很抱歉，我在简历中没有找到相关信息来回答您的问题。请尝试询问其他内容，或者检查问题是否与简历信息相关。

请用中文回答。
"""
        
        context_parts = []
        for item in relevant_data:
            row = item['data']
            context_part = f"""
类型: {row.get('type', '未知')}
公司/组织: {row.get('company_organization', '未知')}
职位/项目: {row.get('position_title', '未知')}
详细信息: {row.get('context', '暂无详细信息')}
---"""
            context_parts.append(context_part)
        
        context = "\n".join(context_parts)
        
        prompt = f"""
你是一个专业的简历分析助手，请基于以下简历信息准确回答用户问题。

简历信息:
{context}

用户问题: {query}

请根据提供的简历信息准确回答问题。回答要求：
1. 基于简历内容回答，不要编造信息
2. 如果信息不足，请明确说明
3. 突出相关的技能、成就和数据
4. 回答要结构化、条理清晰
5. 用中文回答

回答:
"""
        return prompt
    
    def query(self, question: str, stream: bool = True) -> str:
        """
        查询简历信息
        
        Args:
            question: 用户问题
            stream: 是否使用流式输出
            
        Returns:
            回答字符串
        """
        print(f"\n🔍 正在搜索相关信息...")
        
        # 1. 检索相关文档
        relevant_data = self._simple_similarity_search(question, k=5)
        
        if relevant_data:
            print(f"📊 找到 {len(relevant_data)} 条相关信息")
            for i, item in enumerate(relevant_data[:3], 1):
                score = item['score']
                company = item['data'].get('company_organization', '未知')
                position = item['data'].get('position_title', '未知')
                print(f"   {i}. {company} - {position} (相关度: {score:.2f})")
        else:
            print("⚠️ 未找到相关信息")
        
        # 2. 构建提示词
        prompt = self._create_prompt(question, relevant_data)
        
        # 3. 调用模型
        try:
            print(f"\n🤖 正在生成回答...")
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
            error_msg = f"❌ 查询时发生错误: {str(e)}"
            print(error_msg)
            return error_msg
    
    def _handle_stream_response(self, response) -> str:
        """处理流式响应"""
        full_answer = ""
        done_reasoning = False
        
        try:
            print("\n" + "="*60)
            for chunk in response:
                delta = chunk.choices[0].delta
                
                # 处理推理内容
                reasoning_chunk = getattr(delta, 'reasoning_content', None) or ""
                if reasoning_chunk:
                    print(reasoning_chunk, end='', flush=True)
                
                # 处理回答内容
                answer_chunk = getattr(delta, 'content', None) or ""
                if answer_chunk:
                    if not done_reasoning and reasoning_chunk == "":
                        print('\n\n💡 回答:\n')
                        done_reasoning = True
                    print(answer_chunk, end='', flush=True)
                    full_answer += answer_chunk
            
            print("\n" + "="*60)
            return full_answer
            
        except Exception as e:
            error_msg = f"\n❌ 处理响应时出错: {str(e)}"
            print(error_msg)
            return error_msg
    
    def get_summary(self) -> Dict[str, Any]:
        """获取简历摘要统计"""
        work_data = self.data[self.data['type'] == 'Work']
        project_data = self.data[self.data['type'] == 'Project']
        
        summary = {
            "总记录数": len(self.data),
            "工作经历": len(work_data),
            "项目经历": len(project_data),
            "涉及公司": list(self.data['company_organization'].unique()),
            "技能关键词": self._extract_skills()
        }
        return summary
    
    def _extract_skills(self) -> List[str]:
        """提取技能关键词"""
        skills = set()
        
        # 从context中提取Technologies后面的内容
        for _, row in self.data.iterrows():
            context = row.get('context', '')
            
            # 查找Technologies: 后面的内容
            tech_match = re.search(r'Technologies:\s*([^.]+)', context)
            if tech_match:
                tech_text = tech_match.group(1)
                # 按逗号分割并清理
                tech_items = [item.strip() for item in tech_text.split(',')]
                skills.update(tech_items)
        
        return sorted(list(skills))[:10]  # 返回前10个技能
    
    def search_by_company(self, company: str) -> pd.DataFrame:
        """按公司搜索"""
        mask = self.data['company_organization'].str.contains(company, case=False, na=False)
        return self.data[mask]
    
    def search_by_skill(self, skill: str) -> pd.DataFrame:
        """按技能搜索"""
        mask = self.data['context'].str.contains(skill, case=False, na=False)
        return self.data[mask]

def main():
    """主函数 - 交互式问答"""
    print("🚀 简历RAG QA系统启动中...")
    print("=" * 60)
    
    # 获取XLSX文件路径
    xlsx_path = input("📁 请输入XLSX文件路径 (直接回车使用示例数据): ").strip()
    if not xlsx_path:
        xlsx_path = None
    
    try:
        # 初始化系统
        rag_system = ResumeRAGSystem(xlsx_path)
        
        # 显示摘要
        summary = rag_system.get_summary()
        print(f"\n📊 简历摘要:")
        print(f"   总记录数: {summary['总记录数']}")
        print(f"   工作经历: {summary['工作经历']}")
        print(f"   项目经历: {summary['项目经历']}")
        print(f"   涉及公司: {', '.join(summary['涉及公司'][:5])}")
        print(f"   主要技能: {', '.join(summary['技能关键词'][:8])}")
        
        print(f"\n💡 系统已就绪！请输入您的问题")
        print("   输入 'quit' 或 'q' 退出")
        print("   输入 'help' 查看帮助")
        print("=" * 60)
        
        # 交互循环
        while True:
            try:
                question = input("\n🔍 请输入问题: ").strip()
                
                if question.lower() in ['quit', 'exit', '退出', 'q']:
                    print("👋 感谢使用，再见！")
                    break
                
                if question.lower() in ['help', '帮助', 'h']:
                    show_help()
                    continue
                
                if not question:
                    print("❗ 请输入有效问题")
                    continue
                
                # 处理查询
                answer = rag_system.query(question)
                
            except KeyboardInterrupt:
                print("\n\n👋 用户中断，程序退出")
                break
            except Exception as e:
                print(f"\n❌ 发生错误: {str(e)}")
                
    except Exception as e:
        print(f"❌ 系统初始化失败: {str(e)}")

def show_help():
    """显示帮助信息"""
    print(f"\n📖 帮助信息:")
    print(f"   • 询问工作经历: '在百度做了什么工作？'")
    print(f"   • 询问项目经验: '有哪些机器学习项目？'")
    print(f"   • 询问技能: '掌握哪些深度学习技术？'")
    print(f"   • 询问成果: 'Apple实习的主要成果是什么？'")
    print(f"   • 数据分析: '有什么数据分析相关的经验？'")
    print(f"   • 公司对比: '在不同公司的工作有什么区别？'")

def batch_test():
    """批量测试功能"""
    print("🧪 批量测试模式")
    
    rag_system = ResumeRAGSystem()
    
    test_questions = [
        "在百度实习期间做了什么工作？",
        "有哪些机器学习项目经验？",
        "使用过哪些深度学习技术？",
        "在Apple的工作成果是什么？",
        "有什么数据分析经验？",
        "掌握哪些编程技能？"
    ]
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n{'='*60}")
        print(f"测试问题 {i}: {question}")
        print(f"{'='*60}")
        
        try:
            answer = rag_system.query(question, stream=False)
            print(f"\n回答: {answer}")
        except Exception as e:
            print(f"错误: {str(e)}")
        
        input("\n按Enter继续下一个问题...")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "test":
            batch_test()
        elif sys.argv[1] == "help":
            show_help()
        else:
            print("用法:")
            print("  python script.py        # 交互模式")
            print("  python script.py test   # 批量测试")
            print("  python script.py help   # 显示帮助")
    else:
        main()

# 依赖安装命令:
# pip install pandas numpy openai openpyxl