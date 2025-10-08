#!/bin/bash

#############################################
# 服务器初始化脚本
# 仅安装基础环境，不部署应用
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

log_info "开始初始化服务器环境..."

# 更新系统
log_info "更新系统包..."
if command -v yum &> /dev/null; then
    sudo yum update -y
    sudo yum install -y git curl wget vim htop net-tools
elif command -v apt-get &> /dev/null; then
    sudo apt-get update -y
    sudo apt-get upgrade -y
    sudo apt-get install -y git curl wget vim htop net-tools
fi

# 安装 Node.js
log_info "安装 Node.js..."
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
nvm install 18
nvm use 18
npm install -g pnpm pm2

# 安装 Python
log_info "安装 Python..."
if command -v yum &> /dev/null; then
    sudo yum install -y python3 python3-pip python3-devel
elif command -v apt-get &> /dev/null; then
    sudo apt-get install -y python3 python3-pip python3-dev
fi

# 安装 Docker
log_info "安装 Docker..."
if command -v yum &> /dev/null; then
    sudo yum install -y docker
elif command -v apt-get &> /dev/null; then
    sudo apt-get install -y docker.io
fi
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER

# 安装 Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 安装 Nginx
log_info "安装 Nginx..."
if command -v yum &> /dev/null; then
    sudo yum install -y nginx
elif command -v apt-get &> /dev/null; then
    sudo apt-get install -y nginx
fi
sudo systemctl enable nginx

log_success "服务器初始化完成！"
log_info "请重新登录以使 Docker 权限生效"
