#!/bin/bash

# ============================================================================
# LangGraph多智能体AI旅行规划系统 - 服务重启脚本
# ============================================================================

echo "🔄 重启LangGraph多智能体AI旅行规划系统服务"
echo "=================================================="

# 停止现有服务
echo "🛑 停止现有服务..."

# 查找并停止API服务器进程
API_PID=$(ps aux | grep "python api_server.py" | grep -v grep | awk '{print $2}')
if [ ! -z "$API_PID" ]; then
    echo "停止API服务器 (PID: $API_PID)"
    kill -TERM $API_PID
    sleep 2
    # 强制杀死如果还在运行
    if kill -0 $API_PID 2>/dev/null; then
        echo "强制停止API服务器"
        kill -KILL $API_PID
    fi
fi

# 查找并停止Streamlit进程
STREAMLIT_PID=$(ps aux | grep "streamlit run streamlit_app.py" | grep -v grep | awk '{print $2}')
if [ ! -z "$STREAMLIT_PID" ]; then
    echo "停止Streamlit前端 (PID: $STREAMLIT_PID)"
    kill -TERM $STREAMLIT_PID
    sleep 2
    # 强制杀死如果还在运行
    if kill -0 $STREAMLIT_PID 2>/dev/null; then
        echo "强制停止Streamlit前端"
        kill -KILL $STREAMLIT_PID
    fi
fi

# 等待端口释放
echo "⏳ 等待端口释放..."
sleep 3

# 检查端口是否已释放
if lsof -i :8080 > /dev/null 2>&1; then
    echo "⚠️  端口8080仍被占用，尝试强制释放..."
    sudo fuser -k 8080/tcp
    sleep 2
fi

if lsof -i :8501 > /dev/null 2>&1; then
    echo "⚠️  端口8501仍被占用，尝试强制释放..."
    sudo fuser -k 8501/tcp
    sleep 2
fi

# 启动后端服务
echo "🚀 启动后端API服务..."
cd backend
source $(conda info --base)/etc/profile.d/conda.sh
conda activate ai-travel-agents

# 安装新的依赖
echo "📥 安装/更新依赖..."
pip install -r requirements.txt

# 后台启动API服务器
nohup python api_server.py > ../logs/api_server.log 2>&1 &
API_PID=$!
echo "✅ API服务器已启动 (PID: $API_PID)"

# 等待API服务器启动
echo "⏳ 等待API服务器启动..."
sleep 5

# 检查API服务器是否正常启动
for i in {1..10}; do
    if curl -s http://172.16.1.3:8080/health > /dev/null 2>&1; then
        echo "✅ API服务器运行正常"
        break
    else
        echo "⏳ 等待API服务器响应... ($i/10)"
        sleep 2
    fi
done

# 启动前端服务
echo "🌐 启动前端Streamlit服务..."
cd ../frontend

# 安装前端依赖
echo "📥 安装前端依赖..."
pip install -r requirements.txt

# 后台启动Streamlit
nohup streamlit run streamlit_app.py --server.port 8501 --server.address 0.0.0.0 > ../logs/streamlit.log 2>&1 &
STREAMLIT_PID=$!
echo "✅ Streamlit前端已启动 (PID: $STREAMLIT_PID)"

# 等待前端启动
echo "⏳ 等待前端服务启动..."
sleep 5

# 创建日志目录
mkdir -p ../logs

# 保存进程ID
echo $API_PID > ../logs/api_server.pid
echo $STREAMLIT_PID > ../logs/streamlit.pid

echo "=================================================="
echo "🎉 服务重启完成！"
echo "📍 API文档: http://172.16.1.3:8080/docs"
echo "🔧 健康检查: http://172.16.1.3:8080/health"
echo "🌐 前端界面: http://localhost:8501"
echo "📊 查看日志: tail -f logs/api_server.log"
echo "=================================================="

# 显示服务状态
echo "📊 当前服务状态:"
ps aux | grep -E "(api_server.py|streamlit)" | grep -v grep 