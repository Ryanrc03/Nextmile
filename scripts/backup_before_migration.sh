#!/bin/bash

#############################################
# 迁移前备份脚本
# 在旧服务器上运行，备份所有重要数据
#############################################

set -e

# 颜色定义
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

# 配置
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="$HOME/migration_backup_$DATE"
PROJECT_DIR="/home/ec2-user/Nextmile"
DB_NAME="nextmile_db"
DB_USER="root"

log_info "开始备份数据..."
log_info "备份目录: $BACKUP_DIR"

# 创建备份目录
mkdir -p "$BACKUP_DIR"

# 1. 备份数据库
log_info "备份数据库..."
read -sp "请输入数据库密码: " DB_PASSWORD
echo ""
mysqldump -u "$DB_USER" -p"$DB_PASSWORD" "$DB_NAME" > "$BACKUP_DIR/database.sql"
log_success "数据库备份完成"

# 2. 备份上传文件
if [ -d "$PROJECT_DIR/public/uploads" ]; then
    log_info "备份上传文件..."
    tar -czf "$BACKUP_DIR/uploads.tar.gz" -C "$PROJECT_DIR/public" uploads
    log_success "上传文件备份完成"
fi

# 3. 备份配置文件
log_info "备份配置文件..."
cp "$PROJECT_DIR/.env"* "$BACKUP_DIR/" 2>/dev/null || log_info "没有环境配置文件"
cp "$PROJECT_DIR/nginx/"*.conf "$BACKUP_DIR/" 2>/dev/null || log_info "没有 Nginx 配置文件"

# 4. 备份 PM2 配置
if command -v pm2 &> /dev/null; then
    log_info "备份 PM2 配置..."
    pm2 save
    cp -r ~/.pm2 "$BACKUP_DIR/pm2_config" 2>/dev/null || log_info "没有 PM2 配置"
fi

# 5. 创建备份清单
cat > "$BACKUP_DIR/backup_info.txt" << EOF
备份时间: $(date)
服务器: $(hostname)
项目目录: $PROJECT_DIR
数据库: $DB_NAME

备份内容:
- database.sql: 数据库备份
- uploads.tar.gz: 上传文件备份
- .env 文件: 环境配置
- Nginx 配置文件
- PM2 配置

迁移步骤:
1. 将此备份目录复制到新服务器
2. 在新服务器上运行部署脚本
3. 导入数据库: mysql -u user -p database_name < database.sql
4. 解压上传文件: tar -xzf uploads.tar.gz -C /path/to/public/
5. 复制配置文件并根据新服务器环境修改
EOF

# 创建压缩包
log_info "创建备份压缩包..."
cd "$HOME"
tar -czf "migration_backup_$DATE.tar.gz" "migration_backup_$DATE"

log_success "备份完成！"
echo ""
log_info "备份文件:"
log_info "  目录: $BACKUP_DIR"
log_info "  压缩包: $HOME/migration_backup_$DATE.tar.gz"
echo ""
log_info "下一步:"
log_info "1. 下载备份文件到本地: scp -i key.pem ec2-user@server:~/migration_backup_$DATE.tar.gz ."
log_info "2. 上传到新服务器: scp -i key.pem migration_backup_$DATE.tar.gz ec2-user@new-server:~/"
log_info "3. 在新服务器上解压并导入数据"
