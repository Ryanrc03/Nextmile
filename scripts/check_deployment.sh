#!/bin/bash

#############################################
# 快速检查脚本
# 检查部署后的应用状态
#############################################

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}╔═══════════════════════════════════════╗${NC}"
echo -e "${BLUE}║     Nextmile 部署状态检查            ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════╝${NC}"
echo ""

# 检查 PM2 进程
echo -e "${BLUE}[1] PM2 进程状态:${NC}"
if command -v pm2 &> /dev/null; then
    pm2 status
else
    echo -e "${RED}✗ PM2 未安装${NC}"
fi
echo ""

# 检查 Nginx
echo -e "${BLUE}[2] Nginx 状态:${NC}"
if systemctl is-active --quiet nginx; then
    echo -e "${GREEN}✓ Nginx 运行中${NC}"
    sudo nginx -t 2>&1 | grep -q "successful" && echo -e "${GREEN}✓ 配置文件正确${NC}" || echo -e "${RED}✗ 配置文件有误${NC}"
else
    echo -e "${RED}✗ Nginx 未运行${NC}"
fi
echo ""

# 检查端口监听
echo -e "${BLUE}[3] 端口监听状态:${NC}"
check_port() {
    if netstat -tlnp 2>/dev/null | grep -q ":$1 "; then
        echo -e "${GREEN}✓ 端口 $1 正在监听${NC}"
    else
        echo -e "${RED}✗ 端口 $1 未监听${NC}"
    fi
}

check_port 80
check_port 443
check_port 3000
check_port 8000
echo ""

# 测试服务响应
echo -e "${BLUE}[4] 服务响应测试:${NC}"

# 测试前端
if curl -s -o /dev/null -w "%{http_code}" http://localhost:3000 | grep -q "200\|301\|302"; then
    echo -e "${GREEN}✓ 前端响应正常${NC}"
else
    echo -e "${RED}✗ 前端无响应${NC}"
fi

# 测试 API
if curl -s http://localhost:8000/health &> /dev/null; then
    echo -e "${GREEN}✓ API 响应正常${NC}"
else
    echo -e "${YELLOW}⚠ API 可能无响应或无 health 端点${NC}"
fi
echo ""

# 检查磁盘空间
echo -e "${BLUE}[5] 系统资源:${NC}"
echo "磁盘使用: $(df -h / | awk 'NR==2 {print $5}')"
echo "内存使用: $(free -h | awk 'NR==2 {printf "%.1f%%\n", $3/$2*100}')"
echo "CPU 负载: $(uptime | awk -F'load average:' '{print $2}')"
echo ""

# 检查日志文件
echo -e "${BLUE}[6] 最近的错误日志:${NC}"
if [ -f /var/log/nginx/error.log ]; then
    echo "Nginx 错误 (最近 5 条):"
    sudo tail -5 /var/log/nginx/error.log || echo "无错误日志"
fi
echo ""

# 检查 SSL 证书
echo -e "${BLUE}[7] SSL 证书状态:${NC}"
if command -v certbot &> /dev/null; then
    sudo certbot certificates 2>/dev/null | grep -E "Certificate Name|Expiry Date" || echo "未配置 SSL 证书"
else
    echo "Certbot 未安装"
fi
echo ""

# 快速操作提示
echo -e "${BLUE}╔═══════════════════════════════════════╗${NC}"
echo -e "${BLUE}║     常用命令                          ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════╝${NC}"
echo "查看日志: pm2 logs"
echo "重启应用: pm2 restart all"
echo "重启 Nginx: sudo systemctl restart nginx"
echo "查看 Nginx 日志: sudo tail -f /var/log/nginx/error.log"
echo ""
