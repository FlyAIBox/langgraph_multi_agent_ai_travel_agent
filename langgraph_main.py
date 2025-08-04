#!/usr/bin/env python3
"""
LangGraph多智能体AI旅行规划系统
使用LangGraph框架、Google Gemini和DuckDuckGo搜索的高级旅行规划系统

这个模块是LangGraph多智能体系统的主入口点，它：
1. 初始化和配置所有AI智能体
2. 处理用户输入和交互
3. 协调多个智能体的协作
4. 生成完整的旅行规划报告

适用于大模型技术初级用户：
- LangGraph是一个用于构建多智能体系统的框架
- 每个智能体都有专门的职责和能力
- 智能体之间通过状态图进行协调和通信
"""

import sys
import os
import asyncio
from datetime import datetime, timedelta
import json

# 将当前目录添加到Python路径中，确保可以导入项目模块
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.langgraph_agents import LangGraphTravelAgents
from modules.user_input import UserInputHandler
from config.langgraph_config import langgraph_config as config

def display_langgraph_header():
    """
    显示LangGraph系统的标题信息

    这个函数向用户展示系统的能力和智能体团队组成，
    帮助用户了解系统的功能和特点。
    """
    print("\n" + "="*80)
    print("🚀 LANGGRAPH多智能体AI旅行规划师")
    print("="*80)
    print("🤖 由Google Gemini Flash-2.0和DuckDuckGo搜索驱动")
    print("="*80)
    print("\n🎯 AI智能体团队 (LangGraph框架):")
    print("   🎯 协调员智能体     - 工作流编排与决策综合")
    print("   ✈️  旅行顾问        - 目的地专业知识与实时搜索")
    print("   💰 预算优化师      - 成本分析与实时定价")
    print("   🌤️  天气分析师      - 天气情报与当前数据")
    print("   🏠 当地专家        - 内部知识与实时本地信息")
    print("   📅 行程规划师      - 日程优化与物流安排")
    print("\n🔧 增强功能:")
    print("   • Google Gemini Flash-2.0处理所有AI交互")
    print("   • DuckDuckGo搜索获取实时信息")
    print("   • LangGraph状态管理和工作流")
    print("   • 高级工具集成和执行")
    print("   • 异步多智能体协作")
    print("="*80)

def validate_environment():
    """
    验证环境设置

    检查系统运行所需的环境变量和配置，
    确保所有必要的API密钥和设置都已正确配置。

    功能说明：
    1. 检查Google Gemini API密钥是否存在
    2. 验证配置文件是否正确加载
    3. 提供详细的错误信息和解决方案
    """
    print("🔍 正在验证环境配置...")

    # 检查Gemini API密钥
    if not config.GEMINI_API_KEY:
        print("❌ 错误: 环境中未找到GEMINI_API_KEY")
        print("请在.env文件中设置您的Google Gemini API密钥:")
        print("GEMINI_API_KEY=your_api_key_here")
        print("\n获取API密钥: https://makersuite.google.com/app/apikey")
        return False

    print(f"✅ Gemini API密钥: {'*' * 10}{config.GEMINI_API_KEY[-4:]}")
    print(f"✅ 模型: {config.GEMINI_MODEL}")
    print(f"✅ DuckDuckGo搜索: 已启用")

    return True

def create_sample_request():
    """
    创建演示用的示例旅行请求

    返回一个包含典型旅行规划参数的字典，
    用于演示系统的功能和能力。

    示例使用中国大陆城市：上海
    """
    return {
        "destination": "上海",
        "duration": 5,
        "budget_range": "中等预算",
        "interests": ["文化", "美食", "科技", "历史"],
        "group_size": 2,
        "travel_dates": "2024-04-15 至 2024-04-20"
    }

def demonstrate_langgraph_system():
    """
    演示LangGraph多智能体系统

    这个函数展示系统的完整工作流程：
    1. 创建示例旅行请求
    2. 初始化多智能体系统
    3. 运行协作规划过程
    4. 显示规划结果

    适用于大模型技术初级用户：
    这是一个完整的端到端演示，展示了多个AI智能体
    如何协同工作来创建旅行计划。
    """
    print("\n" + "🎭 LANGGRAPH系统演示")
    print("-" * 60)

    print("📋 示例旅行请求:")
    sample_request = create_sample_request()
    for key, value in sample_request.items():
        print(f"   {key.replace('_', ' ').title()}: {value}")

    print(f"\n🚀 正在初始化LangGraph多智能体系统...")

    try:
        # 初始化系统
        travel_agents = LangGraphTravelAgents()
        print("✅ LangGraph工作流编译成功")

        print(f"\n🤝 开始多智能体协作...")
        print("   完整分析可能需要1-2分钟...")

        # 运行规划
        result = travel_agents.run_travel_planning(sample_request)

        if result["success"]:
            print(f"\n✅ Planning completed successfully!")
            print(f"   Total iterations: {result['total_iterations']}")
            print(f"   Agents involved: {len(result['agent_outputs'])}")
            
            # Display agent contributions
            print(f"\n🤖 AGENT CONTRIBUTIONS:")
            for agent_name, output in result["agent_outputs"].items():
                status = output.get("status", "unknown")
                timestamp = output.get("timestamp", "")
                print(f"   {agent_name.replace('_', ' ').title():<20}: {status.upper()} ({timestamp[:19]})")
            
            # Display final plan summary
            travel_plan = result["travel_plan"]
            print(f"\n📋 TRAVEL PLAN SUMMARY:")
            print(f"   Destination: {travel_plan.get('destination')}")
            print(f"   Duration: {travel_plan.get('duration')} days")
            print(f"   Planning Method: {travel_plan.get('planning_method')}")
            
            print(f"\n🎉 DEMONSTRATION COMPLETED SUCCESSFULLY!")
            return True
            
        else:
            print(f"❌ Planning failed: {result.get('error')}")
            return False
            
    except Exception as e:
        print(f"❌ System error: {str(e)}")
        return False

def run_interactive_planning():
    """Run interactive travel planning with user input"""
    print("\n" + "="*80)
    print("🎯 INTERACTIVE TRAVEL PLANNING")
    print("="*80)
    
    # Get user input
    input_handler = UserInputHandler()
    user_data = input_handler.get_trip_details()
    
    if not user_data:
        print("❌ Planning cancelled by user")
        return
    
    # Convert user data to LangGraph format
    travel_request = {
        "destination": user_data.get("destination", ""),
        "duration": user_data.get("duration", 3),
        "budget_range": user_data.get("budget_range", "mid-range"),
        "interests": user_data.get("interests", []),
        "group_size": user_data.get("group_size", 1),
        "travel_dates": f"{user_data.get('start_date', '')} to {user_data.get('end_date', '')}"
    }
    
    print(f"\n🚀 Starting LangGraph Multi-Agent Planning...")
    print("   This process uses multiple AI agents collaborating in real-time")
    print("   Each agent will search for current information and provide expertise")
    
    try:
        # Initialize and run the system
        travel_agents = LangGraphTravelAgents()
        result = travel_agents.run_travel_planning(travel_request)
        
        if result["success"]:
            display_planning_results(result, travel_request)
            
            # Save results
            save_results = input("\n💾 Save complete travel plan to file? (y/n): ").lower().strip()
            if save_results == 'y':
                save_langgraph_results(result, travel_request)
        else:
            print(f"❌ Planning failed: {result.get('error')}")
            
    except Exception as e:
        print(f"❌ System error: {str(e)}")

def display_planning_results(result: dict, request: dict):
    """
    显示全面的规划结果

    这个函数将多智能体协作的结果以结构化的方式展示给用户，
    包括行程概览、系统性能指标和各个智能体的贡献。

    参数：
    - result: 包含规划结果的字典
    - request: 原始的旅行请求字典

    功能说明：
    1. 显示行程基本信息
    2. 展示系统性能指标
    3. 列出各个智能体的具体贡献
    """
    print("\n" + "="*80)
    print("📋 LANGGRAPH多智能体规划结果")
    print("="*80)

    travel_plan = result["travel_plan"]

    # 行程概览
    print(f"🌍 行程概览:")
    print(f"   目的地: {travel_plan.get('destination')}")
    print(f"   行程时长: {travel_plan.get('duration')} 天")
    print(f"   团队人数: {travel_plan.get('group_size')} 人")
    print(f"   预算范围: {travel_plan.get('budget_range').title()}")
    print(f"   兴趣爱好: {', '.join(travel_plan.get('interests', []))}")

    # 系统性能
    print(f"\n🤖 系统性能:")
    print(f"   规划方法: {travel_plan.get('planning_method')}")
    print(f"   总迭代次数: {result.get('total_iterations')}")
    print(f"   参与智能体: {len(result['agent_outputs'])}个")
    print(f"   规划状态: {'✅ 完成' if result.get('planning_complete') else '⚠️ 部分完成'}")

    # 智能体贡献
    print(f"\n🎯 智能体贡献:")
    agent_outputs = result.get("agent_outputs", {})
    for agent_name, output in agent_outputs.items():
        print(f"\n   {agent_name.replace('_', ' ').title().upper()}:")
        contribution = output.get("response", "无输出")
        # 截断过长的响应以便显示
        if len(contribution) > 300:
            contribution = contribution[:300] + "..."
        print(f"   {contribution}")

    print("\n" + "="*80)

def save_langgraph_results(result: dict, request: dict):
    """
    将LangGraph结果保存到文件

    这个函数将多智能体协作的完整结果保存为文本文件，
    便于用户后续查看和分享。

    参数：
    - result: 包含规划结果的字典
    - request: 原始的旅行请求字典

    功能说明：
    1. 生成包含时间戳的文件名
    2. 格式化所有规划内容
    3. 保存为UTF-8编码的文本文件
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    destination = request.get('destination', 'unknown').replace(' ', '_').lower()
    filename = f"langgraph旅行计划_{destination}_{timestamp}.txt"

    content = []
    content.append("="*80)
    content.append("LANGGRAPH多智能体AI旅行规划报告")
    content.append("="*80)
    content.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    content.append(f"System: LangGraph Framework with Google Gemini & DuckDuckGo")
    content.append("")
    
    # Trip details
    travel_plan = result["travel_plan"]
    content.append("TRIP OVERVIEW:")
    content.append("-" * 40)
    content.append(f"Destination: {travel_plan.get('destination')}")
    content.append(f"Duration: {travel_plan.get('duration')} days")
    content.append(f"Group Size: {travel_plan.get('group_size')} people")
    content.append(f"Budget Range: {travel_plan.get('budget_range')}")
    content.append(f"Interests: {', '.join(travel_plan.get('interests', []))}")
    content.append("")
    
    # System performance
    content.append("SYSTEM PERFORMANCE:")
    content.append("-" * 40)
    content.append(f"Planning Method: {travel_plan.get('planning_method')}")
    content.append(f"Total Iterations: {result.get('total_iterations')}")
    content.append(f"Agents Involved: {len(result['agent_outputs'])}")
    content.append("")
    
    # Agent contributions
    content.append("AGENT CONTRIBUTIONS:")
    content.append("-" * 40)
    agent_outputs = result.get("agent_outputs", {})
    for agent_name, output in agent_outputs.items():
        content.append(f"\n{agent_name.replace('_', ' ').title().upper()}:")
        content.append(f"Status: {output.get('status', 'Unknown')}")
        content.append(f"Timestamp: {output.get('timestamp', 'Unknown')}")
        content.append(f"Response: {output.get('response', 'No output available')}")
        content.append("")
    
    content.append("="*80)
    content.append("LangGraph多智能体旅行规划报告结束")
    content.append("="*80)

    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("\n".join(content))
        print(f"✅ 旅行计划已保存为: {filename}")
    except Exception as e:
        print(f"❌ 保存文件时出错: {str(e)}")

def main():
    """
    LangGraph旅行规划系统的主入口点

    这是程序的主函数，它：
    1. 显示系统介绍和功能说明
    2. 验证环境配置
    3. 提供用户交互菜单
    4. 根据用户选择执行相应功能

    适用于大模型技术初级用户：
    这个函数展示了如何构建一个完整的AI应用程序，
    包括用户界面、错误处理和功能分发。
    """
    try:
        # 显示系统标题
        display_langgraph_header()

        # 验证环境配置
        if not validate_environment():
            return

        print("\n" + "="*60)
        print("选择您的体验:")
        print("1. 🎭 快速演示 (上海示例行程)")
        print("2. 🎯 交互式旅行规划 (自定义行程)")
        print("3. ❌ 退出")

        while True:
            choice = input("\n请选择选项 (1-3): ").strip()
            
            if choice == '1':
                print("\n🎭 开始LangGraph系统演示...")
                if demonstrate_langgraph_system():
                    print("\n🎉 演示成功完成!")
                break

            elif choice == '2':
                print("\n🎯 开始交互式规划...")
                run_interactive_planning()
                break

            elif choice == '3':
                print("\n👋 感谢您试用LangGraph旅行规划系统!")
                break

            else:
                print("请输入 1、2 或 3。")

    except KeyboardInterrupt:
        print("\n\n❌ 用户中断了规划过程。")
    except Exception as e:
        print(f"\n❌ 系统错误: {str(e)}")
        print("请检查您的配置并重试。")

if __name__ == "__main__":
    main()
