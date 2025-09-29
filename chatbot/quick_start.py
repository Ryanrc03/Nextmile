#!/usr/bin/env python3
"""
快速开始脚本 - 演示如何使用重构后的RAG系统
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def demo_rag_core():
    """演示RAG核心功能"""
    print("🚀 演示RAG核心功能")
    print("=" * 50)
    
    try:
        from rag_core import ResumeRAGCore
        
        # 初始化RAG系统
        print("正在初始化RAG系统...")
        rag = ResumeRAGCore()
        
        # 显示系统摘要
        summary = rag.get_summary()
        print(f"\n📊 系统摘要:")
        print(f"  总记录数: {summary['total_records']}")
        print(f"  工作经历: {summary['work_experience']}")
        print(f"  项目经历: {summary['project_experience']}")
        
        # 示例查询
        test_queries = [
            "What work experience do you have at Baidu?",
            "Tell me about your machine learning projects",
            "What data science experience do you have?"
        ]
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n🔍 示例查询 {i}: {query}")
            print("-" * 40)
            
            result = rag.query(query)
            
            if result['success']:
                print(f"✅ 回答: {result['answer'][:200]}...")
                print(f"📊 检索到 {result['retrieved_count']} 个相关文档")
                print(f"⏱️ 响应时间: {result['response_time']:.3f}s")
            else:
                print(f"❌ 查询失败: {result.get('error', 'Unknown error')}")
        
        print(f"\n✅ RAG核心功能演示完成!")
        
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        print("请确保已安装所需依赖: pip install openai pandas numpy")
    except Exception as e:
        print(f"❌ 运行失败: {e}")

def demo_debugger():
    """演示调试器功能"""
    print("\n🔧 启动RAG调试器")
    print("=" * 50)
    
    try:
        from rag_debugger import RAGDebugger
        
        debugger = RAGDebugger()
        
        # 运行一个简单的调试会话
        print("\n运行调试示例...")
        debugger._debug_query("What technologies have you used?")
        
        print(f"\n💡 提示: 运行 'python rag_debugger.py' 进入完整的交互式调试模式")
        
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
    except Exception as e:
        print(f"❌ 运行失败: {e}")

def show_api_info():
    """显示API服务器信息"""
    print("\n🌐 API服务器信息")
    print("=" * 50)
    
    print("新的API服务器文件: api_server.py")
    print("启动命令: python api_server.py")
    print("API文档: http://localhost:8000/docs")
    print("健康检查: http://localhost:8000/health")
    print("\n主要端点:")
    print("  POST /chat - 聊天对话")
    print("  GET /history/{session_id} - 获取历史")
    print("  GET /system/info - 系统信息")
    print("  GET /admin/* - 管理功能")

def show_file_structure():
    """显示新的文件结构"""
    print("\n📁 重构后的文件结构")
    print("=" * 50)
    
    structure = """
chatbot/
├── config.py           # 配置文件 (新)
├── rag_core.py         # RAG核心算法 (新)
├── rag_debugger.py     # 本地调试工具 (新) 
├── api_server.py       # API服务器 (新)
├── quick_start.py      # 快速开始脚本 (新)
├── rag_en.py          # 原始文件 (保留)
├── admin_api.py       # 管理API (保留)
├── db_config.py       # 数据库配置 (保留)
└── requirements.txt   # 依赖列表 (保留)
"""
    print(structure)
    
    print("📝 文件说明:")
    print("• config.py - 集中管理所有配置参数")
    print("• rag_core.py - 纯算法实现，可独立使用和测试")
    print("• rag_debugger.py - 强大的本地调试工具")
    print("• api_server.py - 清洁的API服务，调用rag_core")
    print("• quick_start.py - 演示如何使用各个模块")

def show_usage_examples():
    """显示使用示例"""
    print("\n💡 使用示例")
    print("=" * 50)
    
    examples = """
1. 本地调试RAG算法:
   python rag_debugger.py

2. 批量测试:
   python rag_debugger.py batch

3. 使用自定义Excel文件:
   python rag_debugger.py file your_file.xlsx

4. 启动API服务器:
   python api_server.py

5. 在Python代码中使用RAG核心:
   from rag_core import ResumeRAGCore
   rag = ResumeRAGCore("your_file.xlsx")
   result = rag.query("你的问题")

6. 自定义配置:
   config = {
       "rag": {"similarity_top_k": 3},
       "model": {"temperature": 0.5}
   }
   rag = ResumeRAGCore(config=config)
"""
    print(examples)

def main():
    """主函数"""
    print("🎯 Nextmile RAG系统 - 快速开始指南")
    print("=" * 60)
    
    while True:
        print("\n请选择操作:")
        print("1. 演示RAG核心功能")
        print("2. 演示调试器功能")
        print("3. 显示API服务器信息")
        print("4. 显示文件结构")
        print("5. 显示使用示例")
        print("0. 退出")
        
        choice = input("\n请输入选择 (0-5): ").strip()
        
        if choice == '0':
            print("👋 再见!")
            break
        elif choice == '1':
            demo_rag_core()
        elif choice == '2':
            demo_debugger()
        elif choice == '3':
            show_api_info()
        elif choice == '4':
            show_file_structure()
        elif choice == '5':
            show_usage_examples()
        else:
            print("❌ 无效选择，请重试")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "demo":
            demo_rag_core()
        elif sys.argv[1] == "debug":
            demo_debugger()
        elif sys.argv[1] == "info":
            show_api_info()
        else:
            print("用法:")
            print("  python quick_start.py       # 交互式菜单")
            print("  python quick_start.py demo  # 直接运行RAG演示")
            print("  python quick_start.py debug # 直接运行调试演示")
            print("  python quick_start.py info  # 显示API信息")
    else:
        main()