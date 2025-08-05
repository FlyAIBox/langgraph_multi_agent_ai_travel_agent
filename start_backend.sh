#!/bin/bash

echo "🚀 启动LangGraph多智能体AI旅行规划系统后端服务"
echo "=================================================="

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 未安装，请先安装Python3"
    exit 1
fi

# 进入后端目录
cd backend

# 检查是否存在虚拟环境
if [ ! -d "venv" ]; then
    echo "📦 创建Python虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
echo "🔧 激活虚拟环境..."
source venv/bin/activate

# 安装依赖
echo "📥 安装依赖包..."
pip install -r requirements.txt

# 检查环境变量
if [ ! -f "../.env" ]; then
    echo "⚠️  警告: 未找到.env文件，请确保设置了GEMINI_API_KEY"
    echo "创建.env文件示例:"
    echo "GEMINI_API_KEY=your_api_key_here"
fi

# 启动API服务器
echo "🌐 启动FastAPI服务器..."
echo "📍 API文档: http://localhost:8000/docs"
echo "🔧 健康检查: http://localhost:8000/health"
echo "=================================================="

python api_server.py
