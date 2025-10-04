#!/bin/bash
# 自动化部署脚本 - obsicat.com域名部署
# 使用方法: ./deploy.sh [staging|production]

set -e

ENVIRONMENT=${1:-production}
DOMAIN="obsicat.com"
APP_DIR="/home/runner/ai-memory"
NGINX_CONF="/etc/nginx/sites-available/obsicat.com"
NGINX_ENABLED="/etc/nginx/sites-enabled/obsicat.com"

echo "========================================="
echo "Obsi喵 AI Memory 部署脚本"
echo "环境: $ENVIRONMENT"
echo "域名: $DOMAIN"
echo "========================================="

# 颜色输出
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

# 检查是否为root用户
if [ "$EUID" -ne 0 ]; then 
    print_error "请使用sudo运行此脚本"
    exit 1
fi

# 1. 更新代码
echo ""
echo "[1/8] 更新代码..."
cd $APP_DIR
git pull origin main
print_success "代码更新完成"

# 2. 安装/更新依赖
echo ""
echo "[2/8] 安装Python依赖..."
pip install -r requirements.txt --upgrade
print_success "依赖安装完成"

# 3. 配置环境变量
echo ""
echo "[3/8] 配置环境变量..."
if [ ! -f "$APP_DIR/.env" ]; then
    cat > $APP_DIR/.env <<EOF
JWT_SECRET_KEY=$(openssl rand -hex 32)
FLASK_ENV=$ENVIRONMENT
REDIS_HOST=localhost
REDIS_PORT=6379
PORT=8000
EOF
    print_success "环境变量文件已创建"
else
    print_warning "环境变量文件已存在，跳过创建"
fi

# 4. 设置NGINX配置
echo ""
echo "[4/8] 配置NGINX..."
if [ ! -f "$NGINX_CONF" ]; then
    cp $APP_DIR/deployment/nginx-obsicat.conf $NGINX_CONF
    ln -s $NGINX_CONF $NGINX_ENABLED
    print_success "NGINX配置已设置"
else
    print_warning "NGINX配置已存在，更新中..."
    cp $APP_DIR/deployment/nginx-obsicat.conf $NGINX_CONF
    print_success "NGINX配置已更新"
fi

# 5. 测试NGINX配置
echo ""
echo "[5/8] 测试NGINX配置..."
nginx -t
print_success "NGINX配置测试通过"

# 6. 配置SSL证书 (使用Let's Encrypt)
echo ""
echo "[6/8] 配置SSL证书..."
if [ ! -d "/etc/letsencrypt/live/$DOMAIN" ]; then
    print_warning "首次部署，需要安装certbot并获取SSL证书"
    echo "运行以下命令获取证书:"
    echo "  sudo apt-get update && sudo apt-get install -y certbot python3-certbot-nginx"
    echo "  sudo certbot --nginx -d $DOMAIN -d www.$DOMAIN"
else
    print_success "SSL证书已存在"
    # 自动续期
    certbot renew --quiet
    print_success "SSL证书已检查/续期"
fi

# 7. 启动/重启服务
echo ""
echo "[7/8] 启动服务..."

# 使用systemd管理应用
if [ ! -f "/etc/systemd/system/ai-memory.service" ]; then
    cat > /etc/systemd/system/ai-memory.service <<EOF
[Unit]
Description=AI Memory Flask Application
After=network.target redis.service

[Service]
Type=simple
User=runner
WorkingDirectory=$APP_DIR
Environment="PATH=$APP_DIR/venv/bin"
EnvironmentFile=$APP_DIR/.env
ExecStart=/usr/local/bin/gunicorn -w 4 -b 0.0.0.0:8000 main:app
Restart=always

[Install]
WantedBy=multi-user.target
EOF
    systemctl daemon-reload
    print_success "Systemd服务文件已创建"
fi

systemctl enable ai-memory
systemctl restart ai-memory
print_success "应用服务已启动"

# 重启NGINX
systemctl reload nginx
print_success "NGINX已重启"

# 8. 健康检查
echo ""
echo "[8/8] 健康检查..."
sleep 3
if curl -f http://localhost:8000/ > /dev/null 2>&1; then
    print_success "应用运行正常"
else
    print_error "应用健康检查失败，请检查日志"
    journalctl -u ai-memory -n 50
    exit 1
fi

echo ""
echo "========================================="
echo -e "${GREEN}部署完成！${NC}"
echo "应用访问地址: https://$DOMAIN"
echo "API文档: https://$DOMAIN/docs"
echo ""
echo "常用命令:"
echo "  查看应用日志: sudo journalctl -u ai-memory -f"
echo "  重启应用: sudo systemctl restart ai-memory"
echo "  重启NGINX: sudo systemctl reload nginx"
echo "  查看应用状态: sudo systemctl status ai-memory"
echo "========================================="
