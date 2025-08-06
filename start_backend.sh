#!/bin/bash

# ============================================================================
# 安装说明（环境配置与依赖安装指南）
# ============================================================================
#
# 1. 创建虚拟环境（推荐）：
#    conda create -n ai-travel-agents python=3.10
#    conda activate ai-travel-agents
#
# 2. 安装依赖：
#    pip install -r requirements.txt
#
# 3. 配置环境变量：
#    创建 .env 文件，添加必要的接口密钥
#    GOOGLE_API_KEY=你的谷歌接口密钥
#
# ============================================================================

echo "🚀 启动LangGraph多智能体AI旅行规划系统后端服务"
echo "=================================================="

# 检查conda环境
if ! command -v conda &> /dev/null; then
    echo "❌ Conda 未安装，请先安装Anaconda或Miniconda"
    echo "下载地址: https://docs.conda.io/en/latest/miniconda.html"
    exit 1
fi

# 进入后端目录
cd backend

# 检查是否存在conda虚拟环境
if ! conda env list | grep -q "ai-travel-agents"; then
    echo "📦 创建conda虚拟环境..."
    conda create -n ai-travel-agents python=3.10 -y
fi

# 激活虚拟环境
echo "🔧 激活conda虚拟环境..."
source $(conda info --base)/etc/profile.d/conda.sh
conda activate ai-travel-agents

# 安装依赖
echo "📥 安装依赖包..."
pip install -r requirements.txt

# 检查环境变量
if [ ! -f "../.env" ]; then
    echo "⚠️  警告: 未找到.env文件，请确保设置了GOOGLE_API_KEY"
    echo "创建.env文件示例:"
    echo "GOOGLE_API_KEY=your_google_api_key_here"
fi

# 启动API服务器
echo "🌐 启动FastAPI服务器..."
echo "📍 API文档: http://localhost:8000/docs"
echo "🔧 健康检查: http://localhost:8000/health"
echo "=================================================="

python api_server.py
