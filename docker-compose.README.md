# Docker Compose开发环境快速启动指南

## 使用方法

### 启动所有服务
```bash
docker-compose up -d
```

### 查看日志
```bash
docker-compose logs -f
```

### 停止服务
```bash
docker-compose down
```

### 重启单个服务
```bash
docker-compose restart app
```

## 服务说明

- **app**: Flask应用，端口8000
- **redis**: Redis缓存和任务队列，端口6379

## 环境变量

创建 `.env` 文件配置环境变量:
```
JWT_SECRET_KEY=your-secret-key-here
REDIS_HOST=redis
REDIS_PORT=6379
```

## 访问应用

- 应用主页: http://localhost:8000
- API文档: http://localhost:8000/docs
- 支付页面: http://localhost:8000/pay

## 数据持久化

- Redis数据保存在Docker volume `redis-data`
- 上传文件映射到本地 `./uploads` 目录
- 静态文件映射到本地 `./static` 目录
