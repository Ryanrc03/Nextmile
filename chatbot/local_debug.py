#!/usr/bin/env python3
"""
本地RAG调试工具 - 连接Docker数据库
专门用于本地算法调试，同时可以连接Docker中的MongoDB
"""

import sys
import os
import time
import logging
from typing import Dict, List, Any, Optional

# 设置路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from rag_core import ResumeRAGCore
    from debug_config import DEBUG_CONFIG
except ImportError as e:
    print(f"❌ 导入失败: {e}")
    print("请确保在chatbot目录下运行此脚本")
    sys.exit(1)

class LocalRAGDebugger:
    """本地RAG调试器 - 可连接Docker数据库"""
    
    def __init__(self, use_docker_db: bool = True):
        """
        初始化本地调试器
        
        Args:
            use_docker_db: 是否连接Docker中的MongoDB
        """
        print("🔧 初始化本地RAG调试器...")
        print("=" * 60)
        
        # 使用调试配置
        self.rag_core = ResumeRAGCore(config=DEBUG_CONFIG)
        self.debug_history = []
        self.use_docker_db = use_docker_db
        
        # 配置数据库连接
        if use_docker_db:
            self._setup_docker_db()
        
        print(f"✅ 本地RAG调试器初始化完成")
        self._show_system_info()
    
    def _setup_docker_db(self):
        """设置Docker数据库连接"""
        try:
            from db_config import db_handler
            # 测试连接
            db_handler.client.admin.command('ping')
            print("✅ 已连接到Docker数据库")
            self.db_handler = db_handler
        except Exception as e:
            print(f"⚠️ 无法连接Docker数据库: {e}")
            print("   请确保Docker数据库服务正在运行")
            self.use_docker_db = False
    
    def _show_system_info(self):
        """显示系统信息"""
        summary = self.rag_core.get_summary()
        config = self.rag_core.get_config()
        
        print(f"\n📊 系统概览:")
        print(f"   模式: 本地调试 + {'Docker数据库' if self.use_docker_db else '无数据库'}")
        print(f"   数据记录: {summary['total_records']}")
        print(f"   工作经历: {summary['work_experience']}")
        print(f"   项目经历: {summary['project_experience']}")
        
        print(f"\n⚙️ 调试配置:")
        print(f"   检索Top-K: {config['rag']['similarity_top_k']}")
        print(f"   关键词权重: {config['rag']['keyword_weight']}")
        print(f"   AI温度: {config['model']['temperature']}")
        print(f"   最大Tokens: {config['model']['max_tokens']}")
    
    def debug_query_step_by_step(self, query: str):
        """分步骤调试查询"""
        print(f"\n{'='*20} 开始分步调试 {'='*20}")
        print(f"查询: {query}")
        
        # 步骤1: 检索
        print(f"\n🔍 步骤1: 文档检索")
        start_time = time.time()
        retrieved_docs = self.rag_core.retrieve(query)
        retrieve_time = time.time() - start_time
        
        if retrieved_docs:
            print(f"✅ 检索到 {len(retrieved_docs)} 个文档 (耗时: {retrieve_time:.3f}s)")
            for i, doc in enumerate(retrieved_docs, 1):
                company = doc['data'].get('company_organization', 'Unknown')
                position = doc['data'].get('position_title', 'Unknown')
                score = doc['score']
                print(f"   {i}. {company} - {position}")
                print(f"      相似度: {score:.4f}")
                print(f"      内容预览: {doc['data'].get('context', '')[:80]}...")
        else:
            print("❌ 未检索到相关文档")
        
        # 步骤2: 生成Prompt
        print(f"\n📝 步骤2: Prompt生成")
        start_time = time.time()
        prompt = self.rag_core.generate_prompt(query, retrieved_docs)
        prompt_time = time.time() - start_time
        print(f"✅ Prompt生成完成 (耗时: {prompt_time:.3f}s)")
        print(f"   长度: {len(prompt)} 字符")
        
        show_prompt = input("   是否显示完整Prompt? (y/n): ").lower().strip()
        if show_prompt in ['y', 'yes']:
            print(f"\n{'-'*40}")
            print(prompt)
            print(f"{'-'*40}")
        
        # 步骤3: AI生成
        print(f"\n🤖 步骤3: AI回答生成")
        start_time = time.time()
        response = self.rag_core.generate_response(prompt, stream=False)
        generation_time = time.time() - start_time
        
        print(f"✅ 回答生成完成 (耗时: {generation_time:.3f}s)")
        print(f"\n💡 AI回答:")
        print(f"{'-'*40}")
        print(response)
        print(f"{'-'*40}")
        
        # 总结
        total_time = retrieve_time + prompt_time + generation_time
        print(f"\n📊 性能分析:")
        print(f"   检索时间: {retrieve_time:.3f}s ({retrieve_time/total_time*100:.1f}%)")
        print(f"   Prompt时间: {prompt_time:.3f}s ({prompt_time/total_time*100:.1f}%)")
        print(f"   生成时间: {generation_time:.3f}s ({generation_time/total_time*100:.1f}%)")
        print(f"   总计时间: {total_time:.3f}s")
        
        # 保存到历史
        debug_record = {
            "timestamp": time.time(),
            "query": query,
            "retrieved_count": len(retrieved_docs),
            "retrieve_time": retrieve_time,
            "generation_time": generation_time,
            "total_time": total_time,
            "response_length": len(response)
        }
        self.debug_history.append(debug_record)
        
        # 保存到Docker数据库（如果连接）
        if self.use_docker_db and hasattr(self, 'db_handler'):
            try:
                import asyncio
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                
                conversation_id = loop.run_until_complete(
                    self.db_handler.save_conversation_async(
                        user_query=query,
                        bot_response=response,
                        session_id=f"local_debug_{int(time.time())}",
                        user_id="local_debugger",
                        response_time=total_time,
                        model_used="local_debug",
                        metadata={
                            "debug_mode": True,
                            "retrieved_count": len(retrieved_docs),
                            "retrieve_time": retrieve_time,
                            "generation_time": generation_time
                        }
                    )
                )
                print(f"✅ 调试记录已保存到Docker数据库: {conversation_id}")
            except Exception as e:
                print(f"⚠️ 保存到数据库失败: {e}")
    
    def compare_configurations(self, query: str, configs: List[Dict]):
        """比较不同配置的效果"""
        print(f"\n🔬 配置对比测试")
        print(f"查询: {query}")
        print(f"测试配置数量: {len(configs)}")
        
        results = []
        original_config = self.rag_core.get_config()
        
        for i, config in enumerate(configs, 1):
            print(f"\n--- 配置 {i} ---")
            print(f"参数: {config}")
            
            # 更新配置
            self.rag_core.update_config(config)
            
            # 测试查询
            start_time = time.time()
            result = self.rag_core.query(query, stream=False)
            test_time = time.time() - start_time
            
            if result['success']:
                print(f"✅ 成功 - 耗时: {test_time:.3f}s")
                print(f"检索文档: {result['retrieved_count']}")
                print(f"回答预览: {result['answer'][:80]}...")
                
                results.append({
                    "config": config,
                    "success": True,
                    "response_time": test_time,
                    "retrieved_count": result['retrieved_count'],
                    "answer_length": len(result['answer'])
                })
            else:
                print(f"❌ 失败: {result.get('error', 'Unknown')}")
                results.append({
                    "config": config,
                    "success": False,
                    "error": result.get('error', 'Unknown')
                })
        
        # 恢复原配置
        self.rag_core.update_config(original_config)
        
        # 显示对比结果
        print(f"\n📊 配置对比结果:")
        successful_results = [r for r in results if r['success']]
        
        if successful_results:
            best_result = min(successful_results, key=lambda x: x['response_time'])
            print(f"🏆 最快配置: {best_result['response_time']:.3f}s")
            print(f"   参数: {best_result['config']}")
            
            avg_time = sum(r['response_time'] for r in successful_results) / len(successful_results)
            print(f"📈 平均响应时间: {avg_time:.3f}s")
        
        return results
    
    def interactive_debug(self):
        """交互式调试"""
        print(f"\n💡 进入交互式调试模式")
        print(f"   'quit' - 退出")
        print(f"   'config' - 配置管理")
        print(f"   'compare' - 配置对比")
        print(f"   'history' - 调试历史")
        print(f"   'docker' - Docker服务状态")
        print("=" * 60)
        
        while True:
            try:
                user_input = input("\n🔍 请输入查询或命令: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("👋 退出调试器")
                    break
                
                if user_input.lower() == 'config':
                    self._config_manager()
                    continue
                
                if user_input.lower() == 'compare':
                    self._run_config_comparison()
                    continue
                
                if user_input.lower() == 'history':
                    self._show_debug_history()
                    continue
                
                if user_input.lower() == 'docker':
                    self._check_docker_status()
                    continue
                
                if not user_input:
                    print("❗ 请输入有效的查询")
                    continue
                
                # 执行分步调试
                self.debug_query_step_by_step(user_input)
                
            except KeyboardInterrupt:
                print("\n\n👋 用户中断，退出程序")
                break
            except Exception as e:
                print(f"\n❌ 发生错误: {str(e)}")
    
    def _config_manager(self):
        """配置管理"""
        current_config = self.rag_core.get_config()
        
        print(f"\n⚙️ 当前配置:")
        print(f"1. 检索Top-K: {current_config['rag']['similarity_top_k']}")
        print(f"2. 关键词权重: {current_config['rag']['keyword_weight']}")
        print(f"3. 精确匹配权重: {current_config['rag']['exact_match_weight']}")
        print(f"4. AI温度: {current_config['model']['temperature']}")
        print(f"5. 最大Tokens: {current_config['model']['max_tokens']}")
        
        choice = input(f"\n选择要修改的配置项 (1-5, 回车跳过): ").strip()
        
        if choice == '1':
            new_val = input(f"新的Top-K值 (当前: {current_config['rag']['similarity_top_k']}): ")
            if new_val:
                self.rag_core.update_config({"rag": {"similarity_top_k": int(new_val)}})
        elif choice == '2':
            new_val = input(f"新的关键词权重 (当前: {current_config['rag']['keyword_weight']}): ")
            if new_val:
                self.rag_core.update_config({"rag": {"keyword_weight": float(new_val)}})
        elif choice == '4':
            new_val = input(f"新的AI温度 (当前: {current_config['model']['temperature']}): ")
            if new_val:
                self.rag_core.update_config({"model": {"temperature": float(new_val)}})
    
    def _run_config_comparison(self):
        """运行配置对比"""
        query = input("请输入测试查询: ").strip()
        if not query:
            return
        
        # 预定义几种配置
        configs = [
            {"rag": {"similarity_top_k": 3, "keyword_weight": 0.8}},
            {"rag": {"similarity_top_k": 5, "keyword_weight": 0.6}},
            {"rag": {"similarity_top_k": 3, "keyword_weight": 0.5}},
            {"model": {"temperature": 0.3}},
            {"model": {"temperature": 0.8}}
        ]
        
        self.compare_configurations(query, configs)
    
    def _show_debug_history(self):
        """显示调试历史"""
        if not self.debug_history:
            print("📝 暂无调试历史")
            return
        
        print(f"\n📝 调试历史 (最近10条):")
        recent = self.debug_history[-10:]
        
        for i, record in enumerate(recent, 1):
            timestamp = time.strftime("%H:%M:%S", time.localtime(record['timestamp']))
            print(f"{i:2d}. [{timestamp}] {record['query'][:40]}...")
            print(f"    检索: {record['retrieved_count']}, 总时间: {record['total_time']:.3f}s")
    
    def _check_docker_status(self):
        """检查Docker服务状态"""
        print(f"\n🐳 Docker服务状态检查:")
        
        try:
            import requests
            
            # 检查API服务
            try:
                response = requests.get("http://localhost:8000/health", timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    print(f"✅ Docker API服务: {data.get('status', 'unknown')}")
                    print(f"   数据库: {data.get('database', 'unknown')}")
                    print(f"   RAG系统: {data.get('rag_system', 'unknown')}")
                else:
                    print(f"❌ Docker API服务异常: {response.status_code}")
            except Exception as e:
                print(f"❌ Docker API服务不可用: {e}")
            
            # 检查数据库连接
            if self.use_docker_db and hasattr(self, 'db_handler'):
                try:
                    self.db_handler.client.admin.command('ping')
                    print(f"✅ Docker数据库连接正常")
                except Exception as e:
                    print(f"❌ Docker数据库连接失败: {e}")
            else:
                print(f"⚠️ 未连接Docker数据库")
                
        except ImportError:
            print(f"❌ 无法检查Docker状态: 缺少requests库")

def main():
    """主函数"""
    print("🔧 本地RAG调试器 (支持Docker数据库)")
    print("=" * 60)
    
    # 检查是否连接Docker数据库
    use_docker = input("是否连接Docker数据库? (y/n, 默认y): ").strip().lower()
    use_docker_db = use_docker != 'n'
    
    try:
        debugger = LocalRAGDebugger(use_docker_db)
        
        if len(sys.argv) > 1:
            # 命令行模式
            query = ' '.join(sys.argv[1:])
            debugger.debug_query_step_by_step(query)
        else:
            # 交互模式
            debugger.interactive_debug()
            
    except Exception as e:
        print(f"❌ 调试器启动失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()