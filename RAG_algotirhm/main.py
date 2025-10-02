#!/usr/bin/env python3
"""
RAG System Main Entry Point
用于独立测试和调试 RAG 算法
"""

import sys
import os

# 确保能够导入 rag_core 模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rag_system_project.rag_core.rag_simple import ResumeRAGCore


def print_separator():
    """打印分隔线"""
    print("\n" + "="*80 + "\n")


def test_basic_query(rag_system):
    """测试基本查询功能"""
    print("📝 测试基本查询功能")
    print_separator()
    
    test_questions = [
        "候选人有哪些主要技能？",
        "在百度的工作经历是什么？",
        "Tell me about work experience at Apple",
        "What machine learning projects have you done?",
    ]
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n问题 {i}: {question}")
        print("-" * 80)
        
        result = rag_system.query(question)
        
        print(f"\n回答:")
        print(result['answer'])
        print(f"\n检索到 {result['retrieved_count']} 个相关文档，耗时 {result['response_time']:.3f} 秒")
        
        if result['retrieved_count'] > 0:
            print(f"\n相关文档（按相似度排序）:")
            for idx, doc in enumerate(result['retrieved_docs'], 1):
                print(f"  {idx}. {doc['data'].get('company_organization', 'N/A')} - "
                      f"{doc['data'].get('position_title', 'N/A')} "
                      f"(相似度: {doc['score']:.3f})")
        
        print_separator()


def test_summary(rag_system):
    """测试摘要功能"""
    print("\n📊 简历摘要统计")
    print_separator()
    
    summary = rag_system.get_summary()
    
    print(f"总记录数: {summary['total_records']}")
    print(f"工作经历: {summary['work_experience']}")
    print(f"项目经历: {summary['project_experience']}")
    print(f"\n涉及公司:")
    for company in summary['companies_involved']:
        print(f"  - {company}")
    
    print(f"\n关键技能:")
    for skill in summary['key_skills']:
        print(f"  - {skill}")
    
    print_separator()


def interactive_mode(rag_system):
    """交互式查询模式"""
    print("\n💬 交互式查询模式")
    print("输入你的问题，输入 'exit' 或 'quit' 退出")
    print("输入 'summary' 查看简历摘要")
    print("输入 'config' 查看当前配置")
    print_separator()
    
    while True:
        try:
            user_query = input("\n👤 你的问题: ").strip()
            
            if not user_query:
                continue
                
            if user_query.lower() in ['exit', 'quit', 'q']:
                print("\n👋 再见！")
                break
            
            if user_query.lower() == 'summary':
                test_summary(rag_system)
                continue
            
            if user_query.lower() == 'config':
                config = rag_system.get_config()
                print("\n当前配置:")
                print(f"模型: {config['model']['model_name']}")
                print(f"Top K: {config['rag']['similarity_top_k']}")
                print(f"最小相似度阈值: {config['rag']['min_score_threshold']}")
                continue
            
            # 执行查询
            result = rag_system.query(user_query)
            
            print(f"\n🤖 回答:")
            print(result['answer'])
            print(f"\n⏱️  检索到 {result['retrieved_count']} 个相关文档，耗时 {result['response_time']:.3f} 秒")
            
            # 显示检索到的文档
            if result['retrieved_count'] > 0:
                show_docs = input("\n是否查看检索到的文档详情？(y/n): ").strip().lower()
                if show_docs == 'y':
                    print("\n📄 检索到的相关文档:")
                    for idx, doc in enumerate(result['retrieved_docs'], 1):
                        print(f"\n文档 {idx} (相似度: {doc['score']:.3f}):")
                        print(f"  类型: {doc['data'].get('type', 'N/A')}")
                        print(f"  公司/组织: {doc['data'].get('company_organization', 'N/A')}")
                        print(f"  职位/项目: {doc['data'].get('position_title', 'N/A')}")
                        print(f"  详情: {doc['data'].get('context', 'N/A')[:200]}...")
            
        except KeyboardInterrupt:
            print("\n\n👋 再见！")
            break
        except Exception as e:
            print(f"\n❌ 发生错误: {str(e)}")


def main():
    """主函数"""
    print("\n" + "="*80)
    print("🚀 Resume RAG System - 独立测试模式")
    print("="*80)
    
    # 初始化 RAG 系统
    print("\n⚙️  正在初始化 RAG 系统...")
    try:
        rag_system = ResumeRAGCore(xlsx_path=None)  # 使用内置样例数据
        print("✅ RAG 系统初始化成功！")
    except Exception as e:
        print(f"❌ 初始化失败: {str(e)}")
        return
    
    # 显示菜单
    print("\n请选择测试模式:")
    print("1. 运行预设测试用例")
    print("2. 查看简历摘要")
    print("3. 交互式查询模式")
    print("4. 运行所有测试")
    
    try:
        choice = input("\n请输入选项 (1-4，直接回车默认为3): ").strip()
        
        if not choice:
            choice = "3"
        
        if choice == "1":
            test_basic_query(rag_system)
        elif choice == "2":
            test_summary(rag_system)
        elif choice == "3":
            interactive_mode(rag_system)
        elif choice == "4":
            test_summary(rag_system)
            test_basic_query(rag_system)
            print("\n是否进入交互模式？(y/n): ", end="")
            if input().strip().lower() == 'y':
                interactive_mode(rag_system)
        else:
            print("❌ 无效选项，默认进入交互模式")
            interactive_mode(rag_system)
            
    except KeyboardInterrupt:
        print("\n\n👋 程序被中断，再见！")
    except Exception as e:
        print(f"\n❌ 发生错误: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()