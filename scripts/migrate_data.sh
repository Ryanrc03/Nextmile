#!/bin/bash

#############################################
# 数据迁移脚本
# 从旧服务器迁移数据到新服务器
#############################################

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 默认值
OLD_SERVER=""
SSH_KEY=""
DB_NAME="nextmile_db"
DB_USER="root"
DB_PASSWORD=""
BACKUP_DIR="/tmp/migration_backup"

# 解析参数
while [[ $# -gt 0 ]]; do
    case $1 in
        --from)
            OLD_SERVER="$2"
            shift 2
            ;;
        --ssh-key)
            SSH_KEY="$2"
            shift 2
            ;;
        --db-name)
            DB_NAME="$2"
            shift 2
            ;;
        --db-user)
            DB_USER="$2"
            shift 2
            ;;
        --db-password)
            DB_PASSWORD="$2"
            shift 2
            ;;
        --help)
            echo "使用方法: $0 --from <旧服务器IP> --ssh-key <SSH密钥路径>"
            echo "可选参数:"
            echo "  --db-name <数据库名>   (默认: nextmile_db)"
            echo "  --db-user <用户名>     (默认: root)"
            echo "  --db-password <密码>   (数据库密码)"
            exit 0
            ;;
        *)
            log_error "未知参数: $1"
            exit 1
            ;;
    esac
done

# 检查必需参数
if [ -z "$OLD_SERVER" ]; then
    log_error "必须指定旧服务器地址！使用 --from 参数"
    exit 1
fi

if [ -z "$SSH_KEY" ]; then
    log_error "必须指定 SSH 密钥！使用 --ssh-key 参数"
    exit 1
fi

log_info "开始数据迁移..."
log_info "从服务器: $OLD_SERVER"

# 创建备份目录
mkdir -p "$BACKUP_DIR"

# 1. 从旧服务器导出数据库
log_info "导出数据库..."
ssh -i "$SSH_KEY" "ec2-user@$OLD_SERVER" "mysqldump -u $DB_USER -p'$DB_PASSWORD' $DB_NAME" > "$BACKUP_DIR/${DB_NAME}.sql"
log_success "数据库导出完成"

# 2. 同步上传文件
log_info "同步上传文件..."
rsync -avz -e "ssh -i $SSH_KEY" "ec2-user@$OLD_SERVER:/home/ec2-user/Nextmile/public/uploads/" "$BACKUP_DIR/uploads/" || log_info "没有上传文件或同步失败"

# 3. 同步配置文件
log_info "同步配置文件..."
rsync -avz -e "ssh -i $SSH_KEY" "ec2-user@$OLD_SERVER:/home/ec2-user/Nextmile/.env*" "$BACKUP_DIR/" || log_info "没有环境配置文件"

# 4. 导入数据库到本地
log_info "导入数据库到本地..."
if [ -z "$DB_PASSWORD" ]; then
    mysql -u "$DB_USER" "$DB_NAME" < "$BACKUP_DIR/${DB_NAME}.sql"
else
    mysql -u "$DB_USER" -p"$DB_PASSWORD" "$DB_NAME" < "$BACKUP_DIR/${DB_NAME}.sql"
fi
log_success "数据库导入完成"

# 5. 恢复上传文件
if [ -d "$BACKUP_DIR/uploads" ]; then
    log_info "恢复上传文件..."
    mkdir -p /home/ec2-user/Nextmile/public/uploads
    cp -r "$BACKUP_DIR/uploads/"* /home/ec2-user/Nextmile/public/uploads/
    log_success "上传文件恢复完成"
fi

log_success "数据迁移完成！"
log_info "备份文件保存在: $BACKUP_DIR"
