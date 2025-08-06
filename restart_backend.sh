#!/bin/bash

echo "🔄 重启LangGraph后端服务"
echo "========================"

# 杀死现有的后端进程
echo "🛑 停止现有后端进程..."
pkill -f "api_server.py" || echo "没有找到运行中的后端进程"
pkill -f "python.*api_server" || echo "没有找到运行中的API服务器"

# 等待进程完全停止
sleep 2

# 检查端口是否被释放
echo "🔍 检查端口8080状态..."
if lsof -i :8080 > /dev/null 2>&1; then
    echo "⚠️  端口8080仍被占用，尝试强制释放..."
    lsof -ti :8080 | xargs kill -9 2>/dev/null || echo "无法强制释放端口"
    sleep 2
fi

# 激活conda环境
echo "🔧 激活conda环境..."
source $(conda info --base)/etc/profile.d/conda.sh
conda activate ai-travel-agents

# 进入后端目录
cd backend

# 清理Python缓存
echo "🧹 清理Python缓存..."
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
find . -name "*.pyc" -delete 2>/dev/null || true

# 检查环境变量
echo "🔍 检查环境变量..."
if [ ! -f "../.env" ]; then
    echo "⚠️  警告: 未找到.env文件"
    echo "请确保设置了GOOGLE_API_KEY"
else
    echo "✅ .env文件存在"
fi

# 启动后端服务
echo "🚀 启动后端服务..."
echo "📍 API文档: http://localhost:8080/docs"
echo "🔧 健康检查: http://localhost:8080/health"
echo "========================"

python api_server.py
