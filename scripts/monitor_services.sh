#!/bin/bash

# ============================================================================
# AI旅行规划智能体 - 服务监控脚本
# ============================================================================

echo "📊 AI旅行规划智能体 - 服务状态监控"
echo "=================================================="

# 检查API服务器状态
echo "🔍 检查API服务器状态..."
API_PID=$(ps aux | grep "python api_server.py" | grep -v grep | awk '{print $2}')
if [ ! -z "$API_PID" ]; then
    echo "✅ API服务器运行中 (PID: $API_PID)"
    
    # 检查端口监听
    if netstat -tlnp | grep ":8080" > /dev/null; then
        echo "✅ 端口8080正在监听"
        
        # 测试API响应
        if curl -s http://172.16.1.3:8080/health > /dev/null 2>&1; then
            echo "✅ API健康检查通过"
            HEALTH_RESPONSE=$(curl -s http://172.16.1.3:8080/health)
            echo "📋 健康状态详情:"
            echo "$HEALTH_RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$HEALTH_RESPONSE"
        else
            echo "❌ API健康检查失败"
        fi
    else
        echo "❌ 端口8080未监听"
    fi
else
    echo "❌ API服务器未运行"
fi

echo ""

# 检查Streamlit前端状态
echo "🔍 检查Streamlit前端状态..."
STREAMLIT_PID=$(ps aux | grep "streamlit run streamlit_app.py" | grep -v grep | awk '{print $2}')
if [ ! -z "$STREAMLIT_PID" ]; then
    echo "✅ Streamlit前端运行中 (PID: $STREAMLIT_PID)"
    
    # 检查端口监听
    if netstat -tlnp | grep ":8501" > /dev/null; then
        echo "✅ 端口8501正在监听"
        
        # 测试前端响应
        if curl -s http://localhost:8501 > /dev/null 2>&1; then
            echo "✅ 前端服务响应正常"
        else
            echo "❌ 前端服务响应异常"
        fi
    else
        echo "❌ 端口8501未监听"
    fi
else
    echo "❌ Streamlit前端未运行"
fi

echo ""

# 检查系统资源
echo "🔍 检查系统资源..."
echo "CPU使用率: $(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)%"
echo "内存使用率: $(free | grep Mem | awk '{printf("%.1f%%", $3/$2 * 100.0)}')"
echo "磁盘使用率: $(df -h / | tail -1 | awk '{print $5}')"

echo ""

# 检查日志文件
echo "🔍 检查日志文件..."
if [ -f "logs/api_server.log" ]; then
    echo "✅ API服务器日志存在"
    echo "📋 最近5行日志:"
    tail -5 logs/api_server.log
else
    echo "❌ API服务器日志不存在"
fi

echo ""

if [ -f "logs/streamlit.log" ]; then
    echo "✅ Streamlit前端日志存在"
    echo "📋 最近5行日志:"
    tail -5 logs/streamlit.log
else
    echo "❌ Streamlit前端日志不存在"
fi

echo ""

# 检查环境变量
echo "🔍 检查环境配置..."
if [ -f ".env" ]; then
    echo "✅ .env文件存在"
    if grep -q "GEMINI_API_KEY" .env; then
        echo "✅ GEMINI_API_KEY已配置"
    else
        echo "❌ GEMINI_API_KEY未配置"
    fi
else
    echo "❌ .env文件不存在"
fi

echo ""
echo "=================================================="
echo "📊 监控完成"
echo "🔄 运行 ./restart_services.sh 重启服务"
echo "📋 运行 tail -f logs/api_server.log 查看实时日志" 