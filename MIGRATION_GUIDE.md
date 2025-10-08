# 项目迁移到新 AWS EC2 服务器指南

本指南将帮助您将 Nextmile 项目完整迁移到新的 AWS EC2 服务器，并配置新域名。

## 📋 迁移前准备

### 1. 新服务器信息
准备以下信息：
- [ ] 新服务器 IP 地址
- [ ] 新域名（如果有）
- [ ] SSH 密钥文件路径
- [ ] 数据库访问信息
- [ ] 必要的 API 密钥和环境变量

### 2. 旧服务器备份
```bash
# 在旧服务器上执行数据备份
cd /home/ec2-user/Nextmile
./scripts/backup_before_migration.sh
```

## 🚀 自动化部署步骤

### 步骤 1: 在新服务器上准备环境

SSH 登录到新的 EC2 实例：
```bash
ssh -i "your-key.pem" ec2-user@<NEW_SERVER_IP>
```

### 步骤 2: 运行初始化脚本

```bash
# 下载初始化脚本
curl -O https://raw.githubusercontent.com/Ryanrc03/Nextmile/main/scripts/init_new_server.sh

# 或者如果已经克隆了代码
git clone https://github.com/Ryanrc03/Nextmile.git
cd Nextmile

# 给脚本执行权限
chmod +x scripts/init_new_server.sh

# 运行初始化脚本
sudo ./scripts/init_new_server.sh
```

### 步骤 3: 配置环境变量

```bash
# 编辑配置文件
nano .env.production

# 必须修改的配置项：
# - DATABASE_HOST=<新的数据库地址>
# - NEXT_PUBLIC_API_URL=https://<你的新域名>
# - SERVER_IP=<新服务器IP>
```

### 步骤 4: 运行自动部署脚本

```bash
# 使用自动部署脚本
./scripts/deploy_to_new_server.sh --domain <your-domain.com>

# 或者手动指定所有参数
./scripts/deploy_to_new_server.sh \
  --domain nextmile.space \
  --email your-email@example.com \
  --db-host localhost \
  --db-name nextmile_db
```

### 步骤 5: 数据迁移

```bash
# 从旧服务器导入数据
./scripts/migrate_data.sh --from <OLD_SERVER_IP> --ssh-key /path/to/key.pem
```

## 🔧 手动部署步骤（如果自动脚本失败）

### 1. 系统环境安装

```bash
# 更新系统
sudo yum update -y

# 安装 Node.js
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
source ~/.bashrc
nvm install 18
nvm use 18

# 安装 Python 3.10+
sudo yum install python3.10 python3.10-pip -y

# 安装 Docker 和 Docker Compose
sudo yum install docker -y
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker ec2-user

# 安装 Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 安装 Nginx
sudo yum install nginx -y

# 安装 PM2
npm install -g pm2
npm install -g pnpm
```

### 2. 克隆项目代码

```bash
cd /home/ec2-user
git clone https://github.com/Ryanrc03/Nextmile.git
cd Nextmile
```

### 3. 配置环境变量

```bash
# 复制环境变量模板
cp .env.example .env.production

# 编辑环境变量
nano .env.production
```

必须配置的环境变量：
```bash
# API 配置
NEXT_PUBLIC_API_URL=https://your-domain.com
API_PORT=8000

# 数据库配置
DATABASE_HOST=localhost
DATABASE_PORT=3306
DATABASE_NAME=nextmile_db
DATABASE_USER=your_db_user
DATABASE_PASSWORD=your_db_password

# Redis 配置
REDIS_HOST=localhost
REDIS_PORT=6379

# OpenAI API (如果使用)
OPENAI_API_KEY=your_openai_key

# 邮件服务 (如果使用)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_password
```

### 4. 安装项目依赖

```bash
# Frontend 依赖
cd Frontend
pnpm install
cd ..

# Chatbot 依赖
cd chatbot
pip3 install -r requirements.txt
cd ..
```

### 5. 构建前端

```bash
cd Frontend
pnpm build
cd ..
```

### 6. 配置 Nginx

```bash
# 复制 Nginx 配置
sudo cp nginx/nextmile.space.conf /etc/nginx/conf.d/

# 编辑配置文件，替换域名
sudo nano /etc/nginx/conf.d/nextmile.space.conf
```

修改以下内容：
- `server_name` 改为你的新域名
- 确认前端和后端的 `proxy_pass` 端口正确

### 7. 配置 SSL 证书

```bash
# 安装 Certbot
sudo yum install certbot python3-certbot-nginx -y

# 获取 SSL 证书
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# 测试自动续期
sudo certbot renew --dry-run
```

### 8. 配置防火墙

```bash
# 开放必要端口
sudo firewall-cmd --permanent --add-port=80/tcp
sudo firewall-cmd --permanent --add-port=443/tcp
sudo firewall-cmd --permanent --add-port=8000/tcp
sudo firewall-cmd --reload

# 或者关闭防火墙（不推荐生产环境）
# sudo systemctl stop firewalld
# sudo systemctl disable firewalld
```

在 AWS 控制台配置安全组：
- HTTP (80)
- HTTPS (443)
- Custom TCP (8000) - 如果需要直接访问 API
- SSH (22) - 限制到你的 IP

### 9. 启动数据库（使用 Docker）

```bash
# 启动 MySQL 或其他数据库
docker-compose up -d mysql

# 或者安装本地 MySQL
sudo yum install mysql-server -y
sudo systemctl start mysqld
sudo systemctl enable mysqld

# 创建数据库
mysql -u root -p
CREATE DATABASE nextmile_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'nextmile_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON nextmile_db.* TO 'nextmile_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### 10. 数据迁移

从旧服务器导出数据：
```bash
# 在旧服务器上
mysqldump -u username -p nextmile_db > nextmile_backup.sql
```

在新服务器上导入：
```bash
# 传输文件到新服务器
scp -i your-key.pem ec2-user@old-server:/path/to/nextmile_backup.sql .

# 导入数据
mysql -u nextmile_user -p nextmile_db < nextmile_backup.sql
```

### 11. 启动应用

```bash
# 启动后端 API
cd chatbot
pm2 start api_server.py --name nextmile-api --interpreter python3
cd ..

# 启动前端
cd Frontend
pm2 start npm --name nextmile-frontend -- start
cd ..

# 保存 PM2 配置
pm2 save
pm2 startup

# 启动 Nginx
sudo systemctl start nginx
sudo systemctl enable nginx
```

### 12. 验证部署

```bash
# 检查服务状态
pm2 status
sudo systemctl status nginx

# 检查端口监听
sudo netstat -tulpn | grep LISTEN

# 测试 API
curl http://localhost:8000/health

# 测试前端
curl http://localhost:3000

# 查看日志
pm2 logs nextmile-api
pm2 logs nextmile-frontend
sudo tail -f /var/log/nginx/error.log
```

## 🔍 故障排查

### 前端无法访问
```bash
# 检查前端进程
pm2 logs nextmile-frontend

# 检查端口占用
sudo lsof -i :3000

# 重启前端
pm2 restart nextmile-frontend
```

### API 无法访问
```bash
# 检查后端日志
pm2 logs nextmile-api

# 检查 Python 依赖
pip3 list

# 测试数据库连接
cd chatbot
python3 -c "from db_config import *; print('DB connected')"
```

### Nginx 配置错误
```bash
# 测试配置文件
sudo nginx -t

# 查看错误日志
sudo tail -f /var/log/nginx/error.log

# 重启 Nginx
sudo systemctl restart nginx
```

### SSL 证书问题
```bash
# 检查证书状态
sudo certbot certificates

# 手动续期
sudo certbot renew

# 重新获取证书
sudo certbot --nginx -d your-domain.com --force-renewal
```

## 📊 性能优化

### PM2 集群模式
```bash
# 使用集群模式启动前端
pm2 start npm --name nextmile-frontend -i max -- start
```

### Nginx 缓存优化
编辑 `/etc/nginx/conf.d/nextmile.space.conf`，添加：
```nginx
# 静态资源缓存
location ~* \.(jpg|jpeg|png|gif|ico|css|js|woff|woff2)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}

# Gzip 压缩
gzip on;
gzip_vary on;
gzip_types text/plain text/css application/json application/javascript text/xml application/xml;
```

## 🔐 安全加固

```bash
# 配置防火墙
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --reload

# 禁用 root SSH 登录
sudo nano /etc/ssh/sshd_config
# 设置: PermitRootLogin no
sudo systemctl restart sshd

# 配置自动安全更新
sudo yum install yum-cron -y
sudo systemctl enable yum-cron
sudo systemctl start yum-cron
```

## 📝 DNS 配置

在你的域名注册商（如 GoDaddy、Namecheap、阿里云等）：

1. 添加 A 记录：
   - 主机名: `@`
   - 类型: `A`
   - 值: `<新服务器IP>`
   - TTL: `3600`

2. 添加 CNAME 记录（可选）：
   - 主机名: `www`
   - 类型: `CNAME`
   - 值: `your-domain.com`
   - TTL: `3600`

等待 DNS 传播（通常 5-30 分钟）

## 🔄 备份策略

### 自动备份脚本
```bash
# 创建备份脚本
nano ~/backup.sh
```

添加以下内容：
```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/home/ec2-user/backups"
mkdir -p $BACKUP_DIR

# 备份数据库
mysqldump -u nextmile_user -p'your_password' nextmile_db > $BACKUP_DIR/db_$DATE.sql

# 备份上传文件
tar -czf $BACKUP_DIR/uploads_$DATE.tar.gz /home/ec2-user/Nextmile/public/uploads

# 删除 7 天前的备份
find $BACKUP_DIR -name "*.sql" -mtime +7 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete
```

设置定时任务：
```bash
crontab -e
# 每天凌晨 2 点备份
0 2 * * * /home/ec2-user/backup.sh
```

## ✅ 部署检查清单

- [ ] 新服务器环境已安装完成
- [ ] 代码已克隆到服务器
- [ ] 环境变量已正确配置
- [ ] 依赖包已安装
- [ ] 数据库已创建并导入数据
- [ ] Nginx 已配置并启动
- [ ] SSL 证书已获取并配置
- [ ] 防火墙和安全组已配置
- [ ] 应用已启动（PM2）
- [ ] DNS 已指向新服务器
- [ ] 网站可以正常访问
- [ ] 所有功能已测试
- [ ] 备份策略已配置
- [ ] 监控和日志已配置

## 📞 获取帮助

如果遇到问题，请检查：
1. PM2 日志: `pm2 logs`
2. Nginx 日志: `sudo tail -f /var/log/nginx/error.log`
3. 系统日志: `sudo journalctl -xe`

---

**祝部署顺利！** 🎉
