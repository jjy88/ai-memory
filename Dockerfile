FROM python:3.11-slim

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 默认端口
ENV PORT=8000
EXPOSE 8000

# main.py 里必须有 app 对象： app = Flask(__name__)
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:8000", "main:app"]
