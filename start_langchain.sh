#!/bin/bash

# Nextmile LangChain RAG Chatbot 启动脚本

echo "=================================="
echo "  Nextmile LangChain RAG Chatbot"
echo "=================================="
echo ""

# 检查 Docker 是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker 未安装，请先安装 Docker"
    exit 1
fi

if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose 未安装，请先安装 Docker Compose"
    exit 1
fi

# 显示选项
echo "请选择操作:"
echo "1) 启动服务 (docker-compose up)"
echo "2) 后台启动服务 (docker-compose up -d)"
echo "3) 停止服务 (docker-compose down)"
echo "4) 重新构建并启动 (docker-compose up --build)"
echo "5) 查看日志 (docker-compose logs -f)"
echo "6) 查看服务状态"
echo "7) 退出"
echo ""

read -p "请输入选项 (1-7): " choice

case $choice in
    1)
        echo "📦 启动服务..."
        docker-compose -f docker-compose.langchain.yml up
        ;;
    2)
        echo "📦 后台启动服务..."
        docker-compose -f docker-compose.langchain.yml up -d
        echo "✅ 服务已在后台启动"
        echo "📍 API 地址: http://localhost:8000"
        echo "📚 API 文档: http://localhost:8000/docs"
        echo "💾 MongoDB: mongodb://localhost:27017"
        echo ""
        echo "查看日志: docker-compose -f docker-compose.langchain.yml logs -f"
        echo "停止服务: docker-compose -f docker-compose.langchain.yml down"
        ;;
    3)
        echo "🛑 停止服务..."
        docker-compose -f docker-compose.langchain.yml down
        echo "✅ 服务已停止"
        ;;
    4)
        echo "🔨 重新构建并启动服务..."
        docker-compose -f docker-compose.langchain.yml up --build -d
        echo "✅ 服务已重新构建并启动"
        echo "📍 API 地址: http://localhost:8000"
        echo "📚 API 文档: http://localhost:8000/docs"
        ;;
    5)
        echo "📋 查看日志..."
        docker-compose -f docker-compose.langchain.yml logs -f
        ;;
    6)
        echo "📊 服务状态:"
        docker-compose -f docker-compose.langchain.yml ps
        ;;
    7)
        echo "👋 退出"
        exit 0
        ;;
    *)
        echo "❌ 无效选项"
        exit 1
        ;;
esac
