# 使用一个官方的 Python 运行时镜像作为基础镜像
FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# 复制当前目录的所有内容到容器的工作目录
COPY . /app

# 安装必要的系统依赖和 Python 包
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    && pip install --no-cache-dir -r requirements.txt

# 暴露 Flask 应用的端口
EXPOSE 6001

# 设置环境变量
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# 启动 Flask 应用
CMD ["flask", "run", "--host=0.0.0.0", "--port=6001"]
