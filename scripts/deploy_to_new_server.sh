#!/bin/bash

#############################################
# Nextmile 项目自动部署脚本
# 用于在新的 AWS EC2 服务器上部署项目
#############################################

set -e  # 遇到错误立即退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 显示 banner
show_banner() {
    echo -e "${GREEN}"
    cat << "EOF"
╔═══════════════════════════════════════════════════╗
║                                                   ║
║     Nextmile 自动部署脚本                        ║
║     AWS EC2 一键部署解决方案                     ║
║                                                   ║
╚═══════════════════════════════════════════════════╝
EOF
    echo -e "${NC}"
}

# 默认配置
DOMAIN=""
EMAIL=""
DB_HOST="localhost"
DB_PORT="3306"
DB_NAME="nextmile_db"
DB_USER="nextmile_user"
DB_PASSWORD=""
SKIP_SSL=false
SKIP_DB=false
PROJECT_DIR="/home/ec2-user/Nextmile"

# 解析命令行参数
parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --domain)
                DOMAIN="$2"
                shift 2
                ;;
            --email)
                EMAIL="$2"
                shift 2
                ;;
            --db-host)
                DB_HOST="$2"
                shift 2
                ;;
            --db-port)
                DB_PORT="$2"
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
            --skip-ssl)
                SKIP_SSL=true
                shift
                ;;
            --skip-db)
                SKIP_DB=true
                shift
                ;;
            --project-dir)
                PROJECT_DIR="$2"
                shift 2
                ;;
            --help)
                show_help
                exit 0
                ;;
            *)
                log_error "未知参数: $1"
                show_help
                exit 1
                ;;
        esac
    done
}

# 显示帮助信息
show_help() {
    cat << EOF
使用方法: $0 [选项]

选项:
    --domain <域名>           域名（必需，例如: nextmile.space）
    --email <邮箱>            SSL 证书邮箱（必需，如果不跳过 SSL）
    --db-host <主机>          数据库主机（默认: localhost）
    --db-port <端口>          数据库端口（默认: 3306）
    --db-name <数据库名>      数据库名称（默认: nextmile_db）
    --db-user <用户名>        数据库用户名（默认: nextmile_user）
    --db-password <密码>      数据库密码
    --skip-ssl               跳过 SSL 证书配置
    --skip-db                跳过数据库安装
    --project-dir <路径>      项目目录（默认: /home/ec2-user/Nextmile）
    --help                   显示此帮助信息

示例:
    $0 --domain nextmile.space --email admin@nextmile.space
    $0 --domain example.com --email admin@example.com --skip-ssl
EOF
}

# 检查必需参数
check_required_params() {
    if [ -z "$DOMAIN" ]; then
        log_error "必须指定域名！使用 --domain 参数"
        exit 1
    fi

    if [ "$SKIP_SSL" = false ] && [ -z "$EMAIL" ]; then
        log_error "必须指定邮箱用于 SSL 证书！使用 --email 参数或 --skip-ssl 跳过"
        exit 1
    fi
}

# 检查是否以 root 或 sudo 运行某些命令
check_sudo() {
    if [ "$EUID" -ne 0 ]; then
        log_warning "某些操作需要 sudo 权限"
    fi
}

# 步骤 1: 检查系统信息
check_system() {
    log_info "检查系统信息..."
    
    # 检查操作系统
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        log_info "操作系统: $NAME $VERSION"
    fi
    
    # 检查 CPU 和内存
    log_info "CPU: $(nproc) 核心"
    log_info "内存: $(free -h | awk '/^Mem:/ {print $2}')"
    log_info "磁盘: $(df -h / | awk 'NR==2 {print $4}') 可用"
    
    log_success "系统检查完成"
}

# 步骤 2: 更新系统
update_system() {
    log_info "更新系统包..."
    
    if command -v yum &> /dev/null; then
        sudo yum update -y
    elif command -v apt-get &> /dev/null; then
        sudo apt-get update -y
        sudo apt-get upgrade -y
    else
        log_error "不支持的包管理器"
        exit 1
    fi
    
    log_success "系统更新完成"
}

# 步骤 3: 安装 Node.js 和 npm
install_nodejs() {
    log_info "检查 Node.js 安装..."
    
    if command -v node &> /dev/null; then
        NODE_VERSION=$(node --version)
        log_info "Node.js 已安装: $NODE_VERSION"
    else
        log_info "安装 Node.js..."
        
        # 安装 nvm
        curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
        
        # 加载 nvm
        export NVM_DIR="$HOME/.nvm"
        [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
        
        # 安装 Node.js 18
        nvm install 18
        nvm use 18
        
        log_success "Node.js 安装完成"
    fi
    
    # 安装 pnpm
    if ! command -v pnpm &> /dev/null; then
        log_info "安装 pnpm..."
        npm install -g pnpm
    fi
    
    # 安装 PM2
    if ! command -v pm2 &> /dev/null; then
        log_info "安装 PM2..."
        npm install -g pm2
    fi
    
    log_success "Node.js 工具链安装完成"
}

# 步骤 4: 安装 Python
install_python() {
    log_info "检查 Python 安装..."
    
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version)
        log_info "Python 已安装: $PYTHON_VERSION"
    else
        log_info "安装 Python 3..."
        
        if command -v yum &> /dev/null; then
            sudo yum install python3 python3-pip -y
        elif command -v apt-get &> /dev/null; then
            sudo apt-get install python3 python3-pip -y
        fi
        
        log_success "Python 安装完成"
    fi
}

# 步骤 5: 安装 Docker
install_docker() {
    log_info "检查 Docker 安装..."
    
    if command -v docker &> /dev/null; then
        DOCKER_VERSION=$(docker --version)
        log_info "Docker 已安装: $DOCKER_VERSION"
    else
        log_info "安装 Docker..."
        
        if command -v yum &> /dev/null; then
            sudo yum install docker -y
        elif command -v apt-get &> /dev/null; then
            sudo apt-get install docker.io -y
        fi
        
        sudo systemctl start docker
        sudo systemctl enable docker
        sudo usermod -aG docker $USER
        
        log_success "Docker 安装完成"
    fi
    
    # 安装 Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        log_info "安装 Docker Compose..."
        sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
        sudo chmod +x /usr/local/bin/docker-compose
    fi
    
    log_success "Docker 工具链安装完成"
}

# 步骤 6: 安装 Nginx
install_nginx() {
    log_info "检查 Nginx 安装..."
    
    if command -v nginx &> /dev/null; then
        log_info "Nginx 已安装"
    else
        log_info "安装 Nginx..."
        
        if command -v yum &> /dev/null; then
            sudo yum install nginx -y
        elif command -v apt-get &> /dev/null; then
            sudo apt-get install nginx -y
        fi
        
        log_success "Nginx 安装完成"
    fi
    
    sudo systemctl enable nginx
}

# 步骤 7: 安装数据库
install_database() {
    if [ "$SKIP_DB" = true ]; then
        log_warning "跳过数据库安装"
        return
    fi
    
    log_info "安装 MySQL..."
    
    if command -v mysql &> /dev/null; then
        log_info "MySQL 已安装"
    else
        if command -v yum &> /dev/null; then
            sudo yum install mysql-server -y
        elif command -v apt-get &> /dev/null; then
            sudo apt-get install mysql-server -y
        fi
        
        sudo systemctl start mysqld || sudo systemctl start mysql
        sudo systemctl enable mysqld || sudo systemctl enable mysql
        
        log_success "MySQL 安装完成"
    fi
}

# 步骤 8: 克隆或更新项目代码
setup_project() {
    log_info "设置项目代码..."
    
    if [ -d "$PROJECT_DIR" ]; then
        log_info "项目目录已存在，拉取最新代码..."
        cd "$PROJECT_DIR"
        git pull origin main || log_warning "无法拉取最新代码，继续使用现有代码"
    else
        log_info "克隆项目代码..."
        git clone https://github.com/Ryanrc03/Nextmile.git "$PROJECT_DIR"
        cd "$PROJECT_DIR"
    fi
    
    log_success "项目代码准备完成"
}

# 步骤 9: 配置环境变量
configure_env() {
    log_info "配置环境变量..."
    
    cd "$PROJECT_DIR"
    
    # 创建 .env.production 文件
    cat > .env.production << EOF
# API 配置
NEXT_PUBLIC_API_URL=https://${DOMAIN}
API_PORT=8000
API_HOST=0.0.0.0

# 数据库配置
DATABASE_HOST=${DB_HOST}
DATABASE_PORT=${DB_PORT}
DATABASE_NAME=${DB_NAME}
DATABASE_USER=${DB_USER}
DATABASE_PASSWORD=${DB_PASSWORD}

# Redis 配置
REDIS_HOST=localhost
REDIS_PORT=6379

# 其他配置
NODE_ENV=production
EOF
    
    log_success "环境变量配置完成"
    log_info "请检查并编辑 .env.production 文件添加其他必要的配置"
}

# 步骤 10: 安装项目依赖
install_dependencies() {
    log_info "安装项目依赖..."
    
    cd "$PROJECT_DIR"
    
    # 安装前端依赖
    log_info "安装前端依赖..."
    cd Frontend
    pnpm install
    cd ..
    
    # 安装后端依赖
    log_info "安装后端依赖..."
    cd chatbot
    pip3 install -r requirements.txt
    cd ..
    
    log_success "依赖安装完成"
}

# 步骤 11: 构建前端
build_frontend() {
    log_info "构建前端应用..."
    
    cd "$PROJECT_DIR/Frontend"
    pnpm build
    
    log_success "前端构建完成"
}

# 步骤 12: 配置 Nginx
configure_nginx() {
    log_info "配置 Nginx..."
    
    # 备份原配置
    if [ -f /etc/nginx/conf.d/nextmile.space.conf ]; then
        sudo cp /etc/nginx/conf.d/nextmile.space.conf /etc/nginx/conf.d/nextmile.space.conf.bak
    fi
    
    # 创建 Nginx 配置
    sudo tee /etc/nginx/conf.d/${DOMAIN}.conf > /dev/null << EOF
# Nextmile Nginx 配置
# 域名: ${DOMAIN}

upstream nextmile_frontend {
    server 127.0.0.1:3000;
}

upstream nextmile_api {
    server 127.0.0.1:8000;
}

# HTTP 服务器（重定向到 HTTPS）
server {
    listen 80;
    listen [::]:80;
    server_name ${DOMAIN} www.${DOMAIN};

    # Let's Encrypt 验证
    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }

    # 重定向到 HTTPS
    location / {
        return 301 https://\$server_name\$request_uri;
    }
}

# HTTPS 服务器
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name ${DOMAIN} www.${DOMAIN};

    # SSL 配置（Certbot 会自动填充）
    # ssl_certificate /etc/letsencrypt/live/${DOMAIN}/fullchain.pem;
    # ssl_certificate_key /etc/letsencrypt/live/${DOMAIN}/privkey.pem;

    # SSL 优化
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;
    ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384';

    # 安全头
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Gzip 压缩
    gzip on;
    gzip_vary on;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types text/plain text/css text/xml text/javascript application/json application/javascript application/xml+rss application/rss+xml font/truetype font/opentype application/vnd.ms-fontobject image/svg+xml;

    # API 代理
    location /api/ {
        proxy_pass http://nextmile_api/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_cache_bypass \$http_upgrade;
    }

    # 前端代理
    location / {
        proxy_pass http://nextmile_frontend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_cache_bypass \$http_upgrade;
    }

    # 静态资源缓存
    location ~* \.(jpg|jpeg|png|gif|ico|css|js|woff|woff2|ttf|svg)$ {
        proxy_pass http://nextmile_frontend;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
EOF
    
    # 测试 Nginx 配置
    sudo nginx -t
    
    log_success "Nginx 配置完成"
}

# 步骤 13: 配置 SSL
configure_ssl() {
    if [ "$SKIP_SSL" = true ]; then
        log_warning "跳过 SSL 配置"
        return
    fi
    
    log_info "配置 SSL 证书..."
    
    # 安装 Certbot
    if ! command -v certbot &> /dev/null; then
        log_info "安装 Certbot..."
        
        if command -v yum &> /dev/null; then
            sudo yum install certbot python3-certbot-nginx -y
        elif command -v apt-get &> /dev/null; then
            sudo apt-get install certbot python3-certbot-nginx -y
        fi
    fi
    
    # 创建 certbot 目录
    sudo mkdir -p /var/www/certbot
    
    # 获取 SSL 证书
    log_info "正在获取 SSL 证书，这可能需要几分钟..."
    sudo certbot --nginx -d "$DOMAIN" -d "www.$DOMAIN" --email "$EMAIL" --agree-tos --non-interactive --redirect || {
        log_warning "SSL 证书获取失败，请手动配置: sudo certbot --nginx -d $DOMAIN"
    }
    
    # 设置自动续期
    (crontab -l 2>/dev/null; echo "0 3 * * * /usr/bin/certbot renew --quiet") | crontab -
    
    log_success "SSL 配置完成"
}

# 步骤 14: 配置防火墙
configure_firewall() {
    log_info "配置防火墙..."
    
    if command -v firewall-cmd &> /dev/null; then
        sudo firewall-cmd --permanent --add-port=80/tcp
        sudo firewall-cmd --permanent --add-port=443/tcp
        sudo firewall-cmd --permanent --add-port=8000/tcp
        sudo firewall-cmd --reload
        log_success "Firewalld 配置完成"
    elif command -v ufw &> /dev/null; then
        sudo ufw allow 80/tcp
        sudo ufw allow 443/tcp
        sudo ufw allow 8000/tcp
        sudo ufw reload
        log_success "UFW 配置完成"
    else
        log_warning "未检测到防火墙，请手动配置 AWS 安全组"
    fi
    
    log_info "请确保在 AWS 安全组中开放以下端口:"
    log_info "  - 80 (HTTP)"
    log_info "  - 443 (HTTPS)"
    log_info "  - 22 (SSH)"
}

# 步骤 15: 启动应用
start_application() {
    log_info "启动应用..."
    
    cd "$PROJECT_DIR"
    
    # 停止旧进程
    pm2 delete nextmile-api 2>/dev/null || true
    pm2 delete nextmile-frontend 2>/dev/null || true
    
    # 启动后端 API
    log_info "启动后端 API..."
    cd chatbot
    pm2 start api_server.py --name nextmile-api --interpreter python3
    cd ..
    
    # 启动前端
    log_info "启动前端..."
    cd Frontend
    pm2 start npm --name nextmile-frontend -- start
    cd ..
    
    # 保存 PM2 配置
    pm2 save
    pm2 startup | tail -n 1 | sudo bash || log_warning "PM2 启动脚本配置失败，请手动运行: pm2 startup"
    
    # 启动 Nginx
    sudo systemctl restart nginx
    
    log_success "应用启动完成"
}

# 步骤 16: 验证部署
verify_deployment() {
    log_info "验证部署..."
    
    sleep 5  # 等待服务启动
    
    # 检查 PM2 进程
    log_info "PM2 进程状态:"
    pm2 status
    
    # 检查端口监听
    log_info "检查端口监听..."
    netstat -tlnp 2>/dev/null | grep -E ':(80|443|3000|8000)' || log_warning "部分端口未监听"
    
    # 测试 API
    log_info "测试 API..."
    if curl -s http://localhost:8000/health > /dev/null; then
        log_success "API 响应正常"
    else
        log_warning "API 可能未正常启动"
    fi
    
    # 测试前端
    log_info "测试前端..."
    if curl -s http://localhost:3000 > /dev/null; then
        log_success "前端响应正常"
    else
        log_warning "前端可能未正常启动"
    fi
    
    log_success "部署验证完成"
}

# 显示部署总结
show_summary() {
    echo ""
    log_success "====================================="
    log_success "    部署完成！"
    log_success "====================================="
    echo ""
    log_info "访问地址:"
    log_info "  前端: https://${DOMAIN}"
    log_info "  API: https://${DOMAIN}/api"
    echo ""
    log_info "管理命令:"
    log_info "  查看状态: pm2 status"
    log_info "  查看日志: pm2 logs"
    log_info "  重启应用: pm2 restart all"
    log_info "  停止应用: pm2 stop all"
    echo ""
    log_info "Nginx 命令:"
    log_info "  测试配置: sudo nginx -t"
    log_info "  重启 Nginx: sudo systemctl restart nginx"
    log_info "  查看日志: sudo tail -f /var/log/nginx/error.log"
    echo ""
    log_warning "下一步:"
    log_warning "1. 检查并编辑 .env.production 文件"
    log_warning "2. 配置数据库并导入数据"
    log_warning "3. 在域名注册商处配置 DNS A 记录指向服务器 IP"
    log_warning "4. 测试所有功能是否正常"
    echo ""
}

# 主函数
main() {
    show_banner
    parse_args "$@"
    check_required_params
    check_sudo
    
    log_info "开始部署 Nextmile 项目到新服务器..."
    log_info "域名: $DOMAIN"
    log_info "项目目录: $PROJECT_DIR"
    echo ""
    
    # 执行部署步骤
    check_system
    update_system
    install_nodejs
    install_python
    install_docker
    install_nginx
    install_database
    setup_project
    configure_env
    install_dependencies
    build_frontend
    configure_nginx
    configure_ssl
    configure_firewall
    start_application
    verify_deployment
    show_summary
    
    log_success "部署流程完成！"
}

# 错误处理
trap 'log_error "部署过程中发生错误，请检查日志"; exit 1' ERR

# 运行主函数
main "$@"
