# NextMile 域名部署指南

## 域名信息
- **域名**: nextmile.space
- **服务器 IP**: 18.222.37.37 (EC2 Ohio)
- **域名注册商**: GoDaddy

## 部署架构

```
Internet → GoDaddy DNS → EC2 (18.222.37.37)
                          ↓
                        Nginx (反向代理)
                          ↓
            ┌─────────────┴─────────────┐
            ↓                           ↓
      Frontend (3000)            Backend API (8000)
      Next.js                    FastAPI + MongoDB
```

## 快速部署步骤

### 1. 配置 DNS (在 GoDaddy)

登录 GoDaddy 管理面板，配置以下 DNS 记录：

#### A 记录配置
| 类型 | 名称 | 值 | TTL |
|------|------|-----|-----|
| A | @ | 18.222.37.37 | 600 |
| A | www | 18.222.37.37 | 600 |

**配置步骤**:
1. 登录 [GoDaddy](https://www.godaddy.com/)
2. 进入 "我的产品" → "域名"
3. 找到 `nextmile.space` 点击 "DNS"
4. 点击 "添加" 或编辑现有的 A 记录
5. 添加上述两条 A 记录
6. 保存更改

**验证 DNS 生效**:
```bash
# 检查域名解析
dig nextmile.space
# 或
nslookup nextmile.space

# 应该看到: 18.222.37.37
```

> ⚠️ **注意**: DNS 传播可能需要 5 分钟到 48 小时，通常在 15-30 分钟内生效。

### 2. 运行部署脚本

等待 DNS 生效后，在服务器上执行：

```bash
cd /home/ec2-user/Nextmile

# 给脚本执行权限
chmod +x deploy_domain.sh

# 运行部署脚本 (需要 sudo)
sudo ./deploy_domain.sh
```

脚本会自动完成：
- ✅ 安装 Certbot
- ✅ 配置 Nginx 反向代理
- ✅ 获取 Let's Encrypt SSL 证书
- ✅ 配置 HTTPS
- ✅ 设置证书自动续期
- ✅ 配置防火墙规则

### 3. 启动应用

```bash
cd /home/ec2-user/Nextmile

# 停止现有容器
docker-compose down

# 重新构建并启动
docker-compose up -d --build

# 查看容器状态
docker-compose ps

# 查看日志
docker-compose logs -f
```

### 4. 验证部署

访问以下 URL 验证部署成功：

- 🌐 **前端**: https://nextmile.space
- 🔌 **API 健康检查**: https://nextmile.space/api/health
- 🤖 **聊天机器人**: https://nextmile.space (底部聊天窗口)

## 手动部署步骤（如果自动脚本失败）

### 1. 安装 Certbot

```bash
# Amazon Linux 2023
sudo dnf install -y certbot python3-certbot-nginx

# 或 Amazon Linux 2
sudo amazon-linux-extras install -y epel
sudo yum install -y certbot python-certbot-nginx
```

### 2. 创建证书验证目录

```bash
sudo mkdir -p /var/www/certbot
```

### 3. 配置临时 Nginx (HTTP only)

```bash
sudo tee /etc/nginx/conf.d/nextmile.space.temp.conf > /dev/null << 'EOF'
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
    }
}
EOF

sudo nginx -t
sudo systemctl restart nginx
```

### 4. 获取 SSL 证书

```bash
sudo certbot certonly \
    --webroot \
    --webroot-path=/var/www/certbot \
    --email your-email@example.com \
    --agree-tos \
    --no-eff-email \
    -d nextmile.space \
    -d www.nextmile.space
```

### 5. 应用完整 Nginx 配置

```bash
# 删除临时配置
sudo rm /etc/nginx/conf.d/nextmile.space.temp.conf

# 复制正式配置
sudo cp /home/ec2-user/Nextmile/nginx/nextmile.space.conf /etc/nginx/conf.d/

# 测试并重启
sudo nginx -t
sudo systemctl restart nginx
```

### 6. 配置自动续期

```bash
# 添加 cron job (每天凌晨 3 点检查并续期)
sudo crontab -e
# 添加以下行：
0 3 * * * certbot renew --quiet && systemctl reload nginx
```

## 配置文件说明

### Nginx 配置 (`nginx/nextmile.space.conf`)

- **HTTP (80)**: 自动重定向到 HTTPS
- **HTTPS (443)**: 主要服务端口
  - `/` → Frontend (localhost:3000)
  - `/api/` → Backend API (localhost:8000)
  
### Docker Compose (`docker-compose.yml`)

服务:
- **frontend**: Next.js (端口 3000)
- **chatbot**: FastAPI (端口 8000)
- **mongodb**: MongoDB (端口 27017)
- **mongo-express**: 数据库管理界面 (端口 8081)

### 环境变量

**Frontend** (`.env.production`):
```env
NEXT_PUBLIC_API_URL=https://nextmile.space/api
NEXT_PUBLIC_SITE_URL=https://nextmile.space
NODE_ENV=production
```

**Backend** (`chatbot/config.py`):
- CORS 已配置为允许所有来源
- API 监听 0.0.0.0:8000

## 安全配置

### SSL/TLS
- ✅ Let's Encrypt 免费证书
- ✅ TLS 1.2 和 1.3
- ✅ 强加密套件
- ✅ HTTP 严格传输安全 (HSTS)

### 安全头部
```
Strict-Transport-Security: max-age=31536000; includeSubDomains
X-Frame-Options: SAMEORIGIN
X-Content-Type-Options: nosniff
X-XSS-Protection: 1; mode=block
```

### 防火墙
```bash
# 开放必要端口
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --reload
```

## 故障排查

### 1. 检查 DNS 解析

```bash
# 方法 1: dig
dig nextmile.space +short
# 应该返回: 18.222.37.37

# 方法 2: nslookup
nslookup nextmile.space
```

### 2. 检查端口是否开放

```bash
# 检查 80 和 443 端口
sudo netstat -tlnp | grep -E ':80|:443'

# 或使用 ss
sudo ss -tlnp | grep -E ':80|:443'
```

### 3. 检查 Nginx 状态

```bash
# 查看 Nginx 状态
sudo systemctl status nginx

# 测试配置
sudo nginx -t

# 查看错误日志
sudo tail -f /var/log/nginx/nextmile.space.error.log

# 查看访问日志
sudo tail -f /var/log/nginx/nextmile.space.access.log
```

### 4. 检查 Docker 容器

```bash
cd /home/ec2-user/Nextmile

# 查看所有容器状态
docker-compose ps

# 查看特定容器日志
docker-compose logs frontend
docker-compose logs chatbot
docker-compose logs mongodb

# 实时查看所有日志
docker-compose logs -f
```

### 5. 检查 SSL 证书

```bash
# 查看证书信息
sudo certbot certificates

# 手动测试续期
sudo certbot renew --dry-run

# 查看证书文件
sudo ls -la /etc/letsencrypt/live/nextmile.space/
```

### 6. 测试 API 连接

```bash
# 从服务器内部测试
curl http://localhost:3000
curl http://localhost:8000/health

# 从外部测试 (DNS 生效后)
curl -I https://nextmile.space
curl https://nextmile.space/api/health
```

### 常见问题

#### Q: SSL 证书获取失败
**A**: 确保:
1. DNS 已正确配置并生效
2. 端口 80 和 443 对外开放
3. Nginx 正在运行
4. 防火墙规则正确

```bash
# 检查 AWS Security Group
# 确保入站规则包含:
# - HTTP (80) from 0.0.0.0/0
# - HTTPS (443) from 0.0.0.0/0
```

#### Q: 网站无法访问
**A**: 检查顺序:
1. DNS 是否解析到正确 IP
2. Nginx 是否运行
3. Docker 容器是否启动
4. 防火墙/安全组配置

#### Q: API 请求失败 (CORS)
**A**: 检查 `chatbot/config.py`:
```python
API_CONFIG = {
    "cors_origins": ["*"],  # 或指定域名
    "cors_credentials": True,
    "cors_methods": ["*"],
    "cors_headers": ["*"]
}
```

#### Q: 前端无法连接后端
**A**: 检查环境变量:
```bash
# Frontend/.env.production
NEXT_PUBLIC_API_URL=https://nextmile.space/api
```

## 维护命令

### 重启服务

```bash
# 重启 Nginx
sudo systemctl restart nginx

# 重启 Docker 容器
cd /home/ec2-user/Nextmile
docker-compose restart

# 重启特定容器
docker-compose restart frontend
docker-compose restart chatbot
```

### 更新代码

```bash
cd /home/ec2-user/Nextmile

# 拉取最新代码
git pull

# 重新构建并启动
docker-compose down
docker-compose up -d --build
```

### 查看资源使用

```bash
# Docker 资源使用
docker stats

# 系统资源
htop
# 或
top
```

### 备份

```bash
# 备份 MongoDB 数据
docker exec nextmile_mongodb mongodump --out /data/backup

# 备份配置文件
sudo tar -czf nginx-backup.tar.gz /etc/nginx/conf.d/nextmile.space.conf
```

## 监控和日志

### 日志位置

```bash
# Nginx 日志
/var/log/nginx/nextmile.space.access.log
/var/log/nginx/nextmile.space.error.log

# Docker 日志
docker-compose logs -f frontend
docker-compose logs -f chatbot

# 系统日志
sudo journalctl -u nginx -f
```

### 性能监控

```bash
# 实时请求监控
sudo tail -f /var/log/nginx/nextmile.space.access.log

# Nginx 状态
curl http://localhost/nginx_status  # 需要配置 stub_status
```

## 优化建议

### 1. 启用 Gzip 压缩

在 Nginx 配置中添加:
```nginx
gzip on;
gzip_vary on;
gzip_min_length 1024;
gzip_types text/plain text/css text/xml text/javascript application/json application/javascript application/xml+rss;
```

### 2. 配置缓存

```nginx
# 静态资源缓存
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=my_cache:10m max_size=1g inactive=60m;
```

### 3. 限流

```nginx
# 限制请求速率
limit_req_zone $binary_remote_addr zone=mylimit:10m rate=10r/s;
```

## 联系和支持

- **项目仓库**: https://github.com/Ryanrc03/Nextmile
- **域名**: https://nextmile.space
- **服务器**: AWS EC2 Ohio (us-east-2)

## 更新历史

- **2025-10-05**: 初始域名部署配置
- 域名: nextmile.space
- SSL: Let's Encrypt
- 服务器: EC2 18.222.37.37

---

**祝贺！您的 NextMile 项目现在已经部署到 nextmile.space！** 🎉
