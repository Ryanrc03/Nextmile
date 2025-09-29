#!/usr/bin/env python3
"""
本地RAG调试工具
用于本地测试和优化RAG算法，独立于API服务
"""

import sys
import time
import json
from typing import Dict, List, Any, Optional
from rag_core import ResumeRAGCore
from config import DEFAULT_EXCEL_PATH

class RAGDebugger:
    """RAG算法调试器"""
    
    def __init__(self, xlsx_path: Optional[str] = None, config: Optional[Dict] = None):
        """
        初始化调试器
        
        Args:
            xlsx_path: Excel文件路径
            config: 自定义配置
        """
        print("🚀 初始化RAG调试器...")
        print("=" * 60)
        
        self.rag_core = ResumeRAGCore(xlsx_path, config)
        self.debug_history = []
        
        print(f"✅ RAG系统初始化完成")
        self._show_system_info()
    
    def _show_system_info(self):
        """显示系统信息"""
        summary = self.rag_core.get_summary()
        config = self.rag_core.get_config()
        
        print(f"\n📊 系统概览:")
        print(f"   总记录数: {summary['total_records']}")
        print(f"   工作经历: {summary['work_experience']}")
        print(f"   项目经历: {summary['project_experience']}")
        print(f"   涉及公司: {', '.join(summary['companies_involved'][:3])}{'...' if len(summary['companies_involved']) > 3 else ''}")
        print(f"   关键技能: {', '.join(summary['key_skills'][:5])}{'...' if len(summary['key_skills']) > 5 else ''}")
        
        print(f"\n⚙️ 当前配置:")
        print(f"   模型: {config['model']['model_name']}")
        print(f"   检索Top-K: {config['rag']['similarity_top_k']}")
        print(f"   最低分数阈值: {config['rag']['min_score_threshold']}")
        print(f"   关键词权重: {config['rag']['keyword_weight']}")
    
    def interactive_debug(self):
        """交互式调试模式"""
        print(f"\n💡 进入交互式调试模式")
        print(f"   输入 'quit' 或 'q' 退出")
        print(f"   输入 'help' 或 'h' 查看帮助")
        print(f"   输入 'config' 查看/修改配置")
        print(f"   输入 'stats' 查看统计信息")
        print(f"   输入 'history' 查看调试历史")
        print("=" * 60)
        
        while True:
            try:
                user_input = input("\n🔍 请输入查询 (或命令): ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("👋 退出调试器")
                    break
                
                if user_input.lower() in ['help', 'h']:
                    self._show_help()
                    continue
                
                if user_input.lower() == 'config':
                    self._config_manager()
                    continue
                
                if user_input.lower() == 'stats':
                    self._show_detailed_stats()
                    continue
                
                if user_input.lower() == 'history':
                    self._show_debug_history()
                    continue
                
                if not user_input:
                    print("❗ 请输入有效的查询")
                    continue
                
                # 执行调试查询
                self._debug_query(user_input)
                
            except KeyboardInterrupt:
                print("\n\n👋 用户中断，退出程序")
                break
            except Exception as e:
                print(f"\n❌ 发生错误: {str(e)}")
    
    def _debug_query(self, query: str):
        """调试单个查询"""
        print(f"\n{'='*20} 开始调试查询 {'='*20}")
        print(f"查询: {query}")
        
        start_time = time.time()
        
        # 分步骤调试
        print(f"\n📝 步骤1: 检索相关文档")
        retrieved_docs = self.rag_core.retrieve(query)
        
        if retrieved_docs:
            print(f"✅ 找到 {len(retrieved_docs)} 个相关文档:")
            for i, doc in enumerate(retrieved_docs, 1):
                company = doc['data'].get('company_organization', 'Unknown')
                position = doc['data'].get('position_title', 'Unknown')
                score = doc['score']
                print(f"   {i}. {company} - {position} (相似度: {score:.3f})")
        else:
            print("❌ 未找到相关文档")
        
        print(f"\n📝 步骤2: 生成Prompt")
        prompt = self.rag_core.generate_prompt(query, retrieved_docs)
        print(f"✅ Prompt生成完成 (长度: {len(prompt)} 字符)")
        
        print(f"\n📝 步骤3: 调用AI模型生成回答")
        result = self.rag_core.query(query, stream=False)
        
        if result['success']:
            print(f"✅ 回答生成成功")
            print(f"\n💡 最终回答:")
            print(f"{'-'*40}")
            print(result['answer'])
            print(f"{'-'*40}")
        else:
            print(f"❌ 回答生成失败: {result.get('error', 'Unknown error')}")
        
        total_time = time.time() - start_time
        print(f"\n📊 性能统计:")
        print(f"   总耗时: {total_time:.3f}s")
        print(f"   检索文档数: {result['retrieved_count']}")
        print(f"   AI响应时间: {result['response_time']:.3f}s")
        
        # 保存调试历史
        debug_record = {
            "timestamp": time.time(),
            "query": query,
            "retrieved_count": result['retrieved_count'],
            "response_time": result['response_time'],
            "success": result['success'],
            "answer_length": len(result['answer']) if result['success'] else 0
        }
        self.debug_history.append(debug_record)
        
        # 询问是否显示详细信息
        show_details = input(f"\n🔧 是否显示详细调试信息? (y/n): ").strip().lower()
        if show_details in ['y', 'yes']:
            self._show_detailed_debug_info(query, retrieved_docs, prompt, result)
    
    def _show_detailed_debug_info(self, query: str, retrieved_docs: List[Dict], 
                                prompt: str, result: Dict[str, Any]):
        """显示详细调试信息"""
        print(f"\n🔍 详细调试信息:")
        print(f"{'='*60}")
        
        print(f"\n1. 查询预处理:")
        query_lower = query.lower()
        import re
        query_words = set(re.findall(r'\w+', query_lower))
        print(f"   原始查询: {query}")
        print(f"   小写查询: {query_lower}")
        print(f"   提取词汇: {sorted(query_words)}")
        
        print(f"\n2. 文档检索详情:")
        if retrieved_docs:
            for i, doc in enumerate(retrieved_docs, 1):
                print(f"\n   文档 {i}:")
                print(f"     公司: {doc['data'].get('company_organization', 'N/A')}")
                print(f"     职位: {doc['data'].get('position_title', 'N/A')}")
                print(f"     相似度分数: {doc['score']:.4f}")
                print(f"     内容片段: {doc['data'].get('context', 'N/A')[:100]}...")
        else:
            print("   无相关文档")
        
        print(f"\n3. 生成的Prompt:")
        print(f"   长度: {len(prompt)} 字符")
        if input("   是否显示完整Prompt? (y/n): ").strip().lower() in ['y', 'yes']:
            print(f"\n{'-'*40}")
            print(prompt)
            print(f"{'-'*40}")
        
        print(f"\n4. AI响应详情:")
        print(f"   成功: {result['success']}")
        print(f"   回答长度: {len(result['answer'])} 字符")
        print(f"   响应时间: {result['response_time']:.3f}s")
        
        if not result['success']:
            print(f"   错误信息: {result.get('error', 'N/A')}")
    
    def _show_help(self):
        """显示帮助信息"""
        print(f"\n📖 调试器帮助:")
        print(f"   • 直接输入问题进行调试")
        print(f"   • 'config' - 查看和修改配置")
        print(f"   • 'stats' - 查看详细统计信息")
        print(f"   • 'history' - 查看调试历史")
        print(f"   • 'quit' - 退出调试器")
        print(f"\n📝 示例查询:")
        print(f"   • What work experience do you have at Baidu?")
        print(f"   • Tell me about machine learning projects")
        print(f"   • What technologies have you used?")
        print(f"   • Describe your data science experience")
    
    def _config_manager(self):
        """配置管理器"""
        while True:
            current_config = self.rag_core.get_config()
            print(f"\n⚙️ 当前配置:")
            print(f"1. 检索Top-K: {current_config['rag']['similarity_top_k']}")
            print(f"2. 最低分数阈值: {current_config['rag']['min_score_threshold']}")
            print(f"3. 关键词权重: {current_config['rag']['keyword_weight']}")
            print(f"4. 精确匹配权重: {current_config['rag']['exact_match_weight']}")
            print(f"5. 长度奖励权重: {current_config['rag']['length_bonus_weight']}")
            print(f"6. AI温度参数: {current_config['model']['temperature']}")
            print(f"7. 最大token数: {current_config['model']['max_tokens']}")
            print(f"0. 返回主菜单")
            
            choice = input(f"\n请选择要修改的配置项 (0-7): ").strip()
            
            if choice == '0':
                break
            elif choice == '1':
                new_val = self._get_int_input("检索Top-K", current_config['rag']['similarity_top_k'], 1, 20)
                self.rag_core.update_config({"rag": {"similarity_top_k": new_val}})
            elif choice == '2':
                new_val = self._get_float_input("最低分数阈值", current_config['rag']['min_score_threshold'], 0.0, 1.0)
                self.rag_core.update_config({"rag": {"min_score_threshold": new_val}})
            elif choice == '3':
                new_val = self._get_float_input("关键词权重", current_config['rag']['keyword_weight'], 0.0, 1.0)
                self.rag_core.update_config({"rag": {"keyword_weight": new_val}})
            elif choice == '4':
                new_val = self._get_float_input("精确匹配权重", current_config['rag']['exact_match_weight'], 0.0, 1.0)
                self.rag_core.update_config({"rag": {"exact_match_weight": new_val}})
            elif choice == '5':
                new_val = self._get_float_input("长度奖励权重", current_config['rag']['length_bonus_weight'], 0.0, 1.0)
                self.rag_core.update_config({"rag": {"length_bonus_weight": new_val}})
            elif choice == '6':
                new_val = self._get_float_input("AI温度参数", current_config['model']['temperature'], 0.0, 2.0)
                self.rag_core.update_config({"model": {"temperature": new_val}})
            elif choice == '7':
                new_val = self._get_int_input("最大token数", current_config['model']['max_tokens'], 100, 4000)
                self.rag_core.update_config({"model": {"max_tokens": new_val}})
            else:
                print("❌ 无效选择")
    
    def _get_int_input(self, name: str, current: int, min_val: int, max_val: int) -> int:
        """获取整数输入"""
        while True:
            try:
                new_val = input(f"请输入新的{name} (当前: {current}, 范围: {min_val}-{max_val}): ").strip()
                if not new_val:
                    return current
                new_val = int(new_val)
                if min_val <= new_val <= max_val:
                    print(f"✅ {name}已更新为: {new_val}")
                    return new_val
                else:
                    print(f"❌ 值必须在 {min_val}-{max_val} 范围内")
            except ValueError:
                print("❌ 请输入有效的整数")
    
    def _get_float_input(self, name: str, current: float, min_val: float, max_val: float) -> float:
        """获取浮点数输入"""
        while True:
            try:
                new_val = input(f"请输入新的{name} (当前: {current}, 范围: {min_val:.2f}-{max_val:.2f}): ").strip()
                if not new_val:
                    return current
                new_val = float(new_val)
                if min_val <= new_val <= max_val:
                    print(f"✅ {name}已更新为: {new_val}")
                    return new_val
                else:
                    print(f"❌ 值必须在 {min_val:.2f}-{max_val:.2f} 范围内")
            except ValueError:
                print("❌ 请输入有效的数字")
    
    def _show_detailed_stats(self):
        """显示详细统计信息"""
        summary = self.rag_core.get_summary()
        
        print(f"\n📊 详细统计信息:")
        print(f"{'='*50}")
        
        print(f"\n📈 数据概览:")
        print(f"   总记录数: {summary['total_records']}")
        print(f"   工作经历: {summary['work_experience']}")
        print(f"   项目经历: {summary['project_experience']}")
        
        print(f"\n🏢 涉及公司:")
        for company in summary['companies_involved']:
            count = len(self.rag_core.search_by_company(company))
            print(f"   • {company}: {count} 条记录")
        
        print(f"\n🛠️ 技能统计 (前10个):")
        for i, skill in enumerate(summary['key_skills'][:10], 1):
            count = len(self.rag_core.search_by_skill(skill))
            print(f"   {i:2d}. {skill}: {count} 条记录")
        
        if self.debug_history:
            print(f"\n🔍 调试历史统计:")
            total_queries = len(self.debug_history)
            successful_queries = sum(1 for h in self.debug_history if h['success'])
            avg_response_time = sum(h['response_time'] for h in self.debug_history) / total_queries
            avg_retrieved = sum(h['retrieved_count'] for h in self.debug_history) / total_queries
            
            print(f"   总查询次数: {total_queries}")
            print(f"   成功率: {successful_queries/total_queries*100:.1f}%")
            print(f"   平均响应时间: {avg_response_time:.3f}s")
            print(f"   平均检索文档数: {avg_retrieved:.1f}")
    
    def _show_debug_history(self):
        """显示调试历史"""
        if not self.debug_history:
            print("📝 暂无调试历史")
            return
        
        print(f"\n📝 调试历史 (最近10条):")
        print(f"{'='*80}")
        
        recent_history = self.debug_history[-10:]
        for i, record in enumerate(recent_history, 1):
            status = "✅" if record['success'] else "❌"
            timestamp = time.strftime("%H:%M:%S", time.localtime(record['timestamp']))
            
            print(f"{i:2d}. [{timestamp}] {status} {record['query'][:40]}...")
            print(f"    检索文档: {record['retrieved_count']}, "
                  f"响应时间: {record['response_time']:.3f}s, "
                  f"回答长度: {record.get('answer_length', 0)}")
    
    def batch_test(self, test_queries: Optional[List[str]] = None):
        """批量测试"""
        if test_queries is None:
            test_queries = [
                "What work experience do you have at Baidu?",
                "Tell me about your machine learning projects",
                "What technologies have you used for data analysis?",
                "Describe your achievements at Apple",
                "What programming skills do you have?",
                "What deep learning experience do you have?",
                "Tell me about your internship at Michelin",
                "What A/B testing experience do you have?"
            ]
        
        print(f"🧪 开始批量测试 ({len(test_queries)} 个查询)")
        print(f"{'='*60}")
        
        results = []
        for i, query in enumerate(test_queries, 1):
            print(f"\n📝 测试 {i}/{len(test_queries)}: {query}")
            print(f"{'-'*40}")
            
            start_time = time.time()
            result = self.rag_core.query(query, stream=False)
            test_time = time.time() - start_time
            
            if result['success']:
                print(f"✅ 成功 | 耗时: {test_time:.3f}s | 检索: {result['retrieved_count']}文档")
                print(f"💡 回答: {result['answer'][:100]}...")
            else:
                print(f"❌ 失败 | 错误: {result.get('error', 'Unknown')}")
            
            results.append({
                "query": query,
                "success": result['success'],
                "response_time": test_time,
                "retrieved_count": result['retrieved_count'],
                "answer_length": len(result['answer']) if result['success'] else 0
            })
            
            input("按Enter继续下一个测试...")
        
        # 显示批量测试总结
        self._show_batch_test_summary(results)
    
    def _show_batch_test_summary(self, results: List[Dict[str, Any]]):
        """显示批量测试总结"""
        print(f"\n📊 批量测试总结:")
        print(f"{'='*60}")
        
        total_tests = len(results)
        successful_tests = sum(1 for r in results if r['success'])
        avg_response_time = sum(r['response_time'] for r in results) / total_tests
        avg_retrieved = sum(r['retrieved_count'] for r in results) / total_tests
        avg_answer_length = sum(r['answer_length'] for r in results if r['success']) / max(successful_tests, 1)
        
        print(f"总测试数: {total_tests}")
        print(f"成功率: {successful_tests/total_tests*100:.1f}% ({successful_tests}/{total_tests})")
        print(f"平均响应时间: {avg_response_time:.3f}s")
        print(f"平均检索文档数: {avg_retrieved:.1f}")
        print(f"平均回答长度: {avg_answer_length:.0f} 字符")
        
        # 显示失败的测试
        failed_tests = [r for r in results if not r['success']]
        if failed_tests:
            print(f"\n❌ 失败的测试:")
            for i, test in enumerate(failed_tests, 1):
                print(f"   {i}. {test['query']}")

def main():
    """主函数"""
    print("🔧 RAG算法调试工具")
    print("=" * 60)
    
    # 解析命令行参数
    if len(sys.argv) > 1:
        if sys.argv[1] == "batch":
            # 批量测试模式
            debugger = RAGDebugger()
            debugger.batch_test()
        elif sys.argv[1] == "file" and len(sys.argv) > 2:
            # 指定文件模式
            xlsx_path = sys.argv[2]
            debugger = RAGDebugger(xlsx_path)
            debugger.interactive_debug()
        else:
            print("用法:")
            print("  python rag_debugger.py                # 交互式调试模式")
            print("  python rag_debugger.py batch          # 批量测试模式")
            print("  python rag_debugger.py file <path>    # 指定Excel文件")
    else:
        # 默认交互式模式
        # 询问是否使用自定义Excel文件
        use_custom_file = input("是否使用自定义Excel文件? (y/n): ").strip().lower()
        xlsx_path = None
        
        if use_custom_file in ['y', 'yes']:
            xlsx_path = input(f"请输入Excel文件路径 (默认: {DEFAULT_EXCEL_PATH}): ").strip()
            if not xlsx_path:
                xlsx_path = DEFAULT_EXCEL_PATH
        
        debugger = RAGDebugger(xlsx_path)
        debugger.interactive_debug()

if __name__ == "__main__":
    main()