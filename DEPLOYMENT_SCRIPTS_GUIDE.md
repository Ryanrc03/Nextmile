# Nextmile 项目迁移快速开始

## 📦 脚本说明

本项目提供了完整的自动化部署脚本，帮助您快速将项目迁移到新的 AWS EC2 服务器。

### 可用脚本

| 脚本名称 | 用途 | 运行位置 |
|---------|------|---------|
| `init_new_server.sh` | 初始化新服务器环境 | 新服务器 |
| `backup_before_migration.sh` | 备份旧服务器数据 | 旧服务器 |
| `deploy_to_new_server.sh` | 自动部署应用 | 新服务器 |
| `migrate_data.sh` | 迁移数据 | 新服务器 |
| `check_deployment.sh` | 检查部署状态 | 新服务器 |

## 🚀 快速部署（三步走）

### 步骤 1: 在旧服务器上备份数据

```bash
# SSH 登录到旧服务器
ssh -i your-key.pem ec2-user@<OLD_SERVER_IP>

# 运行备份脚本
cd /home/ec2-user/Nextmile
./scripts/backup_before_migration.sh

# 下载备份到本地
# 在本地机器运行：
scp -i your-key.pem ec2-user@<OLD_SERVER_IP>:~/migration_backup_*.tar.gz .
```

### 步骤 2: 在新服务器上部署应用

```bash
# SSH 登录到新服务器
ssh -i your-key.pem ec2-user@<NEW_SERVER_IP>

# 克隆项目代码
git clone https://github.com/Ryanrc03/Nextmile.git
cd Nextmile

# 运行自动部署脚本（一键部署）
./scripts/deploy_to_new_server.sh \
  --domain your-domain.com \
  --email your-email@example.com
```

### 步骤 3: 迁移数据

```bash
# 上传备份文件到新服务器
# 在本地机器运行：
scp -i your-key.pem migration_backup_*.tar.gz ec2-user@<NEW_SERVER_IP>:~/

# 在新服务器上解压并导入
cd ~
tar -xzf migration_backup_*.tar.gz
cd migration_backup_*

# 导入数据库
mysql -u nextmile_user -p nextmile_db < database.sql

# 恢复上传文件
tar -xzf uploads.tar.gz -C /home/ec2-user/Nextmile/public/
```

## 🛠️ 详细使用说明

### 1. init_new_server.sh - 初始化脚本

**功能**: 安装所有必需的基础软件（Node.js、Python、Docker、Nginx 等）

**使用方法**:
```bash
sudo ./scripts/init_new_server.sh
```

**安装内容**:
- Node.js 18 (通过 nvm)
- Python 3
- Docker & Docker Compose
- Nginx
- PM2
- pnpm
- 常用工具（git、curl、wget 等）

**注意**: 运行后需要重新登录以使 Docker 权限生效

---

### 2. deploy_to_new_server.sh - 自动部署脚本

**功能**: 一键完成整个项目的部署，包括安装依赖、配置环境、启动服务

**使用方法**:
```bash
./scripts/deploy_to_new_server.sh --domain <域名> --email <邮箱>
```

**完整参数**:
```bash
./scripts/deploy_to_new_server.sh \
  --domain nextmile.space \              # 必需：域名
  --email admin@nextmile.space \         # 必需（不跳过SSL时）：邮箱
  --db-host localhost \                  # 可选：数据库主机
  --db-port 3306 \                       # 可选：数据库端口
  --db-name nextmile_db \                # 可选：数据库名
  --db-user nextmile_user \              # 可选：数据库用户
  --db-password yourpassword \           # 可选：数据库密码
  --skip-ssl \                           # 可选：跳过SSL配置
  --skip-db \                            # 可选：跳过数据库安装
  --project-dir /path/to/project         # 可选：项目目录
```

**执行流程**:
1. ✅ 检查系统信息
2. ✅ 更新系统包
3. ✅ 安装 Node.js 和工具
4. ✅ 安装 Python
5. ✅ 安装 Docker
6. ✅ 安装 Nginx
7. ✅ 安装数据库（可选）
8. ✅ 克隆/更新项目代码
9. ✅ 配置环境变量
10. ✅ 安装项目依赖
11. ✅ 构建前端
12. ✅ 配置 Nginx
13. ✅ 配置 SSL 证书
14. ✅ 配置防火墙
15. ✅ 启动应用
16. ✅ 验证部署

**示例**:
```bash
# 完整部署（包含 SSL）
./scripts/deploy_to_new_server.sh \
  --domain nextmile.space \
  --email admin@nextmile.space

# 不配置 SSL（手动配置）
./scripts/deploy_to_new_server.sh \
  --domain nextmile.space \
  --skip-ssl

# 使用外部数据库
./scripts/deploy_to_new_server.sh \
  --domain nextmile.space \
  --email admin@nextmile.space \
  --db-host rds.amazonaws.com \
  --db-user admin \
  --db-password secret \
  --skip-db
```

---

### 3. backup_before_migration.sh - 备份脚本

**功能**: 在旧服务器上备份所有重要数据

**使用方法**:
```bash
./scripts/backup_before_migration.sh
```

**备份内容**:
- 📦 数据库完整导出
- 📁 上传文件（uploads 目录）
- ⚙️ 环境配置文件（.env）
- 🔧 Nginx 配置文件
- 📝 PM2 配置

**输出**:
- 备份目录: `~/migration_backup_YYYYMMDD_HHMMSS/`
- 压缩包: `~/migration_backup_YYYYMMDD_HHMMSS.tar.gz`

---

### 4. migrate_data.sh - 数据迁移脚本

**功能**: 从旧服务器自动拉取并导入数据

**使用方法**:
```bash
./scripts/migrate_data.sh \
  --from <旧服务器IP> \
  --ssh-key /path/to/key.pem
```

**完整参数**:
```bash
./scripts/migrate_data.sh \
  --from 54.123.45.67 \              # 必需：旧服务器IP
  --ssh-key ~/.ssh/my-key.pem \      # 必需：SSH密钥路径
  --db-name nextmile_db \            # 可选：数据库名
  --db-user root \                   # 可选：数据库用户
  --db-password password             # 可选：数据库密码
```

**执行流程**:
1. 从旧服务器导出数据库
2. 同步上传文件
3. 同步配置文件
4. 导入数据库到本地
5. 恢复上传文件

---

### 5. check_deployment.sh - 状态检查脚本

**功能**: 快速检查部署状态和应用健康

**使用方法**:
```bash
./scripts/check_deployment.sh
```

**检查项目**:
- ✅ PM2 进程状态
- ✅ Nginx 运行状态
- ✅ 端口监听（80、443、3000、8000）
- ✅ 服务响应测试
- ✅ 系统资源使用
- ✅ 错误日志
- ✅ SSL 证书状态

---

## 🎯 常见部署场景

### 场景 1: 全新部署（推荐）

```bash
# 1. 在新服务器上克隆代码
git clone https://github.com/Ryanrc03/Nextmile.git
cd Nextmile

# 2. 一键部署
./scripts/deploy_to_new_server.sh \
  --domain your-domain.com \
  --email your-email@example.com

# 3. 配置 DNS（在域名注册商处）
# A 记录: your-domain.com -> 新服务器IP

# 4. 等待 5-10 分钟让 DNS 生效和 SSL 证书获取
```

### 场景 2: 从旧服务器迁移

```bash
# 步骤 1: 在旧服务器备份
ssh old-server
cd /home/ec2-user/Nextmile
./scripts/backup_before_migration.sh
exit

# 步骤 2: 在新服务器部署
ssh new-server
git clone https://github.com/Ryanrc03/Nextmile.git
cd Nextmile
./scripts/deploy_to_new_server.sh --domain your-domain.com --email your-email@example.com

# 步骤 3: 迁移数据
./scripts/migrate_data.sh --from <old-server-ip> --ssh-key ~/.ssh/key.pem

# 步骤 4: 检查状态
./scripts/check_deployment.sh
```

### 场景 3: 仅初始化环境（手动部署）

```bash
# 1. 初始化环境
sudo ./scripts/init_new_server.sh

# 2. 重新登录
exit
ssh new-server

# 3. 手动部署（参考 MIGRATION_GUIDE.md）
```

### 场景 4: 使用外部数据库（如 AWS RDS）

```bash
./scripts/deploy_to_new_server.sh \
  --domain your-domain.com \
  --email your-email@example.com \
  --db-host mydb.xxxx.rds.amazonaws.com \
  --db-port 3306 \
  --db-user admin \
  --db-password mypassword \
  --skip-db  # 跳过本地数据库安装
```

## 🔧 部署后配置

### 1. 编辑环境变量

```bash
cd /home/ec2-user/Nextmile
nano .env.production
```

重要配置项:
```bash
# API 配置
NEXT_PUBLIC_API_URL=https://your-domain.com
API_PORT=8000

# 数据库
DATABASE_HOST=localhost
DATABASE_PASSWORD=your_secure_password

# OpenAI (如果使用)
OPENAI_API_KEY=sk-xxxxx

# 邮件服务 (如果使用)
SMTP_HOST=smtp.gmail.com
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password
```

### 2. 重启服务使配置生效

```bash
pm2 restart all
```

### 3. 配置 DNS

在域名注册商（如 GoDaddy、Namecheap、阿里云）添加 A 记录:
- 主机: `@`
- 类型: `A`
- 值: `新服务器IP`
- TTL: `3600`

### 4. 配置 AWS 安全组

在 AWS EC2 控制台，编辑安全组入站规则:
- HTTP (80): `0.0.0.0/0`
- HTTPS (443): `0.0.0.0/0`
- SSH (22): `你的IP/32`（限制访问）

## 🐛 故障排查

### 脚本执行失败

```bash
# 查看详细错误信息
bash -x ./scripts/deploy_to_new_server.sh --domain your-domain.com --email your-email@example.com

# 检查日志
pm2 logs
sudo tail -f /var/log/nginx/error.log
```

### 应用无法启动

```bash
# 检查端口占用
sudo lsof -i :3000
sudo lsof -i :8000

# 手动启动测试
cd Frontend
npm start

cd ../chatbot
python3 api_server.py
```

### SSL 证书获取失败

```bash
# 确保 DNS 已指向新服务器
dig your-domain.com

# 手动获取证书
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# 查看证书状态
sudo certbot certificates
```

### 数据库连接失败

```bash
# 测试数据库连接
mysql -u nextmile_user -p nextmile_db

# 检查数据库服务
sudo systemctl status mysqld

# 查看数据库日志
sudo tail -f /var/log/mysqld.log
```

## 📝 常用命令

### PM2 管理

```bash
pm2 status              # 查看进程状态
pm2 logs               # 查看所有日志
pm2 logs nextmile-api  # 查看特定服务日志
pm2 restart all        # 重启所有服务
pm2 stop all           # 停止所有服务
pm2 delete all         # 删除所有进程
pm2 monit             # 实时监控
```

### Nginx 管理

```bash
sudo nginx -t                          # 测试配置
sudo systemctl restart nginx           # 重启
sudo systemctl status nginx            # 查看状态
sudo tail -f /var/log/nginx/error.log  # 查看错误日志
sudo tail -f /var/log/nginx/access.log # 查看访问日志
```

### 系统管理

```bash
# 查看磁盘使用
df -h

# 查看内存使用
free -h

# 查看进程
htop

# 查看端口监听
sudo netstat -tlnp

# 查看系统日志
sudo journalctl -xe
```

## 🔐 安全建议

1. **修改 SSH 端口** (可选)
2. **禁用 root 登录**
3. **配置防火墙规则**
4. **使用强密码**
5. **定期更新系统**
6. **配置自动备份**
7. **启用 fail2ban**

## 📚 更多文档

- [完整迁移指南](./MIGRATION_GUIDE.md) - 详细的手动部署步骤
- [部署指南](./DEPLOYMENT_GUIDE.md) - 通用部署文档
- [项目 README](./README.md) - 项目介绍

## ❓ 获取帮助

如果遇到问题:
1. 查看脚本输出的错误信息
2. 运行 `check_deployment.sh` 检查状态
3. 查看相关日志文件
4. 参考 MIGRATION_GUIDE.md 手动操作

---

**祝部署顺利！** 🎉

有问题欢迎提 Issue 或联系维护者。
