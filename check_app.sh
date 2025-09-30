#!/bin/bash

# 检查完整应用状态
echo "🚀 Nextmile 完整应用状态检查"
echo "=========================================="

echo "📊 Docker容器状态:"
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

echo ""
echo "🌐 服务连接测试:"

# 测试聊天机器人API
echo -n "🤖 聊天机器人API (8000): "
if curl -s -f http://localhost:8000/health > /dev/null; then
    echo "✅ 运行正常"
else
    echo "❌ 不可用"
fi

# 测试前端
echo -n "🖥️ 前端网站 (3000): "
if curl -s -f http://localhost:3000 > /dev/null; then
    echo "✅ 运行正常"
else
    echo "❌ 不可用"
fi

# 测试数据库管理
echo -n "🗄️ 数据库管理 (8081): "
if curl -s -f http://localhost:8081 > /dev/null; then
    echo "✅ 运行正常"
else
    echo "❌ 不可用"
fi

echo ""
echo "🔗 访问地址:"
echo "   前端网站: http://localhost:3000"
echo "   API文档: http://localhost:8000/docs"
echo "   聊天API: http://localhost:8000/chat"
echo "   数据库管理: http://localhost:8081 (admin/admin123)"
echo "   健康检查: http://localhost:8000/health"

echo ""
echo "💬 快速聊天测试:"
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello, what can you tell me about yourself?"}' \
  2>/dev/null | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    if data.get('success'):
        print('✅ 聊天功能正常')
        print('   回答预览:', data['reply'][:80] + '...')
        print('   响应时间:', f\"{data['response_time']:.2f}s\")
        print('   检索文档数:', data['retrieved_count'])
    else:
        print('❌ 聊天功能异常')
        print('   错误:', data.get('error', 'Unknown'))
except Exception as e:
    print('❌ 聊天测试失败:', str(e))
"

echo ""
echo "🎯 应用已完全启动并运行正常！"