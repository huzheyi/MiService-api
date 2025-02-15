# 使用 Python 3.13.2 作为基础镜像
FROM python:3.13.2-slim

# 设置工作目录
WORKDIR /app

# 安装 Git（用于拉取代码）
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# 克隆仓库（构建时拉取代码）
RUN git clone https://github.com/huzheyi/MiService-api.git /app

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 设置环境变量
ENV PYTHONUNBUFFERED=1
ENV MI_USER="YourMIUser"
ENV MI_PASS="YourMIPass"
ENV MI_DID="YourMIDid"

# 运行时自动拉取最新代码并启动应用
CMD ["sh", "-c", "cd /app && git pull && python server.py"]
