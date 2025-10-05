#!/bin/bash

# 域名部署脚本
# 用于配置 nextmile.space 域名和 SSL 证书

set -e

echo "=========================================="
echo "NextMile 域名部署脚本"
echo "域名: nextmile.space"
echo "=========================================="

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查是否为 root 用户
if [ "$EUID" -ne 0 ]; then 
    echo -e "${RED}请使用 sudo 运行此脚本${NC}"
    exit 1
fi

# 1. 安装 Certbot (Let's Encrypt)
echo -e "${GREEN}步骤 1: 安装 Certbot...${NC}"
if ! command -v certbot &> /dev/null; then
    echo "安装 Certbot..."
    # Amazon Linux 2023
    dnf install -y certbot python3-certbot-nginx || \
    # 或者 Amazon Linux 2
    amazon-linux-extras install -y epel && yum install -y certbot python-certbot-nginx
else
    echo "Certbot 已安装"
fi

# 2. 创建 certbot webroot 目录
echo -e "${GREEN}步骤 2: 创建 Certbot webroot 目录...${NC}"
mkdir -p /var/www/certbot

# 3. 复制 Nginx 配置文件
echo -e "${GREEN}步骤 3: 配置 Nginx...${NC}"
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cp "$SCRIPT_DIR/nginx/nextmile.space.conf" /etc/nginx/conf.d/nextmile.space.conf

# 4. 测试 Nginx 配置 (使用临时配置)
echo -e "${GREEN}步骤 4: 创建临时 Nginx 配置用于获取证书...${NC}"
cat > /etc/nginx/conf.d/nextmile.space.temp.conf << 'EOF'
server {
    listen 80;
    listen [::]:80;
    server_name nextmile.space www.nextmile.space;

    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }

    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
EOF

# 移除包含 SSL 的配置
rm -f /etc/nginx/conf.d/nextmile.space.conf

# 重启 Nginx
echo "重启 Nginx..."
nginx -t && systemctl restart nginx

# 5. 获取 SSL 证书
echo -e "${GREEN}步骤 5: 获取 Let's Encrypt SSL 证书...${NC}"
echo -e "${YELLOW}注意: 请确保您的域名已经指向此服务器 IP (18.222.37.37)${NC}"
echo -e "${YELLOW}您可以使用 'dig nextmile.space' 或 'nslookup nextmile.space' 验证${NC}"
read -p "域名是否已配置并生效? (yes/no): " dns_ready

if [ "$dns_ready" != "yes" ]; then
    echo -e "${RED}请先在 GoDaddy 配置 DNS 后再运行此脚本${NC}"
    echo ""
    echo "DNS 配置说明："
    echo "1. 登录 GoDaddy"
    echo "2. 找到域名 nextmile.space"
    echo "3. 进入 DNS 管理"
    echo "4. 添加/修改 A 记录："
    echo "   - 类型: A"
    echo "   - 名称: @"
    echo "   - 值: 18.222.37.37"
    echo "   - TTL: 600"
    echo ""
    echo "5. 添加 www 子域名："
    echo "   - 类型: A"
    echo "   - 名称: www"
    echo "   - 值: 18.222.37.37"
    echo "   - TTL: 600"
    echo ""
    exit 1
fi

# 获取证书
certbot certonly \
    --webroot \
    --webroot-path=/var/www/certbot \
    --email your-email@example.com \
    --agree-tos \
    --no-eff-email \
    -d nextmile.space \
    -d www.nextmile.space

# 6. 恢复完整的 Nginx 配置
echo -e "${GREEN}步骤 6: 应用完整的 Nginx 配置...${NC}"
rm -f /etc/nginx/conf.d/nextmile.space.temp.conf
cp "$SCRIPT_DIR/nginx/nextmile.space.conf" /etc/nginx/conf.d/nextmile.space.conf

# 7. 测试并重启 Nginx
echo -e "${GREEN}步骤 7: 测试并重启 Nginx...${NC}"
nginx -t
if [ $? -eq 0 ]; then
    systemctl restart nginx
    echo -e "${GREEN}Nginx 配置成功！${NC}"
else
    echo -e "${RED}Nginx 配置测试失败，请检查配置文件${NC}"
    exit 1
fi

# 8. 配置自动续期
echo -e "${GREEN}步骤 8: 配置 SSL 证书自动续期...${NC}"
# 添加 cron job
(crontab -l 2>/dev/null; echo "0 3 * * * certbot renew --quiet && systemctl reload nginx") | crontab -

# 9. 配置防火墙
echo -e "${GREEN}步骤 9: 配置防火墙规则...${NC}"
if command -v firewall-cmd &> /dev/null; then
    firewall-cmd --permanent --add-service=http
    firewall-cmd --permanent --add-service=https
    firewall-cmd --reload
    echo "防火墙规则已更新"
fi

# 10. 检查 Docker 容器状态
echo -e "${GREEN}步骤 10: 检查 Docker 容器状态...${NC}"
cd "$SCRIPT_DIR"
docker-compose ps

echo ""
echo -e "${GREEN}=========================================="
echo "部署完成！"
echo "==========================================${NC}"
echo ""
echo "您的网站现在可以通过以下地址访问："
echo -e "${GREEN}https://nextmile.space${NC}"
echo -e "${GREEN}https://www.nextmile.space${NC}"
echo ""
echo "SSL 证书将在到期前自动续期"
echo ""
echo "如果遇到问题，请检查："
echo "1. Nginx 日志: tail -f /var/log/nginx/nextmile.space.error.log"
echo "2. Docker 日志: docker-compose logs -f"
echo "3. SSL 证书状态: certbot certificates"
echo ""
