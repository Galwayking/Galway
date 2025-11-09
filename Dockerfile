FROM python:3.10-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 复制后端代码
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ ./backend/

# 复制前端代码
COPY frontend/ ./frontend/

# 暴露端口
EXPOSE 8000

# 启动后端服务
WORKDIR /app/backend
CMD ["python", "run.py"]
