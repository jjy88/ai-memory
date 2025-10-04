# 快速开始指南

本指南帮助你快速了解和使用Obsi喵 AI Memory项目的新功能。

## 5分钟快速体验

### 1. 启动应用

选择以下任一方式：

#### 方式A: 使用Docker Compose (推荐)
```bash
docker-compose up -d
```

#### 方式B: 本地Python
```bash
pip install -r requirements.txt
python main.py
```

应用将在 `http://localhost:8000` 启动

### 2. 查看API文档

打开浏览器访问: http://localhost:8000/docs

你将看到所有可用的API端点和使用说明。

### 3. 测试JWT认证

运行示例脚本：
```bash
bash examples/jwt_demo.sh
```

或手动测试：

```bash
# 1. 注册用户
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "myuser", "password": "mypass123"}'

# 2. 登录获取JWT
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "myuser", "password": "mypass123"}'

# 将返回的access_token保存，用于后续请求
```

### 4. 使用JWT访问受保护资源

```bash
# 替换 YOUR_ACCESS_TOKEN 为登录返回的实际token
curl -X GET http://localhost:8000/auth/verify \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## 主要功能概览

### JWT认证系统

- ✅ 安全的用户注册和登录
- ✅ Access token (7天有效期)
- ✅ Refresh token (30天有效期)
- ✅ Token验证和刷新机制

### API端点

| 端点 | 方法 | 说明 |
|------|------|------|
| `/auth/register` | POST | 用户注册 |
| `/auth/login` | POST | 用户登录 |
| `/auth/refresh` | POST | 刷新token |
| `/auth/verify` | GET | 验证token |
| `/chat` | POST | 聊天接口 |
| `/upload` | POST | 文件上传 |
| `/pay` | GET | 支付页面 |
| `/health` | GET | 健康检查 |
| `/docs` | GET | API文档 |

## Docker Compose使用

### 启动服务
```bash
docker-compose up -d
```

### 查看日志
```bash
docker-compose logs -f app
docker-compose logs -f redis
```

### 停止服务
```bash
docker-compose down
```

### 重启单个服务
```bash
docker-compose restart app
```

## 生产环境部署

### 快速部署到服务器

1. 克隆项目到服务器
```bash
git clone https://github.com/jjy88/ai-memory.git
cd ai-memory
```

2. 运行自动化部署脚本
```bash
sudo ./deployment/deploy.sh production
```

3. 访问你的域名
```
https://obsicat.com
https://obsicat.com/docs
```

详细部署说明请查看: [deployment/README.md](deployment/README.md)

## 环境变量配置

创建 `.env` 文件 (或使用 `.env.example` 作为模板):

```bash
# 复制模板
cp .env.example .env

# 编辑配置
nano .env
```

重要配置项:
- `JWT_SECRET_KEY`: JWT签名密钥（生产环境必须修改）
- `FLASK_ENV`: 环境类型 (development/production)
- `REDIS_HOST`: Redis服务器地址
- `PORT`: 应用端口

## 常见问题

### Q: 如何生成安全的JWT密钥？
```bash
openssl rand -hex 32
```

### Q: 如何查看应用日志？
```bash
# Docker环境
docker-compose logs -f app

# 生产环境 (Systemd)
sudo journalctl -u ai-memory -f
```

### Q: 如何重启应用？
```bash
# Docker环境
docker-compose restart app

# 生产环境
sudo systemctl restart ai-memory
```

### Q: Token过期了怎么办？
使用refresh token获取新的access token:
```bash
curl -X POST http://localhost:8000/auth/refresh \
  -H "Authorization: Bearer YOUR_REFRESH_TOKEN"
```

## 下一步

- 阅读 [UPGRADE_SUMMARY.md](UPGRADE_SUMMARY.md) 了解项目升级详情
- 查看 [deployment/README.md](deployment/README.md) 学习生产部署
- 探索 `/docs` 页面了解完整API
- 运行 `examples/jwt_demo.sh` 查看JWT认证演示

## 获取帮助

- 查看API文档: http://localhost:8000/docs
- 阅读项目README: [README.md](README.md)
- 查看升级说明: [UPGRADE_SUMMARY.md](UPGRADE_SUMMARY.md)

---

**提示**: 所有改进都遵循最小化改动原则，现有功能完全兼容！
