FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 先拷贝依赖文件并安装
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 再拷贝剩余代码
COPY . .

# 设置 Flask/Gunicorn 启动端口（平台会注入PORT环境变量）
ENV PORT=8000

# 开放端口
EXPOSE 8000

# use Gunicorn start Flask app.py's app object
CMD ["gunicorn","-w","2","-b","0.0.0.0:8000","app:app"]

