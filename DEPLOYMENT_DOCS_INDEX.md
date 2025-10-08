# 项目迁移部署文档索引

本项目现在包含完整的自动化部署脚本和详细文档，帮助您快速将项目迁移到新的 AWS EC2 服务器。

## 📚 文档列表

### 快速开始文档

| 文档 | 说明 | 适合人群 |
|------|------|---------|
| **DEPLOYMENT_QUICK_REFERENCE.txt** | 快速参考卡片 | ⭐ 所有人 - 最快上手 |
| **DEPLOYMENT_SCRIPTS_GUIDE.md** | 脚本详细使用指南 | 使用自动化脚本部署 |
| **MIGRATION_GUIDE.md** | 完整手动迁移教程 | 需要手动控制每个步骤 |

### 脚本目录

| 路径 | 说明 |
|------|------|
| **scripts/** | 所有自动化部署脚本 |
| **scripts/README.md** | 脚本目录说明 |

## 🚀 快速开始 - 3 种方式

### 方式 1: 最快部署（推荐）⭐

```bash
# 在新服务器运行
git clone https://github.com/Ryanrc03/Nextmile.git
cd Nextmile
./scripts/deploy_to_new_server.sh --domain 你的域名.com --email 你的邮箱@example.com
```

**适用场景**: 全新部署，不需要迁移旧数据

---

### 方式 2: 完整迁移（含数据）

```bash
# 步骤 1: 旧服务器备份
ssh 旧服务器
cd Nextmile
./scripts/backup_before_migration.sh

# 步骤 2: 新服务器部署
ssh 新服务器
git clone https://github.com/Ryanrc03/Nextmile.git
cd Nextmile
./scripts/deploy_to_new_server.sh --domain 你的域名.com --email 你的邮箱@example.com

# 步骤 3: 迁移数据
./scripts/migrate_data.sh --from 旧服务器IP --ssh-key ~/.ssh/key.pem
```

**适用场景**: 从旧服务器迁移到新服务器，需要保留数据

---

### 方式 3: 手动部署

参考 **MIGRATION_GUIDE.md** 中的详细手动步骤。

**适用场景**: 需要完全控制每个部署步骤，或自动脚本不适合你的环境

---

## 📖 文档详细说明

### 1. DEPLOYMENT_QUICK_REFERENCE.txt

**快速参考卡片** - 打开即用的速查表

包含内容:
- ⚡ 最快部署命令
- 📋 完整迁移流程（3步）
- 🛠️ 所有可用脚本列表
- ⚙️ 脚本参数说明
- 📌 常用示例
- ✅ 部署后检查清单
- 🔧 管理命令
- 🐛 故障排查

**何时使用**: 当你需要快速查找命令或参数时

---

### 2. DEPLOYMENT_SCRIPTS_GUIDE.md

**脚本使用指南** - 自动化部署完整教程

包含内容:
- 📦 所有脚本的详细说明
- 🎯 常见部署场景示例
- 🔧 部署后配置步骤
- 🐛 详细的故障排查
- 📝 常用管理命令
- 🔐 安全建议

**何时使用**: 第一次使用脚本，或需要了解脚本功能和参数

---

### 3. MIGRATION_GUIDE.md

**完整迁移指南** - 手动部署详细步骤

包含内容:
- 🔧 环境准备
- 📦 软件安装步骤
- ⚙️ 配置文件修改
- 💾 数据库迁移
- 🌐 DNS 和 SSL 配置
- 🔍 详细的验证步骤
- 📊 性能优化建议
- ✅ 完整的检查清单

**何时使用**: 
- 自动脚本不适合你的环境
- 需要理解每个步骤的原理
- 需要自定义部署流程
- 学习部署知识

---

### 4. scripts/README.md

**脚本目录说明** - scripts 目录的快速指南

包含内容:
- 📁 脚本列表和说明
- 🎯 常见使用场景
- ⚙️ 环境要求
- 🔍 验证方法

**何时使用**: 查看 scripts 目录时的快速参考

---

## 🎯 选择合适的方式

### 场景对照表

| 你的需求 | 推荐方式 | 参考文档 |
|---------|---------|---------|
| 全新部署，快速上线 | 方式 1: 自动脚本 | DEPLOYMENT_QUICK_REFERENCE.txt |
| 从旧服务器迁移 | 方式 2: 完整迁移 | DEPLOYMENT_SCRIPTS_GUIDE.md |
| 自定义部署流程 | 方式 3: 手动部署 | MIGRATION_GUIDE.md |
| 特殊环境/配置 | 方式 3: 手动部署 | MIGRATION_GUIDE.md |
| 学习部署原理 | 方式 3: 手动部署 | MIGRATION_GUIDE.md |

---

## 🛠️ 可用脚本

所有脚本位于 `scripts/` 目录：

| 脚本 | 功能 | 运行位置 |
|------|------|---------|
| `deploy_to_new_server.sh` | 🚀 一键自动部署 | 新服务器 |
| `init_new_server.sh` | 🔧 初始化环境 | 新服务器 |
| `backup_before_migration.sh` | 💾 备份数据 | 旧服务器 |
| `migrate_data.sh` | 📦 迁移数据 | 新服务器 |
| `check_deployment.sh` | ✅ 检查状态 | 新服务器 |

详细说明见: `scripts/README.md` 或 `DEPLOYMENT_SCRIPTS_GUIDE.md`

---

## 📋 快速命令速查

### 最简单的部署
```bash
./scripts/deploy_to_new_server.sh --domain 域名.com --email 邮箱@example.com
```

### 检查部署状态
```bash
./scripts/check_deployment.sh
```

### 查看服务日志
```bash
pm2 logs
```

### 重启服务
```bash
pm2 restart all
```

---

## 🆘 获取帮助

1. **查看快速参考**: `cat DEPLOYMENT_QUICK_REFERENCE.txt`
2. **查看脚本帮助**: `./scripts/deploy_to_new_server.sh --help`
3. **查看详细文档**: 阅读相应的 .md 文件
4. **提交 Issue**: GitHub 仓库提问

---

## 📝 文档更新记录

- 2025-10-08: 添加完整的自动化部署脚本和文档
- 包含 5 个自动化脚本
- 包含 4 个详细文档
- 支持一键部署和完整迁移

---

## 🎉 开始使用

**建议流程**:

1. 先浏览 `DEPLOYMENT_QUICK_REFERENCE.txt` 了解概况
2. 根据你的场景选择合适的部署方式
3. 参考对应的详细文档进行部署
4. 部署后运行 `check_deployment.sh` 验证

祝部署顺利！🚀
