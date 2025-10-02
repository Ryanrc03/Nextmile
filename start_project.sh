#!/bin/bash

# Nextmile 完整项目启动脚本

echo "=========================================="
echo "       🚀 Nextmile 项目启动器"
echo "=========================================="
echo "包含: MongoDB + Chatbot(LangChain RAG) + Frontend"
echo ""

# 检查 Docker 是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker 未安装，请先安装 Docker Desktop"
    echo "📥 下载地址: https://www.docker.com/products/docker-desktop"
    exit 1
fi

# 检查 Docker Compose
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose 未安装，请先安装 Docker Compose"
    exit 1
fi

# 使用新版 docker compose 或旧版 docker-compose
DOCKER_COMPOSE_CMD="docker compose"
if ! docker compose version &> /dev/null; then
    if command -v docker-compose &> /dev/null; then
        DOCKER_COMPOSE_CMD="docker-compose"
    else
        echo "❌ 无法找到 docker compose 或 docker-compose 命令"
        exit 1
    fi
fi

echo "📦 使用 Docker Compose 命令: $DOCKER_COMPOSE_CMD"
echo ""

# 显示菜单
echo "请选择操作:"
echo "1) 🚀 启动完整项目 (前台运行)"
echo "2) 🔧 后台启动完整项目"
echo "3) 🛠️  重新构建并启动"
echo "4) 🛑 停止所有服务"
echo "5) 📋 查看服务状态"
echo "6) 📝 查看日志"
echo "7) 🧹 清理并重建"
echo "8) 📊 显示服务地址"
echo "9) 🔄 重启服务"
echo "0) 👋 退出"
echo ""

read -p "请输入选项 (0-9): " choice

case $choice in
    1)
        echo "🚀 启动完整项目 (前台运行)..."
        $DOCKER_COMPOSE_CMD up
        ;;
    2)
        echo "🔧 后台启动完整项目..."
        $DOCKER_COMPOSE_CMD up -d
        
        echo ""
        echo "✅ 服务已在后台启动!"
        echo ""
        echo "📍 服务地址:"
        echo "   🤖 Chatbot API:     http://localhost:8000"
        echo "   📚 API 文档:        http://localhost:8000/docs"
        echo "   🌐 Frontend:        http://localhost:3000"
        echo "   💾 MongoDB 管理:    http://localhost:8081"
        echo "      (用户名: admin, 密码: admin123)"
        echo ""
        echo "📋 常用命令:"
        echo "   查看状态: $DOCKER_COMPOSE_CMD ps"
        echo "   查看日志: $DOCKER_COMPOSE_CMD logs -f"
        echo "   停止服务: $DOCKER_COMPOSE_CMD down"
        ;;
    3)
        echo "🛠️  重新构建并启动..."
        $DOCKER_COMPOSE_CMD up --build -d
        echo "✅ 服务已重新构建并启动!"
        ;;
    4)
        echo "🛑 停止所有服务..."
        $DOCKER_COMPOSE_CMD down
        echo "✅ 所有服务已停止"
        ;;
    5)
        echo "📋 服务状态:"
        $DOCKER_COMPOSE_CMD ps
        ;;
    6)
        echo "📝 实时查看日志 (Ctrl+C 退出):"
        $DOCKER_COMPOSE_CMD logs -f
        ;;
    7)
        echo "🧹 清理并重建..."
        echo "⚠️  这将删除所有容器、网络和未命名的卷"
        read -p "确认继续? (y/N): " confirm
        if [[ $confirm =~ ^[Yy]$ ]]; then
            $DOCKER_COMPOSE_CMD down
            docker system prune -f
            $DOCKER_COMPOSE_CMD up --build -d
            echo "✅ 清理并重建完成!"
        else
            echo "❌ 操作已取消"
        fi
        ;;
    8)
        echo "📊 服务地址:"
        echo ""
        echo "🤖 Chatbot API (LangChain RAG):"
        echo "   URL: http://localhost:8000"
        echo "   Health: http://localhost:8000/health"
        echo "   Docs: http://localhost:8000/docs"
        echo ""
        echo "🌐 Frontend (Next.js):"
        echo "   URL: http://localhost:3000"
        echo ""
        echo "💾 数据库:"
        echo "   MongoDB: mongodb://localhost:27017"
        echo "   Web 管理: http://localhost:8081"
        echo "   管理员: admin / admin123"
        echo ""
        echo "🔧 测试命令:"
        echo "   curl http://localhost:8000/health"
        echo "   curl -X POST http://localhost:8000/chat -H 'Content-Type: application/json' -d '{\"text\":\"Hello\"}'"
        ;;
    9)
        echo "🔄 重启服务..."
        $DOCKER_COMPOSE_CMD restart
        echo "✅ 服务已重启"
        ;;
    0)
        echo "👋 退出"
        exit 0
        ;;
    *)
        echo "❌ 无效选项，请重新运行脚本"
        exit 1
        ;;
esac

echo ""
echo "🎉 操作完成!"