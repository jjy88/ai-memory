# AI Memory - 智能文档处理与记忆管理系统

<div align="center">

![Python](https://img.shields.io/badge/python-3.11-blue.svg)
![Flask](https://img.shields.io/badge/flask-2.3+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![CI/CD](https://github.com/jjy88/ai-memory/workflows/CI%2FCD%20Pipeline/badge.svg)

一个功能完整、架构专业的AI驱动文档处理和记忆管理平台

[功能特性](#功能特性) • [快速开始](#快速开始) • [API文档](#api文档) • [架构设计](#架构设计) • [部署](#部署)

</div>

---

## 功能特性

### 🔐 安全认证系统
- **JWT认证**: 基于JSON Web Token的安全认证机制
- **多层级权限**: Free、Premium、Admin三级用户权限系统
- **速率限制**: 防止API滥用，保护系统资源
- **数据验证**: 使用Marshmallow进行请求数据验证

### 📄 文档处理
- **多格式支持**: PDF, DOCX, JPG, PNG, HEIC
- **OCR识别**: 图片文本提取（中英文）
- **智能总结**: AI驱动的文档内容总结
- **异步处理**: Celery支持的后台任务处理

### 💬 智能对话
- **上下文管理**: 支持多轮对话
- **AI集成**: 与Ollama模型集成
- **个性化响应**: 基于用户历史的智能回复

### 📊 管理面板
- **使用统计**: 实时系统使用数据
- **用户管理**: 完整的用户CRUD操作
- **权限控制**: 细粒度的访问控制

### 🚀 现代化DevOps
- **容器化**: Docker & Docker Compose支持
- **CI/CD**: GitHub Actions自动化测试和部署
- **监控健康**: 内置健康检查端点
- **缓存优化**: Redis缓存层提升性能

---

## 快速开始

### 前置要求
- Python 3.11+
- Redis 6.0+ (可选，用于缓存和任务队列)
- Docker & Docker Compose (可选)

### 本地开发

1. **克隆仓库**
```bash
git clone https://github.com/jjy88/ai-memory.git
cd ai-memory
```

2. **创建虚拟环境**
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. **安装依赖**
```bash
pip install -r requirements.txt
```

4. **配置环境变量**
```bash
cp .env.example .env
# 编辑 .env 文件，设置必要的环境变量
```

5. **启动Redis (可选)**
```bash
# 使用Docker
docker run -d -p 6379:6379 redis:7-alpine

# 或使用本地安装的Redis
redis-server
```

6. **运行应用**
```bash
python main.py
```

应用将在 `http://localhost:5000` 启动

7. **访问API文档**
打开浏览器访问: `http://localhost:5000/api/v1/docs`

### 使用Docker Compose

```bash
# 启动所有服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

---

## API文档

### 认证端点

#### 注册用户
```bash
POST /api/v1/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

#### 登录
```bash
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

#### 获取当前用户信息
```bash
GET /api/v1/auth/me
Authorization: Bearer <access_token>
```

### 文件上传端点

#### 上传文件
```bash
POST /api/v1/upload/
Authorization: Bearer <access_token>
Content-Type: multipart/form-data

files: <file1>, <file2>, ...
```

#### 查询上传状态
```bash
GET /api/v1/upload/<upload_id>
Authorization: Bearer <access_token>
```

### 聊天端点

#### 发送消息
```bash
POST /api/v1/chat/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "message": "你好，请帮我总结一下文档",
  "context_id": "optional-context-id"
}
```

### 管理员端点

#### 获取系统统计
```bash
GET /api/v1/admin/stats
Authorization: Bearer <admin_access_token>
```

#### 列出所有用户
```bash
GET /api/v1/admin/users
Authorization: Bearer <admin_access_token>
```

#### 更新用户权限
```bash
PUT /api/v1/admin/users/<user_id>
Authorization: Bearer <admin_access_token>
Content-Type: application/json

{
  "role": "premium",
  "is_active": true
}
```

完整的API文档可通过Swagger UI访问: `/api/v1/docs`

---

## 架构设计

### 技术栈

**后端框架**
- Flask 2.3+ - Web框架
- Flask-RESTX - REST API和Swagger文档
- Flask-JWT-Extended - JWT认证
- Flask-Limiter - 速率限制
- Flask-CORS - 跨域支持

**数据验证**
- Marshmallow - 数据序列化和验证

**异步任务**
- Celery - 分布式任务队列
- Redis - 消息代理和结果存储

**文档处理**
- PyTesseract - OCR文本识别
- PyPDF2 - PDF处理
- python-docx - Word文档处理
- Pillow - 图像处理

**部署和DevOps**
- Docker - 容器化
- Docker Compose - 多容器编排
- GitHub Actions - CI/CD
- Gunicorn - WSGI服务器

### 项目结构

```
ai-memory/
├── api/                    # REST API模块
│   ├── __init__.py        # API蓝图和命名空间
│   ├── auth_api.py        # 认证接口
│   ├── upload_api.py      # 上传接口
│   ├── chat_api.py        # 聊天接口
│   └── admin_api.py       # 管理接口
├── tests/                  # 测试套件
│   ├── conftest.py        # pytest配置
│   ├── test_auth_api.py   # 认证测试
│   ├── test_admin_api.py  # 管理测试
│   └── test_chat_api.py   # 聊天测试
├── templates/              # HTML模板
├── static/                 # 静态文件
├── uploads/                # 上传文件存储
├── main.py                 # 应用入口
├── config.py               # 配置管理
├── models.py               # 数据模型
├── auth_utils.py           # 认证工具
├── schemas.py              # 数据验证模式
├── tasks.py                # Celery任务
├── requirements.txt        # Python依赖
├── docker-compose.yml      # Docker Compose配置
├── Dockerfile              # Docker镜像
├── .env.example            # 环境变量模板
└── .github/
    └── workflows/
        └── ci.yml          # CI/CD配置
```

### 系统架构

```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────┐
│  Nginx (Reverse Proxy)          │
└──────┬──────────────────────────┘
       │
       ▼
┌─────────────────────────────────┐
│  Flask App (Gunicorn)           │
│  ├── API Routes                 │
│  ├── JWT Auth                   │
│  ├── Rate Limiting              │
│  └── CORS                       │
└──────┬──────────────┬───────────┘
       │              │
       ▼              ▼
┌─────────────┐  ┌──────────────┐
│   Redis     │  │   Celery     │
│  (Cache &   │  │   Workers    │
│   Queue)    │  │              │
└─────────────┘  └──────────────┘
```

---

## 部署

### 环境变量配置

创建 `.env` 文件并配置以下变量:

```bash
# Flask配置
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here

# Redis配置
REDIS_URL=redis://localhost:6379/0

# Celery配置
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# 自定义域名
CUSTOM_DOMAIN=obsicat.com
```

### 生产环境部署

1. **使用Docker部署**

```bash
# 构建镜像
docker build -t ai-memory:latest .

# 运行容器
docker run -d \
  -p 8000:8000 \
  -e FLASK_ENV=production \
  -e SECRET_KEY=your-secret \
  -e REDIS_URL=redis://redis:6379/0 \
  --name ai-memory \
  ai-memory:latest
```

2. **使用Docker Compose部署**

```bash
# 生产环境启动
docker-compose -f docker-compose.yml up -d

# 扩展worker数量
docker-compose up -d --scale celery_worker=3
```

3. **传统部署**

```bash
# 安装依赖
pip install -r requirements.txt

# 启动应用
gunicorn -w 4 -b 0.0.0.0:8000 --timeout 120 main:app

# 启动Celery worker
celery -A tasks.celery worker --loglevel=info

# 启动Celery beat (定时任务)
celery -A tasks.celery beat --loglevel=info
```

---

## 开发指南

### 运行测试

```bash
# 安装测试依赖
pip install pytest pytest-cov

# 运行所有测试
pytest

# 运行测试并生成覆盖率报告
pytest --cov=. --cov-report=html

# 运行特定测试
pytest tests/test_auth_api.py
```

### 代码质量检查

```bash
# 安装flake8
pip install flake8

# 检查代码质量
flake8 . --max-line-length=127 --exclude=venv,__pycache__
```

---

## 路线图

- [x] JWT认证系统
- [x] RESTful API with Swagger
- [x] 多层级用户权限
- [x] 速率限制
- [x] Docker支持
- [x] CI/CD管道
- [x] 自动化测试
- [ ] 数据库持久化 (PostgreSQL)
- [ ] WebSocket实时通信
- [ ] 文件版本控制
- [ ] 高级AI模型集成
- [ ] 多语言支持
- [ ] 移动端应用

---

## 贡献

欢迎贡献! 请查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解详情。

---

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

---

## 联系方式

- 项目主页: [https://github.com/jjy88/ai-memory](https://github.com/jjy88/ai-memory)
- 官方网站: [https://obsicat.com](https://obsicat.com)
- 问题反馈: [GitHub Issues](https://github.com/jjy88/ai-memory/issues)

---

<div align="center">
Made with ❤️ by Jynxzzz
</div>
