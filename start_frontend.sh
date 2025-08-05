#!/bin/bash

echo "🌐 启动LangGraph多智能体AI旅行规划系统前端"
echo "=============================================="

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 未安装，请先安装Python3"
    exit 1
fi

# 进入前端目录
cd frontend

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

# 检查后端服务
echo "🔍 检查后端服务状态..."
if ! curl -s http://localhost:8000/health > /dev/null; then
    echo "⚠️  警告: 后端API服务似乎未运行"
    echo "请先启动后端服务: ./start_backend.sh"
    echo "或者在另一个终端中运行: cd backend && python api_server.py"
fi

# 启动Streamlit应用
echo "🚀 启动Streamlit前端应用..."
echo "🌐 前端地址: http://localhost:8501"
echo "=============================================="

streamlit run streamlit_app.py --server.port 8501 --server.address 0.0.0.0
