#!/usr/bin/env python3
"""
任务监控页面

专门用于监控长时间运行的LangGraph任务
"""

import streamlit as st
import requests
import time
import json
from datetime import datetime
import os

# API基础URL
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8080")

st.set_page_config(
    page_title="任务监控 - LangGraph旅行规划",
    page_icon="🔍",
    layout="wide"
)

def check_api_health():
    """检查API健康状态"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def get_task_status(task_id):
    """获取任务状态"""
    try:
        response = requests.get(f"{API_BASE_URL}/status/{task_id}", timeout=10)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            return {"error": "任务不存在"}
        else:
            return {"error": f"HTTP {response.status_code}"}
    except requests.exceptions.Timeout:
        return {"error": "请求超时"}
    except requests.exceptions.ConnectionError:
        return {"error": "连接失败"}
    except Exception as e:
        return {"error": str(e)}

def download_result(task_id):
    """下载任务结果"""
    try:
        response = requests.get(f"{API_BASE_URL}/download/{task_id}", timeout=15)
        if response.status_code == 200:
            return response.content
        else:
            return None
    except:
        return None

def main():
    st.title("🔍 LangGraph任务监控")
    st.markdown("---")
    
    # 检查API状态
    if not check_api_health():
        st.error("🚨 后端API服务不可用")
        st.info("请确保后端服务正在运行: `cd backend && python api_server.py`")
        return
    
    st.success("✅ 后端API服务正常")
    
    # 任务ID输入
    st.subheader("📋 任务查询")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        task_id = st.text_input(
            "任务ID",
            placeholder="输入完整的任务ID，例如: 521f1fcf-2591-4b1a-9bc3-c654ae09c690",
            help="从前端页面或日志中获取的任务ID"
        )
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)  # 添加间距
        check_button = st.button("🔍 检查状态", type="primary")
    
    if task_id and check_button:
        st.markdown("---")
        
        # 显示任务信息
        st.subheader(f"📊 任务状态: {task_id[:8]}...")
        
        # 创建状态显示区域
        status_container = st.container()
        progress_container = st.container()
        details_container = st.container()
        
        with st.spinner("正在查询任务状态..."):
            status = get_task_status(task_id)
        
        if "error" in status:
            st.error(f"❌ 查询失败: {status['error']}")
            
            if status['error'] == "任务不存在":
                st.info("💡 请检查任务ID是否正确")
            elif "连接失败" in status['error'] or "超时" in status['error']:
                st.warning("🔄 网络问题，请稍后重试")
                
        else:
            # 显示状态信息
            task_status = status.get("status", "unknown")
            progress = status.get("progress", 0)
            message = status.get("message", "")
            current_agent = status.get("current_agent", "")
            
            # 状态指示器
            with status_container:
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    if task_status == "completed":
                        st.success("✅ 已完成")
                    elif task_status == "failed":
                        st.error("❌ 失败")
                    elif task_status == "processing":
                        st.info("🔄 处理中")
                    else:
                        st.warning(f"⚠️ {task_status}")
                
                with col2:
                    st.metric("进度", f"{progress}%")
                
                with col3:
                    st.metric("当前智能体", current_agent or "无")
                
                with col4:
                    st.metric("查询时间", datetime.now().strftime("%H:%M:%S"))
            
            # 进度条
            with progress_container:
                st.progress(progress / 100)
                st.caption(message)
            
            # 详细信息
            with details_container:
                st.subheader("📋 详细信息")
                
                info_data = {
                    "任务ID": task_id,
                    "状态": task_status,
                    "进度": f"{progress}%",
                    "当前智能体": current_agent,
                    "消息": message,
                    "API地址": API_BASE_URL
                }
                
                for key, value in info_data.items():
                    st.text(f"{key}: {value}")
            
            # 操作按钮
            st.subheader("🛠️ 操作")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("🔄 刷新状态"):
                    st.rerun()
            
            with col2:
                if task_status == "completed":
                    if st.button("📥 下载结果"):
                        result_data = download_result(task_id)
                        if result_data:
                            st.download_button(
                                label="💾 保存结果文件",
                                data=result_data,
                                file_name=f"travel_plan_{task_id[:8]}.json",
                                mime="application/json"
                            )
                            st.success("✅ 结果可下载")
                        else:
                            st.error("❌ 下载失败")
            
            with col3:
                if task_status == "processing":
                    st.info("⏳ 任务正在处理中，请耐心等待")
                elif task_status == "failed":
                    st.error("💥 任务执行失败")
            
            # 自动刷新选项
            st.markdown("---")
            st.subheader("⚙️ 自动刷新")
            
            auto_refresh = st.checkbox("启用自动刷新 (每30秒)")
            
            if auto_refresh and task_status == "processing":
                time.sleep(30)
                st.rerun()
    
    # 使用说明
    st.markdown("---")
    st.subheader("💡 使用说明")
    
    st.markdown("""
    1. **获取任务ID**: 从主页面创建任务后，复制任务ID
    2. **输入任务ID**: 在上方输入框中粘贴完整的任务ID
    3. **检查状态**: 点击"检查状态"按钮查询任务进度
    4. **自动刷新**: 对于处理中的任务，可启用自动刷新
    5. **下载结果**: 任务完成后，可下载完整的规划结果
    
    **任务状态说明**:
    - 🔄 **处理中**: 智能体正在协作规划
    - ✅ **已完成**: 规划完成，可下载结果
    - ❌ **失败**: 规划过程中出现错误
    """)

if __name__ == "__main__":
    main()
