#!/bin/bash

echo "🔍 启动LangGraph任务监控页面"
echo "================================"

# 检查conda环境
if ! command -v conda &> /dev/null; then
    echo "❌ Conda 未安装，请先安装Anaconda或Miniconda"
    exit 1
fi

# 激活虚拟环境
echo "🔧 激活conda虚拟环境..."
source $(conda info --base)/etc/profile.d/conda.sh
conda activate ai-travel-agents

# 进入前端目录
cd frontend

# 检查后端服务
echo "🔍 检查后端服务状态..."
if ! curl -s http://localhost:8080/health > /dev/null; then
    echo "⚠️  警告: 后端API服务似乎未运行"
    echo "请先启动后端服务: ./start_backend.sh"
fi

# 启动任务监控页面
echo "🚀 启动任务监控页面..."
echo "🌐 监控页面: http://localhost:8502"
echo "================================"

streamlit run task_monitor.py --server.port 8502 --server.address 0.0.0.0
