#!/usr/bin/env python3
"""
本地测试脚本 - 快速测试Docker环境中的各种功能
"""

import requests
import json
import time
import sys

class LocalTester:
    def __init__(self):
        self.base_url = "http://localhost:8000"
        self.frontend_url = "http://localhost:3000"
        self.mongo_express_url = "http://localhost:8081"
        
    def test_health(self):
        """测试健康检查"""
        print("🏥 测试健康检查...")
        try:
            response = requests.get(f"{self.base_url}/health")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ API健康状态: {data['status']}")
                print(f"   数据库状态: {data['database']}")
                print(f"   RAG系统状态: {data['rag_system']}")
                return True
            else:
                print(f"❌ 健康检查失败: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ 连接失败: {e}")
            return False
    
    def test_chat(self, question="What work experience do you have?"):
        """测试聊天功能"""
        print(f"💬 测试聊天功能...")
        print(f"   问题: {question}")
        
        try:
            payload = {"text": question}
            response = requests.post(f"{self.base_url}/chat", json=payload)
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ 聊天成功!")
                print(f"   回答: {data['reply'][:100]}...")
                print(f"   检索文档数: {data['retrieved_count']}")
                print(f"   响应时间: {data['response_time']:.3f}s")
                print(f"   会话ID: {data['session_id']}")
                return data['session_id']
            else:
                print(f"❌ 聊天失败: {response.status_code}")
                print(f"   错误: {response.text}")
                return None
        except Exception as e:
            print(f"❌ 聊天请求失败: {e}")
            return None
    
    def test_system_info(self):
        """测试系统信息"""
        print("📊 测试系统信息...")
        try:
            response = requests.get(f"{self.base_url}/system/info")
            if response.status_code == 200:
                data = response.json()
                summary = data['rag_summary']
                print(f"✅ 系统信息获取成功!")
                print(f"   总记录数: {summary['total_records']}")
                print(f"   工作经历: {summary['work_experience']}")
                print(f"   项目经历: {summary['project_experience']}")
                print(f"   涉及公司: {len(summary['companies_involved'])} 个")
                print(f"   关键技能: {len(summary['key_skills'])} 个")
                return True
            else:
                print(f"❌ 系统信息获取失败: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ 系统信息请求失败: {e}")
            return False
    
    def test_admin_stats(self):
        """测试管理统计"""
        print("📈 测试管理统计...")
        try:
            response = requests.get(f"{self.base_url}/admin/stats")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ 管理统计获取成功!")
                print(f"   总对话数: {data['total_conversations']}")
                print(f"   最近7天对话: {data['recent_conversations']}")
                if data['response_time_stats']:
                    stats = data['response_time_stats']
                    print(f"   平均响应时间: {stats['avg_response_time']:.3f}s")
                    print(f"   最大响应时间: {stats['max_response_time']:.3f}s")
                    print(f"   最小响应时间: {stats['min_response_time']:.3f}s")
                return True
            else:
                print(f"❌ 管理统计获取失败: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ 管理统计请求失败: {e}")
            return False
    
    def test_history(self, session_id):
        """测试历史记录"""
        print(f"📝 测试历史记录...")
        try:
            response = requests.get(f"{self.base_url}/history/{session_id}")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ 历史记录获取成功!")
                print(f"   会话ID: {data['session_id']}")
                print(f"   历史记录数: {data['count']}")
                return True
            else:
                print(f"❌ 历史记录获取失败: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ 历史记录请求失败: {e}")
            return False
    
    def test_multiple_questions(self):
        """测试多个问题"""
        questions = [
            "What work experience do you have at Baidu?",
            "Tell me about your machine learning projects",
            "What data science experience do you have?",
            "What technologies have you used?",
            "Describe your achievements at Apple"
        ]
        
        print(f"🎯 测试多个问题 ({len(questions)} 个)...")
        results = []
        
        for i, question in enumerate(questions, 1):
            print(f"\n   {i}. {question}")
            start_time = time.time()
            session_id = self.test_chat(question)
            test_time = time.time() - start_time
            
            results.append({
                "question": question,
                "success": session_id is not None,
                "session_id": session_id,
                "test_time": test_time
            })
            
            time.sleep(1)  # 避免请求过快
        
        # 统计结果
        successful = sum(1 for r in results if r['success'])
        avg_time = sum(r['test_time'] for r in results) / len(results)
        
        print(f"\n📊 测试结果总结:")
        print(f"   成功率: {successful}/{len(questions)} ({successful/len(questions)*100:.1f}%)")
        print(f"   平均测试时间: {avg_time:.3f}s")
        
        return results
    
    def show_service_urls(self):
        """显示服务URL"""
        print("🌐 服务URL信息:")
        print(f"   🤖 聊天API: {self.base_url}")
        print(f"   📖 API文档: {self.base_url}/docs")
        print(f"   🏥 健康检查: {self.base_url}/health")
        print(f"   📊 系统信息: {self.base_url}/system/info")
        print(f"   🖥️ 前端网站: {self.frontend_url}")
        print(f"   🗄️ 数据库管理: {self.mongo_express_url}")
        print(f"      用户名: admin")
        print(f"      密码: admin123")
    
    def run_full_test(self):
        """运行完整测试"""
        print("🚀 开始完整测试...")
        print("=" * 60)
        
        # 1. 健康检查
        if not self.test_health():
            print("❌ 健康检查失败，请检查服务是否正常启动")
            return False
        
        print()
        
        # 2. 系统信息
        self.test_system_info()
        print()
        
        # 3. 单个聊天测试
        session_id = self.test_chat("What is your background?")
        print()
        
        # 4. 历史记录测试
        if session_id:
            self.test_history(session_id)
            print()
        
        # 5. 管理统计测试
        self.test_admin_stats()
        print()
        
        # 6. 多问题测试
        self.test_multiple_questions()
        print()
        
        # 7. 显示服务URL
        self.show_service_urls()
        
        print("\n✅ 完整测试完成!")
        return True

def main():
    """主函数"""
    print("🧪 Nextmile RAG系统 - 本地测试工具")
    print("=" * 60)
    
    tester = LocalTester()
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "health":
            tester.test_health()
        elif command == "chat":
            question = sys.argv[2] if len(sys.argv) > 2 else "What is your background?"
            tester.test_chat(question)
        elif command == "info":
            tester.test_system_info()
        elif command == "stats":
            tester.test_admin_stats()
        elif command == "multi":
            tester.test_multiple_questions()
        elif command == "urls":
            tester.show_service_urls()
        elif command == "full":
            tester.run_full_test()
        else:
            print("❌ 未知命令")
            print("可用命令: health, chat, info, stats, multi, urls, full")
    else:
        # 交互式菜单
        while True:
            print("\n请选择测试:")
            print("1. 健康检查")
            print("2. 聊天测试")
            print("3. 系统信息")
            print("4. 管理统计")
            print("5. 多问题测试")
            print("6. 显示服务URL")
            print("7. 完整测试")
            print("0. 退出")
            
            choice = input("\n请输入选择 (0-7): ").strip()
            
            if choice == '0':
                print("👋 再见!")
                break
            elif choice == '1':
                tester.test_health()
            elif choice == '2':
                question = input("请输入问题 (回车使用默认): ").strip()
                if not question:
                    question = "What is your background?"
                tester.test_chat(question)
            elif choice == '3':
                tester.test_system_info()
            elif choice == '4':
                tester.test_admin_stats()
            elif choice == '5':
                tester.test_multiple_questions()
            elif choice == '6':
                tester.show_service_urls()
            elif choice == '7':
                tester.run_full_test()
            else:
                print("❌ 无效选择")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 用户中断，退出程序")
    except Exception as e:
        print(f"\n❌ 程序异常: {e}")