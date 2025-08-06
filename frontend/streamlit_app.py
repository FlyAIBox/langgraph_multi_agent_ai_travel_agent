#!/usr/bin/env python3
"""
LangGraph多智能体AI旅行规划系统 - Streamlit前端

这个模块提供基于Streamlit的Web前端界面，用户可以通过浏览器
与LangGraph多智能体旅行规划系统进行交互。

主要功能：
1. 用户友好的旅行规划表单
2. 实时显示规划进度
3. 展示多智能体协作结果
4. 下载规划报告
"""

import streamlit as st
import requests
import json
import time
from datetime import datetime, date, timedelta
from typing import Dict, Any, Optional
import pandas as pd

# 页面配置
st.set_page_config(
    page_title="LangGraph多智能体AI旅行规划师",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API基础URL
import os
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8080")

def check_api_health():
    """检查API服务状态"""
    try:
        # 增加超时时间到10秒
        response = requests.get(f"{API_BASE_URL}/health", timeout=10)
        return response.status_code == 200, response.json()
    except requests.exceptions.Timeout:
        return False, {"error": "API请求超时，请检查后端服务是否正常运行"}
    except requests.exceptions.ConnectionError:
        return False, {"error": "无法连接到API服务器，请确保后端服务已启动"}
    except Exception as e:
        return False, {"error": str(e)}

def create_travel_plan(travel_data: Dict[str, Any]) -> Optional[str]:
    """创建旅行规划任务"""
    try:
        # 增加超时时间到60秒
        response = requests.post(f"{API_BASE_URL}/plan", json=travel_data, timeout=60)
        if response.status_code == 200:
            return response.json()["task_id"]
        else:
            st.error(f"创建任务失败: {response.text}")
            return None
    except requests.exceptions.Timeout:
        st.error("创建任务超时，请稍后重试")
        return None
    except requests.exceptions.ConnectionError:
        st.error("无法连接到API服务器，请确保后端服务已启动")
        return None
    except Exception as e:
        st.error(f"API请求失败: {str(e)}")
        return None

def get_planning_status(task_id: str) -> Optional[Dict[str, Any]]:
    """获取规划状态"""
    max_retries = 3
    for retry in range(max_retries):
        try:
            # 增加超时时间到15秒
            response = requests.get(f"{API_BASE_URL}/status/{task_id}", timeout=15)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                st.error("任务不存在")
                return None
            else:
                st.warning(f"状态查询返回 {response.status_code}，正在重试...")
                continue
        except requests.exceptions.Timeout:
            if retry < max_retries - 1:
                st.warning(f"状态查询超时，正在重试 ({retry + 1}/{max_retries})...")
                time.sleep(2)  # 等待2秒后重试
                continue
            else:
                st.warning("状态查询超时，但任务可能仍在处理中...")
                return None
        except requests.exceptions.ConnectionError:
            st.error("无法连接到API服务器，请确保后端服务已启动")
            return None
        except Exception as e:
            if retry < max_retries - 1:
                st.warning(f"状态查询失败，正在重试: {str(e)}")
                time.sleep(1)
                continue
            else:
                st.error(f"获取状态失败: {str(e)}")
                return None
    return None

def display_header():
    """显示页面标题"""
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <h1>🌍 LangGraph多智能体AI旅行规划师</h1>
        <p style="font-size: 1.2rem; color: #666;">
            🤖 由Google Gemini Flash-2.0和DuckDuckGo搜索驱动的智能旅行规划系统
        </p>
    </div>
    """, unsafe_allow_html=True)

def display_agent_info():
    """显示智能体团队信息"""
    st.markdown("### 🎯 AI智能体团队")
    
    agents = [
        ("🎯", "协调员智能体", "工作流编排与决策综合"),
        ("✈️", "旅行顾问", "目的地专业知识与实时搜索"),
        ("💰", "预算优化师", "成本分析与实时定价"),
        ("🌤️", "天气分析师", "天气情报与当前数据"),
        ("🏠", "当地专家", "内部知识与实时本地信息"),
        ("📅", "行程规划师", "日程优化与物流安排")
    ]
    
    cols = st.columns(3)
    for i, (icon, name, desc) in enumerate(agents):
        with cols[i % 3]:
            st.markdown(f"""
            <div style="border: 1px solid #ddd; border-radius: 8px; padding: 1rem; margin: 0.5rem 0;">
                <h4>{icon} {name}</h4>
                <p style="font-size: 0.9rem; color: #666;">{desc}</p>
            </div>
            """, unsafe_allow_html=True)

def create_travel_form():
    """创建旅行规划表单"""
    st.markdown("### 📋 旅行规划表单")
    
    with st.form("travel_planning_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📍 基本信息")
            destination = st.text_input(
                "目的地城市",
                placeholder="例如: 北京, 上海, 成都...",
                help="请输入您想要前往的城市名称"
            )
            
            start_date = st.date_input(
                "开始日期",
                value=date.today() + timedelta(days=7),
                min_value=date.today()
            )
            
            end_date = st.date_input(
                "结束日期",
                value=date.today() + timedelta(days=14),
                min_value=start_date if 'start_date' in locals() else date.today()
            )
            
            group_size = st.number_input(
                "旅行人数",
                min_value=1,
                max_value=20,
                value=2,
                help="包括您自己在内的总人数"
            )
            
        with col2:
            st.markdown("#### 💰 预算与偏好")
            budget_range = st.selectbox(
                "预算范围",
                ["经济型", "中等预算", "豪华型"],
                help="选择适合您的预算类型"
            )
            
            currency = st.selectbox(
                "货币类型",
                ["CNY", "USD", "EUR", "GBP", "JPY", "CAD", "AUD"],
                help="选择您偏好的货币单位"
            )
            
            activity_level = st.selectbox(
                "活动强度",
                ["轻松", "适中", "活跃"],
                index=1,
                help="选择您偏好的旅行节奏"
            )
            
            travel_style = st.selectbox(
                "旅行风格",
                ["观光客", "探索者", "当地人"],
                index=1,
                help="选择您的旅行体验偏好"
            )
        
        st.markdown("#### 🎯 兴趣爱好")
        interests = st.multiselect(
            "选择您的兴趣爱好",
            ["历史", "文化", "美食", "艺术", "自然风光", "购物", "夜生活", 
             "博物馆", "建筑", "摄影", "音乐", "体育", "冒险活动"],
            default=["历史", "美食"],
            help="选择您感兴趣的活动类型"
        )
        
        col3, col4 = st.columns(2)
        with col3:
            dietary_restrictions = st.text_input(
                "饮食限制/偏好",
                placeholder="例如: 素食, 清真, 无麸质...",
                help="如有特殊饮食要求请填写"
            )
            
            transportation_preference = st.selectbox(
                "交通偏好",
                ["公共交通", "混合交通", "私人交通"],
                help="选择您偏好的交通方式"
            )
            
        with col4:
            accommodation_preference = st.text_input(
                "住宿偏好",
                placeholder="例如: 酒店, 民宿, 青旅...",
                help="描述您偏好的住宿类型"
            )
            
            special_requirements = st.text_area(
                "特殊要求",
                placeholder="其他特殊需求或要求...",
                help="任何其他需要考虑的特殊要求"
            )
        
        submitted = st.form_submit_button("🚀 开始AI智能规划", use_container_width=True)
        
        if submitted:
            # 验证输入
            if not destination:
                st.error("请输入目的地城市")
                return None
                
            if start_date >= end_date:
                st.error("结束日期必须晚于开始日期")
                return None
            
            # 构建请求数据
            travel_data = {
                "destination": destination,
                "start_date": start_date.strftime("%Y-%m-%d"),
                "end_date": end_date.strftime("%Y-%m-%d"),
                "budget_range": budget_range,
                "group_size": group_size,
                "interests": interests,
                "dietary_restrictions": dietary_restrictions,
                "activity_level": activity_level,
                "travel_style": travel_style,
                "transportation_preference": transportation_preference,
                "accommodation_preference": accommodation_preference,
                "special_requirements": special_requirements,
                "currency": currency
            }
            
            return travel_data
    
    return None

def display_planning_progress(task_id: str):
    """显示规划进度"""
    st.markdown("### 🔄 规划进度")

    progress_container = st.container()
    status_container = st.container()
    debug_container = st.container()

    # 创建进度条和状态显示
    progress_bar = progress_container.progress(0)
    status_text = status_container.empty()
    debug_text = debug_container.empty()
    
    # 轮询状态更新
    max_attempts = 360  # 最多等待6分钟（每秒轮询一次）
    attempt = 0
    
    last_known_status = None
    consecutive_failures = 0

    while attempt < max_attempts:
        status = get_planning_status(task_id)

        if status:
            # 重置失败计数
            consecutive_failures = 0
            last_known_status = status

            progress = status.get("progress", 0)
            current_status = status.get("status", "unknown")
            message = status.get("message", "处理中...")
            current_agent = status.get("current_agent", "")

            # 更新进度条
            progress_bar.progress(progress / 100)

            # 更新状态文本
            status_text.markdown(f"""
            **状态**: {current_status}
            **当前智能体**: {current_agent}
            **消息**: {message}
            **进度**: {progress}%
            """)

            # 检查是否完成
            if current_status == "completed":
                st.success("🎉 旅行规划完成！")
                return status.get("result")
            elif current_status == "failed":
                st.error(f"❌ 规划失败: {message}")
                return None

        else:
            # 状态查询失败，但继续尝试
            consecutive_failures += 1
            if last_known_status:
                # 显示最后已知状态
                progress = last_known_status.get("progress", 0)
                current_status = last_known_status.get("status", "unknown")
                message = f"连接中断，正在重试... (失败次数: {consecutive_failures})"
                current_agent = last_known_status.get("current_agent", "")

                status_text.markdown(f"""
                **状态**: {current_status} (连接中断)
                **当前智能体**: {current_agent}
                **消息**: {message}
                **进度**: {progress}%
                """)

            # 如果连续失败太多次，提示用户
            if consecutive_failures >= 10:
                st.warning("⚠️ 网络连接不稳定，但任务可能仍在后台处理中...")

        # 显示调试信息
        debug_text.markdown(f"""
        <details>
        <summary>🔍 调试信息</summary>

        - **任务ID**: {task_id}
        - **尝试次数**: {attempt + 1}/{max_attempts}
        - **连续失败**: {consecutive_failures}
        - **API地址**: {API_BASE_URL}
        - **当前时间**: {time.strftime('%H:%M:%S')}
        </details>
        """, unsafe_allow_html=True)

        time.sleep(1)
        attempt += 1
    
    # 超时后提供手动检查选项
    st.warning("⏰ 自动监控已超时，但任务可能仍在处理中")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 手动检查状态"):
            final_status = get_planning_status(task_id)
            if final_status:
                if final_status.get("status") == "completed":
                    st.success("🎉 任务已完成！")
                    return final_status.get("result")
                else:
                    st.info(f"任务状态: {final_status.get('status')} - {final_status.get('message')}")
            else:
                st.error("无法获取任务状态")

    with col2:
        if st.button("📥 尝试下载结果"):
            try:
                download_url = f"{API_BASE_URL}/download/{task_id}"
                response = requests.get(download_url, timeout=10)
                if response.status_code == 200:
                    st.success("✅ 结果文件可用")
                    st.download_button(
                        label="下载规划结果",
                        data=response.content,
                        file_name=f"travel_plan_{task_id[:8]}.json",
                        mime="application/json"
                    )
                else:
                    st.warning("结果文件暂不可用")
            except Exception as e:
                st.error(f"下载失败: {str(e)}")

    return None

def display_planning_result(result: Dict[str, Any]):
    """显示规划结果"""
    if not result:
        return
    
    st.markdown("### 📋 规划结果")
    
    travel_plan = result.get("travel_plan", {})
    agent_outputs = result.get("agent_outputs", {})
    
    # 显示行程概览
    st.markdown("#### 🌍 行程概览")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("目的地", travel_plan.get("destination", "未知"))
    with col2:
        st.metric("行程天数", f"{travel_plan.get('duration', 0)} 天")
    with col3:
        st.metric("团队人数", f"{travel_plan.get('group_size', 0)} 人")
    with col4:
        st.metric("预算类型", travel_plan.get("budget_range", "未知"))
    
    # 显示智能体贡献
    st.markdown("#### 🤖 智能体贡献")
    
    agent_names_cn = {
        'travel_advisor': '🏛️ 旅行顾问',
        'weather_analyst': '🌤️ 天气分析师',
        'budget_optimizer': '💰 预算优化师',
        'local_expert': '🏠 当地专家',
        'itinerary_planner': '📅 行程规划师'
    }
    
    for agent_name, output in agent_outputs.items():
        agent_display_name = agent_names_cn.get(agent_name, agent_name)
        
        with st.expander(f"{agent_display_name} - {output.get('status', '未知').upper()}"):
            response = output.get("response", "无输出")
            timestamp = output.get("timestamp", "")
            
            st.markdown(f"**完成时间**: {timestamp[:19] if timestamp else '未知'}")
            st.markdown("**专业建议**:")
            st.text_area("", value=response, height=200, disabled=True, key=f"agent_{agent_name}")

def main():
    """主函数"""
    display_header()
    
    # 检查API状态
    api_healthy, health_info = check_api_health()
    
    if not api_healthy:
        st.error("🚨 后端API服务不可用，请确保API服务器正在运行")
        st.code("cd backend && python api_server.py")
        return
    
    st.success("✅ API服务正常运行")
    
    # 显示智能体信息
    with st.expander("🤖 查看AI智能体团队", expanded=False):
        display_agent_info()
    
    # 创建旅行规划表单
    travel_data = create_travel_form()
    
    if travel_data:
        # 创建规划任务
        with st.spinner("正在创建规划任务..."):
            task_id = create_travel_plan(travel_data)
        
        if task_id:
            st.success(f"✅ 任务创建成功！任务ID: {task_id}")
            
            # 显示规划进度
            result = display_planning_progress(task_id)
            
            # 显示结果
            if result:
                display_planning_result(result)
                
                # 提供下载链接
                st.markdown("### 📥 下载报告")
                download_url = f"{API_BASE_URL}/download/{task_id}"
                st.markdown(f"[📄 下载完整规划报告]({download_url})")

if __name__ == "__main__":
    main()
