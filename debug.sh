#!/bin/bash
"""
Docker调试启动脚本
"""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔧 Nextmile RAG Chatbot Docker 调试工具${NC}"
echo "=========================================="

# 检查Docker是否运行
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}❌ Docker未运行，请先启动Docker${NC}"
    exit 1
fi

case "${1:-help}" in
    "db-only")
        echo -e "${YELLOW}📦 只启动数据库服务...${NC}"
        docker-compose -f docker-compose.debug.yml up -d mongodb
        echo -e "${GREEN}✅ 数据库启动完成${NC}"
        echo "MongoDB: localhost:27017"
        ;;
    
    "db-admin")
        echo -e "${YELLOW}📦 启动数据库和管理界面...${NC}"
        docker-compose -f docker-compose.debug.yml --profile debug-full up -d mongodb mongo-express
        echo -e "${GREEN}✅ 数据库和管理界面启动完成${NC}"
        echo "MongoDB: localhost:27017"
        echo "Mongo Express: localhost:8081 (admin/admin123)"
        ;;
    
    "chatbot")
        echo -e "${YELLOW}🤖 启动Chatbot调试服务...${NC}"
        docker-compose -f docker-compose.debug.yml --profile debug-api up -d
        echo -e "${GREEN}✅ Chatbot调试服务启动完成${NC}"
        echo "API: localhost:8000"
        echo "API文档: localhost:8000/docs"
        echo "调试端点: localhost:8000/debug/*"
        ;;
    
    "build")
        echo -e "${YELLOW}🔨 重新构建调试镜像...${NC}"
        docker-compose -f docker-compose.debug.yml build chatbot-debug
        echo -e "${GREEN}✅ 镜像构建完成${NC}"
        ;;
    
    "logs")
        SERVICE="${2:-chatbot-debug}"
        echo -e "${YELLOW}📋 查看${SERVICE}日志...${NC}"
        docker-compose -f docker-compose.debug.yml logs -f "$SERVICE"
        ;;
    
    "shell")
        echo -e "${YELLOW}🐚 进入Chatbot容器Shell...${NC}"
        docker exec -it nextmile_chatbot_debug bash
        ;;
    
    "stop")
        echo -e "${YELLOW}🛑 停止所有调试服务...${NC}"
        docker-compose -f docker-compose.debug.yml down
        echo -e "${GREEN}✅ 所有服务已停止${NC}"
        ;;
    
    "clean")
        echo -e "${YELLOW}🧹 清理调试环境...${NC}"
        docker-compose -f docker-compose.debug.yml down -v
        docker image rm nextmile-chatbot-debug 2>/dev/null || true
        echo -e "${GREEN}✅ 调试环境已清理${NC}"
        ;;
    
    "status")
        echo -e "${YELLOW}📊 检查服务状态...${NC}"
        docker-compose -f docker-compose.debug.yml ps
        echo ""
        echo -e "${BLUE}网络连接测试:${NC}"
        curl -s http://localhost:8000/health 2>/dev/null && echo -e "${GREEN}✅ API健康${NC}" || echo -e "${RED}❌ API不可用${NC}"
        ;;
    
    "test")
        echo -e "${YELLOW}🧪 运行调试测试...${NC}"
        python3 local_tester.py health
        ;;
    
    "help"|*)
        echo -e "${BLUE}使用方法:${NC}"
        echo "  $0 db-only     - 只启动MongoDB数据库"
        echo "  $0 db-admin    - 启动数据库+管理界面"
        echo "  $0 chatbot     - 启动完整的Chatbot调试服务"
        echo "  $0 build       - 重新构建调试镜像"
        echo "  $0 logs [服务]  - 查看服务日志"
        echo "  $0 shell       - 进入Chatbot容器"
        echo "  $0 stop        - 停止所有服务"
        echo "  $0 clean       - 清理所有容器和数据"
        echo "  $0 status      - 检查服务状态"
        echo "  $0 test        - 运行调试测试"
        echo ""
        echo -e "${BLUE}常用调试流程:${NC}"
        echo "1. $0 db-only      # 启动数据库"
        echo "2. 本地运行: python3 rag_debugger.py"
        echo "3. $0 chatbot      # 测试Docker环境"
        echo "4. $0 logs         # 查看日志"
        ;;
esac