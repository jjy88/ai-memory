# Obsi喵 AI Memory - 部署指南

本文档介绍如何将AI Memory项目部署到obsicat.com域名。

## 目录
- [系统要求](#系统要求)
- [本地开发](#本地开发)
- [生产部署](#生产部署)
- [API文档](#api文档)
- [JWT认证](#jwt认证)

## 系统要求

- Ubuntu 20.04+ 或类似Linux发行版
- Python 3.11+
- Docker & Docker Compose (可选，用于本地开发)
- NGINX
- Redis (可选，用于缓存和异步任务)

## 本地开发

### 使用Docker Compose (推荐)

1. 克隆项目:
```bash
git clone https://github.com/jjy88/ai-memory.git
cd ai-memory
```

2. 启动所有服务:
```bash
docker-compose up -d
```

3. 访问应用:
- 应用主页: http://localhost:8000
- API文档: http://localhost:8000/api/docs

4. 停止服务:
```bash
docker-compose down
```

### 不使用Docker

1. 安装依赖:
```bash
pip install -r requirements.txt
```

2. 启动应用:
```bash
python main.py
```

## 生产部署

### 快速部署

使用自动化部署脚本:

```bash
sudo ./deployment/deploy.sh production
```

### 手动部署步骤

#### 1. 安装系统依赖

```bash
sudo apt-get update
sudo apt-get install -y python3.11 python3-pip nginx redis-server certbot python3-certbot-nginx
```

#### 2. 克隆项目

```bash
cd /home/runner
git clone https://github.com/jjy88/ai-memory.git
cd ai-memory
```

#### 3. 安装Python依赖

```bash
pip install -r requirements.txt
```

#### 4. 配置环境变量

创建 `.env` 文件:
```bash
cat > .env <<EOF
JWT_SECRET_KEY=$(openssl rand -hex 32)
FLASK_ENV=production
REDIS_HOST=localhost
REDIS_PORT=6379
PORT=8000
EOF
```

#### 5. 配置NGINX

```bash
sudo cp deployment/nginx-obsicat.conf /etc/nginx/sites-available/obsicat.com
sudo ln -s /etc/nginx/sites-available/obsicat.com /etc/nginx/sites-enabled/
sudo nginx -t
```

#### 6. 获取SSL证书

```bash
sudo certbot --nginx -d obsicat.com -d www.obsicat.com
```

#### 7. 配置Systemd服务

创建 `/etc/systemd/system/ai-memory.service`:
```ini
[Unit]
Description=AI Memory Flask Application
After=network.target redis.service

[Service]
Type=simple
User=runner
WorkingDirectory=/home/runner/ai-memory
EnvironmentFile=/home/runner/ai-memory/.env
ExecStart=/usr/local/bin/gunicorn -w 4 -b 0.0.0.0:8000 main:app
Restart=always

[Install]
WantedBy=multi-user.target
```

启动服务:
```bash
sudo systemctl daemon-reload
sudo systemctl enable ai-memory
sudo systemctl start ai-memory
sudo systemctl reload nginx
```

#### 8. 验证部署

访问 https://obsicat.com 查看应用是否正常运行。

## API文档

访问 https://obsicat.com/docs 查看完整的API文档。

### 主要API端点:

- `POST /auth/register` - 用户注册
- `POST /auth/login` - 用户登录 (获取JWT token)
- `POST /auth/refresh` - 刷新access token
- `GET /auth/verify` - 验证JWT token
- `POST /chat` - 聊天接口
- `POST /upload` - 上传文件
- `GET /pay` - 支付页面
- `POST /pay/success` - 支付成功回调

## JWT认证

### 替换旧的Token机制

新版本使用JWT (JSON Web Tokens) 进行身份认证，替换了原有的简单token机制。

#### 使用流程:

1. **注册用户**:
```bash
curl -X POST https://obsicat.com/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "user1", "password": "password123"}'
```

2. **登录获取JWT**:
```bash
curl -X POST https://obsicat.com/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "user1", "password": "password123"}'
```

响应示例:
```json
{
  "message": "登录成功",
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user_id": "uuid-here"
}
```

3. **使用JWT访问受保护的API**:
```bash
curl -X POST https://obsicat.com/chat \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message": "你好"}'
```

### JWT vs 旧Token对比

| 特性 | 旧Token机制 | JWT机制 |
|------|-----------|---------|
| 安全性 | 较低 (简单UUID) | 高 (签名加密) |
| 过期管理 | 手动检查创建时间 | 自动过期验证 |
| 信息携带 | 需要查询数据库 | token内含用户信息 |
| 刷新机制 | 无 | 支持refresh token |
| 行业标准 | 否 | 是 |

## 维护和监控

### 查看日志
```bash
# 应用日志
sudo journalctl -u ai-memory -f

# NGINX日志
sudo tail -f /var/log/nginx/obsicat_access.log
sudo tail -f /var/log/nginx/obsicat_error.log
```

### 重启服务
```bash
# 重启应用
sudo systemctl restart ai-memory

# 重载NGINX配置
sudo systemctl reload nginx

# 重启Redis
sudo systemctl restart redis
```

### SSL证书自动续期

Certbot会自动配置证书续期，也可手动续期:
```bash
sudo certbot renew
```

## 故障排查

### 应用无法启动
```bash
# 检查服务状态
sudo systemctl status ai-memory

# 查看错误日志
sudo journalctl -u ai-memory -n 100
```

### NGINX 502错误
- 确认应用服务正在运行: `sudo systemctl status ai-memory`
- 检查端口占用: `sudo netstat -tulpn | grep 8000`

### SSL证书问题
```bash
# 测试证书配置
sudo certbot certificates

# 强制续期
sudo certbot renew --force-renewal
```

## 面试讲解要点

本项目的核心改进：

1. **专业的API文档**: 使用flask-restx自动生成Swagger文档，符合行业标准
2. **安全的JWT认证**: 替换简单token机制，提升安全性和专业性
3. **容器化开发**: Docker Compose简化本地开发环境设置
4. **生产级部署**: NGINX反向代理 + SSL + 自动化脚本，展示DevOps能力

所有改动都力求最小化和易理解，便于展示和维护。
