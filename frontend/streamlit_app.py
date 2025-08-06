#!/usr/bin/env python3
"""
AI旅行规划智能体 - Streamlit前端

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
    page_title="AI旅行规划智能体",
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
        <h1>🌍 AI旅行规划智能体</h1>
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

def generate_markdown_report(result: Dict[str, Any], task_id: str) -> str:
    """生成Markdown格式的旅行规划报告"""
    if not result:
        return "# 旅行规划报告\n\n无可用数据"

    travel_plan = result.get("travel_plan", {})
    agent_outputs = result.get("agent_outputs", {})

    # 获取基本信息
    destination = travel_plan.get("destination", "未知")
    duration = travel_plan.get("duration", 0)
    group_size = travel_plan.get("group_size", 0)
    budget_range = travel_plan.get("budget_range", "未知")
    interests = travel_plan.get("interests", [])
    travel_dates = travel_plan.get("travel_dates", "未知")

    # 生成Markdown内容
    markdown_content = f"""# 🌍 {destination}旅行规划报告

## 📋 规划概览

| 项目 | 详情 |
|------|------|
| 🎯 目的地 | {destination} |
| 📅 旅行时间 | {travel_dates} |
| ⏰ 行程天数 | {duration}天 |
| 👥 团队人数 | {group_size}人 |
| 💰 预算类型 | {budget_range} |
| 🎨 兴趣爱好 | {', '.join(interests) if interests else '无特殊偏好'} |

---

## 🤖 AI智能体专业建议

"""

    # 智能体名称映射
    agent_names_cn = {
        'travel_advisor': '🏛️ 旅行顾问',
        'weather_analyst': '🌤️ 天气分析师',
        'budget_optimizer': '💰 预算优化师',
        'local_expert': '🏠 当地专家',
        'itinerary_planner': '📅 行程规划师'
    }

    # 添加各智能体的建议
    for agent_name, output in agent_outputs.items():
        agent_display_name = agent_names_cn.get(agent_name, agent_name)
        status = output.get('status', '未知')
        response = output.get('response', '无输出')
        timestamp = output.get('timestamp', '')

        markdown_content += f"""### {agent_display_name}

**状态**: {status.upper()}
**完成时间**: {timestamp[:19] if timestamp else '未知'}

{response}

---

"""

    # 添加生成信息
    from datetime import datetime
    markdown_content += f"""## 📄 报告信息

- **任务ID**: `{task_id}`
- **生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **生成方式**: LangGraph多智能体AI系统
- **报告格式**: Markdown

---

*本报告由AI旅行规划智能体自动生成*
"""

    return markdown_content

def check_pdf_capability() -> bool:
    """检查PDF生成能力"""
    try:
        import reportlab
        return True
    except ImportError:
        return False

def generate_pdf_report(result: Dict[str, Any], task_id: str) -> bytes:
    """生成PDF格式的旅行规划报告"""
    try:
        # 尝试导入reportlab
        from reportlab.lib.pagesizes import A4
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib import colors
        from io import BytesIO

        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=50, bottomMargin=50)
        styles = getSampleStyleSheet()
        story = []

        # 自定义样式
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=1,  # 居中
            textColor=colors.darkblue
        )

        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            spaceAfter=15,
            textColor=colors.darkgreen
        )

        travel_plan = result.get("travel_plan", {})
        destination = travel_plan.get("destination", "未知")

        # 标题
        story.append(Paragraph(f"🌍 {destination} 旅行规划报告", title_style))
        story.append(Spacer(1, 20))

        # 基本信息表格
        basic_info = [
            ['项目', '详情'],
            ['🎯 目的地', destination],
            ['📅 旅行日期', travel_plan.get('travel_dates', '未知')],
            ['⏰ 行程天数', f"{travel_plan.get('duration', 0)}天"],
            ['👥 团队人数', f"{travel_plan.get('group_size', 0)}人"],
            ['💰 预算类型', travel_plan.get('budget_range', '未知')],
            ['🎨 兴趣爱好', ', '.join(travel_plan.get('interests', [])) or '无特殊偏好']
        ]

        table = Table(basic_info, colWidths=[120, 300])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'TOP')
        ]))

        story.append(table)
        story.append(Spacer(1, 30))

        # AI智能体建议
        story.append(Paragraph("🤖 AI智能体专业建议", heading_style))
        story.append(Spacer(1, 15))

        agent_outputs = result.get("agent_outputs", {})
        agent_names_cn = {
            'travel_advisor': '🏛️ 旅行顾问',
            'weather_analyst': '🌤️ 天气分析师',
            'budget_optimizer': '💰 预算优化师',
            'local_expert': '🏠 当地专家',
            'itinerary_planner': '📅 行程规划师',
            'simple_agent': '🤖 AI规划师',
            'mock_agent': '🎭 模拟规划师'
        }

        for agent_name, output in agent_outputs.items():
            agent_display_name = agent_names_cn.get(agent_name, agent_name)
            response = output.get('response', '无输出')
            status = output.get('status', '未知')

            # 智能体标题
            agent_title = f"{agent_display_name} (状态: {status.upper()})"
            story.append(Paragraph(agent_title, styles['Heading3']))

            # 智能体内容（处理长文本）
            if len(response) > 800:
                content = response[:800] + "\n\n[内容过长，已截取前800字符...]"
            else:
                content = response

            # 将内容分段处理
            paragraphs = content.split('\n\n')
            for para in paragraphs:
                if para.strip():
                    story.append(Paragraph(para.strip(), styles['Normal']))
                    story.append(Spacer(1, 8))

            story.append(Spacer(1, 20))

        # 报告信息
        from datetime import datetime
        story.append(Spacer(1, 30))
        story.append(Paragraph("📄 报告信息", heading_style))

        report_info = [
            ['任务ID', task_id],
            ['生成时间', datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
            ['生成方式', 'LangGraph多智能体AI系统'],
            ['报告格式', 'PDF']
        ]

        info_table = Table(report_info, colWidths=[120, 300])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'TOP')
        ]))

        story.append(info_table)
        story.append(Spacer(1, 20))

        # 页脚
        footer_text = "本报告由LangGraph多智能体AI旅行规划系统自动生成"
        story.append(Paragraph(footer_text, styles['Normal']))

        # 生成PDF
        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()

    except ImportError:
        # 如果reportlab不可用，返回None
        st.warning("PDF生成需要安装reportlab库，请使用Markdown格式下载")
        return None
    except Exception as e:
        st.error(f"PDF生成失败: {str(e)}")
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

                # 生成和下载报告
                st.markdown("### 📥 下载报告")

                # 检查PDF生成能力
                pdf_available = check_pdf_capability()

                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("#### 📄 原始数据")
                    # 下载JSON格式
                    download_url = f"{API_BASE_URL}/download/{task_id}"
                    st.markdown(f"[📊 JSON格式数据]({download_url})")
                    st.caption("包含完整的AI分析数据")

                with col2:
                    st.markdown("#### 📝 格式化报告")

                    # Markdown报告
                    markdown_content = generate_markdown_report(result, task_id)
                    st.download_button(
                        label="📥 下载Markdown报告",
                        data=markdown_content,
                        file_name=f"travel_plan_{task_id[:8]}.md",
                        mime="text/markdown",
                        help="推荐格式，支持所有设备查看"
                    )

                    # PDF报告
                    if pdf_available:
                        if st.button("📄 生成PDF报告", help="生成专业PDF格式报告"):
                            with st.spinner("正在生成PDF报告..."):
                                try:
                                    pdf_content = generate_pdf_report(result, task_id)
                                    if pdf_content:
                                        st.download_button(
                                            label="📥 下载PDF报告",
                                            data=pdf_content,
                                            file_name=f"travel_plan_{task_id[:8]}.pdf",
                                            mime="application/pdf"
                                        )
                                        st.success("PDF报告生成成功！")
                                    else:
                                        st.error("PDF生成失败，请使用Markdown格式")
                                except Exception as e:
                                    st.error(f"PDF生成失败: {str(e)}")
                                    st.info("💡 建议使用Markdown格式，兼容性更好")
                    else:
                        st.info("💡 PDF功能需要安装额外依赖")
                        st.code("pip install reportlab", language="bash")
                        st.caption("或直接使用Markdown格式，效果同样出色")

if __name__ == "__main__":
    main()
