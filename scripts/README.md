# 部署脚本说明

这个目录包含了用于自动化部署 Nextmile 项目的所有脚本。

## 🚀 快速开始

### 最简单的方式（推荐）

```bash
# 在新服务器上运行
cd /home/ec2-user/Nextmile
./scripts/deploy_to_new_server.sh --domain your-domain.com --email your-email@example.com
```

就这么简单！脚本会自动完成所有部署步骤。

## 📁 脚本列表

| 脚本 | 说明 | 何时使用 |
|-----|------|---------|
| `deploy_to_new_server.sh` | **主部署脚本** - 一键部署 | 在新服务器上首次部署 |
| `init_new_server.sh` | 初始化服务器环境 | 仅安装基础软件 |
| `backup_before_migration.sh` | 备份旧服务器数据 | 在旧服务器上运行 |
| `migrate_data.sh` | 从旧服务器迁移数据 | 数据迁移时 |
| `check_deployment.sh` | 检查部署状态 | 验证部署是否成功 |

## 📖 详细文档

完整使用文档请查看: [DEPLOYMENT_SCRIPTS_GUIDE.md](../DEPLOYMENT_SCRIPTS_GUIDE.md)

## 🎯 常见使用场景

### 1. 全新部署
```bash
./scripts/deploy_to_new_server.sh --domain example.com --email admin@example.com
```

### 2. 从旧服务器迁移
```bash
# 旧服务器
./scripts/backup_before_migration.sh

# 新服务器
./scripts/deploy_to_new_server.sh --domain example.com --email admin@example.com
./scripts/migrate_data.sh --from old-server-ip --ssh-key key.pem
```

### 3. 跳过 SSL（手动配置）
```bash
./scripts/deploy_to_new_server.sh --domain example.com --skip-ssl
```

### 4. 使用外部数据库
```bash
./scripts/deploy_to_new_server.sh \
  --domain example.com \
  --email admin@example.com \
  --db-host rds.amazonaws.com \
  --skip-db
```

## ⚙️ 环境要求

- AWS EC2 实例（Amazon Linux 2 或 Ubuntu）
- 至少 2GB RAM
- 10GB 可用磁盘空间
- 已配置的域名（可选）

## 🔍 验证部署

```bash
./scripts/check_deployment.sh
```

## 🆘 需要帮助？

查看详细文档:
- [DEPLOYMENT_SCRIPTS_GUIDE.md](../DEPLOYMENT_SCRIPTS_GUIDE.md) - 脚本使用指南
- [MIGRATION_GUIDE.md](../MIGRATION_GUIDE.md) - 完整迁移指南
