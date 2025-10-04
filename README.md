# Obsi喵 AI Memory 🐾

AI驱动的智能文档处理和记忆管理系统

## 功能特性

- 🔐 **JWT认证**: 安全的用户认证和授权系统
- 📄 **文档处理**: 支持PDF、Word、图片等多种格式
- 🤖 **AI总结**: 智能文档内容总结（基于Ollama）
- 💬 **聊天接口**: AI助手交互
- 💳 **支付集成**: 简单的支付和token管理
- 📚 **API文档**: 完整的API接口文档
- 🐳 **Docker支持**: 容器化开发和部署

## 快速开始

### 使用Docker Compose (推荐)

```bash
# 启动所有服务
docker-compose up -d

# 访问应用
open http://localhost:8000
open http://localhost:8000/docs  # API文档
```

### 本地开发

```bash
# 安装依赖
pip install -r requirements.txt

# 启动应用
python main.py
```

## API文档

访问 `/docs` 查看完整的API文档

### 主要端点

- `POST /auth/register` - 用户注册
- `POST /auth/login` - 用户登录（获取JWT）
- `POST /auth/refresh` - 刷新token
- `GET /auth/verify` - 验证token
- `POST /chat` - 聊天接口
- `POST /upload` - 文件上传
- `GET /health` - 健康检查

## 生产部署

详细部署文档请查看: [deployment/README.md](deployment/README.md)

```bash
# 一键部署到obsicat.com
sudo ./deployment/deploy.sh production
```

## 技术栈

- **后端**: Flask, Flask-JWT-Extended
- **认证**: JWT (JSON Web Tokens)
- **缓存**: Redis
- **文档处理**: PyPDF2, python-docx, Pytesseract
- **AI**: Ollama (可选)
- **容器**: Docker, Docker Compose
- **部署**: NGINX, Gunicorn, Systemd

## 项目结构

```
.
├── main.py              # 主应用入口
├── auth_routes.py       # JWT认证路由
├── chat_routes.py       # 聊天接口
├── upload_routes.py     # 文件上传处理
├── pay_routes.py        # 支付相关
├── token_utils.py       # Token工具函数
├── docker-compose.yml   # Docker编排配置
├── deployment/          # 部署相关文件
│   ├── nginx-obsicat.conf    # NGINX配置
│   ├── deploy.sh             # 自动化部署脚本
│   └── README.md             # 部署文档
└── requirements.txt     # Python依赖

```

## 升级说明

本项目最近完成了重要升级，详情请查看: [UPGRADE_SUMMARY.md](UPGRADE_SUMMARY.md)

主要改进:
- ✅ JWT认证替代简单token机制
- ✅ 专业的API文档系统
- ✅ Docker Compose本地开发环境
- ✅ 生产级NGINX配置和自动化部署

## 许可证

MIT License - 详见 [LICENSE](LICENSE)
